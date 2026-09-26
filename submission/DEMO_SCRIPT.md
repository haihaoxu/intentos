# Demo Script — Intent OS

**Target length:** 90 seconds. Judges watch many submissions; assume they stop at 30 seconds.
**Goal:** prove three things fast — the problem is real, the tool works, and it works from the *outside*.

Record the terminal at a large font size (16pt+). The trace output is the product; make it readable without zooming.

---

## Pre-flight checklist

Run this **the day before recording** and confirm every line succeeds:

```bash
pip install "git+https://github.com/haihaoxu/intentos#subdirectory=reference-runtime"
intent-os demo --auto
intent-os inspect latest
```

**Order matters.** Run `demo --auto` *before* `inspect latest`. The demo writes the trace that `inspect latest` then reads. If you run `inspect latest` first on a clean machine, you get `No traces found` — do not film that.

**Clean-machine check.** To reproduce what a judge sees, isolate state:

```bash
HOME=/tmp/fresh-demo USERPROFILE=/tmp/fresh-demo intent-os demo --auto
```

---

## Shot list

### Shot 1 — The problem (0:00–0:12)

**On screen:** a terminal showing only this.

```
$ claude "refactor the auth module to use JWT"
...
Done.
$ pytest
FAILED tests/test_auth.py::test_jwt_verify
```

**Voiceover:**
> It's late. Your AI agent just spent twenty minutes refactoring your auth module. It says *Done*. Then your tests fail. It ran six steps, called a paid model, and edited your files — and you can see none of it.

---

### Shot 2 — Install (0:12–0:22)

**On screen:**

```bash
pip install "git+https://github.com/haihaoxu/intentos#subdirectory=reference-runtime"
intent-os demo --auto
```

Let the demo's opening lines render, then cut.

**Voiceover:**
> This is Intent OS. It's open source, it's on PyPI, and it needs no API key to try.

---

### Shot 3 — The reveal (0:22–0:50)

**On screen:** the demo's trace section. **Stop and point at four values in turn** (use a highlight or cursor):

```
[!!]  Goal:        refactor-auth-to-jwt
   Duration:   14327ms
   Cost:       $0.0842
   Tokens:     4891
   Error:      test_jwt_verify failed

-- Timeline (6 events) --
   [10:05:39] > START (runtime) refactor-auth-to-jwt task=plan
   [10:05:40] > INVOKE (adapter) read-files task=read-files
   [10:05:44] OK DONE  (runtime) read-files task=read-files
   [10:05:47] > INVOKE (adapter) modify-auth task=modify-auth
   [10:05:53] OK DONE  (runtime) modify-auth task=modify-auth
   [10:05:54] !! FAIL  (runtime) run-tests task=run-tests
```

**Voiceover:**
> Every step. Every model call. Every dollar. Every token. And the exact step that failed — `run-tests`, at 13.8 seconds in.

---

### Shot 4 — It's really recorded (0:50–1:05)

**On screen:** run `intent-os inspect latest` in a **new** shell. The same trace comes back.

```bash
intent-os inspect latest
```

**Voiceover:**
> And that wasn't a screenshot. That trace is in an event store on disk. Wipe the screen, run the command yourself — it comes back. This is a real record, not a mockup.

---

### Shot 5 — The actual claim (1:05–1:22)

**Verified working.** `llama3.2:1b` is pulled and this exact pair of commands
was run end-to-end on 2026-09-26; the model really inferred (18.6 s) and the
trace really came back from `inspect`.

**On screen:** a clean terminal, then this command and its output.

```bash
intent-os run examples/text_summarize.yaml --adapter ollama \
  --input '{"text": "Intent OS records what your AI agent did, why it failed, and what it cost."}'
intent-os inspect latest
```

**Expected:** `Runtime: ollama (OllamaAdapter)`, 3 events, and a real summary in
the output. Cost is `$0.0000` and tokens `0` — correct for a local model, which
reports neither. Do not "fix" those on screen; say why they are zero.

> The `Duration` field reads `0ms` on this path — the run path does not populate
> it the way the demo path does. Either narrate around it or trim the shot before
> that line. Do not edit the output.

**Voiceover:**
> This is a genuine run, captured from the outside. And that's the part that matters — Intent OS records at the **network boundary**. No SDK. No code changes. No framework assumptions.

**On screen (overlay, no narration needed):**

```
✗ SDK instrumentation   →  needs code you control
✗ Framework plugins     →  needs a framework you chose
✓ Proxy-level recording →  works on closed agents
```

**Voiceover:**
> Which means it works on the agents you *don't* own — Claude Code, Codex, Cursor. The ones you can only watch from the outside.

---

### Shot 6 — Close (1:22–1:30)

**On screen:** keep this short — a long pinned URL does not read at a glance.

```
github.com/haihaoxu/intentos
pip install "…intentos#subdirectory=reference-runtime"
AGPLv3
```

**Voiceover:**
> Intent OS. Your agent isn't a black box anymore.

---

## What not to do

| Don't | Why |
|---|---|
| Show `inspect latest` before `demo --auto` | Empty store → `No traces found` → looks broken |
| Claim the demo is a live capture | It's a scripted tour. Say "demo", mean demo. The real capture is Shot 5. |
| Read the whole trace aloud | Judges can read. Narrate only what to notice. |
| Show the 47k lines / 912 tests in the video | That's for the written submission. The video is 90 seconds. |
| Add background music trends | Screen recording, clear voice, no music. |

---

## If the video is cut to 30 seconds

Keep **Shot 1** (8s) + **Shot 3** (15s) + **Shot 5 one-liner** (7s):

> Agent says "Done". Tests fail. Here's every step, every model call, every dollar, and the exact step that broke — recorded from *outside* the agent, so it works on Claude Code and Cursor too.
