
import os
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Keep all MLflow tracking files inside this project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRACKING_DIR = os.path.join(BASE_DIR, "mlruns")
os.makedirs(TRACKING_DIR, exist_ok=True)
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("DA_Experiment_Tracking")

# Load a sample dataset
dataset = load_diabetes(as_frame=True)
X = dataset.data
y = dataset.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

experiments = [
    (
        "Linear_Regression",
        LinearRegression(),
        {"model_type": "LinearRegression"}
    ),
    (
        "Random_Forest",
        RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            random_state=42
        ),
        {
            "model_type": "RandomForestRegressor",
            "n_estimators": 100,
            "max_depth": 5
        }
    )
]

results = []

for run_name, model, params in experiments:
    with mlflow.start_run(run_name=run_name):
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mse ** 0.5
        r2 = r2_score(y_test, predictions)

        mlflow.log_params(params)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)

        mlflow.log_metric("mae", float(mae))
        mlflow.log_metric("mse", float(mse))
        mlflow.log_metric("rmse", float(rmse))
        mlflow.log_metric("r2_score", float(r2))

        mlflow.sklearn.log_model(
        sk_model=model,
        name="model",
        skops_trusted_types=["sklearn.tree._tree.Tree"]
    )

        results.append({
            "experiment": run_name,
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "r2_score": r2
        })

        print(f"\nExperiment: {run_name}")
        print(f"MAE:  {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2:   {r2:.4f}")


# Save and log a comparison report in its own MLflow run
results_df = pd.DataFrame(results)
report_path = os.path.join(BASE_DIR, "experiment_results.csv")
results_df.to_csv(report_path, index=False)

with mlflow.start_run(run_name="Experiment_Comparison_Report"):
    mlflow.log_artifact(report_path)

print("\nExperiment comparison:")
print(results_df.to_string(index=False))
print(f"\nResults saved to: {report_path}")
print(f"MLflow tracking directory: {TRACKING_DIR}")

