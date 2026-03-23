@echo off
REM run_tests.bat - Windows batch file to run tests

echo =========================================
echo   Pink Morsel Dashboard - Test Runner
echo =========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment!
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

REM Check if required files exist
echo Checking required files...
if not exist "formatted_data.csv" (
    echo [ERROR] formatted_data.csv not found!
    echo Please run: python process_data.py first
    exit /b 1
)

if not exist "test_app_simple.py" (
    echo [ERROR] test_app_simple.py not found!
    exit /b 1
)

echo [OK] Required files found
echo.

REM Run the test suite
echo Running test suite...
echo =========================================
echo.

pytest test_app_simple.py -v

REM Capture the exit code
set TEST_EXIT_CODE=%errorlevel%

echo.
echo =========================================

if %TEST_EXIT_CODE% equ 0 (
    echo [OK] All tests passed successfully!
    echo [OK] Exit code: 0
    exit /b 0
) else (
    echo [ERROR] Some tests failed!
    echo [ERROR] Exit code: %TEST_EXIT_CODE%
    exit /b 1
)