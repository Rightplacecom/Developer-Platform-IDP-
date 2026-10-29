#!/usr/bin/env sh
set -eu
python -m compileall api platform
pytest -q
ruff check .
