@echo off
echo Installing Gopa Programming Language...

python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3.11+ is required but not found.
    exit /b 1
)

echo Python found ✓
echo.

pip install -e . --quiet

echo.
echo ✓ Gopa installed successfully!
echo.
echo Try it out:
echo   gopa --help
echo   gopa test
echo   gopa run examples\hello.gopa
echo.

