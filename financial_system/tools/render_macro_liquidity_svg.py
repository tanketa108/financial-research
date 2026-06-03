#!/usr/bin/env python3
"""Render a simple dependency-free SVG liquidity chart for Macro Monitor v0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "financial_system" / "macro" / "data"
OUT = ROOT / "financial_system" / "macro" / "charts" / "2026-06-03-liquidity-triangle-v0.svg"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def points_from_state() -> list[dict[str, Any]]:
    tga = load(DATA / "tga-state.json")
    rrp = load(DATA / "nyfed-rrp-state.json")
    reserves = load(DATA / "fed-reserve-balances-state.json")
    return [
        {
            "label": "TGA",
            "change": (tga.get("tgaTrend") or {}).get("windowChangeUsdMn"),
            "unit": "USD mn",
            "color": "#2563eb",
        },
        {
            "label": "RRP",
            "change": ((rrp.get("trend") or {}).get("windowChangeUsdBn") or 0) * 1000,
            "unit": "USD mn eq.",
            "color": "#0f766e",
        },
        {
            "label": "Reserves",
            "change": (reserves.get("trend") or {}).get("windowChangeUsdMn"),
            "unit": "USD mn",
            "color": "#7c3aed",
        },
    ]


def fmt(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}${value/1000:,.1f}bn"


def render_svg(points: list[dict[str, Any]]) -> str:
    width, height = 920, 360
    left, right, top, bottom = 140, 40, 50, 80
    plot_w = width - left - right
    mid = left + plot_w / 2
    values = [float(p["change"] or 0) for p in points]
    max_abs = max(max(abs(v) for v in values), 1.0)
    scale = (plot_w / 2 - 40) / max_abs

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f8fbff"/>',
        '<text x="40" y="32" font-family="Inter, Arial" font-size="20" font-weight="700" fill="#0f172a">Liquidity triangle — window change</text>',
        '<text x="40" y="56" font-family="Inter, Arial" font-size="12" fill="#475569">TGA rising drains reserves; RRP falling can offset; reserve balances are the direct cross-check.</text>',
        f'<line x1="{mid}" y1="78" x2="{mid}" y2="270" stroke="#94a3b8" stroke-width="1"/>',
        f'<text x="{mid-4}" y="292" font-family="Inter, Arial" font-size="11" fill="#64748b">0</text>',
    ]
    y0 = 105
    for i, p in enumerate(points):
        y = y0 + i * 70
        v = float(p["change"] or 0)
        bar_w = abs(v) * scale
        if v >= 0:
            x = mid
        else:
            x = mid - bar_w
        parts.extend([
            f'<text x="40" y="{y+18}" font-family="Inter, Arial" font-size="15" font-weight="600" fill="#0f172a">{p["label"]}</text>',
            f'<rect x="{x:.1f}" y="{y}" width="{bar_w:.1f}" height="28" rx="7" fill="{p["color"]}" opacity="0.88"/>',
            f'<text x="{mid + (bar_w + 12 if v >= 0 else -bar_w - 82):.1f}" y="{y+19}" font-family="Inter, Arial" font-size="13" font-weight="600" fill="#0f172a">{fmt(v)}</text>',
        ])
    parts.extend([
        '<text x="40" y="330" font-family="Inter, Arial" font-size="11" fill="#64748b">Sources: Treasury FiscalData DTS, NY Fed Markets API, FRED public CSV WRESBAL. Units converted to USD billions for display.</text>',
        '</svg>',
    ])
    return "\n".join(parts)


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_svg(points_from_state()), encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
