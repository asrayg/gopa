# Installation

## Quick Install (Recommended)

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/gopa-lang/gopa/main/install.sh | bash
```

Or manually:

```bash
git clone https://github.com/gopa-lang/gopa.git
cd gopa
bash install.sh
```

### Windows

```powershell
# In PowerShell
git clone https://github.com/gopa-lang/gopa.git
cd gopa
.\install.bat
```

## Verify Installation

After installation, verify it works:

```bash
gopa --help
gopa test
```

You should see the help menu and tests running.

## Usage

Once installed, use `gopa` directly:

```bash
# Run a program
gopa run program.gopa

# Run tests
gopa test

# Start REPL
gopa repl

# Run with permissions
gopa run program.gopa --perm network,files
```

## Troubleshooting

### Command not found

If `gopa` command is not found:

1. Make sure Python's bin directory is in your PATH
2. Try: `python3 -m pip install --user -e .`
3. Restart your terminal

### Python version

Gopa requires Python 3.11+. Check your version:

```bash
python3 --version
```

If you need to upgrade Python, visit [python.org](https://www.python.org/downloads/)

