# Intent OS — Creator Colosseum Submission

**Entrant:** Haihao Xu (徐傲仓) — solo
**Repository:** https://github.com/haihaoxu/intentos
**Package:** `pip install intentos`
**Docs:** https://haihaoxu.github.io/intentos/
**License:** AGPLv3 (open source) + commercial license
**Version submitted:** v0.15.2

---

## 1. One sentence

**Intent OS is an open-source flight recorder for AI agents — it shows you exactly what your agent did, why it failed, and what it cost.**

```bash
pip install intentos

intent-os doctor          # What happened? What went wrong? What did it cost?
intent-os inspect latest  # Every step, every model call, every failure
```

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

The trace format looks like this:

```
  Agent Flight Recorder - Execution Trace
    [OK]  Goal:        refactor-auth-to-jwt
       Runtime:    anthropic (AnthropicAdapter)
       Duration:   14,327ms
       Cost:       $0.0842
       Tokens:     4,891
       Error:      Tests failed: 2 passed, 1 failed

    -- Timeline (6 events) --
    [14:02:01] > START (planner) refactor-auth-to-jwt
    [14:02:05] > START step=read-files
    [14:02:09] > INVOKE (adapter) modify-auth -- model=claude-sonnet-4
    [14:02:27] !! FAIL  run-tests (12713ms) -- reason="test_jwt_verify failed"
```

**Precision about what the demo is.** `intent-os demo --auto` renders the walkthrough above and requires **no API key and no network** — but it is a *scripted tour of the interface*, not a recording of a live run, and it does not persist a trace to the event store. A genuine recorded trace comes from `intent-os proxy start` (observe a real agent) or `intent-os run <manifest> --adapter <ollama|openai|anthropic>` (execute a real capability). I am stating this distinction explicitly because a viewer who runs `demo --auto` and then `inspect latest` will otherwise find no trace and reasonably conclude the tool is broken.

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

**Development method.** This was built with heavy AI-assisted development (Claude Code) across roughly four intensive days in July 2026 — 90 commits. The implementation volume was largely machine-generated. **My contribution was the parts an AI cannot do on its own: the architectural constraints, the specifications, and the verification discipline.**

I consider that honest accounting to be the most important paragraph in this submission, and Section 8 discloses it formally.

What I actually designed and enforced:

**1. A constitution of four unbreakable constraints.** Before writing any code I fixed four rules that every later design had to satisfy:

- **R1 — The Control Plane owns no state.**
- **R2 — No direct inter-processor communication** (everything routes through the Scheduler).
- **R3 — The Event Bus is the single source of truth.** All state changes are events.
- **R4 — Capabilities are stateless** (state lives in the Data Plane).

These exist to make "what did the agent do?" answerable *by construction* rather than by careful logging. R3 is why the Flight Recorder works at all: there is no second source of truth to drift from.

**2. Ten frozen specifications.** `specs/SPEC-0001` through `SPEC-0010` — capability manifest, workflow graph, event schema, security model, federated registry, agent context layer. "Frozen" means: implementation conforms to spec, spec does not bend to implementation. The reference runtime is the *first proof* of the spec, not its owner.

**3. A hard product boundary.** The project's firewall: **Intent OS does not standardize intelligence. It standardizes interaction.** It deliberately does *not* specify which model to use, how to write prompts, or how to reason. Every design decision is tested against this. Without it, the project would have drifted into being yet another agent framework.

**4. Verification discipline — 917 tests.** The suite is not decorative:

| Metric | Value |
|---|---|
| Passing tests | **917** (8 skipped, network-dependent) |
| Test code | 16,420 lines |
| Production code | ~31,150 lines |
| Total Python | **47,572 lines** |
| Non-test modules | 91 |
| CLI commands | 30 |
| Frozen specs | 10 |
| Full suite runtime | 60 seconds |

The suite runs in CI on every push, across Python 3.10, 3.11 and 3.12. I ran it immediately before writing this submission:

```
917 passed, 8 skipped, 10 deselected in 60.09s (0:01:00)
```

**5. Shipping, not demoing.** It is on PyPI. `pip install intentos` works on a machine that isn't mine.

**6. Finding a two-month-old bug that green tests were hiding.** Preparing this submission, I noticed CI had been failing since July and that the published "tests passing" badge was a static image nobody had verified. Chasing it down turned up four separate faults, one of which was in the product rather than the pipeline:

- CI installed from the repository root, where there is no `pyproject.toml` — so the install step had failed on every run and **the tests had never actually executed**. The badge was never true.
- `pytest` appeared in no dependency extra.
- `all = ["ask", ...]` referenced a sibling extra by name, which PEP 621 does not support; pip resolved it to an unrelated PyPI package called `ask` and installed a stranger's code.
- Once the suite finally ran on Linux, 18 tests failed. `parse_manifest` and `parse_workflow_yaml` accept either a file path or raw YAML, and told them apart with `Path(source).exists()` — which on POSIX raises `ENAMETOOLONG` for any string longer than a filename. A manifest is always longer than a filename. Windows returns `False` instead of raising, so this was invisible on the only machine it had ever been run on.

That last one is the one I would point at. The project's whole thesis is *"you should be able to see what actually happened"*, and its own test suite had been reporting success from a CI job that never ran, on one platform, hiding a defect in the parser at the centre of the system. Fixing it required replacing the check with one that tolerates OS-level failure, plus regression tests. CI is green across all three Python versions for the first time.

---

## 6. Feasibility and real-world potential

**It exists today.** This is the least speculative part of the submission:

| Claim | Verification |
|---|---|
| Installable | `pip install intentos` |
| Runs offline | `intent-os demo --auto` — zero config, no API key |
| Tested | 917 passing tests, green CI on Python 3.10 / 3.11 / 3.12 |
| Documented | 10 frozen specs + public docs site |
| Licensed | AGPLv3 + commercial terms in `COMMERCIAL.md` |

**Business model — open core.**

| Tier | Price | Includes |
|---|---|---|
| Individual | Free (AGPLv3) | All CLI commands, proxy, tracing, experience system |
| Team | $99/developer/month | + governance policy engine, audit reports, SSO, team management |
| Enterprise | Custom | + SLA, custom terms |

The strategic logic of open core fits this problem specifically: the free tier is *recording* (which benefits from being ubiquitous and trusted), and the paid tier is *governance* (which is what organizations actually pay for — audit trails, policy enforcement, SSO). AGPLv3 also means a company that wants to embed Intent OS in a distributed product must either open-source it or buy the commercial license.

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
- **Prior work, publicly disclosed.** Intent OS was published to a public GitHub repository and to PyPI in July 2026, two months before this competition. It is not new work created for this submission. `BLUEPRINT.md` and `POSITIONING.md` are in the public repository; `PITCH.md` is a local document from the same period.
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
pip install intentos && intent-os demo --auto
```
