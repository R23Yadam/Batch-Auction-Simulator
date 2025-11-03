# Contributing

Thanks for your interest! This project is kept intentionally small and readable.

## Dev setup

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -U pytest
```

## Commands

* `make gen` – generate deterministic `orders.csv`
* `make simulate` – run batch or continuous examples
* `make benchmark` – write `out_bench/bench.json`
* `make compare` – batch vs continuous table
* `pytest -q` – run tests

## Pull requests

1. Branch name: `feat/...`, `fix/...`, or `docs/...`
2. Keep changes focused; update README if CLI/outputs change
3. Run `pytest -q` before pushing
4. Fill the PR template checklist

## Coding style

* Pure Python, simple data structures
* Keep batch-clearing logic uniform-price + price–time priority
* Deterministic generator semantics must not change

