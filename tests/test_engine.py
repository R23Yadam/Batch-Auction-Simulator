"""Tests for continuous order book engine."""

import pytest
from src.engine import OrderBook


def test_basic_cross():
    """Test basic bid-ask cross."""
    book = OrderBook()
    
    # Add passive ask
    book.add_order(1, "SELL", 100.0, 10, "LIMIT")
    assert len(book.asks) == 1
    
    # Add aggressive bid that crosses
    fills = book.add_order(2, "BUY", 100.0, 5, "LIMIT")
    assert len(fills) == 1
    assert fills[0]["qty"] == 5
    assert fills[0]["price"] == 100.0


def test_fifo_same_price():
    """Test FIFO ordering at same price level."""
    book = OrderBook()
    
    # Three asks at same price
    book.add_order(1, "SELL", 100.0, 5, "LIMIT")
    book.add_order(2, "SELL", 100.0, 5, "LIMIT")
    book.add_order(3, "SELL", 100.0, 5, "LIMIT")
    
    # Buy 10: should match orders 1 and 2 (FIFO)
    fills = book.add_order(4, "BUY", 100.0, 10, "LIMIT")
    assert len(fills) == 2
    assert fills[0]["seller_id"] == 1
    assert fills[1]["seller_id"] == 2


def test_partial_fill():
    """Test partial fills."""
    book = OrderBook()
    
    # Add ask for 10
    book.add_order(1, "SELL", 100.0, 10, "LIMIT")
    
    # Buy only 3
    fills = book.add_order(2, "BUY", 100.0, 3, "LIMIT")
    assert len(fills) == 1
    assert fills[0]["qty"] == 3
    
    # Remaining 7 should still be on book
    assert 100.0 in book.asks
    assert book.asks[100.0][0][1] == 7


def test_ioc_partial_cancel():
    """Test IOC with partial fill and cancel."""
    book = OrderBook()
    
    # Ask for 5
    book.add_order(1, "SELL", 100.0, 5, "LIMIT")
    
    # IOC buy for 10: should fill 5, cancel 5
    fills = book.add_order(2, "BUY", 100.0, 10, "IOC")
    assert len(fills) == 1
    assert fills[0]["qty"] == 5
    
    # No residual buy order on book
    assert 2 not in book.id_index


def test_cancel_by_id():
    """Test cancel by order ID."""
    book = OrderBook()
    
    # Add limit order
    book.add_order(1, "BUY", 100.0, 10, "LIMIT")
    assert 1 in book.id_index
    
    # Cancel it
    result = book.cancel_order(1)
    assert result is True
    assert 1 not in book.id_index
    
    # Cancel non-existent
    result = book.cancel_order(999)
    assert result is False


def test_market_order():
    """Test MARKET order execution."""
    book = OrderBook()
    
    # Add asks at different levels
    book.add_order(1, "SELL", 100.0, 5, "LIMIT")
    book.add_order(2, "SELL", 101.0, 5, "LIMIT")
    
    # Market buy for 7: should take all of 100.0 and 2 of 101.0
    fills = book.add_order(3, "BUY", None, 7, "MARKET")
    assert len(fills) == 2
    assert fills[0]["price"] == 100.0
    assert fills[0]["qty"] == 5
    assert fills[1]["price"] == 101.0
    assert fills[1]["qty"] == 2


def test_no_trade_no_cross():
    """Test no trade when book doesn't cross."""
    book = OrderBook()
    
    # Bid and ask don't cross
    book.add_order(1, "BUY", 99.0, 10, "LIMIT")
    book.add_order(2, "SELL", 101.0, 10, "LIMIT")
    
    assert len(book.trades) == 0
    assert len(book.bids) == 1
    assert len(book.asks) == 1

