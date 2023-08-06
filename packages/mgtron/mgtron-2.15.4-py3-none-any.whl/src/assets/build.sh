#!/usr/bin/bash

set -e
HOME="work_worK_woRk_wOrk_Work_WORK"
WORK="work_worK_woRk_wOrk_Work"
WORK_DIR="/home/${USER}/Documents/${WORK}/mg_tron"
TEST_DIR="/home/${USER}/Documents/${WORK}/pypi_testing"
PROJ_NAME="mgtron"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


pushd $WORK_DIR

# Check for existence of virtual environment
if [ ! -d "$WORK_DIR/venv" ]; then
    echo "Creating virtual environment"
    python -m venv venv
fi

# Use the virtual environment
$WORK_DIR/venv/bin/python -m build -w

# Copy the file to the 'pypi_test' directory
cp $WORK_DIR/dist/*.whl $TEST_DIR

popd

pushd $TEST_DIR

# Check for existence of virtual environment
if [ ! -d "$TEST_DIR/venv" ]; then
    echo "Creating virtual environment"
    python -m venv venv
fi

# activate the virtual environment
source $TEST_DIR/venv/bin/activate

# uninstall the package if it exists
pip uninstall -y $PROJ_NAME

# Use the virtual environment
pip install *2*.whl

# Deactivate the virtual environment
deactivate

# Run the program
./$TEST_DIR/venv/bin/mgtron

# Check the return status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Success${NC}"
    popd
else
    # Print the error message in red
    echo -e "${RED}Error${NC}"
    popd
fi



