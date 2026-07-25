"""Intent OS CLI — share command: generate shareable Markdown summaries.

Creates a portable Markdown summary of an agent's profile, execution
history, and experiences — ready to paste into GitHub, X/Twitter, or
HN comments.

    intent-os share <agent_id>
    intent-os share <agent_id> --format markdown
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Any


_INTENT_OS_TAG = "\n\n---\n*Built with [Intent OS](https://github.com/haihaoxu/intentos) — pip install intentos*"


def cmd_share(args: Any) -> None:
    """Generate a shareable summary of an agent."""
    from core.agent_store import AgentStore
    from core.experience_store import ExperienceStore
    from commands.helpers import get_event_store

    agent_id = args.agent_id
    fmt = getattr(args, "format", "markdown") or "markdown"

    store = AgentStore()
    agent = store.get(agent_id)
    if agent is None:
        print(f"  Agent not found: {agent_id}", file=sys.stderr)
        sys.exit(1)

    # Execution stats
    total_runs = 0
    successes = 0
    total_cost = 0.0
    total_tokens = 0
    try:
        event_store = get_event_store()
        records = event_store.query_records(limit=1000)
        agent_records = [r for r in records
                         if r.get("agent_id") == agent_id
                         or (isinstance(r.get("agent_name"), str) and r["agent_name"] == agent.name)]
        total_runs = len(agent_records)
        successes = sum(1 for r in agent_records if r.get("status") == "success")
        total_cost = sum(r.get("total_cost_usd", 0) or 0 for r in agent_records)
        total_tokens = sum(r.get("total_tokens", 0) or 0 for r in agent_records)
    except Exception:
        pass

    # Experiences
    total_exps = 0
    exp_by_type: dict[str, int] = {}
    try:
        exp_store = ExperienceStore()
        exps = exp_store.list(agent_id=agent_id, limit=100)
        total_exps = len(exps)
        for e in exps:
            t = e.get("type", "unknown")
            exp_by_type[t] = exp_by_type.get(t, 0) + 1
    except Exception:
        pass

    avatar = agent.avatar or ""
    persona = agent.persona or ""
    traits = ", ".join(agent.traits) if agent.traits else ""
    status_icon = ">" if agent.status == "active" else "o"

    success_rate = successes / max(total_runs, 1)
    avg_cost = total_cost / max(total_runs, 1)

    if fmt == "markdown":
        lines = []
        lines.append(f"## {avatar} {agent.name}")
        if persona:
            lines.append(f"")
            lines.append(f"*{persona}*")
        if traits:
            lines.append(f"")
            lines.append(f"Character: {traits}")
        lines.append("")
        lines.append(f"| | |")
        lines.append(f"|---|---|")
        lines.append(f"| Status | {status_icon} {agent.status} |")
        if total_runs > 0:
            bar_len = 12
            filled = int(success_rate * bar_len)
            bar = "#" * filled + "." * (bar_len - filled)
            lines.append(f"| Tasks | {total_runs} ({successes} ok, {total_runs - successes} failed) |")
            lines.append(f"| Success | {bar} {success_rate:.0%} |")
            lines.append(f"| Total cost | ${total_cost:.2f} |")
            lines.append(f"| Avg cost/task | ${avg_cost:.4f} |")
            lines.append(f"| Total tokens | {total_tokens:,} |")
        if total_exps > 0:
            exp_parts = [f"{t}: {c}" for t, c in sorted(exp_by_type.items())]
            lines.append(f"| Experience | {total_exps} patterns ({', '.join(exp_parts)}) |")
        lines.append(f"| Created | {agent.created_at[:10] if agent.created_at else '?'} |")

        text = "\n".join(lines) + _INTENT_OS_TAG
    else:
        text = f"{avatar} {agent.name} — {persona or 'AI Agent'}{_INTENT_OS_TAG}"

    print()
    print(text)
    print()
    print("  Copy the text above and share it on GitHub, X, or HN.")
    print()
