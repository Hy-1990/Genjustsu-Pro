#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHON="${PYTHON:-python3}"
"$PYTHON" -c 'import sys; assert sys.platform == "darwin", "macOS required"; assert sys.version_info >= (3,12), "Python 3.12+ required"'
command -v rubberband >/dev/null || { echo "Install Rubber Band with: brew install rubberband"; exit 1; }
if [ ! -d .venv ]; then "$PYTHON" -m venv .venv; fi
.venv/bin/python -m pip install -r requirements.txt
echo "Ready. Run bash start.command and configure your API keys on the Settings page."
