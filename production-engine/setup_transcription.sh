#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install openai-whisper
printf 'Installed isolated whisper runtime at %s/.venv\n' "$PWD"
