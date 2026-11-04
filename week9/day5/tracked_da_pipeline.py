
from pathlib import Path
import json

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
import sklearn

from mlflow.models import infer_signature
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Project paths and MLflow configuration
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mlflow.db"
OUTPUT_DIR = BASE_DIR / "pipeline_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TRACKING_URI = f"sqlite:///{DB_PATH.as_posix()}"
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment("DA_Tracked_Experiment_Pipeline")

# Load and prepare dataset
dataset = load_diabetes(as_frame=True)
X = dataset.data
y = dataset.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "Linear_Regression": make_pipeline(
        StandardScaler(),
        LinearRegression()
    ),
    "Random_Forest": RandomForestRegressor(
        n_estimators=100,
        max_depth=6,
        random_state=42
    ),
}

results = []

# Track each experiment
for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name) as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mse ** 0.5
        r2 = r2_score(y_test, predictions)

        # Log parameters
        mlflow.log_params({
            "model_name": model_name,
            "test_size": 0.2,
            "random_state": 42,
            "dataset": "sklearn_diabetes",
            "sklearn_version": sklearn.__version__,
        })

        if model_name == "Random_Forest":
            mlflow.log_params({
                "n_estimators": 100,
                "max_depth": 6,
            })

        # Log evaluation metrics
        mlflow.log_metrics({
            "mae": float(mae),
            "mse": float(mse),
            "rmse": float(rmse),
            "r2_score": float(r2),
        })

        # Log model, signature, and trusted tree type when needed
        signature = infer_signature(X_train, model.predict(X_train))

        log_kwargs = {
            "sk_model": model,
            "name": "model",
            "signature": signature,
            "input_example": X_train.head(5),
        }

        if isinstance(model, RandomForestRegressor):
            log_kwargs["skops_trusted_types"] = [
                "sklearn.tree._tree.Tree"
            ]

        mlflow.sklearn.log_model(**log_kwargs)

        results.append({
            "model_name": model_name,
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "r2_score": r2,
            "run_id": run.info.run_id,
        })

        print(
            f"{model_name}: MAE={mae:.4f}, "
            f"RMSE={rmse:.4f}, R2={r2:.4f}"
        )

# Save results and dataset summary
results_df = pd.DataFrame(results).sort_values(
    "r2_score", ascending=False
)

csv_path = OUTPUT_DIR / "experiment_results.csv"
results_df.to_csv(csv_path, index=False)

profile = {
    "dataset": "sklearn_diabetes",
    "rows": int(len(X)),
    "features": int(X.shape[1]),
    "target": "disease_progression",
    "training_rows": int(len(X_train)),
    "testing_rows": int(len(X_test)),
}

profile_path = OUTPUT_DIR / "dataset_profile.json"
profile_path.write_text(
    json.dumps(profile, indent=4),
    encoding="utf-8"
)

# Create metric comparison chart
chart_path = OUTPUT_DIR / "model_comparison.png"

plt.figure(figsize=(8, 5))
plt.bar(results_df["model_name"], results_df["rmse"])
plt.title("Tracked DA Pipeline: RMSE Comparison")
plt.xlabel("Model")
plt.ylabel("RMSE (lower is better)")
plt.tight_layout()
plt.savefig(chart_path, dpi=150)
plt.close()

# Log summary and artifacts in a separate MLflow run
with mlflow.start_run(run_name="Pipeline_Summary"):
    best = results_df.iloc[0]

    mlflow.log_param("models_evaluated", len(results_df))
    mlflow.log_param("best_model", best["model_name"])
    mlflow.log_metric("best_r2_score", float(best["r2_score"]))
    mlflow.log_metric("best_rmse", float(best["rmse"]))

    mlflow.log_artifact(str(csv_path))
    mlflow.log_artifact(str(profile_path))
    mlflow.log_artifact(str(chart_path))

print("\nExperiment results:")
print(results_df.to_string(index=False))
print(f"\nCSV: {csv_path}")
print(f"Chart: {chart_path}")
print(f"Dataset profile: {profile_path}")
print("\nPipeline completed. Open the MLflow UI to inspect the runs.")
