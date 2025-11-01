"""Tests for metrics computation."""

import pytest
from src.metrics import compute_vwap, compute_mid, compute_slippage


def test_vwap_calculation():
    """Test VWAP calculation."""
    trades = [
        {"price": 100.0, "qty": 10},
        {"price": 101.0, "qty": 5},
    ]
    
    vwap = compute_vwap(trades)
    expected = (100.0 * 10 + 101.0 * 5) / 15
    assert abs(vwap - expected) < 0.01


def test_mid_calculation():
    """Test mid price calculation."""
    quotes = [
        {"bid": 99.0, "ask": 101.0},
        {"bid": 99.5, "ask": 100.5},
    ]
    
    mid = compute_mid(quotes)
    expected = (100.0 + 100.0) / 2
    assert abs(mid - expected) < 0.01


def test_slippage_calculation():
    """Test slippage calculation."""
    trades = [
        {"price": 100.5, "qty": 10},
        {"price": 99.5, "qty": 5},
    ]
    
    slippage = compute_slippage(trades, 100.0)
    assert slippage[0] == 0.5
    assert slippage[1] == -0.5

