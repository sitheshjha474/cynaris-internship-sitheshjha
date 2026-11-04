import mlflow

# Set the tracking URI to point to your SQLite database
mlflow.set_tracking_uri("sqlite:///mlflow.db")

experiment_name = "Model Version Comparison"

# Fetch all runs for the specified experiment
runs = mlflow.search_runs(experiment_names=[experiment_name])

if runs.empty:
    print(f"No runs found for experiment: '{experiment_name}'. Make sure you've run train.py first!")
else:
    print(f"Found {len(runs)} run(s) under experiment '{experiment_name}':\n")
    
    # Select key columns to display (run name, version, hyperparameters, metrics)
    columns_to_show = [
        "run_id",
        "tags.mlflow.runName",
        "params.version",
        "params.n_estimators",
        "params.max_depth",
        "metrics.accuracy",
        "metrics.f1_score"
    ]
    
    # Filter to only include columns that exist in the resulting DataFrame
    existing_cols = [col for col in columns_to_show if col in runs.columns]
    
    print(runs[existing_cols].to_string(index=False))