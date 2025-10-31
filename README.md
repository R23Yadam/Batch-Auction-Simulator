# Batch Auction Simulator

## Description
Interactive CLI that gathers buy and sell orders for a single asset, finds the uniform clearing price that maximizes filled volume, and prints the resulting trades. Pure Python, single file, no external packages.

## Quick Start
1. Verify Python 3.8+ is installed (`python3 --version`).
2. From the repo root, run `python3 batch_auction.py`.
3. Enter as many orders as you like; press Enter at the side prompt to finish.

```
$ python3 batch_auction.py
Batch Auction Simulator

Enter orders. Press Enter at 'side' to finish.
side [buy/sell] (Enter to stop): buy
price: 10
quantity: 5
...
```

## Inputs
- `side` - `buy` or `sell`; blank input ends order entry.
- `price` - floating-point number >= 0; reprompted until valid.
- `quantity` - whole number >= 1; reprompted until valid.

## How it clears
1. Aggregate entered orders into bid and ask volume per price level.
2. For every observed price, compute cumulative demand (bids >= price) and cumulative supply (asks <= price).
3. Pick the price band that delivers the highest executable volume; if multiple prices tie, use the midpoint of the lowest and highest winning levels as the clearing price.
4. Sort bids high-to-low and asks low-to-high, then greedily match them at the single clearing price until the target volume is traded.
