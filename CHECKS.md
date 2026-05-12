# Checks

Run the repository smoke check before merging operational changes:

```bash
python3 scripts/check.py
```

The check validates:

- required files exist,
- JSON files parse,
- Python files compile,
- dashboard static build succeeds.

This is intentionally small and fast. It is not a full financial correctness test.
