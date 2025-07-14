import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open('data/user_transactions.json', 'r') as f:
    raw_data = json.load(f)

records = []
for wallet in raw_data:
    for tx in wallet['transactions']:
        records.append({
            'wallet': wallet['wallet'],
            'action': tx['action'],
            'amount': float(tx['amount']),
            'timestamp': tx['timestamp']
        })

df = pd.DataFrame(records)

agg = df.groupby('wallet').agg(
    total_tx=('action', 'count'),
    unique_actions=('action', pd.Series.nunique),
    total_amount=('amount', 'sum'),
    mean_amount=('amount', 'mean'),
    std_amount=('amount', 'std'),
    deposits=('action', lambda x: (x == 'deposit').sum()),
    borrows=('action', lambda x: (x == 'borrow').sum()),
    repays=('action', lambda x: (x == 'repay').sum()),
    redemptions=('action', lambda x: (x == 'redeemunderlying').sum()),
    liquidations=('action', lambda x: (x == 'liquidationcall').sum())
).fillna(0)

agg['score_raw'] = (
    (agg['deposits'] * 3 + agg['repays'] * 3)
    - (agg['liquidations'] * 5)
    + (agg['redemptions'] * 1)
    + (agg['borrows'] * -1)
)

min_s, max_s = agg['score_raw'].min(), agg['score_raw'].max()
agg['score'] = ((agg['score_raw'] - min_s) / (max_s - min_s) * 1000).astype(int)
agg = agg.sort_values('score', ascending=False)

agg[['score']].to_csv('wallet_scores.csv')

bins = list(range(0, 1100, 100))
agg['score'].hist(bins=bins, figsize=(10,6), edgecolor='black')
plt.title('Score Distribution')
plt.xlabel('Score Range')
plt.ylabel('Wallet Count')
plt.grid(True)
plt.savefig('plots/score_distribution.png')
