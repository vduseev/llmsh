#!/bin/bash

# determine_script_location_dir
SCRIPT_DIR=""
__source="${BASH_SOURCE[0]}"
# resolve $__source until the file is no longer a symlink
while [ -h "$__source" ]; do
  SCRIPT_DIR="$( cd -P "$( dirname "$__source" )" >/dev/null 2>&1 && pwd )"
  __source="$(readlink "$__source")"
  # if $__source was a relative symlink, we need to resolve it relative
  # to the path where the symlink file was located
  [[ $__source != /* ]] && __source="$SCRIPT_DIR/$__source"
done
SCRIPT_DIR="$( cd -P "$( dirname "$__source" )" >/dev/null 2>&1 && pwd )"

# Execute interpreter
"${SCRIPT_DIR}/.venv/bin/llmsh" "$@"
