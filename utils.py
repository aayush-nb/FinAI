import pandas as pd
import numpy as np
import shap
import joblib

# Load model
credit_model = joblib.load('models/credit_model.pkl')

def get_credit_score(data: dict) -> dict:
    df = pd.DataFrame([data])
    score = credit_model.predict_proba(df)[0][1]  # Probability of default (lower better)
    dynamic_score = 1000 * (1 - score)  # Scale to 0-1000
    return {'dynamic_credit_score': dynamic_score, 'default_prob': score}

def get_xai_explanation(data: dict) -> dict:
    df = pd.DataFrame([data])
    explainer = shap.TreeExplainer(credit_model)
    shap_values = explainer.shap_values(df)
    return {'shap_values': shap_values[0].tolist(), 'features': df.columns.tolist()}

def analyze_cashflows(transactions: pd.DataFrame) -> dict:
    monthly_income = transactions[transactions['type'] == 'income'].groupby(transactions['date'].dt.to_period('M'))['amount'].sum().mean()
    monthly_expense = transactions[transactions['type'] == 'expense'].groupby(transactions['date'].dt.to_period('M'))['amount'].sum().mean()
    savings_potential = monthly_income - monthly_expense
    return {'monthly_income': monthly_income, 'monthly_expense': monthly_expense, 'savings_potential': savings_potential}

def get_investment_suggestions(cashflows: dict, risk_profile: str) -> list:
    suggestions = []
    if risk_profile == 'low':
        suggestions = ['Government Bonds', 'Liquid Funds']
    elif risk_profile == 'medium':
        suggestions = ['ETFs', 'Balanced Mutual Funds']
    elif risk_profile == 'high':
        suggestions = ['Stocks', 'Fractional Assets']
    invest_amount = cashflows['savings_potential'] * 0.5
    return [f'Invest ₹{invest_amount:.2f} in {s}' for s in suggestions]

def get_nudges(transactions: pd.DataFrame) -> list:
    high_spend = transactions[transactions['type'] == 'expense'].groupby('category')['amount'].sum().sort_values(ascending=False).head(2)
    nudges = []
    for cat, amt in high_spend.items():
        nudge = f'If you reduce {cat} spending by 20%, you could save ₹{amt*0.2:.2f} monthly for investments.'
        nudges.append(nudge)
    return nudges

def mock_kyc_aml(user_data: dict) -> bool:
    # Mock: Check if Aadhaar-like ID is valid, flag if suspicious
    if 'aadhaar' not in user_data or len(str(user_data['aadhaar'])) != 12:
        return False
    # AML: Flag if high transactions but low income (simplified)
    if user_data.get('income', 0) < 10000 and user_data.get('upi_transactions', 0) > 100:
        return False
    return True