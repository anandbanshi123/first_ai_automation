from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import json
import os
import subprocess
from typing import Optional
from src.utils.locators import record_locator
# Try importing the project's locator recorder from common locations; fall back to a no-op stub
# to avoid import errors in environments where the package layout differs.

LOCATOR_REGISTRY = os.environ.get("LOCATOR_REGISTRY", "results/locators.json")
SUGGEST_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "..", "scripts", "suggest_locator.py")

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url, wait_until="networkidle")

    def _load_registry(self):
        try:
            with open(LOCATOR_REGISTRY, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return {}

    def _save_registry(self, reg):
        os.makedirs(os.path.dirname(LOCATOR_REGISTRY) or ".", exist_ok=True)
        with open(LOCATOR_REGISTRY, "w", encoding="utf-8") as fh:
            json.dump(reg, fh, indent=2)

    def _try_fallbacks(self, selector: str):
        reg = self._load_registry()
        fallbacks = reg.get(selector, [])
        for s in fallbacks:
            el = self.page.query_selector(s)
            if el:
                return s, el
        return None, None

    def _ask_ml_suggester(self, failed_snapshot_path: str):
        # If you trained the ML suggester, it can produce suggestions.
        if not os.path.exists(SUGGEST_SCRIPT):
            return []
        try:
            # produce suggestions into stdout as JSON lines using the existing script interface
            out = subprocess.check_output(["python", SUGGEST_SCRIPT, "--dom-file", failed_snapshot_path, "--topk", "5"], stderr=subprocess.DEVNULL)
            # The script prints plain text suggestions; adapt if you change script to output JSON.
            # For robustness, try parsing lines as selectors.
            lines = out.decode().strip().splitlines()
            suggestions = [l.split()[0] for l in lines if l.strip()]
            return suggestions
        except Exception:
            return []

    def _dump_failed_snapshot(self, selector: str, out_path: str):
        try:
            snap = {
                "url": self.page.url,
                "selector": selector,
                "outer_html": self.page.eval_on_selector_all("html", "(els) => els.map(e => e.outerHTML).join('\\n')") if True else self.page.content(),
                # you can refine to capture surrounding context / attributes of candidate nodes
            }
            os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(snap, fh, indent=2)
            return out_path
        except Exception:
            return None

    def find(self, selector: str, timeout: int = 5000, heal: bool = True) -> Optional[object]:
        """Find element with optional self-healing fallback. Returns ElementHandle or None."""
        try:
            return self.page.wait_for_selector(selector, timeout=timeout)
        except PlaywrightTimeoutError:
            # first try registry fallbacks
            fallback_sel, el = self._try_fallbacks(selector)
            if el:
                # record the successful selector usage for future training
                try:
                    record_locator(self.page, fallback_sel, label=f"self-healed-for:{selector}")
                except Exception:
                    pass
                return el

            if not heal:
                return None

            # Dump a minimal failure snapshot and run ML suggester (if available)
            snapshot_path = os.path.join("results", "failed_dom_for_suggest.json")
            snap = self._dump_failed_snapshot(selector, snapshot_path)
            suggestions = self._ask_ml_suggester(snapshot_path) if snap else []

            # try ML suggestions
            for s in suggestions:
                try:
                    el = self.page.query_selector(s)
                    if el:
                        # persist the successful suggestion into registry for quicker future recovery
                        reg = self._load_registry()
                        reg.setdefault(selector, [])
                        if s not in reg[selector]:
                            reg[selector].insert(0, s)  # prefer recent success first
                            # keep registry small
                            reg[selector] = reg[selector][:10]
                            self._save_registry(reg)
                        try:
                            record_locator(self.page, s, label=f"ml-suggested-for:{selector}")
                        except Exception:
                            pass
                        return el
                except Exception:
                    continue

            # nothing found
            return None

    def click(self, selector: str, **kwargs):
        el = self.find(selector)
        if not el:
            raise PlaywrightTimeoutError(f"Element not found and self-heal failed: {selector}")
        return el.click(**kwargs)

    def fill(self, selector: str, text: str, **kwargs):
        el = self.find(selector)
        if not el:
            raise PlaywrightTimeoutError(f"Element not found and self-heal failed: {selector}")
        return el.fill(text, **kwargs)

from pathlib import Path
import json
from pathlib import Path
REGISTRY = Path(__file__).resolve().parent.joinpath("locators.json")
import json
from typing import List
def list_mappings() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def add_mapping(original: str, replacement: str):
    reg = list_mappings()
    reg.setdefault(original, [])
    if replacement not in reg[original]:
        reg[original].insert(0, replacement)
        reg[original] = reg[original][:10]
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(reg, indent=2), encoding="utf-8")

def remove_mapping(original: str, replacement: str):
    reg = list_mappings()
    if original in reg and replacement in reg[original]:
        reg[original].remove(replacement)
        REGISTRY.write_text(json.dumps(reg, indent=2), encoding="utf-8")

#mapping
value= {"user": "locator2"} #dict
