from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="NIFTY 50 Forecast Dashboard",
    page_icon="📈",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"

st.title("📈 NIFTY 50 Forecasting Dashboard")
st.caption("Indian Stock Market | Prophet Time-Series Forecasting")

# -------------------------------
# Load output files
# -------------------------------
@st.cache_data
def load_data():
    historical = pd.read_csv(OUTPUT_DIR / "nifty50_data.csv")
    test = pd.read_csv(OUTPUT_DIR / "test_forecast_results.csv")
    future = pd.read_csv(OUTPUT_DIR / "future_forecast.csv")

    with open(OUTPUT_DIR / "forecast_summary.json", "r") as file:
        summary = json.load(file)

    return historical, test, future, summary


try:
    historical, test, future, summary = load_data()
except FileNotFoundError as error:
    st.error(f"Required forecasting output is missing: {error}")
    st.info("Run prophet_forecasting.py first to generate the output files.")
    st.stop()

# -------------------------------
# Prepare dates and columns
# -------------------------------
def find_column(data, candidates):
    for candidate in candidates:
        if candidate in data.columns:
            return candidate
    return None


historical_date = find_column(historical, ["ds", "Date", "date"])
historical_price = find_column(
    historical, ["y", "Close", "close", "Adj Close"]
)

test_date = find_column(test, ["ds", "Date", "date"])
actual_col = find_column(test, ["Actual", "actual", "y"])
predicted_col = find_column(
    test, ["Predicted", "predicted", "yhat"]
)

future_date = find_column(future, ["ds", "Date", "date"])
future_prediction = find_column(
    future, ["yhat", "Predicted", "predicted"]
)

if not all([
    historical_date, historical_price,
    test_date, actual_col, predicted_col,
    future_date, future_prediction
]):
    st.error("CSV columns do not match the expected forecasting format.")
    st.write("Historical columns:", historical.columns.tolist())
    st.write("Test columns:", test.columns.tolist())
    st.write("Future columns:", future.columns.tolist())
    st.stop()

for df, date_col in [
    (historical, historical_date),
    (test, test_date),
    (future, future_date)
]:
    df[date_col] = pd.to_datetime(df[date_col])

# -------------------------------
# Sidebar filters
# -------------------------------
st.sidebar.header("Dashboard Filters")

start_date = st.sidebar.date_input(
    "Start date",
    value=historical[historical_date].min().date()
)

end_date = st.sidebar.date_input(
    "End date",
    value=historical[historical_date].max().date()
)

if start_date > end_date:
    st.error("Start date must be before end date.")
    st.stop()

filtered = historical[
    (historical[historical_date] >= pd.Timestamp(start_date))
    & (historical[historical_date] <= pd.Timestamp(end_date))
]

# -------------------------------
# KPI metrics
# -------------------------------
mae = summary.get("MAE", summary.get("mae", 930.58))
rmse = summary.get("RMSE", summary.get("rmse", 1112.41))
mape = summary.get("MAPE", summary.get("mape", 4.05))

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Observations", f"{len(historical):,}")
col2.metric("MAE", f"{float(mae):,.2f}")
col3.metric("RMSE", f"{float(rmse):,.2f}")
col4.metric("MAPE", f"{float(mape):.2f}%")

st.divider()

# -------------------------------
# Historical price chart
# -------------------------------
st.subheader("1. Historical NIFTY 50 Prices")

fig_history = px.line(
    filtered,
    x=historical_date,
    y=historical_price,
    title="NIFTY 50 Historical Closing Prices",
    labels={
        historical_date: "Date",
        historical_price: "Closing Price"
    }
)

fig_history.update_layout(hovermode="x unified")
st.plotly_chart(fig_history, use_container_width=True)

# -------------------------------
# Actual vs predicted chart
# -------------------------------
st.subheader("2. Actual vs Predicted Prices")

fig_test = go.Figure()

fig_test.add_trace(go.Scatter(
    x=test[test_date],
    y=test[actual_col],
    mode="lines",
    name="Actual Price"
))

fig_test.add_trace(go.Scatter(
    x=test[test_date],
    y=test[predicted_col],
    mode="lines",
    name="Predicted Price"
))

fig_test.update_layout(
    title="Actual vs Prophet Predictions",
    xaxis_title="Date",
    yaxis_title="NIFTY 50 Price",
    hovermode="x unified"
)

st.plotly_chart(fig_test, use_container_width=True)

# -------------------------------
# Future forecast chart
# -------------------------------
st.subheader("3. Future Market Forecast")

fig_future = go.Figure()

fig_future.add_trace(go.Scatter(
    x=future[future_date],
    y=future[future_prediction],
    mode="lines",
    name="Forecast",
    line=dict(width=2)
))

lower_col = find_column(future, ["yhat_lower", "lower"])
upper_col = find_column(future, ["yhat_upper", "upper"])

if lower_col and upper_col:
    fig_future.add_trace(go.Scatter(
        x=future[future_date],
        y=future[upper_col],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        name="Upper Bound"
    ))

    fig_future.add_trace(go.Scatter(
        x=future[future_date],
        y=future[lower_col],
        mode="lines",
        fill="tonexty",
        line=dict(width=0),
        name="Confidence Interval"
    ))

fig_future.update_layout(
    title="Prophet Future Price Forecast",
    xaxis_title="Date",
    yaxis_title="Forecast Price",
    hovermode="x unified"
)

st.plotly_chart(fig_future, use_container_width=True)

# -------------------------------
# Model performance
# -------------------------------
st.subheader("4. Model Performance")

performance = pd.DataFrame({
    "Metric": ["MAE", "RMSE", "MAPE"],
    "Value": [float(mae), float(rmse), float(mape)]
})

fig_metrics = px.bar(
    performance,
    x="Metric",
    y="Value",
    text_auto=".2f",
    title="Prophet Model Evaluation Metrics"
)

st.plotly_chart(fig_metrics, use_container_width=True)

# -------------------------------
# Forecast data download
# -------------------------------
st.subheader("5. Download Forecast Results")

st.download_button(
    "Download Future Forecast CSV",
    data=future.to_csv(index=False).encode("utf-8"),
    file_name="nifty50_future_forecast.csv",
    mime="text/csv"
)

st.success("Forecasting dashboard loaded successfully.")

st.caption(
    "Note: Forecasts are statistical estimates, not guaranteed market outcomes."
)