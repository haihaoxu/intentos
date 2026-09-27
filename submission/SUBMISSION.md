# Intent OS — Creator Colosseum Submission

**Entrant:** Haihao Xu — solo
**Repository:** https://github.com/haihaoxu/intentos
**Install:** `pip install "git+https://github.com/haihaoxu/intentos#subdirectory=reference-runtime"`
**Docs:** https://haihaoxu.github.io/intentos/
**License:** AGPLv3 (open source) + commercial license
**Version submitted:** v0.15.2 (source); PyPI carries v0.15.2 from July 2026

---

## 1. One sentence

**Intent OS is an open-source flight recorder for AI agents — it shows you exactly what your agent did, why it failed, and what it cost.**

```bash
pip install "git+https://github.com/haihaoxu/intentos#subdirectory=reference-runtime"

intent-os doctor          # What happened? What went wrong? What did it cost?
intent-os inspect latest  # Every step, every model call, every failure
```

> **A note on installing.** Install from the repository, not from PyPI. The published `intentos` 0.15.2 on PyPI dates from July 2026 and predates the fixes described in Section 5 — including the one that makes `demo` record a trace at all. Installing from the repository gives you the version this submission describes. The PyPI release has not been superseded because publishing a new version is a separate step I have not taken.

---

## 2. The problem

AI coding agents have become genuinely useful, and almost completely opaque.

You give an agent a task. It thinks for several minutes. It reads files, calls a model, edits code, runs a test suite. Then it reports one line: **"Done."** — or worse, it fails and tells you nothing about where.

Concretely, an agent run looks like this:

```
Task: Refactor authentication module to use JWT

  [Planning] Planner created workflow with 4 steps
  [Reading]  Read files: auth.py, config.py, requirements.txt
  [Model]    Called Claude Sonnet 4 (prompt: 2,451 tokens)
  [Writing]  Modified auth.py (+89 lines, -23 lines)
  [Testing]  Ran pytest tests/test_auth.py
  [Result]   Tests failed: 2 passed, 1 failed
```

Six steps. A paid model call. Files changed on disk. **A failure.** And a typical agent surfaces none of it.

Today, if you want to know what an agent actually did, your options are:

- **Read its chat log** — which is a narrative, not a record. It tells you what the agent *said* it did.
- **Adopt a hosted observability SaaS** — which requires SDK instrumentation inside your code, assumes you control the framework, and ships your traces to someone else's cloud.
- **Guess.**

None of these work when the agent is a black box you don't own — which is increasingly the normal case. Claude Code, Codex, and Cursor are closed products. You cannot add an SDK to them. You can only watch them from the outside.

**The gap: agents are becoming the primary way software gets written, and we have no flight recorder for them.**

---

## 3. What Intent OS does

Intent OS records agent execution from the **outside**, at the network and process boundary — no SDK integration, no framework assumptions, no code changes.

This is the core design bet, and it is what separates Intent OS from existing tools: **it does not require the agent to cooperate.** It intercepts the API calls an agent makes and reconstructs what happened from them.

Three commands carry the product:

| Command | Question it answers |
|---|---|
| `intent-os proxy start` | *Record everything.* Sits between the agent and the model API. |
| `intent-os inspect latest` | *What happened?* Reconstructs a timeline: goal, steps, model calls, tokens, cost, failure point. |
| `intent-os doctor` | *What went wrong, and how do I fix it?* Diagnoses the failure and suggests an action. |

The trace `demo --auto` produces looks like this (trimmed; timings vary per run):

```
  Agent Flight Recorder - Execution Trace

  [!!]  Goal:        refactor-auth-to-jwt
     Runtime:    anthropic (AnthropicAdapter)
     Duration:   14327ms
     Cost:       $0.0842
     Tokens:     4891
     Error:      test_jwt_verify failed

  -- Timeline (6 events) --

  [10:05:39] > START (runtime)   refactor-auth-to-jwt  task=plan
  [10:05:40] > INVOKE (adapter)  read-files            task=read-files
  [10:05:44] OK DONE  (runtime)  read-files            task=read-files
  [10:05:47] > INVOKE (adapter)  modify-auth           task=modify-auth
  [10:05:53] OK DONE  (runtime)  modify-auth           task=modify-auth
  [10:05:54] !! FAIL  (runtime)  run-tests             task=run-tests
```

