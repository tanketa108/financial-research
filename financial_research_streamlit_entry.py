#!/usr/bin/env python3
"""Import-safe wrapper for the Macro Monitor Streamlit app."""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    app = Path(__file__).resolve().parent / "financial_system" / "macro" / "app" / "streamlit_macro_monitor.py"
    runpy.run_path(str(app), run_name="__main__")


if __name__ == "__main__":
    main()
