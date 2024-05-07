#!/bin/bash
set -e

# Color variables
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function for colored echo
cecho() {
    echo -e "${GREEN}👉 $1${NC}"
}

CMD="poetry run pytest -s -rsx ${args[*]}"
cecho "Running tests with pytest: $CMD"
# -o log_cli=true --capture=tee-sys
cecho "To see logging output from tests themselves, run with --log-cli-level=DEBUG or --log-cli-level=INFO"
cecho "To see more output from pytest itself, run with --verbose"
eval $CMD
