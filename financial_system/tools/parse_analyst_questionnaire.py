#!/usr/bin/env python3
"""Parse a simple analyst questionnaire markdown into analyst-input JSON."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path('/data/.openclaw/workspace/financial_system')
VALUATIONS = ROOT / 'valuations'


def get_value(line: str) -> str | None:
    if ':' not in line:
        return None
    value = line.split(':', 1)[1].strip()
    return value or None


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('Usage: parse_analyst_questionnaire.py <TICKER>', file=sys.stderr)
        return 1

    ticker = argv[1].upper()
    q_path = VALUATIONS / f'{ticker}-analyst-questionnaire-v1.md'
    out_path = VALUATIONS / f'{ticker}-analyst-input-v1.json'
    if not q_path.exists():
        print(f'missing {q_path}', file=sys.stderr)
        return 1

    lines = q_path.read_text().splitlines()
    data = {
        'thesis': {},
        'segments': [],
        'drivers': [],
        'scenarios': [],
        'catalysts': [],
        'risks': [],
        'qualitative_notes': {},
        'valuation_methods': {
            'dcf': {'assumptions': {}, 'output': None, 'range': None},
            'gordon': {'assumptions': {}, 'output': None, 'range': None},
            'terminal_multiple': {'assumptions': {}, 'output': None, 'range': None},
            'aggregate': {'central_reference': None, 'range': None, 'dispersion': None},
        },
    }

    section = None
    current_segment = None
    current_scenario = None
    current_method = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line == '## Thesis':
            section = 'thesis'
            continue
        if line == '## Segments':
            section = 'segments'
            continue
        if line == '## Drivers':
            section = 'drivers'
            continue
        if line == '## Scenarios':
            section = 'scenarios'
            continue
        if line == '## Catalysts':
            section = 'catalysts'
            continue
        if line == '## Risks':
            section = 'risks'
            continue
        if line == '## Qualitative Notes':
            section = 'qualitative_notes'
            continue
        if line == '## Valuation Assumptions':
            section = 'valuation'
            continue

        if line.startswith('### Segment'):
            current_segment = {'name': None, 'importance': None, 'growth_view': None, 'margin_view': None, 'notes': None}
            data['segments'].append(current_segment)
            continue
        if line.startswith('### Scenario'):
            current_scenario = {'name': None, 'description': None, 'business_model_implication': None, 'valuation_implication': None, 'key_assumptions': []}
            data['scenarios'].append(current_scenario)
            continue
        if line == '### DCF':
            current_method = 'dcf'
            continue
        if line == '### Gordon':
            current_method = 'gordon'
            continue
        if line == '### Terminal Multiple':
            current_method = 'terminal_multiple'
            continue
        if line == '### Aggregate':
            current_method = 'aggregate'
            continue

        if section == 'thesis' and line.startswith('- '):
            if line.startswith('- Thesis short:'):
                data['thesis']['thesis_short'] = get_value(line)
            elif line.startswith('- Current stance:'):
                data['thesis']['current_stance'] = get_value(line)
            elif line.startswith('- What would change my mind:'):
                data['thesis']['what_would_change_my_mind'] = get_value(line)

        elif section == 'segments' and current_segment and line.startswith('- '):
            if line.startswith('- Name:'):
                current_segment['name'] = get_value(line)
            elif line.startswith('- Importance:'):
                current_segment['importance'] = get_value(line)
            elif line.startswith('- Growth view:'):
                current_segment['growth_view'] = get_value(line)
            elif line.startswith('- Margin view:'):
                current_segment['margin_view'] = get_value(line)
            elif line.startswith('- Notes:'):
                current_segment['notes'] = get_value(line)

        elif section == 'drivers' and line.startswith('- '):
            value = line[2:].strip()
            if value:
                data['drivers'].append(value)

        elif section == 'scenarios' and current_scenario and line.startswith('- '):
            if line.startswith('- Name:'):
                current_scenario['name'] = get_value(line)
            elif line.startswith('- Description:'):
                current_scenario['description'] = get_value(line)
            elif line.startswith('- Business model implication:'):
                current_scenario['business_model_implication'] = get_value(line)
            elif line.startswith('- Valuation implication:'):
                current_scenario['valuation_implication'] = get_value(line)
            elif line.startswith('- Key assumptions:'):
                value = get_value(line)
                current_scenario['key_assumptions'] = [value] if value else []

        elif section == 'catalysts' and line.startswith('- '):
            value = line[2:].strip()
            if value:
                data['catalysts'].append(value)

        elif section == 'risks' and line.startswith('- '):
            value = line[2:].strip()
            if value:
                data['risks'].append(value)

        elif section == 'qualitative_notes' and line.startswith('- '):
            if line.startswith('- Moat:'):
                data['qualitative_notes']['moat'] = get_value(line)
            elif line.startswith('- Fragilities:'):
                data['qualitative_notes']['fragilities'] = get_value(line)
            elif line.startswith('- Management quality:'):
                data['qualitative_notes']['management_quality'] = get_value(line)
            elif line.startswith('- Industry structure:'):
                data['qualitative_notes']['industry_structure'] = get_value(line)

        elif section == 'valuation' and current_method and line.startswith('- '):
            if current_method in ('dcf', 'gordon', 'terminal_multiple'):
                if line.startswith('- Assumptions:'):
                    value = get_value(line)
                    data['valuation_methods'][current_method]['assumptions'] = {'notes': value} if value else {}
                elif line.startswith('- Output:'):
                    data['valuation_methods'][current_method]['output'] = get_value(line)
                elif line.startswith('- Range:'):
                    data['valuation_methods'][current_method]['range'] = get_value(line)
            elif current_method == 'aggregate':
                if line.startswith('- Central reference:'):
                    data['valuation_methods']['aggregate']['central_reference'] = get_value(line)
                elif line.startswith('- Range:'):
                    data['valuation_methods']['aggregate']['range'] = get_value(line)
                elif line.startswith('- Dispersion:'):
                    data['valuation_methods']['aggregate']['dispersion'] = get_value(line)

    data['segments'] = [s for s in data['segments'] if any(v is not None for v in s.values())]
    data['scenarios'] = [s for s in data['scenarios'] if any((v not in (None, [])) for v in s.values())]

    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(str(out_path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
