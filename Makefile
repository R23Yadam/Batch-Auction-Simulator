.PHONY: help test clean gen simulate benchmark compare

help:
	@echo "Batch Auction Simulator - Make targets:"
	@echo "  test       - Run pytest suite"
	@echo "  gen        - Generate sample orders"
	@echo "  simulate   - Run batch simulation"
	@echo "  benchmark  - Run benchmark"
	@echo "  compare    - Compare batch vs continuous"
	@echo "  clean      - Remove output files"

test:
	pytest tests/ -v

clean:
	rm -rf out/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

gen:
	python -m src.cli gen --n 10000 --seed 42 --auction_ms 1000 --cross_rate 0.2 > orders.csv

simulate:
	python -m src.cli simulate --in orders.csv --mode batch --interval 1000 --out out/batch

benchmark:
	python -m src.cli benchmark --in orders.csv --mode batch --interval 1000 --out out/bench

compare:
	python -m src.cli compare --in orders.csv --interval 1000

