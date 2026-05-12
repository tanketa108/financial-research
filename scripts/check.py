#!/usr/bin/env python3
from __future__ import annotations

import json
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    'financial_system/positions.json',
    'financial_system/registry/dashboard_state.json',
    'financial_system/registry/thesis_monitor_input.json',
    'financial_system/registry/thesis_monitor_output.json',
    'financial_dashboard/build_dashboard_html.py',
    'financial_dashboard/static/styles.css',
]

JSON_GLOBS = [
    'financial_system/*.json',
    'financial_system/config/*.json',
    'financial_system/registry/*.json',
    'financial_system/valuations/*.json',
]

PYTHON_GLOBS = [
    'financial_system/tools/*.py',
    'financial_dashboard/*.py',
    'scripts/*.py',
]


def fail(message: str) -> None:
    print(f'[FAIL] {message}')
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f'[OK] {message}')


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail('missing required files: ' + ', '.join(missing))
    ok('required files present')


def check_json() -> None:
    paths: list[Path] = []
    for pattern in JSON_GLOBS:
        paths.extend(ROOT.glob(pattern))
    paths = sorted(set(paths))
    for path in paths:
        try:
            json.loads(path.read_text())
        except Exception as exc:
            fail(f'invalid JSON: {path.relative_to(ROOT)}: {exc}')
    ok(f'valid JSON files: {len(paths)}')


def check_python_compile() -> None:
    paths: list[Path] = []
    for pattern in PYTHON_GLOBS:
        paths.extend(ROOT.glob(pattern))
    paths = sorted(set(paths))
    for path in paths:
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            fail(f'python compile failed: {path.relative_to(ROOT)}: {exc}')
    ok(f'python files compile: {len(paths)}')


def check_dashboard_build() -> None:
    with tempfile.TemporaryDirectory(prefix='financial-dashboard-check-') as tmp:
        out = Path(tmp) / 'dashboard'
        cmd = [
            sys.executable,
            str(ROOT / 'financial_dashboard' / 'build_dashboard_html.py'),
            '--repo-root',
            str(ROOT),
            '--output-dir',
            str(out),
        ]
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            fail('dashboard build failed')
        required_outputs = [
            out / 'index.html',
            out / 'companies' / 'UBER.html',
            out / 'static' / 'styles.css',
        ]
        missing = [str(p) for p in required_outputs if not p.exists()]
        if missing:
            fail('dashboard build missing outputs: ' + ', '.join(missing))
    ok('dashboard build')


def main() -> None:
    check_required_files()
    check_json()
    check_python_compile()
    check_dashboard_build()
    ok('all checks passed')


if __name__ == '__main__':
    main()
