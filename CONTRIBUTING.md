# contributing to gopa

i'm building gopa to be simple, safe, and fun. contributions are welcome if they move that goal forward.

## quick rules

- keep syntax beginner-friendly
- keep error messages readable (no compiler-goblin stuff)
- ship tests with changes
- don't add features that bypass the permission sandbox

## dev setup

requirements:

- python 3.11+
- (optional) `requests` for network tests/examples

clone, then:

```bash
python -m gopa_lang.gopa test
```

## repo structure (high level)

* `lexer.py` → turns source into tokens
* `parser.py` → turns tokens into an AST
* `interpreter.py` → runs the AST
* `builtin_stdlib.py` → string/list/random/io builtins
* `graphics_stub.py` → canvas + draw commands (stub or real backend)
* `packages.py` → install/use + registry + manifests + permission checks

## how to contribute

1. open an issue for what you want to do (or just start a draft PR)
2. keep PRs small and focused
3. add/modify tests in `tests/`
4. make sure `python -m gopa_lang.gopa test` passes

## coding style

* readability > cleverness
* explicit > magical
* prefer small pure functions
* no huge refactors without a heads up

## feature guidelines (important)

if you're adding anything that touches:

* network
* files
* server
* cron/timers
* python interop

it MUST go through permissions and have tests proving the permission gate works.

## reporting security issues

see [SECURITY.md](SECURITY.md)

thanks for helping build this.

