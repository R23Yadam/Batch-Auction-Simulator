# Batch Auction + Continuous LOB Simulator

High-performance order book simulator with batch auction and continuous matching modes. Features deterministic order generation, comprehensive benchmarking, and trade quality metrics.

## Features

- **Price-Time Priority**: FIFO queues per price level
- **Order Types**: LIMIT, MARKET, IOC, CANCEL-by-id
- **Partial Fills**: Full support for partial order execution
- **Batch Clearing**: Uniform clearing price that maximizes matched volume
- **Benchmarking**: Throughput (orders/sec) and latency (p50/p95/p99)
- **Metrics**: Mid, VWAP, signed slippage, batch vs continuous comparison
- **Deterministic**: Seeded RNG produces byte-identical CSV output

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
make test

# Generate orders
make gen

# Run simulation
make simulate

# Run benchmark
make benchmark

# Compare modes
make compare
```

## CLI Commands

### Generate Orders

```bash
python -m src.cli gen --n 1000000 --seed 42 --auction_ms 1000 --cross_rate 0.2 > orders.csv
```

- `--n`: Number of orders to generate
- `--seed`: Random seed for reproducibility
- `--auction_ms`: Batch auction interval in milliseconds
- `--cross_rate`: Fraction of orders that cross the spread (0.0-1.0)

### Simulate (Batch Mode)

```bash
python -m src.cli simulate --in orders.csv --mode batch --interval 1000 --out out/
```

- `--in`: Input CSV file with orders
- `--mode`: `batch` or `continuous`
- `--interval`: Batch interval in milliseconds (required for batch mode)
- `--out`: Output directory for trades and quotes

### Simulate (Continuous Mode)

```bash
python -m src.cli simulate --in orders.csv --mode continuous --out out/
```

### Benchmark

```bash
python -m src.cli benchmark --in orders.csv --mode batch --interval 1000 --out out/
```

Outputs `bench.json` with:
- `orders_processed`: Total orders processed
- `orders_per_sec`: Throughput
- `latency_us_p50/p95/p99`: Latency percentiles in microseconds
- `cpu`, `python`: System information
- `mode`, `interval_ms`: Configuration

### Compare Modes

```bash
python -m src.cli compare --in orders.csv --interval 1000
```

Runs both batch and continuous simulations and prints a comparison table.

### Compute Metrics

```bash
python -m src.cli metrics --trades out/trades.csv --quotes out/quotes.csv --out out/
```

Generates `tearsheet.md` with trade quality metrics.

## Architecture

### Core Modules

- **`src/engine.py`**: Continuous order book with dict-of-deque levels and heaps for best prices
- **`src/auction.py`**: Batch clearing logic with uniform price maximizing volume
- **`src/gen.py`**: Deterministic order generator with configurable parameters
- **`src/bench.py`**: Benchmarking framework with latency tracking
- **`src/metrics.py`**: Trade quality metrics (VWAP, slippage, mid)
- **`src/cli.py`**: Command-line interface

### Testing

10 comprehensive pytest tests covering:
- Basic cross matching
- FIFO at same price level
- Partial fills
- IOC with partial cancel
- Cancel by order ID
- Market order execution
- No trade when book doesn't cross
- Batch auction max volume
- Tie-break to mid
- Generator determinism

Run tests:

```bash
pytest tests/ -v
```

## File Layout

```
project/
  README.md
  src/
    cli.py          # CLI interface
    engine.py       # Continuous order book
    auction.py      # Batch auction clearing
    gen.py          # Order generator
    metrics.py      # Trade metrics
    bench.py        # Benchmarking
  tests/
    test_engine.py
    test_auction.py
    test_metrics.py
    test_integration.py
  out/              # gitignored
  Makefile
  requirements.txt
  .gitignore
  LICENSE
```

## Batch Auction Algorithm

1. **Aggregate Orders**: Group by price level
2. **Compute Curves**: Build cumulative demand and supply curves
3. **Find Max Volume**: Identify price(s) that maximize matched volume
4. **Tie-Break**: Select price closest to pre-auction mid, or midpoint of tie range
5. **Allocate Fills**: Execute trades at uniform clearing price, FIFO within each side

## Continuous Matching

Price-time priority with aggressive matching:
- **LIMIT**: Match immediately at best available prices, rest goes to book
- **MARKET**: Execute immediately at best available, no residual
- **IOC**: Match what you can at limit price, cancel rest
- **CANCEL**: Remove order by ID from book

## Performance

Typical benchmarks on modern hardware:
- **Throughput**: 100K-500K orders/sec (continuous mode)
- **Latency**: p50 < 10μs, p99 < 100μs per order

## License

MIT License - see LICENSE file

## Author

Riley Adam (2025)
