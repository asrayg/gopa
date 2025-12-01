#!/bin/bash

set -e

echo "Installing Gopa Programming Language..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3.11+ is required but not found."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python 3.11+ is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Python version: $PYTHON_VERSION ✓"

if python3 -m pip install -e . --user 2>/dev/null; then
    INSTALL_METHOD="--user"
elif python3 -m pip install -e . 2>/dev/null; then
    INSTALL_METHOD="system"
else
    echo ""
    echo "⚠️  System Python is protected. Installing to user directory..."
    python3 -m pip install -e . --user --break-system-packages 2>/dev/null || {
        echo ""
        echo "Error: Could not install. Try:"
        echo "  python3 -m pip install --user -e ."
        echo "Or use a virtual environment:"
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate"
        echo "  pip install -e ."
        exit 1
    }
fi

echo ""
echo "✓ Gopa installed successfully!"
echo ""
echo "Try it out:"
echo "  gopa --help"
echo "  gopa test"
echo "  gopa run examples/hello.gopa"
echo ""
echo "Note: If 'gopa' command not found, restart your terminal or run:"
echo "  export PATH=\$PATH:\$HOME/.local/bin"
echo ""

