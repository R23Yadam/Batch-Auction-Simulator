#!/bin/bash
# Script to push the batch auction upgrade to GitHub

set -e

echo "=========================================="
echo "Batch Auction Simulator - Push to GitHub"
echo "=========================================="
echo ""

# Confirm we're on the feature branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "feature/batch-auction-upgrade" ]; then
    echo "ERROR: Not on feature/batch-auction-upgrade branch"
    exit 1
fi

# Show commit summary
echo ""
echo "Commit to push:"
git log -1 --oneline

echo ""
echo "Files changed:"
git show --name-status --oneline HEAD | tail -n +2

echo ""
echo "Pushing to GitHub..."
git push -u origin feature/batch-auction-upgrade

echo ""
echo "✅ Push complete!"
echo ""
echo "Next steps:"
echo "1. Visit: https://github.com/R23Yadam/Batch-Auction-Simulator"
echo "2. Create a Pull Request from 'feature/batch-auction-upgrade' to 'main'"
echo ""
echo "Or use GitHub CLI if available:"
echo "  gh pr create --title \"Batch Auction Upgrade: clearing, benchmarks, metrics, tests\" \\"
echo "               --body \"Implements price-time priority, LIMIT/MARKET/IOC/CANCEL; true uniform-price batch clearing; deterministic generator; bench.json (orders/sec & latency p50/p95/p99); VWAP/slippage metrics; 15 pytest cases.\" \\"
echo "               --base main --head feature/batch-auction-upgrade"

ls push_to_github.sh

