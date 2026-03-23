#!/bin/bash

# run_tests.sh - Automated test runner for the Dash application
# This script activates the virtual environment and runs the test suite

echo "========================================="
echo "  Pink Morsel Dashboard - Test Runner"
echo "========================================="
echo ""

# Set colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_message() {
    echo -e "${2}${1}${NC}"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_message "Error: Virtual environment not found!" "$RED"
    print_message "Please run: python -m venv venv" "$YELLOW"
    exit 1
fi

# Activate virtual environment
print_message "Activating virtual environment..." "$YELLOW"

# Check the operating system
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Check if activation was successful
if [ $? -ne 0 ]; then
    print_message "Error: Failed to activate virtual environment!" "$RED"
    exit 1
fi

print_message "✓ Virtual environment activated" "$GREEN"
echo ""

# Verify required files exist
print_message "Checking required files..." "$YELLOW"

if [ ! -f "formatted_data.csv" ]; then
    print_message "Error: formatted_data.csv not found!" "$RED"
    print_message "Please run: python process_data.py first" "$YELLOW"
    exit 1
fi

if [ ! -f "test_app_simple.py" ]; then
    print_message "Error: test_app_simple.py not found!" "$RED"
    exit 1
fi

print_message "✓ Required files found" "$GREEN"
echo ""

# Check if pytest is installed
print_message "Checking pytest installation..." "$YELLOW"
python -c "import pytest" 2>/dev/null
if [ $? -ne 0 ]; then
    print_message "Error: pytest not installed!" "$RED"
    print_message "Installing pytest..." "$YELLOW"
    pip install pytest
fi
print_message "✓ pytest is available" "$GREEN"
echo ""

# Run the test suite
print_message "Running test suite..." "$YELLOW"
print_message "=========================================" "$NC"
echo ""

# Run pytest with verbose output
pytest test_app_simple.py -v

# Capture the exit code
TEST_EXIT_CODE=$?

echo ""
print_message "=========================================" "$NC"

# Report results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    print_message "✓ All tests passed successfully!" "$GREEN"
    print_message "✓ Exit code: 0" "$GREEN"
    exit 0
else
    print_message "✗ Some tests failed!" "$RED"
    print_message "✗ Exit code: $TEST_EXIT_CODE" "$RED"
    exit 1
fi