# Quick Start Guide

## Installation

### From Source

```bash
git clone https://github.com/gopa-lang/gopa.git
cd gopa
pip install -e .
```

### Development Installation

```bash
pip install -e ".[network]"
pip install -r requirements-dev.txt
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

