
from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Project folders
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Generate sample sales transaction data
np.random.seed(42)

n = 1000

df = pd.DataFrame({
    "transaction_id": range(1, n + 1),
    "transaction_amount": np.random.normal(1500, 300, n),
    "quantity": np.random.randint(1, 10, n),
    "discount": np.random.uniform(0, 30, n)
})

# Add artificial anomalies for testing
anomaly_indices = np.random.choice(n, 25, replace=False)

df.loc[anomaly_indices[:10], "transaction_amount"] *= 4
df.loc[anomaly_indices[10:18], "transaction_amount"] *= 0.1
df.loc[anomaly_indices[18:], "quantity"] *= 10

df.to_csv(OUTPUT_DIR / "sales_data.csv", index=False)

print("Total transactions:", len(df))

# 2. Z-score method
mean_value = df["transaction_amount"].mean()
std_value = df["transaction_amount"].std()

df["z_score"] = (
    df["transaction_amount"] - mean_value
) / std_value

df["z_score_anomaly"] = df["z_score"].abs() > 3

# 3. IQR statistical method
Q1 = df["transaction_amount"].quantile(0.25)
Q3 = df["transaction_amount"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df["iqr_anomaly"] = (
    (df["transaction_amount"] < lower_bound)
    | (df["transaction_amount"] > upper_bound)
)

# 4. Isolation Forest
features = [
    "transaction_amount",
    "quantity",
    "discount"
]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[features])

model = IsolationForest(
    n_estimators=100,
    contamination=0.025,
    random_state=42
)

predictions = model.fit_predict(scaled_features)

df["isolation_forest_anomaly"] = predictions == -1

# 5. Compare detection methods
df["total_methods_flagged"] = (
    df["z_score_anomaly"].astype(int)
    + df["iqr_anomaly"].astype(int)
    + df["isolation_forest_anomaly"].astype(int)
)

df["combined_anomaly"] = df["total_methods_flagged"] >= 2

# Save complete results
df.to_csv(
    OUTPUT_DIR / "anomaly_detection_results.csv",
    index=False
)

# Save only detected anomalies
anomalies = df[df["combined_anomaly"]].copy()

anomalies.to_csv(
    OUTPUT_DIR / "detected_anomalies.csv",
    index=False
)

# 6. Print detection summary
summary = {
    "total_transactions": int(len(df)),
    "z_score_anomalies": int(df["z_score_anomaly"].sum()),
    "iqr_anomalies": int(df["iqr_anomaly"].sum()),
    "isolation_forest_anomalies": int(
        df["isolation_forest_anomaly"].sum()
    ),
    "combined_anomalies": int(df["combined_anomaly"].sum()),
    "z_score_threshold": 3,
    "iqr_multiplier": 1.5,
    "isolation_forest_contamination": 0.025
}

with open(
    OUTPUT_DIR / "anomaly_summary.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(summary, file, indent=4)

print("\nANOMALY DETECTION SUMMARY")
for key, value in summary.items():
    print(f"{key}: {value}")

# 7. Plot transaction amounts and anomalies
plt.figure(figsize=(12, 6))

plt.scatter(
    df["transaction_id"],
    df["transaction_amount"],
    label="Normal / all transactions",
    alpha=0.5
)

plt.scatter(
    anomalies["transaction_id"],
    anomalies["transaction_amount"],
    label="Combined anomalies",
    marker="x"
)

plt.title("Sales Transaction Anomaly Detection")
plt.xlabel("Transaction ID")
plt.ylabel("Transaction Amount")
plt.legend()
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "anomaly_scatter_plot.png",
    dpi=150
)
plt.close()

# 8. Compare detection counts
method_counts = pd.Series({
    "Z-Score": df["z_score_anomaly"].sum(),
    "IQR": df["iqr_anomaly"].sum(),
    "Isolation Forest": df["isolation_forest_anomaly"].sum(),
    "Combined": df["combined_anomaly"].sum()
})

plt.figure(figsize=(9, 5))
method_counts.plot(kind="bar")

plt.title("Anomalies Detected by Each Method")
plt.xlabel("Detection Method")
plt.ylabel("Number of Anomalies")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "method_comparison.png",
    dpi=150
)
plt.close()

print("\nDetected anomaly sample:")
print(anomalies.head(10).to_string(index=False))

print("\nAnalysis completed successfully!")
print("Results saved in:", OUTPUT_DIR)
