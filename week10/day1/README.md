# Time Series Analysis — Trends, Seasonality and ARIMA

## Objective
Analyze monthly sales data to identify trends and seasonal patterns, test stationarity, and forecast future sales using a seasonal ARIMA model.

## Technologies Used
- Python
- Pandas and NumPy
- Matplotlib
- Statsmodels
- Scikit-learn

## Implementation

1. Generated a sample monthly sales dataset containing trend, seasonality, and random noise.
2. Visualized the original time series.
3. Decomposed the series into trend, seasonal, and residual components.
4. Applied the Augmented Dickey-Fuller (ADF) test to check stationarity.
5. Divided the data into training and testing sets.
6. Trained a SARIMA(1,1,1)(1,1,1,12) forecasting model.
7. Forecasted the final 12 months.
8. Evaluated the predictions using MAE and RMSE.
9. Saved forecast results, charts, and analysis summary.

## How to Run

Install dependencies:

`python -m pip install pandas numpy matplotlib statsmodels scikit-learn`

Run:

`python time_series_analysis.py`

## Output Files

- `monthly_sales.csv` — generated monthly sales dataset.
- `time_series_plot.png` — original sales trend.
- `trend_seasonality_decomposition.png` — decomposed time series.
- `forecast_results.csv` — actual and predicted sales.
- `sales_forecast.png` — forecast visualization.
- `analysis_summary.json` — model and evaluation summary.

## Evaluation

MAE and RMSE are used to measure forecasting errors. Lower values indicate better predictions. The ADF test uses a 0.05 significance level to assess stationarity.

## Limitations

This project uses synthetic monthly sales data for demonstration. The results do not represent actual business sales. Model parameters should be tuned and validated when applying the workflow to real-world data.
