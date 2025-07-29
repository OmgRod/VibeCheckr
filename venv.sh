#!/bin/sh
if [ -d ".venv" ]; then
    . .venv/bin/activate
else
    if command -v python3.10 >/dev/null 2>&1; then
        python3.10 -m venv .venv
    else
        python3 -m venv .venv
    fi
    . .venv/bin/activate
fi