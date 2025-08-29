# FinAI: AI-Driven Credit Scoring and Personalized Investment Engine

## Overview
This is an innovative Fintech project targeting financial inclusion. It uses AI to score credit with alternative data and suggests personalized investments with behavioral nudges. Built with compliance in mind for easy bank integration.

## Setup
1. Clone repo: `git clone <repo-url>`
2. Create data and models folders: `mkdir data models`
3. Generate synthetic data: `python generate_synthetic_data.py`
4. Train model: `python train_credit_model.py`
5. Run app: `uvicorn main:app --reload`

For real datasets:
- Download Home Credit Default Risk from https://www.kaggle.com/competitions/home-credit-default-risk/data
- Replace 'synthetic_credit_data.csv' with 'application_train.csv' (select alternative features like DAYS_EMPLOYED, AMT_REQ_CREDIT_BUREAU, etc.)
- Download Personal Finance Tracker from https://www.kaggle.com/datasets/khushikyad001/personal-finance-tracker-dataset
- Use in investment endpoint by passing real transactions.

## Deployment
1. Build Docker image: `docker build -t finai .`
2. Run container: `docker run -p 8000:80 finai`
3. Access API at http://localhost:8000/docs (Swagger UI for testing).

## Usage
- Credit Score: POST /credit_score with JSON body e.g., {"age": 25, "income": 40000, ...}
- Investments: POST /investment_suggestions with transactions list and risk_profile.
- Compliance: POST /compliance_check.

## Local Testing
- Run `python generate_synthetic_data.py` to generate data.
- Run `python train_credit_model.py` to train the model.
- Start the server with `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`.
- Test endpoints at `http://localhost:8000/docs`.
- Build and scan Docker image: `docker build -t finai . && docker scout cves finai`.

This project is deployable in banks via API integration. For production, add database (e.g., PostgreSQL) and real API keys for KYC.

