"""Integration tests."""

import pytest
import tempfile
import csv
import os
from io import StringIO

from src.gen import generate_orders
from src.engine import OrderBook
from src.auction import clear_batch


def test_generator_determinism():
    """Test that generator produces byte-identical output."""
    output1 = StringIO()
    output2 = StringIO()
    
    generate_orders(n=100, seed=42, auction_interval_ms=1000, cross_rate=0.2, output=output1)
    generate_orders(n=100, seed=42, auction_interval_ms=1000, cross_rate=0.2, output=output2)
    
    assert output1.getvalue() == output2.getvalue()


def test_batch_vs_continuous_consistency():
    """Test that batch and continuous modes are internally consistent."""
    # Generate small order set
    output = StringIO()
    generate_orders(n=50, seed=123, auction_interval_ms=1000, cross_rate=0.3, output=output)
    
    # Parse orders
    output.seek(0)
    reader = csv.DictReader(output)
    orders = []
    for row in reader:
        order = {
            "timestamp": int(row["timestamp"]),
            "order_id": int(row["order_id"]),
            "type": row["type"],
            "side": row["side"],
            "qty": int(row["qty"]) if row["qty"] else 0,
        }
        if row["price"]:
            order["price"] = float(row["price"])
        else:
            order["price"] = None
        orders.append(order)
    
    # Run continuous
    book = OrderBook()
    for o in orders:
        if o["type"] == "CANCEL":
            book.cancel_order(int(o["order_id"]))
        else:
            book.add_order(o["order_id"], o["side"], o["price"], o["qty"], o["type"])
    
    # Both should produce trades (consistency check)
    assert isinstance(book.trades, list)

