# security policy

gopa runs code, which means security matters.

## supported versions

right now: whatever is on `main`.

once gopa has releases, we'll define active supported versions.

## reporting a vulnerability

please do NOT open a public issue for security bugs.

include:

- what you found
- minimal repro code
- expected vs actual behavior
- impact (what can an attacker do?)
- environment (os, python version, commit hash)

## what we care about most

- sandbox escapes (files/network/server without permission)
- arbitrary code execution via packages
- python interop bypassing allowlists
- denial-of-service (infinite loops, memory blowups) without guardrails

we'll respond asap and coordinate a fix + disclosure.

