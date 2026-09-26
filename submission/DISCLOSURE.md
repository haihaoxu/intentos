# Disclosure Statement — Intent OS

**Entrant:** Haihao Xu (徐傲仓) — GitHub: [@haihaoxu](https://github.com/haihaoxu)
**Submission:** Creator Colosseum, 2026

This document satisfies the competition's **Originality** requirements:

> *"Outside tools, libraries, or resources may be used if properly credited."*
> *"Any prior work included should be clearly disclosed."*

Everything below is stated so that it can be independently verified against the public record. Where a claim is checkable, I give the check.

---

## 1. Summary

| Item | Disclosure |
|---|---|
| AI-assisted development | **Yes — extensive.** Built with Claude Code. (Section 2) |
| Prior work, pre-dating this competition | **Yes.** Built in four days, July 2026; published the same week. (Section 3) |
| Third-party code dependencies | `pyyaml`, `requests`; optional `openai`, `anthropic`. (Section 4) |
| Third-party ideas / framing | POSIX / OCI / Kubernetes analogy, borrowed and attributed. (Section 5) |
| Work I claim as mine | Architecture, specifications, constraints, verification. (Section 6) |

---

## 2. AI-assisted development

**Intent OS was built with heavy use of Claude Code (Anthropic).**

A `CLAUDE.md` session-context file — the working document I used to brief the AI assistant — exists in my **local working copy**, and I can supply it on request. I am noting precisely where it lives because it is **not** in the public repository: `CLAUDE.md` is listed in `.gitignore`, so a person cloning the repo will not see it, and neither will a person reading the commit history. My AI assistance is therefore **not** discoverable from the repository — which is exactly why I am stating it here rather than relying on a reader to notice it.

**How the work divided:**

| Machine-generated | Mine |
|---|---|
| Most implementation code | The four constitutional constraints (R1–R4) |
| Most test bodies | The ten frozen specifications (`specs/SPEC-0001`–`SPEC-0010`) |
| Boilerplate, CLI plumbing | The product boundary ("does not standardize intelligence") |
| Docstrings, error messages | Deciding *what to build and what to refuse to build* |
| Most documentation prose | Verifying the result: running the suite, rejecting what failed |

**What I am not claiming.** I am not claiming to have hand-written 47,663 lines of Python. At 90 commits across four days (2026-07-22 to 2026-07-25), that would be implausible on inspection, and the git history is public.

**What I am claiming.** The architectural decisions, the constraint system, the specification-first method, and the verification discipline are my work. These are the parts that determine whether a project holds together, and they are the parts an AI cannot originate on its own behalf.

**Why I used AI, and why I am stating it plainly.** The competition rules explicitly permit outside tools when credited. I judged that a clear disclosure is more defensible than an ambiguous one, and that a project whose own thesis is *"you should be able to see exactly what happened"* would be poorly served by an opaque account of how it was made.

---

## 3. Prior work

**Intent OS is prior work. It was not created for Creator Colosseum.**

To be precise about what is old and what is new: the *project* — all 47,663 lines, the specs, the architecture, the PyPI package — was **built in four days** and is submitted as-is. The commits dated 2026-09-26, and the `submission/` directory itself, are **new work created for this submission**. The commit messages state plainly what each one changes, and the git history distinguishes them by author name.

**On the duration — and why "prior work" does not mean "long-running".** Intent OS was written in a single four-day stretch, 2026-07-22 to 2026-07-25. It was then published and left alone for two months: there are **zero commits between 2026-07-25 and 2026-09-26**. The two-month figure elsewhere in this disclosure is the age of the *publication*, not the length of the work. The development was one sprint, and the git history shows it plainly — `git log --format=%ad --date=format:%Y-%m | sort | uniq -c` returns 90 commits in 2026-07 and 10 in 2026-09, with nothing in August.

**Timeline:**

| Date | Event |
|---|---|
| 2026-07-22 → 07-25 | **The whole build.** 90 commits in four days (prior work) |
| 2026-07-25 | Published: public GitHub repository, `main` pushed |
| 2026-07 | Released to PyPI as `intentos` |
| 2026-07-26 → 09-25 | **Dormant. Zero commits.** |
| 2026-09-26 | Submission directory and eight defect fixes, in the commits dated today (**new work**) |
| 2026-09-26 | This submission |

**How to verify:**

- **Git history** — the repository is public. `git log` shows 90 commits authored `Intent OS` dated 2026-07-22 through 2026-07-25, all pre-dating this competition, plus the commits dated 2026-09-26 authored `Haihao Xu` — count them with `git log --since=2026-09-26`.
- **PyPI release dates** — `intentos` has been publicly installable since July 2026: https://pypi.org/project/intentos/
- **Docs site** — https://haihaoxu.github.io/intentos/ has been live since July 2026.

**The new commits, and why they exist.** Building this submission meant checking the claims the project made about itself, and eight of them turned out to be false. The commits fix the defects behind those claims: `demo` printed a trace it never recorded; CI had never once executed the test suite, so the "tests passing" badge had never been verified; the proxy wrote captured agent traffic to a database no command read; `inspect` could not list a trace that had no execution record; and the parser mistook manifest text for a filename on POSIX. None of these change what the product is, and all of them are visible in the diff. I am flagging them because a submission that quietly patches its own record while claiming to disclose everything would be a contradiction.

**Pre-existing documents.** These were written during the July development period, before this competition.

**Publicly visible** (tracked in the repository, readable by anyone):

| File | Purpose |
|---|---|
| `POSITIONING.md` | Positioning statement (frozen v1.0, July 2026) |
| `BLUEPRINT.md` | Seven-layer architecture roadmap |
| `GO_TO_MARKET.md` | Go-to-market plan |
| `COMMERCIAL.md` | Commercial license terms |
| `EXECUTION_CONTRACT.md` | Strategic definition |
| `CONSTITUTION.md` | R1–R4 constraints |
| `ROADMAP.md` | Development roadmap |
| `HN_POST.md` | Launch post draft |
| `CHANGELOG.md` | Version history |
| `specs/SPEC-0001`–`SPEC-0010` | Ten frozen specifications |

**Local only — NOT in the public repository** (listed in `.gitignore`, absent from both the tree and the commit history):

| File | Purpose |
|---|---|
| `PITCH.md` | Project overview written in July |
| `CLAUDE.md` | AI session-context working document |
| `PLAN.md`, `GUIDE.md`, `STRATEGY.md`, `HANDOVER.md` | Internal planning documents |
| `AGENT_HOOK.md`, `CONTENT_PLAN.md` | Internal working notes |
| `site/` | Built documentation site |

I can supply any of the local-only files on request.

**Important — conflicting positioning between documents.** The July documents describe the project under an earlier framing ("an interoperability standard for AI capabilities," using a POSIX / OCI / Kubernetes analogy). The product subsequently evolved, and `README.md` and `pyproject.toml` now frame it as an **agent flight recorder**. The public `POSITIONING.md` still carries the earlier framing; the local-only `PITCH.md` and `CLAUDE.md` additionally carry stale version numbers and metrics (`v0.4.0` / `v0.5.0`, where the shipped version is `0.15.2`).

**`SUBMISSION.md` uses the current, verified framing and metrics.** Where the July documents and `SUBMISSION.md` disagree on a number, the July documents are out of date and `SUBMISSION.md` reflects the state I verified immediately before submitting. This discrepancy is disclosed rather than quietly corrected, because the earlier documents are part of the public record.

---

## 4. Third-party code dependencies

| Package | Role | License |
|---|---|---|
| `pyyaml` | Manifest parsing | MIT |
| `requests` | HTTP (proxy, registry) | Apache-2.0 |
| `openai` | Optional OpenAI adapter | Apache-2.0 |
| `anthropic` | Optional Anthropic adapter | MIT |
| `pytest` | Test framework (development) | MIT |

No third-party source code was copied into this repository. All dependencies are consumed as declared package dependencies.

**Model providers.** The `ask` command and the runtime adapters call external LLM APIs (OpenAI, Anthropic) when the user supplies their own API key. No API keys are included in this repository — the git history was scanned and contains only `.env.example`, which holds placeholder values.

---

## 5. Third-party ideas and framing

**The POSIX / OCI / Kubernetes analogy** used in `POSITIONING.md` is borrowed from those projects' own historical positioning, used as an explanatory analogy. `POSITIONING.md` explicitly notes that Intent OS "does not claim to be 'the Linux of AI.'"

**MCP comparison.** `POSITIONING.md` positions Intent OS as complementary to Anthropic's Model Context Protocol (MCP). MCP is a third-party project; the comparison is descriptive.

**Agent observability category.** `SUBMISSION.md` Section 7 names LangSmith, Langfuse, Helicone, and W&B Weave as operating in the same category. These are third-party products, referenced for honest competitive positioning, not incorporated.

No third-party ideas are claimed as original. The original contributions claimed here are the R1–R4 constraint system, the seven-layer execution contract, the ten specifications, and the outside-observer (proxy-level) recording architecture.

---

## 6. Authorship statement

I, **Haihao Xu**, am the sole author of Intent OS. The GitHub account `haihaoxu` owns the repository. Development took place on my own hardware during July 2026.

**One caveat on the commit record.** The 90 commits from July 2026 are authored under the name **`Intent OS`** rather than `haihaoxu` — a git configuration choice from the initial setup. Their author field therefore does not directly display my name, and a reader of `git log` cannot confirm authorship from it alone.

The commits dated 2026-09-26 **are** authored under my real name (`Haihao Xu <haihao.xu@outlook.com>`), so the repository history now contains entries that tie my identity to the project and to work I did on it. Repository ownership, the PyPI package, the documentation site, and the commit timestamps remain the corroborating record for the July work.

**My claim of authorship covers:** the concept, the architectural constraints, the specifications, the scope decisions (including what the project deliberately does not do), and the verification standard. It does not extend to claiming hand-authorship of machine-generated implementation code, which is disclosed in Section 2.

---

## 7. Competition rule compliance

| Rule | Status |
|---|---|
| Own work and ideas reflected | Architecture, specs, constraints, and verification are mine. Implementation is AI-assisted — disclosed in §2. |
| Outside tools properly credited | Claude Code credited in §2; libraries in §4; ideas in §5. |
| Prior work clearly disclosed | §3, with a verifiable timeline. |
| Public GitHub repository | https://github.com/haihaoxu/intentos — public since 2026-07-25. |
| Supporting materials provided | Ten frozen specs, `BLUEPRINT.md`, `EXECUTION_CONTRACT.md`, `ROADMAP.md`, README, docs site. |
| Pitch / demo content | `DEMO_SCRIPT.md` (in this directory) with a reproducible zero-config demo. |
| Honest conduct | No user, revenue, or adoption figures are claimed that do not exist. §7 of `SUBMISSION.md` reports 2 GitHub stars and zero users. |

---

*Contact: haihao@intent-os.dev*
