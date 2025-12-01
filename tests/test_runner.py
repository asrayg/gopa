"""Test runner for Gopa conformance tests."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gopa_lang.gopa import run_tests

if __name__ == '__main__':
    sys.exit(run_tests())