**Precision about what the demo is.** `intent-os demo --auto` requires **no API key and no network**. The narrative it prints is a *scripted tour of the interface*, not a live capture — but it records a synthetic run to the event store as it goes, attributed to `demo-agent`, so the `inspect latest` it points you at returns a real trace with six events, a cost, and the failing step. A capture of your *own* agent comes from `intent-os proxy start`; a real capability execution comes from `intent-os run <manifest> --adapter <ollama|openai|anthropic>`.

---

## 4. Why this is more than a log viewer

A flight recorder alone is a tool. The reason I kept building is that once execution is recorded as structured data, it becomes a substrate for things a chat log can never support.

Intent OS is built as **seven layers of an execution contract**:

```
1. Context        — what environment an agent runs in
2. Identity       — who this agent is, what it is permitted to do
3. Execution      — the workflow: plan, steps, retries, failure semantics
4. Verification   — evidence for what the agent claims it did
5. Governance     — policy enforcement, audit reports
6. Interoperability — capability manifests, cross-runtime portability
7. Experience     — what the agent learned, carried forward
```

The layer I find most interesting is **7 — Experience**. Agents today have amnesia. Claude Code spends 30 minutes researching, trying approaches, hitting dead ends, and learning from mistakes. You close the session. Everything it learned is gone. Tomorrow it starts from a blank slate and repeats the same dead ends.

That is not a model-capability problem. It is a **missing infrastructure layer** problem. The model is capable of learning from experience; nothing persists the experience for it to learn from.

Intent OS records execution events into a store that outlives the session, then extracts durable patterns from them — failure patterns, successful strategies — and makes them queryable:

```bash
intent-os experience record --agent <id> --type failure_pattern --observation "..."
intent-os experience extract --agent <id>
intent-os experience query "how to handle timeout"
```

This is what turns a flight recorder from a debugging tool into infrastructure.

---

## 5. Thoughtfulness of execution

I want to be direct about how this was built, because the repository is public and the git history is readable.

**Development method.** The work was AI-assisted throughout (Claude Code), so the implementation volume was largely machine-generated. **What is mine is the part an AI cannot originate on its own behalf: the architectural constraints, the specifications, the scope decisions, and the verification discipline.**

I consider that honest accounting to be the most important paragraph in this submission, and Section 8 discloses it formally.

What I actually designed and enforced:

**1. A constitution of four unbreakable constraints.** Before writing any code I fixed four rules that every later design had to satisfy:

- **R1 — The Control Plane owns no state.**
- **R2 — No direct inter-processor communication** (everything routes through the Scheduler).
- **R3 — The Event Bus is the single source of truth.** All state changes are events.
- **R4 — Capabilities are stateless** (state lives in the Data Plane).

These exist to make "what did the agent do?" answerable *by construction* rather than by careful logging. R3 is why the Flight Recorder works at all: there is no second source of truth to drift from.

**2. Ten specification documents, written before the code.** `specs/SPEC-0001` through `SPEC-0010` — capability manifest, workflow graph, event schema, security model, federated registry, agent context layer. **Seven carry a v1.0 status; three are still design drafts** (the `ask` command, the federated registry, and the agent context layer). For the frozen ones the rule is: implementation conforms to spec, spec does not bend to implementation, and the reference runtime is the *first proof* of the spec rather than its owner. I state the split rather than the flattering version because the drafts are exactly where the spec-first method has not yet paid off.

**3. A hard product boundary.** The project's firewall: **Intent OS does not standardize intelligence. It standardizes interaction.** It deliberately does *not* specify which model to use, how to write prompts, or how to reason. Every design decision is tested against this. Without it, the project would have drifted into being yet another agent framework.

**4. Verification discipline — 919 tests.** The suite is not decorative:

| Metric | Value |
|---|---|
| Passing tests | **919** (8 skipped, network-dependent) |
| Test code | 16,465 lines |
| Production code | ~31,200 lines |
| Total Python | **47,663 lines** |
| Non-test modules | 91 |
| CLI commands | 30 |
| Frozen specs | 10 |
| Full suite runtime | 60–70 seconds (Windows, CPU only) |

The suite runs in CI on every push, across Python 3.10, 3.11 and 3.12. I ran it immediately before writing this submission:

```
919 passed, 8 skipped, 10 deselected in 70.40s (0:01:10)
```

**5. Shipping, not demoing.** It is published to PyPI and installable from the repository. `pip install` works on a machine that isn't mine.

**6. What preparing this submission actually found.** I set out to check whether the project's own claims about itself were true. Thirteen of them were not. I think this is the most useful thing in the submission, so I have not tidied it up.

