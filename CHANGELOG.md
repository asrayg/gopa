# Changelog

All notable changes to Gopa will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-30

### Added
- Initial release of Gopa Programming Language
- English-like syntax with `end`-terminated blocks
- Dynamic types: numbers, strings, booleans, nothing, lists, objects, dictionaries
- Control flow: if/otherwise, repeat loops, break/continue/stop
- Functions with recursion and closures
- List operations: filter, map, add, remove, sort, reverse, shuffle
- Dictionary and object literals
- String operations: split, join, replace, find, slice
- Match statements with range matching
- Web API support (GET/POST) with permission sandbox
- File I/O with permission sandbox
- Graphics stubs: canvas, drawing primitives, mouse events
- Timer system: wait, after, every, named jobs
- Server blocks: HTTP server with GET/POST handlers
- Cron scheduling: friendly and standard cron syntax
- Package manager: local install/use, stdlib support
- Python FFI: safe allowlist (math, random, datetime, re)
- Permission sandbox: network, files, graphics, sound, packages, python_ffi, server, timers, cron
- CLI: run, test, repl commands
- Comprehensive test suite with 19 conformance tests
- Standard library modules: math, time, colors, sounds, turtle, games, charts

### Security
- All network/file/server operations require explicit permissions
- Python interop restricted to allowlist
- Package permissions checked before loading

