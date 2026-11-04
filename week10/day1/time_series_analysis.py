from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Project folders
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Create sample monthly sales data
np.random.seed(42)

dates = pd.date_range(
    start="2018-01-01",
    periods=96,
    freq="MS"
)

trend = np.linspace(100, 250, 96)
seasonality = 25 * np.sin(2 * np.pi * np.arange(96) / 12)
noise = np.random.normal(0, 8, 96)

sales = trend + seasonality + noise

df = pd.DataFrame({
    "date": dates,
    "sales": sales
})

df.to_csv(OUTPUT_DIR / "monthly_sales.csv", index=False)

# Set date as index
df.set_index("date", inplace=True)
series = df["sales"]

# 2. Plot original time series
plt.figure(figsize=(12, 5))
plt.plot(series, label="Monthly Sales")
plt.title("Monthly Sales — Time Series")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "time_series_plot.png", dpi=150)
plt.close()

# 3. Decompose trend, seasonality and residuals
decomposition = seasonal_decompose(
    series,
    model="additive",
    period=12
)

fig = decomposition.plot()
fig.set_size_inches(12, 8)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "trend_seasonality_decomposition.png", dpi=150)
plt.close(fig)

# 4. Check stationarity using ADF test
adf_result = adfuller(series.dropna())

adf_statistic = float(adf_result[0])
p_value = float(adf_result[1])
stationarity = (
    "Stationary"
    if p_value < 0.05
    else "Non-stationary"
)

print("ADF Test")
print("ADF Statistic:", adf_statistic)
print("p-value:", p_value)
print("Result:", stationarity)

# 5. Split data into training and testing sets
train = series.iloc[:-12]
test = series.iloc[-12:]

# 6. Fit seasonal ARIMA (SARIMA) model
# Seasonal period = 12 months
model = SARIMAX(
    train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)

model_fit = model.fit(disp=False)

# 7. Forecast the next 12 months
forecast_result = model_fit.get_forecast(steps=len(test))
forecast = forecast_result.predicted_mean
confidence = forecast_result.conf_int()

forecast.index = test.index
confidence.index = test.index

# 8. Evaluate forecast
mae = mean_absolute_error(test, forecast)
rmse = np.sqrt(mean_squared_error(test, forecast))

results = pd.DataFrame({
    "actual_sales": test,
    "predicted_sales": forecast
})

results.to_csv(OUTPUT_DIR / "forecast_results.csv")

print("\nForecast Evaluation")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))

# 9. Plot actual vs predicted sales
plt.figure(figsize=(12, 5))
plt.plot(train.index, train, label="Training Data")
plt.plot(test.index, test, label="Actual Sales")
plt.plot(forecast.index, forecast, label="Forecast")

plt.fill_between(
    confidence.index,
    confidence.iloc[:, 0],
    confidence.iloc[:, 1],
    alpha=0.2,
    label="Confidence Interval"
)

plt.title("SARIMA Sales Forecast")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_forecast.png", dpi=150)
plt.close()

# 10. Save analysis summary
summary = {
    "dataset": "Synthetic Monthly Sales",
    "observations": int(len(series)),
    "frequency": "Monthly",
    "seasonal_period": 12,
    "adf_statistic": adf_statistic,
    "adf_p_value": p_value,
    "stationarity_result": stationarity,
    "model": "SARIMA(1,1,1)(1,1,1,12)",
    "training_observations": int(len(train)),
    "testing_observations": int(len(test)),
    "mae": float(mae),
    "rmse": float(rmse)
}

with open(OUTPUT_DIR / "analysis_summary.json", "w") as file:
    json.dump(summary, file, indent=4)

print("\nAnalysis completed successfully!")
print("Output files saved in:", OUTPUT_DIR)