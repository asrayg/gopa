<div align="center">

<img src="https://drive.google.com/uc?export=view&id=1rtY0U7miS549C_mmOruCArjJqdvLTZhp" alt="Gopa Logo" width="200"/>

# Gopa Programming Language

### (or just **Gopa**)

A tiny, readable programming language that feels like English — built so **kids can code**, but still powerful enough to build real stuff.

[Contributing](CONTRIBUTING.md)

</div>

---

## what is gopa?

gopa is a beginner-first language with "sentence" syntax:

```gopa
name is "asray"
x is 4
repeat 5 times
  say "x is " and x
  x becomes x plus 1
end
```

it's designed to be:

* **readable** (no punctuation soup)
* **safe by default** (permissions for network/files/servers)
* **fun** (graphics + events for instant feedback)
* **real** (functions, recursion, lists/dictionaries, api calls, servers, cron)

---

## why gopa?

* **low friction:** kids can read the code out loud and understand it.
* **fast feedback:** prints, simple graphics, simple input — great for learning.
* **safe sandbox:** no surprise filesystem/network access unless you allow it.
* **practical:** you can still do real programming (data structures, api calls, servers).

---

## quick start

> requirements: python 3.11+

### install (super quick)

**Option 1: Install script (recommended)**
```bash
git clone https://github.com/gopa-lang/gopa.git && cd gopa && bash install.sh
```

**Option 2: Use directly (no install needed)**
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
.\install.bat
```

### use

```bash
# Run a program
gopa run examples/hello.gopa

# Run tests
gopa test

# Start REPL
gopa repl

# With permissions
gopa run examples/weather.gopa --perm network
gopa run examples/server.gopa --perm server,network
gopa run examples/cron.gopa --forever --perm cron,timers
```

---

## example snippets

### api calls

```gopa
city is "Ames"
weather is get "https://api.weather.com/today" using city is city
say weather.temp
```

### graphics (stubbed or real, depending on runtime)

```gopa
canvas is create canvas 400 by 400
draw circle at 100, 100 with size 50 and color "red"
```

### server that runs forever

```gopa
server on port 3000
  when get "/"
    return "hello world"
  end
end
```

### cron

```gopa
cron "every day at 9:00"
  say "good morning"
end
```

---

## getting help

* open an issue if something's broken or unclear
* if you found a security issue, please follow [SECURITY.md](SECURITY.md)

---

## contributing

want to build gopa with me? love that.

start here: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## license

gopa is dual-licensed under either of:

* Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE))
* MIT License ([LICENSE-MIT](LICENSE-MIT))

you can pick whichever works for you. see [LICENSE](LICENSE).

---

## trademark

"gopa" and the gopa logo are trademarks of the project maintainers (not trying to be annoying — just keeping naming clean). if you're building something based on gopa, you can say "built with gopa" without asking.
