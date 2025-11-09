# first_ai_automation
this for AI test automation
# ...existing code...
# first_ai_automation
this for AI test automation

Project layout
- src/pages: Page objects (BasePage, HomePage, ...)
- tests: pytest tests and conftest with Playwright fixtures
- scripts: CI helpers (test_results_to_jira.py, push_screenshots.sh)
- Jenkinsfile: example CI pipeline
- requirements.txt: python deps

Quick start (mac):
1) Install deps:
   python -m pip install -r requirements.txt
   npx playwright install --with-deps

2) Run tests:
   pytest -q --junitxml=results/junit.xml

3) Post results to Jira:
   python scripts/test_results_to_jira.py --junit results/junit.xml --screens results/screenshots --jira-base "https://jira.example.com" --issue "PROJECT-1" --user "bot" --token "API_TOKEN"

4) Push screenshots:
   chmod +x scripts/push_screenshots.sh
   bash scripts/push_screenshots.sh results/screenshots "ci: add screenshots"

Notes
- Configure Jenkins credentials (jira-creds, JIRA_BASE, JIRA_ISSUE).
- The tests use pytest-playwright. The pytest hook in tests/conftest.py will save screenshots for failing tests to results/screenshots.