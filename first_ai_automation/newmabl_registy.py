# ...existing code...
from pathlib import Path
import json
import subprocess
from typing import Optional
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from src.utils.locator_collector import record_locator

# repository-aware paths
_THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = _THIS_DIR.parents[2]  # .../first_ai_automation (repo root)
LOCATOR_REGISTRY = REPO_ROOT.joinpath("first_ai_automation", "src", "pages", "locators.json")
SUGGEST_SCRIPT = REPO_ROOT.joinpath("first_ai_automation", "scripts", "suggest_locator.py")

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
        LOCATOR_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
        with open(LOCATOR_REGISTRY, "w", encoding="utf-8") as fh:
            json.dump(reg, fh, indent=2)

    def _try_registry(self, selector: str):
        reg = self._load_registry()
        for cand in reg.get(selector, []):
            try:
                el = self.page.query_selector(cand)
                if el:
                    return cand, el
            except Exception:
                continue
        return None, None

    def _ask_ml_suggester(self, snapshot_path: str, topk: int = 5):
        if not SUGGEST_SCRIPT.exists():
            return []
        try:
            out = subprocess.check_output(
                ["python", str(SUGGEST_SCRIPT), "--dom-file", str(snapshot_path), "--topk", str(topk)],
                stderr=subprocess.DEVNULL,
                cwd=str(REPO_ROOT)
            )
            lines = out.decode().strip().splitlines()
            # expect each line starts with selector; adjust if suggestor outputs JSON
            return [l.split()[0] for l in lines if l.strip()]
        except Exception:
            return []

    def _dump_failure_snapshot(self, selector: str, out_path: Path):
        try:
            snap = {
                "url": self.page.url,
                "failed_selector": selector,
                "page_html": self.page.content()[:200000]  # truncated for size
            }
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(snap, fh, indent=2)
            return out_path
        except Exception:
            return None

    def find(self, selector: str, timeout: int = 5000, heal: bool = True) -> Optional[object]:
        """Find element with optional self-healing. Returns ElementHandle or None."""
        try:
            return self.page.wait_for_selector(selector, timeout=timeout)
        except Exception:
            # registry fallbacks
            cand, el = self._try_registry(selector)
            if el:
                try:
                    record_locator(self.page, cand, label=f"registry-heal:{selector}")
                except Exception:
                    pass
                return el

            if not heal:
                return None

            # create a small snapshot for suggester and ask ML model
            snap_file = REPO_ROOT.joinpath("results", "failed_dom", f"failed_{selector.replace(' ','_')}.json")
            snap = self._dump_failure_snapshot(selector, snap_file)
            suggestions = self._ask_ml_suggester(snap) if snap else []

            for s in suggestions:
                try:
                    el = self.page.query_selector(s)
                    if el:
                        # persist mapping for faster future healing
                        reg = self._load_registry()
                        reg.setdefault(selector, [])
                        if s not in reg[selector]:
                            reg[selector].insert(0, s)
                            reg[selector] = reg[selector][:10]
                            self._save_registry(reg)
                        try:
                            record_locator(self.page, s, label=f"ml-heal:{selector}")
                        except Exception:
                            pass
                        return el
                except Exception:
                    continue
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
# ...existing code...