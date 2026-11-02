# Prophet Forecasting on Indian Market Data

## Objective
Analyze and forecast the NIFTY 50 Indian stock market index using Facebook Prophet.

## Technologies
- Python
- Prophet
- Yahoo Finance (yfinance)
- Pandas and NumPy
- Matplotlib
- Scikit-learn

## Implementation
1. Downloaded five years of historical NIFTY 50 data.
2. Cleaned and prepared daily closing-price data.
3. Split data into training and testing sets.
4. Trained a Prophet forecasting model.
5. Evaluated predictions using MAE, RMSE and MAPE.
6. Forecasted the next 60 weekdays.
7. Visualized future predictions, trend and seasonality.

## Run Instructions
Install dependencies:

`python -m pip install -r requirements.txt`

Run the project:

`python prophet_forecasting.py`

## Output Files
- nifty50_data.csv
- test_forecast_results.csv
- future_forecast.csv
- holdout_forecast.png
- future_forecast.png
- trend_seasonality.png
- forecast_summary.json

## Evaluation
MAE, RMSE and MAPE measure forecasting error. Lower values indicate better predictions.

## Limitations
This is an educational forecasting project. Stock market forecasts are uncertain and should not be treated as investment advice. Weekday forecasts may include Indian market holidays.