*The demo showed a trace it never recorded.* `demo --auto` printed a convincing execution record and wrote nothing to the event store, so the `inspect latest` the README invites you to run next returned "No traces found". The output looked like evidence and was not.

*The test suite had never run.* CI installed from the repository root, where there is no `pyproject.toml`, so the install step failed on every run. The "tests passing" badge in the README was a static image that encoded a number nobody had verified. Three further faults sat behind it: `pytest` appeared in no dependency extra; `all = ["ask", ...]` referenced a sibling extra by name, which PEP 621 does not support, so pip resolved it to an unrelated PyPI package called `ask` and installed a stranger's code; and once the suite finally ran on Linux, 18 tests failed because `parse_manifest` distinguished "a path" from "YAML text" with `Path(source).exists()` — which on POSIX raises `ENAMETOOLONG` for any string longer than a filename, and a manifest always is. Windows returns `False` instead of raising, so it was invisible on the only machine it had ever run on.

*The flight recorder did not record, and could not be read.* Two separate defects. The proxy opened its own `events.db` while every reading command — `inspect`, `doctor`, `event` — opened the shared `intent.db`, so captured agent traffic went somewhere nothing looked; the project's own notes had this logged as technical debt, without noting that it meant the headline feature silently did nothing. Then, once both sides shared one database, `inspect` still found nothing, because it listed traces from `execution_records` and proxy traffic is recorded as events. Fixing that surfaced a third: the renderer read `cost`, `tokens` and `error` outside the branch that assigned them, and a proxy trace is exactly the case where that branch never runs. A fourth was already there — the timeline header printed twice with the totals stranded between the two.

*It said everything twice, and advertised a command it does not have.* The trace summary printed once in the identity block and again under the timeline header. And `inspect` closed by telling you to run `intent-os replay <id>` — a command that has never existed; typing it returns `invalid choice: 'replay'`. I found both while building the screenshots for this page, which is the least flattering way to find them.

*Two claims about the project itself were overstated.* I had written "ten frozen specifications": six are marked Frozen, three are still `Design Draft v0.1`. And `COMMERCIAL.md` sold governance, audit reporting and SSO as commercial-only when nothing in the codebase is gated at all — those commands run in the free build, and SSO does not exist at all. I had been repeating claims from documents written alongside the code rather than checking the files. Both are corrected here and in the repository.

*Why I am reporting this rather than just the fixes.* A flight recorder whose own test suite reported success from a job that never executed, whose own capture path wrote to a database nothing read, and whose own output recommended a command it does not have, is a specific and interesting kind of failure: every component worked, and the connections between them did not. That is the failure mode this product exists to make visible. Finding it in my own project, with the tool's own philosophy as the method, is the most honest demonstration of the idea I can offer — and it is why the trace output on this page comes from a path I have watched work rather than one I assumed worked.

All of it is in the public history: the commits dated 2026-09-26, authored `Haihao Xu`, with the reasoning in the messages. CI is green across all three Python versions for the first time. Local suite:

```
919 passed, 8 skipped, 10 deselected in 70.40s (0:01:10)
```


---

## 6. Feasibility and real-world potential

**It exists today.** This is the least speculative part of the submission:

| Claim | Verification |
|---|---|
| Installable | `pip install "git+https://github.com/haihaoxu/intentos#subdirectory=reference-runtime"` |
| Runs offline | `intent-os demo --auto` — zero config, no API key |
| Tested | 919 passing tests, green CI on Python 3.10 / 3.11 / 3.12 |
| Documented | 10 specs (7 at v1.0, 3 drafts) + public docs site |
| Licensed | AGPLv3 + commercial terms in `COMMERCIAL.md` |

**Business model — open core, not yet enforced.**

| Tier | Price | Intended to include |
|---|---|---|
| Individual | Free (AGPLv3) | Everything that exists today |
| Team | $99/developer/month | Governance, audit reporting, SSO, team management |
| Enterprise | Custom | SLA, custom terms |

**What is real, and what is a plan.** Nothing is gated. There is no licence check anywhere in the codebase — I searched — and `intent-os security policy` and `intent-os audit report` both run in the free build. SSO does not exist at all. The paid tier is an intention, not a product, and I am labelling it that way rather than presenting a pricing table as though a customer could buy it today.

I am stating this plainly because the alternative is easy to catch: anyone who installs the free build and runs `intent-os audit report` finds the "commercial" feature working, and would be right to distrust the rest of this document. `COMMERCIAL.md` in the repository carries the same correction.

