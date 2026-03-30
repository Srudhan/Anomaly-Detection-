import pandas as pd
import joblib
import time
from datetime import datetime

from sklearn.preprocessing import LabelEncoder


# Load model and scaler
model = joblib.load("isolation_forest.pkl")
scaler = joblib.load("scaler.pkl")

print("Model and scaler loaded")


# Load dataset
df = pd.read_csv("transactions_data.csv")

# Basic preprocessing
df = df.drop_duplicates()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna("UNKNOWN")
    else:
        df[col] = df[col].fillna(df[col].median())


# Encode categorical columns
df_processed = df.copy()

for col in df_processed.columns:
    if df_processed[col].dtype == "object":
        encoder = LabelEncoder()
        df_processed[col] = encoder.fit_transform(df_processed[col])


feature_columns = df_processed.columns.tolist()


# Create output file
with open("anomalies_live.csv", "w") as f:
    f.write("timestamp,anomaly_score,reason\n")


print("\nStarting real-time simulation...\n")


# Simulate streaming
for i in range(len(df_processed)):

    row_df = df_processed.iloc[[i]]

    X = scaler.transform(row_df[feature_columns])

    pred = model.predict(X)[0]
    score = model.decision_function(X)[0]

    if pred == -1:
        anomaly = {
            "timestamp": datetime.now(),
            "anomaly_score": score,
            "reason": "Transaction deviates from normal pattern"
        }

        pd.DataFrame([anomaly]).to_csv(
            "anomalies_live.csv",
            mode="a",
            header=False,
            index=False
        )

        print(f"⚠️ Anomaly detected at row {i}")

    else:
        print(f"Processed row {i}")

    time.sleep(0.5)