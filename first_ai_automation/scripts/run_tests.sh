#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")/.."

# Install dependencies
pip install -r requirements.txt

# Run the tests
pytest tests/uat --maxfail=1 --disable-warnings -q

# Optionally, you can add commands to generate reports or perform other actions after tests run
# e.g., pytest --html=report.html tests/uat