The strategic logic of open core fits this problem specifically: the free tier is *recording* (which benefits from being ubiquitous and trusted), and the paid tier is *governance* (what organisations actually pay for — audit trails, policy enforcement, SSO). AGPLv3 also means a company that wants to embed Intent OS in a distributed product must either open-source it or buy the commercial licence. That is the argument for the model; the model itself is unbuilt.

**Market.** Every team running agents in production has the same question and no good answer: *what did it do, and what did it cost?* The category is real and growing — which is also the honest risk, addressed next.

---

## 7. Honest assessment of competition and risk

**This space has incumbents.** LangSmith, Langfuse, Helicone, and W&B Weave all operate in agent observability. I am not going to pretend otherwise.

My differentiator is architectural, not marketing: **those tools instrument from the inside (SDK in your code, assumes you own the framework); Intent OS observes from the outside (proxy-level, works on closed agents you do not control).** Claude Code, Codex, and Cursor cannot be SDK-instrumented. That is a real and growing gap — but it is a gap I am *arguing* exists, not one I have proven with paying customers.

**Honest state of traction:**

| Metric | Reality |
|---|---|
| GitHub stars | **2** |
| External users | **None yet** |
| Paying customers | **None** |
| My status as a user | Not yet a daily user — this is a stated internal P0 |

I built working infrastructure but have not yet found product-market fit. I am reporting that plainly because the alternative — presenting adoption I don't have — would be dishonest, and because knowing precisely where a project is weak is more useful to a judge than a polished overstatement.

**The specific risk.** Standards and infrastructure projects face a cold-start problem: the value depends on adoption, and adoption depends on value. Intent OS survives this only if the free tier is immediately useful *to one developer with no network effects* — which is exactly why I led this submission with the Flight Recorder rather than the interoperability standard. Recording your own agent's execution is valuable on day one, alone. Standardizing cross-runtime execution is valuable only at scale.

---

## 8. Disclosure

Full detail in [`DISCLOSURE.md`](DISCLOSURE.md). Summary:

- **AI-assisted development.** Built with Claude Code. Implementation was largely machine-generated; architecture, specifications, constraints, and verification are mine. I have not represented it as hand-written.
- **Prior work, publicly disclosed.** The Intent OS project was published to a public GitHub repository and to PyPI in July 2026, before this competition — it is not work created for this submission. `BLUEPRINT.md` and `POSITIONING.md` are in the public repository; `PITCH.md` is a local document from the same period. What *is* new is the `submission/` directory and the defect fixes described in Section 5; both are dated 2026-09-26 and authored under my name.
- **Third-party dependencies.** `pyyaml`, `requests`; optional `openai`, `anthropic` adapters. All standard, all credited.
- **Third-party ideas.** The POSIX / OCI / Kubernetes historical analogy in `POSITIONING.md` is borrowed framing from those ecosystems and is attributed as such.

---

## 9. Roadmap

**Next 30 days — become user #1.** Run `intent-os proxy start` continuously for a week and fix whatever breaks. The project has never been used by anyone, including me, for a sustained period. That is the highest-value next step and it does not require anyone's permission.

**Next 90 days — first external user.** Publish to Hacker News and r/LocalLLaMA (drafts exist in `HN_POST.md`), and instrument feedback into the Experience layer — so the tool's first users' problems become the tool's next features.

**Next 12 months — governance as the paid product.** The commercial tier depends on the governance layers being real. Policy enforcement and audit reporting exist at a basic level; they need to be good enough that a security-conscious team would pay for them.

---

## 10. Why I built this

I am a high-school student in Ningbo, China, planning to study quantitative finance. I use coding agents constantly, and the thing that frustrated me was never that they failed — it was that when they failed, **I could not find out why.**

I didn't want a better agent. I wanted to be able to see.

That instinct — that the missing piece is usually the layer nobody is building, not the model everyone is racing on — is the same instinct that draws me to quantitative finance. The edge is rarely in the thing everyone is watching.

---

## 11. Links

| | |
|---|---|
| Repository | https://github.com/haihaoxu/intentos |
| PyPI | https://pypi.org/project/intentos/ |
| Documentation | https://haihaoxu.github.io/intentos/ |
| License | AGPLv3 — https://github.com/haihaoxu/intentos/blob/main/LICENSE |
| Commercial terms | `COMMERCIAL.md` |

**Try it in 30 seconds, no API key required:**

```bash
pip install "git+https://github.com/haihaoxu/intentos#subdirectory=reference-runtime" && intent-os demo --auto
```
