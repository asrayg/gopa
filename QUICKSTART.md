# Quick Start Guide

## Installation

### Option 1: Install Script (Recommended)

**macOS / Linux:**
```bash
git clone https://github.com/gopa-lang/gopa.git
cd gopa
bash install.sh
```

**Windows:**
```powershell
git clone https://github.com/gopa-lang/gopa.git
cd gopa
.\install.bat
```

After installation, the `gopa` command is available globally.

### Option 2: Use Directly (No Install)

Just clone and use the `gopa` script directly:

```bash
git clone https://github.com/gopa-lang/gopa.git
cd gopa
./gopa test
./gopa run examples/hello.gopa
```

**Windows:**
```powershell
git clone https://github.com/gopa-lang/gopa.git
cd gopa
python gopa test
python gopa run examples\hello.gopa
```

### Verify

```bash
gopa --help
gopa test
```

## Your First Program

Create `hello.gopa`:

```gopa
say "Hello, Gopa!"
name is "World"
say "Hello, " and name
```

Run it:

```bash
gopa run hello.gopa
```

## Common Commands

```bash
# Run a program
gopa run program.gopa

# Run with permissions
gopa run program.gopa --perm network,files

# Run tests
gopa test

# Start REPL
gopa repl
```

## Next Steps

- Check out `examples/` for more examples
- Read the [full documentation](https://gopa.dev/docs)
- Join the [community](https://gopa.dev/community)

