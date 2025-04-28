#!/bin/bash
set -eu

black --check .
isort --check .
flake8 --max-line-length=120 --exclude=.git,env .
mypy .
