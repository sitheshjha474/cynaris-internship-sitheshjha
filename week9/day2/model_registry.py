
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd

from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# 1. Configure MLflow
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mlflow.db"

tracking_uri = f"sqlite:///{DB_PATH.as_posix()}"

mlflow.set_tracking_uri(tracking_uri)
mlflow.set_registry_uri(tracking_uri)
mlflow.set_experiment("DA_Model_Registry")

client = MlflowClient()


# --------------------------------------------------
# 2. Load and split dataset
# --------------------------------------------------

dataset = load_diabetes(as_frame=True)

X = dataset.data
y = dataset.target

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# --------------------------------------------------
# 3. Define models
# --------------------------------------------------

models = {
    "DA_Linear_Regression": LinearRegression(),
    "DA_Random_Forest": RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
}

results = []


# --------------------------------------------------
# 4. Train, evaluate, log, and register models
# --------------------------------------------------

for model_name, model in models.items():

    with mlflow.start_run(run_name=model_name) as run:

        # Train model
        model.fit(X_train, y_train)

        # Make predictions
        predictions = model.predict(X_test)

        # Calculate metrics
        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mean_squared_error(
            y_test, predictions
        ) ** 0.5
        r2 = r2_score(y_test, predictions)

        # Log parameters
        mlflow.log_params({
            "model_type": model.__class__.__name__,
            "test_size": 0.2,
            "random_state": 42
        })

        # Log metrics
        mlflow.log_metrics({
            "mae": float(mae),
            "mse": float(mse),
            "rmse": float(rmse),
            "r2_score": float(r2)
        })

        # Create model signature
        signature = infer_signature(
            X_train,
            model.predict(X_train)
        )

        # Register model under its own registered name
        log_kwargs = {
            "sk_model": model,
            "name": "model",
            "registered_model_name": model_name,
            "signature": signature,
            "input_example": X_train.head(5)
        }

        # Explicitly trust the tree type only for our
        # locally trained Random Forest model.
        if isinstance(model, RandomForestRegressor):
            log_kwargs["skops_trusted_types"] = [
                "sklearn.tree._tree.Tree"
            ]

        mlflow.sklearn.log_model(**log_kwargs)

        # Find the registered version associated with this run
        versions = client.search_model_versions(
            f"name='{model_name}'"
        )

        matching_versions = [
            version
            for version in versions
            if version.run_id == run.info.run_id
        ]

        if not matching_versions:
            raise RuntimeError(
                f"Registration failed for {model_name}"
            )

        version = max(
            matching_versions,
            key=lambda item: int(item.version)
        )

        # Add metadata tags to model version
        client.set_model_version_tag(
            model_name,
            version.version,
            "purpose",
            "analyst_model"
        )

        client.set_model_version_tag(
            model_name,
            version.version,
            "r2_score",
            f"{r2:.4f}"
        )

        # Save results
        results.append({
            "model_name": model_name,
            "version": version.version,
            "run_id": run.info.run_id,
            "mae": mae,
            "rmse": rmse,
            "r2_score": r2
        })

        print(f"\nRegistered model: {model_name}")
        print(f"Version: {version.version}")
        print(
            f"MAE: {mae:.4f} | "
            f"RMSE: {rmse:.4f} | "
            f"R2: {r2:.4f}"
        )


# --------------------------------------------------
# 5. Select the best model
# --------------------------------------------------

best = max(
    results,
    key=lambda item: item["r2_score"]
)

best_name = best["model_name"]
best_version = best["version"]

client.set_registered_model_alias(
    best_name,
    "champion",
    best_version
)


# --------------------------------------------------
# 6. Load and test the champion model
# --------------------------------------------------

champion = mlflow.sklearn.load_model(
    f"models:/{best_name}@champion"
)

test_predictions = champion.predict(
    X_test.head(5)
)


# --------------------------------------------------
# 7. Export model comparison report
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_path = BASE_DIR / "registry_results.csv"

results_df.to_csv(
    results_path,
    index=False
)


# --------------------------------------------------
# 8. Print final results
# --------------------------------------------------

print("\nModel comparison:")
print(results_df.to_string(index=False))

print(f"\nChampion model: {best_name}")
print(f"Champion version: {best_version}")
print(f"Champion alias: {best_name}@champion")
print(f"Test predictions: {test_predictions.tolist()}")
print(f"Comparison report: {results_path}")
print(f"MLflow database: {DB_PATH}")
