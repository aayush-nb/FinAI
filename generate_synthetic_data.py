import pandas as pd
import numpy as np

# Synthetic credit data (alternative signals)
np.random.seed(42)
n_samples = 1000
data = {
    'age': np.random.randint(18, 70, n_samples),
    'income': np.random.normal(50000, 20000, n_samples),
    'upi_transactions': np.random.poisson(50, n_samples),
    'phone_recharges': np.random.poisson(10, n_samples),
    'ecommerce_repayments': np.random.binomial(1, 0.8, n_samples),
    'default': np.random.binomial(1, 0.1, n_samples)
}
data['default'] = ((data['income'] < 30000) | (data['upi_transactions'] < 20) | (data['ecommerce_repayments'] == 0)).astype(int)
pd.DataFrame(data).to_csv('data/synthetic_credit_data.csv', index=False)

# Synthetic transactions for investments
n_trans = 5000
date_range = pd.date_range('2023-01-01', '2024-01-01', freq='D')
users = np.random.choice(['user1', 'user2', 'user3'], n_trans)
dates = np.random.choice(date_range, n_trans, replace=True)
categories = np.random.choice(['food', 'transport', 'salary', 'shopping', 'bills'], n_trans)
types = np.random.choice(['income', 'expense'], n_trans, p=[0.2, 0.8])
amounts = np.zeros(n_trans)
income_mask = (types == 'income')
amounts[income_mask] = np.abs(np.random.lognormal(7, 1, income_mask.sum()))
amounts[~income_mask] = np.abs(np.random.lognormal(4, 1, (~income_mask).sum()))
trans_df = pd.DataFrame({'user_id': users, 'date': dates, 'category': categories, 'type': types, 'amount': amounts})
trans_df.to_csv('data/synthetic_transactions.csv', index=False)

print('Synthetic data generated.')