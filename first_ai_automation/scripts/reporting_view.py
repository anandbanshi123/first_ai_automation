import os
import json
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from collections import defaultdict

DB_PATH = st.sidebar.text_input("Report DB path", "results/report_db.json")
st.set_page_config(layout="wide", page_title="Test AI Dashboard")

if not os.path.exists(DB_PATH):
    st.warning(f"No DB found at {DB_PATH}. Run tests and collect runs first.")
    st.stop()

with open(DB_PATH, "r") as fh:
    runs = json.load(fh)

if not runs:
    st.info("No runs in DB")
    st.stop()

# Dataframe of runs
df = pd.DataFrame([{
    "id": r["id"],
    "timestamp": r["timestamp"],
    "total": r["total"],
    "passed": r["passed"],
    "failed": r["failed"],
    "skipped": r["skipped"],
    "pass_rate": (r["passed"]/r["total"]*100) if r["total"] else 0,
    "build": r["meta"].get("build"),
    "branch": r["meta"].get("branch"),
    "commit": r["meta"].get("commit"),
    "jira": r["meta"].get("jira"),
} for r in runs])

df['ts'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('ts')

st.title("Automated Test AI Dashboard")
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Pass rate trend")
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('ts:T', title='Run time'),
        y=alt.Y('pass_rate:Q', title='Pass %'),
        tooltip=['id','build','branch','pass_rate','failed']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

    st.subheader("Recent runs")
    st.dataframe(df[['id','ts','build','branch','pass_rate','failed']].tail(10).rename(columns={'ts':'time'}))

with col2:
    last = runs[-1]
    st.subheader("Latest run")
    st.metric("Pass %", f"{last['passed']}/{last['total']} ({(last['passed']/last['total']*100):.1f}%)")
    st.metric("Failed", last['failed'])
    if last['meta'].get('jira'):
        st.markdown(f"Jira: `{last['meta']['jira']}`")

# Flaky detection: tests that have both failures and passes across runs
st.subheader("Flaky test detection (heuristic)")
test_history = defaultdict(list)
for r in runs:
    for f in r.get("failures", []):
        key = (f.get("classname") or "") + "." + f.get("name")
        test_history[key].append({"run": r["id"], "status": "FAIL", "message": f.get("message")})
    # infer passed tests by name absence in failures (approx)
    # not comprehensive but practical for quick detection
all_test_names = set()
for r in runs:
    for f in r.get("failures", []):
        all_test_names.add((f.get("classname") or "") + "." + f.get("name"))
# build simple pass records by comparing totals (best-effort)
# Count occurrences across runs
for r in runs:
    # approximate: if test not in failures and total>0 => mark PASS for previously seen tests
    for name in list(all_test_names):
        failed_here = any(((f.get("classname") or "") + "." + f.get("name"))==name for f in r.get("failures", []))
        if not failed_here:
            test_history[name].append({"run": r["id"], "status": "PASS"})

flaky = []
for name, hist in test_history.items():
    statuses = {h["status"] for h in hist}
    if "PASS" in statuses and "FAIL" in statuses:
        fail_count = sum(1 for h in hist if h["status"]=="FAIL")
        flaky.append({"test": name, "fail_count": fail_count, "history": hist})

flaky_df = pd.DataFrame(flaky).sort_values("fail_count", ascending=False)
st.write("Potential flaky tests:", flaky_df.head(20).to_dict(orient="records"))

# Failure drill-down for latest run with screenshots
st.subheader("Failures and screenshots (latest run)")
if last.get("failures"):
    for f in last["failures"]:
        name = (f.get("classname") or "") + "." + f.get("name")
        st.markdown(f"**{name}**")
        st.text(f.get("message", "")[:1000])
        # show matching screenshot if any
        for s in last.get("screenshots", []):
            if os.path.basename(s).lower().startswith(f.get("name","").lower()):
                st.image(s, width=300)
else:
    st.write("No failures in latest run")