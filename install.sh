#!/bin/bash

ANSWER="y"

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

# Check that Python3 is installed

IS_PYTHON3=NO
IS_PYTHON=NO

if which python &> /dev/null; then
  IS_PYTHON=YES
elif ! which python3 &> /dev/null; then
  IS_PYTHON3=YES
fi

if [[ "$IS_PYTHON3" != "YES" && "$IS_PYTHON" != "YES" ]]; then
  echo "No Python installation found. Please install Python 3 first!" 
  exit 1
fi

if [[ "$IS_PYTHON" == "YES" ]]; then
  PYTHON="$(which python)"
elif [[ "$IS_PYTHON3" == "YES" ]]; then
  PYTHON="$(which python3)"
fi

PYTHON_VERSION="$($PYTHON --version)"
if [[ ! "${PYTHON_VERSION:0:9}" == "Python 3." ]]; then
  echo "Python was found but has wrong version. Python 3 or later is expected. Instead got: ${PYTHON_VERSION}"
  exit 1
fi

echo "Will be using ${PYTHON_VERSION} found in ${PYTHON}..."

# Create a virtual environment
# -r: RAW read, distinguish between return key and escape key
# -s: Do not echo Input char
# -n: Read only 1 char
# -p: Prompt
read -r -n 1 -p "Create a python virtual environment? (Y/n) " ANSWER
echo ""
if [[ "$ANSWER" == "y" || "$ANSWER" == "Y" || "$ANSWER" == "" ]]; then
  VENV_PATH="${SCRIPT_DIR}/.venv"
  echo "Creating a virtual environment in ${VENV_PATH}..."
  "$PYTHON" -m venv "$VENV_PATH"  
  echo "Virtual environment created successfully in ${VENV_PATH}!"
fi

# Install llmsh
read -r -n 1 -p "Install llmsh and its dependencies? (Y/n) " ANSWER
echo ""
if [[ "$ANSWER" == "y" || "$ANSWER" == "Y" || "$ANSWER" == "" ]]; then
  echo "Installing llmsh..."
  "$PYTHON" -m pip install llmsh
  if [[ "$?" == "0" ]]; then
    echo "Installation of llmsh completed successfully!"
  else
    echo "Installation of llmsh failed!"
    exit 1
  fi
fi

# Install symlinks
SYMLINK_DIR=/usr/local/bin
read -r -n 1 -p "Install symlink to llmsh in ${SYMLINK_DIR}? (Y/n) " ANSWER
echo ""
if [[ "$ANSWER" == "y" || "$ANSWER" == "Y" || "$ANSWER" == "" ]]; then
  echo "The script is now going to create an llmsh symlink in /usr/local/bin."
  echo ""
  echo "Creating a symlink allows for llmsh to be called from any directory."
  echo "But creating symlinks in /usr/local/bin/ requires sudo permissions."
  echo ""
  echo "The script will now ask for your password. Please press Ctrl+C to safely stop"
  echo "this script from proceeding any further if you are not comfortable with this"
  echo "operation. You can verify the source code of this script at:"
  echo "https://github.com/vduseev/llmsh"
  echo ""
  # Create symlinks
  sudo ln -s -f "${SCRIPT_DIR}/llm.sh" "${SYMLINK_DIR}/llmsh"
  if [[ "$?" == "0" ]]; then
    echo "Symlinks were installed!"
  else
   echo "Symlinks were not installed. Check for any errors above."
   exit 1
  fi
fi

echo ""
echo "Installation complete!"
