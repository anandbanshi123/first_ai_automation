import os
import json
import argparse
import requests
from pathlib import Path

# Keep locators under src/pages/locators.json as canonical
LOCATORS_FILE = Path(__file__).resolve().parents[1].joinpath("src", "pages", "locators.json")

def load_locators():
    if not LOCATORS_FILE.exists():
        return {}
    return json.loads(LOCATORS_FILE.read_text(encoding="utf-8"))

def push_locators(base_url: str, api_token: str, project_id: str):
    locs = load_locators()
    if not locs:
        print("No locators to push.")
        return
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    # endpoint is vendor-specific — adapt to Functionize API docs / tenant
    url = f"{base_url.rstrip('/')}/api/projects/{project_id}/locators/bulk"
    resp = requests.post(url, json={"locators": locs}, headers=headers)
    resp.raise_for_status()
    print("Pushed locators, response:", resp.status_code)

def pull_recommendations(base_url: str, api_token: str, project_id: str, out_file: str):
    headers = {"Authorization": f"Bearer {api_token}"}
    url = f"{base_url.rstrip('/')}/api/projects/{project_id}/locators/recommendations"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    recs = resp.json()
    Path(out_file).write_text(json.dumps(recs, indent=2), encoding="utf-8")
    print("Saved recommendations to", out_file)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True, help="Functionize base URL")
    p.add_argument("--token", required=True, help="API token")
    p.add_argument("--project", required=True, help="Functionize project id")
    p.add_argument("--push", action="store_true")
    p.add_argument("--pull", metavar="OUT_FILE")
    args = p.parse_args()

    if args.push:
        push_locators(args.base, args.token, args.project)
    if args.pull:
        pull_recommendations(args.base, args.token, args.project, args.pull)

if __name__ == "__main__":
    main()