from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from utils import get_credit_score, get_xai_explanation, analyze_cashflows, get_investment_suggestions, get_nudges, mock_kyc_aml

app = FastAPI(title="FinAI Engine")

class CreditInput(BaseModel):
    age: int
    income: float
    upi_transactions: int
    phone_recharges: int
    ecommerce_repayments: int

class InvestmentInput(BaseModel):
    transactions: list[dict]  # List of {'date': str, 'category': str, 'type': str, 'amount': float}
    risk_profile: str  # low, medium, high

class KYCInput(BaseModel):
    aadhaar: int
    income: float
    upi_transactions: int

@app.post("/credit_score")
def credit_score(input: CreditInput):
    data = input.dict()
    score = get_credit_score(data)
    explanation = get_xai_explanation(data)
    return {"score": score, "explanation": explanation}

@app.post("/investment_suggestions")
def investment_suggestions(input: InvestmentInput):
    trans_df = pd.DataFrame(input.transactions)
    trans_df['date'] = pd.to_datetime(trans_df['date'])
    cashflows = analyze_cashflows(trans_df)
    suggestions = get_investment_suggestions(cashflows, input.risk_profile)
    nudges = get_nudges(trans_df)
    return {"suggestions": suggestions, "nudges": nudges, "cashflows": cashflows}

@app.post("/compliance_check")
def compliance_check(input: KYCInput):
    if not mock_kyc_aml(input.dict()):
        raise HTTPException(status_code=400, detail="KYC/AML failed")
    return {"status": "Compliant"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)