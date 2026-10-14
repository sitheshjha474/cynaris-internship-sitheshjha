# MLflow Tracking — DA Experiments

## Objective

Implement experiment tracking for data analysis and regression-model experiments using MLflow.

## Tools and Technologies

- Python
- MLflow
- Pandas
- Scikit-learn
- MLflow UI

## Implementation

1. Loaded the Diabetes regression dataset provided by Scikit-learn.
2. Split the dataset into training and testing sets.
3. Trained Linear Regression and Random Forest Regression models.
4. Calculated MAE, MSE, RMSE, and R² score for each model.
5. Logged experiment parameters and metrics using MLflow.
6. Logged trained model artifacts.
7. Saved a CSV report comparing experiment results.
8. Used the MLflow UI to inspect the recorded runs.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the experiments:

```bash
python da_experiment.py
```

Launch the MLflow dashboard:

```bash
mlflow ui --backend-store-uri ./mlruns --host 127.0.0.1 --port 5000
```

Open `http://127.0.0.1:5000` in a browser.

## Deliverables

- `da_experiment.py` — experiment tracking implementation
- `requirements.txt` — required libraries
- `experiment_results.csv` — generated comparison report
- `mlruns/` — local MLflow experiment tracking data
- `evidence/` — screenshots of experiment runs and logged metrics

## Results

The actual model metrics are recorded in `experiment_results.csv` and the MLflow UI after running the script.

## Limitations

The demonstration uses a built-in sample dataset. The reported scores are for this dataset and are not evidence of production model performance.
