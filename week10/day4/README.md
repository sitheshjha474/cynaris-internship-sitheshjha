# NIFTY 50 Forecasting Dashboard

## Project Overview
Developed an interactive stock market forecasting dashboard using Prophet, Plotly, and Streamlit. The dashboard visualizes historical NIFTY 50 prices, compares actual and predicted values, and displays future price forecasts.

## Technologies Used
- Python
- Prophet
- Pandas
- Plotly
- Streamlit
- Yahoo Finance data

## Features
1. Historical NIFTY 50 price visualization.
2. Actual vs predicted price comparison.
3. Future price forecasting with confidence intervals.
4. Model evaluation using MAE, RMSE, and MAPE.
5. Interactive date filtering.
6. CSV download for future forecast results.

## Model Evaluation
- MAE: 930.58
- RMSE: 1112.41
- MAPE: 4.05%

## How to Run

Install dependencies:

```bash
pip install prophet yfinance pandas numpy matplotlib scikit-learn streamlit plotly
```

Generate forecasting outputs:

```bash
python prophet_forecasting.py
```

Launch dashboard:

```bash
streamlit run dashboard.py
```

Open `http://localhost:8501`.

## Project Outputs
- Historical market data
- Test forecast results
- Future forecast results
- Interactive dashboard
- Model evaluation metrics

## Limitations
- Historical market data does not guarantee future performance.
- Forecast accuracy may change with market volatility.
- The dashboard is intended for educational and analytical purposes, not investment advice.

## Conclusion
The project combines time-series forecasting and interactive visualization to make NIFTY 50 market trends and model predictions easier to explore.
