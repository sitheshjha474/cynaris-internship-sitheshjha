
from pathlib import Path
import json
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Download NIFTY 50 Indian market data
print("Downloading NIFTY 50 data...")

market = yf.download(
    "^NSEI",
    period="5y",
    interval="1d",
    auto_adjust=True,
    progress=False
)

if market.empty:
    raise SystemExit("No data downloaded. Check your internet connection.")

close = market["Close"]

if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]

df = close.rename("y").dropna().reset_index()
df.columns = ["ds", "y"]
df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)
df = df.dropna().sort_values("ds").reset_index(drop=True)

df.to_csv(OUTPUT_DIR / "nifty50_data.csv", index=False)

print("Total observations:", len(df))

# Train-test split: last 60 trading sessions for testing
if len(df) <= 90:
    raise SystemExit("Not enough data for training and testing.")

train = df.iloc[:-60].copy()
test = df.iloc[-60:].copy()

# Train Prophet model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False,
    seasonality_mode="additive"
)

model.fit(train)

# Predict on test dates
forecast = model.predict(test[["ds"]])

actual = test["y"].values
predicted = forecast["yhat"].values

# Evaluation
mae = mean_absolute_error(actual, predicted)
rmse = np.sqrt(mean_squared_error(actual, predicted))
mape = np.mean(
    np.abs((actual - predicted) / np.maximum(np.abs(actual), 1e-8))
) * 100

print("\nModel Evaluation")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("MAPE:", round(mape, 2), "%")

# Save test predictions
test_results = pd.DataFrame({
    "Date": test["ds"].values,
    "Actual": test["y"].values,
    "Predicted": forecast["yhat"].iloc[:len(test)].values
})

test_results.to_csv(
    OUTPUT_DIR / "test_forecast_results.csv",
    index=False
)

# Plot actual vs predicted
plt.figure(figsize=(12, 6))
plt.plot(train["ds"], train["y"], label="Training data")
plt.plot(test["ds"], actual, label="Actual values")
plt.plot(test["ds"], predicted, label="Predicted values")

plt.fill_between(
    test["ds"],
    forecast["yhat_lower"],
    forecast["yhat_upper"],
    alpha=0.2,
    label="Prediction interval"
)

plt.title("NIFTY 50 Prophet Forecast")
plt.xlabel("Date")
plt.ylabel("Index Value")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "holdout_forecast.png", dpi=150)
plt.close()

# Refit model on all historical data
final_model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False
)

final_model.fit(df)

# Forecast next 60 weekdays
future = final_model.make_future_dataframe(
    periods=60,
    freq="B"
)

future_forecast = final_model.predict(future)

future_forecast[
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
].tail(60).to_csv(
    OUTPUT_DIR / "future_forecast.csv",
    index=False
)

# Future forecast chart
fig = final_model.plot(future_forecast)
plt.title("NIFTY 50 — Future 60 Weekday Forecast")
plt.tight_layout()
fig.savefig(OUTPUT_DIR / "future_forecast.png", dpi=150)
plt.close(fig)

# Trend and seasonality chart
fig = final_model.plot_components(future_forecast)
fig.tight_layout()
fig.savefig(
    OUTPUT_DIR / "trend_seasonality.png",
    dpi=150
)
plt.close(fig)

# Save summary
summary = {
    "market": "NIFTY 50",
    "ticker": "^NSEI",
    "observations": len(df),
    "training_rows": len(train),
    "testing_rows": len(test),
    "model": "Prophet",
    "MAE": float(mae),
    "RMSE": float(rmse),
    "MAPE": float(mape)
}

with open(
    OUTPUT_DIR / "forecast_summary.json",
    "w"
) as file:
    json.dump(summary, file, indent=4)

print("\nForecasting completed successfully!")
print("All files saved inside:", OUTPUT_DIR)
