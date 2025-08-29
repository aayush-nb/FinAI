import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load data (replace with Kaggle Home Credit for real use)
df = pd.read_csv('data/synthetic_credit_data.csv')

features = ['age', 'income', 'upi_transactions', 'phone_recharges', 'ecommerce_repayments']
X = df[features]
y = df['default']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBClassifier(eval_metric='logloss', use_label_encoder=False)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, preds)}')

joblib.dump(model, 'models/credit_model.pkl')
print('Model trained and saved.')