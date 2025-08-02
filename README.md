# Wallet Scoring Based on Aave Transactions

This script generates credit-like scores for wallets using past transaction behavior. It uses statistical aggregation and normalizes results to a scale from 0 to 1000.

## Instructions

1. Place the raw file `user_transactions.json` inside the `data/` folder.
2. Run the scoring script:

```
pip install -r requirements.txt
python score_wallets.py
```

Outputs:
- `wallet_scores.csv`
- `plots/score_distribution.png`


## Author
Kartik Sharma
