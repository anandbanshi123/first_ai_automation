import os
import json
import argparse
from datetime import datetime
from junitparser import JUnitXml

def parse_junit(path):
    xml = JUnitXml.fromfile(path)
    total = passed = failed = skipped = 0
    failures = []
    for suite in xml:
        for case in suite:
            total += 1
            if case.result is None:
                passed += 1
            else:
                tag = getattr(case.result, "_tag", "")
                if tag in ("failure", "error"):
                    failed += 1
                    failures.append({
                        "name": case.name,
                        "classname": case.classname,
                        "message": str(case.result),
                    })
                elif tag == "skipped":
                    skipped += 1
    return total, passed, failed, skipped, failures

def collect(junit, screenshots_dir, out_db, meta):
    total, passed, failed, skipped, failures = parse_junit(junit)
    screenshots = []
    if os.path.isdir(screenshots_dir):
        for root, _, files in os.walk(screenshots_dir):
            for f in files:
                screenshots.append(os.path.join(root, f))
    record = {
        "id": meta.get("build") or datetime.utcnow().isoformat(),
        "timestamp": datetime.utcnow().isoformat(),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "failures": failures,
        "screenshots": screenshots,
        "meta": meta
    }
    db = []
    if os.path.exists(out_db):
        try:
            with open(out_db, "r") as fh:
                db = json.load(fh)
        except Exception:
            db = []
    db.append(record)
    os.makedirs(os.path.dirname(out_db) or ".", exist_ok=True)
    with open(out_db, "w") as fh:
        json.dump(db, fh, indent=2)
    print("Appended run:", record["id"])
    return record

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--junit", default="results/junit.xml")
    p.add_argument("--screens", default="results/screenshots")
    p.add_argument("--out", default="results/report_db.json")
    p.add_argument("--build", default=os.environ.get("BUILD_NUMBER"))
    p.add_argument("--branch", default=os.environ.get("GIT_BRANCH"))
    p.add_argument("--commit", default=os.environ.get("GIT_COMMIT"))
    p.add_argument("--jira", default=os.environ.get("JIRA_ISSUE"))
    args = p.parse_args()
    meta = {"build": args.build, "branch": args.branch, "commit": args.commit, "jira": args.jira}
    collect(args.junit, args.screens, args.out, meta)

if __name__ == "__main__":
    main()