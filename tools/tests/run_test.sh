#!/bin/bash

source ../.venv/bin/activate

TOOLS_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$TOOLS_ROOT/../" && (nose2 --plugin nose2.plugins.junitxml --junit-xml test_python || true)