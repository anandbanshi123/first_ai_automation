import json
from pathlib import Path
from typing import Optional

THIS_DIR = Path(__file__).resolve().parent
LOCATORS_FILE = THIS_DIR / "locators.json"

_default = {
    "HomePageLocators": {
        "SEARCH_INPUT": 'input[type="search"], input[aria-label*="search"]',
        "SEARCH_BUTTON": 'button[type="submit"], button:has-text("Search")',
        "DISMISS_COOKIES": 'button[title*="Accept"], button:has-text("Accept"), button:has-text("OK")',
        "BANNER_LINKS": "a.banner, a.promo, .banner a",
        # category locator can be a template or a simple attribute selector
        "CATEGORY_TEMPLATE": 'a:has-text("{name}")'
    }
}

def _load_json():
    try:
        if LOCATORS_FILE.exists():
            return json.loads(LOCATORS_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return _default

_locators = _load_json().get("HomePageLocators", _default["HomePageLocators"])

class HomePageLocators:
    SEARCH_INPUT: str = _locators.get("SEARCH_INPUT", _default["HomePageLocators"]["SEARCH_INPUT"])
    SEARCH_BUTTON: str = _locators.get("SEARCH_BUTTON", _default["HomePageLocators"]["SEARCH_BUTTON"])
    DISMISS_COOKIES: str = _locators.get("DISMISS_COOKIES", _default["HomePageLocators"]["DISMISS_COOKIES"])
    BANNER_LINKS: str = _locators.get("BANNER_LINKS", _default["HomePageLocators"]["BANNER_LINKS"])
    CATEGORY_TEMPLATE: str = _locators.get("CATEGORY_TEMPLATE", _default["HomePageLocators"]["CATEGORY_TEMPLATE"])

    @classmethod
    def get_category_locator(cls, name: str) -> str:
        # prefer explicit mapping in JSON (e.g., {"categories": {"Men": "...", ...}})
        try:
            j = _load_json()
            mapping = j.get("categories") or {}
            if name in mapping:
                return mapping[name]
        except Exception:
            pass
        # fallback to template
        return cls.CATEGORY_TEMPLATE.format(name=name)