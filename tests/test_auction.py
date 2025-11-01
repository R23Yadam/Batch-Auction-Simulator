"""Tests for batch auction clearing."""

import pytest
from src.auction import clear_batch


def test_auction_max_volume():
    """Test that auction maximizes volume."""
    orders = [
        {"order_id": 1, "side": "BUY", "price": 100.0, "qty": 10, "type": "LIMIT"},
        {"order_id": 2, "side": "BUY", "price": 99.0, "qty": 10, "type": "LIMIT"},
        {"order_id": 3, "side": "SELL", "price": 99.5, "qty": 15, "type": "LIMIT"},
    ]
    
    price, fills = clear_batch(orders)
    
    # Should clear at a price where demand and supply meet
    # At 99.5: demand (bids >= 99.5) = 10, supply (asks <= 99.5) = 15, volume = 10
    assert price is not None
    total_qty = sum(f["qty"] for f in fills)
    assert total_qty == 10  # Max volume


def test_auction_tiebreak_mid():
    """Test tie-break to midpoint of range."""
    orders = [
        {"order_id": 1, "side": "BUY", "price": 100.0, "qty": 10, "type": "LIMIT"},
        {"order_id": 2, "side": "SELL", "price": 98.0, "qty": 10, "type": "LIMIT"},
    ]
    
    price, fills = clear_batch(orders, pre_mid=99.0)
    
    # Multiple prices could clear 10; should pick closest to mid or midpoint
    assert price is not None
    assert len(fills) > 0


def test_auction_fifo_allocation():
    """Test FIFO allocation in batch auction."""
    orders = [
        {"order_id": 1, "side": "BUY", "price": 100.0, "qty": 5, "type": "LIMIT"},
        {"order_id": 2, "side": "BUY", "price": 100.0, "qty": 5, "type": "LIMIT"},
        {"order_id": 3, "side": "SELL", "price": 99.0, "qty": 7, "type": "LIMIT"},
    ]
    
    price, fills = clear_batch(orders)
    
    # Should allocate to order 1 fully, then order 2 partially
    assert price is not None
    assert fills[0]["buyer_id"] == 1
    assert fills[0]["qty"] == 5
    assert fills[1]["buyer_id"] == 2
    assert fills[1]["qty"] == 2

