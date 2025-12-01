# Getting Started with Gopa

## The Fastest Way

### 1. Clone the repo
```bash
git clone https://github.com/gopa-lang/gopa.git
cd gopa
```

### 2. Use it immediately (no install needed!)

**macOS / Linux:**
```bash
./gopa test
./gopa run examples/hello.gopa
```

**Windows:**
```bash
python gopa test
python gopa run examples\hello.gopa
```

That's it! You're ready to code.

## Make it Global (Optional)

If you want to use `gopa` from anywhere:

```bash
bash install.sh
```

Then you can use:
```bash
gopa test
gopa run myfile.gopa
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
./gopa run hello.gopa
```

## What's Next?

- Check out `examples/` for more examples
- Read the [full documentation](README.md)
- Try the REPL: `./gopa repl`

