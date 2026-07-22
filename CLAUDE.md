# Intent OS

> An **open interoperability layer** for AI capabilities, workflows, and execution.

## Project Identity

- **What:** Standards + reference runtime that let AI capabilities run across different runtimes (OpenAI, Anthropic, Ollama, etc.)
- **Not:** A model, an agent framework, an application, or a closed platform
- **Core principle:** *Intent OS does not standardize intelligence. It standardizes interaction.*
- **GitHub:** https://github.com/X-code-sourse/intentos
- **Directory:** `~/Desktop/intent-os` — working directory is `reference-runtime/`

## Quick Start

```bash
cd ~/Desktop/intent-os/reference-runtime
pip install -e .           # or: pip install intent-os[all]
intent-os quickstart        # 7-step getting-started guide
intent-os validate examples/text_summarize.yaml
intent-os run examples/text_summarize.yaml --adapter ollama --input '{"text":"Hello"}'
```

## Running Tests

```bash
cd ~/Desktop/intent-os/reference-runtime

# Full suite (560 tests)
python -m pytest tests/ -v --tb=short -q

# Single file
python -m pytest tests/test_security.py -v

# Single test
python -m pytest tests/test_workflow.py::TestWorkflowDAGValidation::test_cycle_detection -v

# Fast check (no details)
python -m pytest tests/ --tb=no -q
```

## Architecture

### Three Specs (in `specs/`)
| Spec | What | Phase |
|---|---|---|
| SPEC-0001 | Capability Manifest — describe what a capability does | Frozen |
| SPEC-0002 | Workflow Graph — compose capabilities (structure + execution semantics) | Frozen |
| SPEC-0003 | Event Schema — record execution events | Frozen |
| SPEC-0004 | Security Model — permissions, policy, audit | Design (Phase 2) |

### Five-Plane Architecture
```
User Plane    → Goal/intent from natural language
Control Plane → Planner, Executor, Security Manager — OWNS NO STATE
Metadata Plane → Registries, policies, versions
Data Plane    → Event Store, execution history
Runtime Plane → Model pools, tool pools, adapters
```

All planes communicate through Event Bus (append-only, single source of truth).

## Test Map (560 total)

| File | Tests | What |
|---|---|---|
| `test_adapters.py` | 45 | Adapter schema translation + cost calculation |
| `test_cli_commands.py` | 37 | All 14 CLI commands |
| `test_executor.py` | 41 | Execution engine |
| `test_event_store.py` | 35 | SQLite event store |
| `test_import_export.py` | 26 | OpenAI/MCP ↔ Manifest |
| `test_mcp_server.py` | 21 | MCP server protocol |
| `test_registry_persistence.py` | 29 | Registry + semantic search |
| `test_search.py` | 27 | TF-IDF search engine |
| `test_workflow.py` | 39 | DAG + planner + scheduler |
| `test_workflow_integration.py` | 28 | End-to-end workflows |
| `test_workflow_parser.py` | 23 | YAML parsing |
| `test_conditions.py` | 25 | Condition expression DSL |
| `test_adaptive_workflow.py` | 11 | Conditional edges + skip_if |
| `test_workflow_adapter_integration.py` | 3 | Adapter ↔ workflow |
| `test_evolution.py` | 14 | Evolution Loop |
| `test_security.py` | 120 | Security Manager |
| `test_cross_runtime.py` | 42 | L1-L4 compatibility (8 skip without Ollama) |

## Key Files

| File | Why It Matters |
|---|---|
| `cli.py` | CLI entry point — `intent-os` command dispatcher |
| `core/models.py` | All data models (CapabilityManifest, Event, ExecutionRecord) |
| `core/workflow.py` | Workflow DAG + execution semantics data model |
| `core/scheduler.py` | Workflow execution scheduler (most complex component) |
| `core/executor.py` | Capability execution engine |
| `core/security.py` | Policy evaluation engine (SPEC-0004) |
| `core/conditions.py` | Adaptive execution condition DSL |
| `core/search.py` | TF-IDF semantic search |
| `core/evolution.py` | Evolution Loop engine |
| `GUIDE.md` | Full project manual |
| `CONSTITUTION.md` | Frozen hard constraints (R1-R4) |
| `POSITIONING.md` | Strategic positioning |

## Code Conventions

- Python 3.10+, type annotations (`from __future__ import annotations`)
- `dataclass` for models, not hand-written classes
- filenames: `snake_case.py`
- classes: `PascalCase`, methods/variables: `snake_case`
- All adapters inherit `adapters/base.py::AdapterBase`
- CLI commands in `commands/` — function signature `def cmd_xxx(args) -> None`
- Tests: `class TestComponent`, method `def test_scenario`, plain `assert`
- Module docstring starts with `"Intent OS — "`

## CLI Commands (14)

```
validate  run  compare  list  registry  security
event  analytics  workflow  mcp-server  import  export
quickstart  evolution
```

## Build & Install

```bash
pip install -e .                    # editable install
pip install .[all]                  # + openai + anthropic
pip install intent-os               # from PyPI (future)
```

## Adapters (6)

| Adapter | Protocol | Requires |
|---|---|---|
| `openai_adapter.py` | OpenAI Function Calling | `OPENAI_API_KEY` |
| `anthropic_adapter.py` | Anthropic Tool Use | `ANTHROPIC_API_KEY` |
| `ollama_adapter.py` | Ollama native /api/chat | `ollama serve` running |
| `openrouter_adapter.py` | OpenAI-compatible via OpenRouter | `OPENROUTER_API_KEY` |
| `github_models_adapter.py` | OpenAI-compatible via GitHub | `GITHUB_TOKEN` |

## Git Branch Strategy

- `main` — release branch, CI runs on push/PR
- Feature branches: `feat/<name>`, fix branches: `fix/<name>`
- Tags: `v0.x.y` for releases
- Commit messages: imperative mood, `Co-Authored-By: Claude ...`
