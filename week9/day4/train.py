import mlflow
import mlflow.sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score


# Force the script to log to the exact same SQLite database the server is using
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Load dataset
data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# Define two versions with different hyperparameters to compare
experiments = [
    {"version": "v1.2", "n_estimators": 50, "max_depth": 4},
    {"version": "v1.3", "n_estimators": 150, "max_depth": 8}
]

mlflow.set_experiment("Model Version Comparison")

for exp in experiments:
    with mlflow.start_run(run_name=f"RandomForest_{exp['version']}"):
        # Train model
        model = RandomForestClassifier(
            n_estimators=exp["n_estimators"],
            max_depth=exp["max_depth"],
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Evaluate
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        
        # Log to MLflow
        # Log to MLflow with trusted tree types for skops serialization
        mlflow.log_param("version", exp["version"])
        mlflow.log_param("n_estimators", exp["n_estimators"])
        mlflow.log_param("max_depth", exp["max_depth"])
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        
        mlflow.sklearn.log_model(
            model, 
            "model", 
            skops_trusted_types=["sklearn.tree._tree.Tree"]
        )
        print(f"Logged {exp['version']} -> Accuracy: {acc:.4f}, F1: {f1:.4f}")