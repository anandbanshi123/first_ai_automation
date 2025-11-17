from pathlib import Path
import json
from typing import Dict, List

REGISTRY = Path(__file__).resolve().parent.joinpath("locators.json")

def list_mappings() -> Dict[str, List[str]]:
    if not REGISTRY.exists():
        return {}
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