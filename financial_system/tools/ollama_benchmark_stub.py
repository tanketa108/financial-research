#!/usr/bin/env python3
"""Stub for future Ollama benchmark tasks.

Does not call Ollama yet. This file defines the benchmark fixtures we will use
once the VPS is upgraded and Ollama is available.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
OUT = ROOT / 'outputs' / 'ollama_benchmark_plan.json'

PLAN = {
    'tasks': [
        {
            'name': 'filing_delta_summary',
            'goal': 'Turn structured filing deltas into a concise analyst-facing summary.',
            'success_signals': ['clear summary', 'correct prioritization', 'low hallucination'],
        },
        {
            'name': 'materiality_classification',
            'goal': 'Classify changes as low/medium/high materiality and explain why.',
            'success_signals': ['reasonable classification', 'traceable reasoning', 'stable output'],
        },
        {
            'name': 'thesis_monitor_draft',
            'goal': 'Produce a first-pass thesis-monitor note from structured inputs.',
            'success_signals': ['usable first draft', 'captures main changes', 'limited noise'],
        },
    ],
    'models_to_test': [
        {'role': 'small_fast', 'status': 'pending_selection'},
        {'role': 'medium_reasoning', 'status': 'pending_selection'},
    ],
    'decision_rule': {
        'promote_to_workforce_if': [
            'quality sufficient for repetitive work',
            'latency acceptable',
            'resource usage sustainable',
        ]
    }
}

OUT.write_text(json.dumps(PLAN, ensure_ascii=False, indent=2) + '\n')
print(OUT)
