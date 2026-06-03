#!/usr/bin/env python3
"""Render Discord-ready macro release stubs from the macro release registry.

This is intentionally small and dependency-free. It does not fetch live data;
it turns the canonical registry into a checklist / release-card skeleton so the
manual workflow can be used before adding fragile calendar automation.
"""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "financial_system" / "macro" / "macro-release-calendar-registry.json"
DEFAULT_EVENTS = ROOT / "financial_system" / "macro" / "macro-release-events.json"

CATEGORY_ORDER = [
    "policy",
    "inflation",
    "inflation_consumption",
    "labor",
    "growth",
    "growth_consumption",
    "growth_capex",
    "growth_industrial",
    "housing",
    "liquidity_treasury",
]
IMPORTANCE_ORDER = {"high": 0, "medium": 1, "low": 2}


def load_registry(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data.get("releases"), list):
        raise ValueError(f"Registry missing releases[]: {path}")
    return data


def sort_releases(releases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    category_rank = {name: i for i, name in enumerate(CATEGORY_ORDER)}
    return sorted(
        releases,
        key=lambda r: (
            IMPORTANCE_ORDER.get(str(r.get("importance", "low")), 9),
            category_rank.get(str(r.get("category", "")), 99),
            str(r.get("id", "")),
        ),
    )


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def render_index(registry: dict[str, Any], *, importance: str | None = None, category: str | None = None) -> str:
    releases = registry["releases"]
    if importance:
        releases = [r for r in releases if r.get("importance") == importance]
    if category:
        releases = [r for r in releases if r.get("category") == category]
    releases = sort_releases(releases)

    lines = [
        "**US Macro Release Registry — v0.1**",
        f"Scope: {registry.get('scope', 'US macro releases')}",
        "",
    ]
    for release in releases:
        lines.append(
            f"- `{release['id']}` — {release['name']} "
            f"({release['sourceAgency']}, {release['frequency']}, {release['importance']}, "
            f"usual {release.get('usualReleaseTimeET', 'TBD')} ET)"
        )
    return "\n".join(lines)


def render_upcoming(
    registry: dict[str, Any],
    events_path: Path,
    *,
    today: date | None = None,
    days: int = 45,
    include_pending: bool = True,
) -> str:
    today = today or date.today()
    horizon = date.fromordinal(today.toordinal() + days)
    events_data = load_registry_like(events_path, required_key="events")
    releases_by_id = {r["id"]: r for r in registry["releases"]}

    dated: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []
    for event in events_data["events"]:
        release = releases_by_id.get(event.get("releaseId"))
        if not release:
            continue
        merged = {**event, "release": release}
        if event.get("releaseDate"):
            event_date = date.fromisoformat(event["releaseDate"])
            if today <= event_date <= horizon:
                dated.append(merged)
        elif include_pending:
            pending.append(merged)

    dated.sort(key=lambda e: (e["releaseDate"], e.get("releaseTimeET") or "99:99", e["releaseId"]))

    lines = [
        f"**Upcoming US Macro Releases — next {days} days**",
        f"Window: {today.isoformat()} to {horizon.isoformat()}",
        "",
    ]
    if not dated:
        lines.append("No confirmed dated events in the current window.")
    for event in dated:
        release = event["release"]
        lines.append(
            f"- {event['releaseDate']} {event.get('releaseTimeET', release.get('usualReleaseTimeET', 'TBD'))} ET — "
            f"`{event['releaseId']}` {release['name']} ({event.get('period', 'period TBD')}) — {event.get('status', 'status TBD')}"
        )
    if pending:
        lines.extend(["", "**Pending manual confirmation**"])
        for event in pending:
            release = event["release"]
            lines.append(f"- `{event['releaseId']}` {release['name']} — {event.get('sourceNote', 'date not yet confirmed')}")
    return "\n".join(lines)


def load_registry_like(path: Path, *, required_key: str) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data.get(required_key), list):
        raise ValueError(f"File missing {required_key}[]: {path}")
    return data


def render_stub(release: dict[str, Any], *, period: str | None = None) -> str:
    period_text = period or "<period>"
    fields = as_list(release.get("reportFields"))
    field_lines = [f"- {field}: <actual> | previous/revision: <...>" for field in fields]
    primary_series = as_list(release.get("primarySeries"))

    lines = [
        f"**{release['name']} — {period_text}**",
        f"Source: {release['sourceAgency']} | usual release time: {release.get('usualReleaseTimeET', 'TBD')} ET",
        "",
        "**Facts**",
    ]
    lines.extend(field_lines or ["- <metric>: <actual> | previous/revision: <...>"])
    lines.extend(
        [
            "",
            "**Read-through**",
            f"- {release.get('interpretationHint', '<interpretation>')}",
            "- <what changed versus prior release>",
            "",
            "**Caveats**",
            "- Consensus/surprise: not included unless explicitly sourced.",
            "- Revisions: <confirm / none / pending>",
        ]
    )
    if primary_series:
        lines.extend(["", f"Series context: {', '.join(primary_series)}"])
    lines.extend(["", f"Source: <{release.get('officialDataUrl') or release.get('officialCalendarUrl')}>"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render macro release registry index or Discord-ready stub.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS)
    parser.add_argument("--id", dest="release_id", help="Release id to render as a post stub")
    parser.add_argument("--period", help="Release period label for the stub, e.g. 'May 2026'")
    parser.add_argument("--importance", choices=["high", "medium", "low"], help="Filter index by importance")
    parser.add_argument("--category", help="Filter index by category")
    parser.add_argument("--upcoming", action="store_true", help="Render upcoming dated releases from macro-release-events.json")
    parser.add_argument("--days", type=int, default=45, help="Upcoming release horizon in days")
    parser.add_argument("--today", help="Override today's date as YYYY-MM-DD, useful for tests")
    args = parser.parse_args()

    registry = load_registry(args.registry)

    if args.upcoming:
        today = date.fromisoformat(args.today) if args.today else None
        print(render_upcoming(registry, args.events, today=today, days=args.days))
    elif args.release_id:
        matches = [r for r in registry["releases"] if r.get("id") == args.release_id]
        if not matches:
            available = ", ".join(r["id"] for r in sort_releases(registry["releases"]))
            raise SystemExit(f"Unknown release id: {args.release_id}\nAvailable: {available}")
        print(render_stub(matches[0], period=args.period))
    else:
        print(render_index(registry, importance=args.importance, category=args.category))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
