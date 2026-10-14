
from pathlib import Path

import mlflow
import pandas as pd
from scipy.stats import norm
import numpy as np

# Project paths and MLflow setup
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "mlflow.db"

tracking_uri = f"sqlite:///{DB_PATH.as_posix()}"
mlflow.set_tracking_uri(tracking_uri)
mlflow.set_registry_uri(tracking_uri)
mlflow.set_experiment("DA_AB_Test_Tracking")

# Simulated A/B test settings
SEED = 42
SAMPLE_SIZE = 5000
CONTROL_RATE = 0.12
TREATMENT_RATE = 0.14
ALPHA = 0.05

# Reproducible simulated user outcomes
rng = np.random.default_rng(SEED)

control = rng.binomial(1, CONTROL_RATE, SAMPLE_SIZE)
treatment = rng.binomial(1, TREATMENT_RATE, SAMPLE_SIZE)

control_conversions = int(control.sum())
treatment_conversions = int(treatment.sum())

control_rate = control.mean()
treatment_rate = treatment.mean()

absolute_lift = treatment_rate - control_rate
relative_lift = (
    absolute_lift / control_rate if control_rate > 0 else 0.0
)

# Two-proportion z-test using pooled conversion rate
pooled_rate = (
    control_conversions + treatment_conversions
) / (2 * SAMPLE_SIZE)

standard_error = np.sqrt(
    pooled_rate * (1 - pooled_rate) * (2 / SAMPLE_SIZE)
)

if standard_error > 0:
    z_statistic = absolute_lift / standard_error
    p_value = 2 * norm.sf(abs(z_statistic))
else:
    z_statistic = 0.0
    p_value = 1.0

statistically_significant = p_value < ALPHA

if statistically_significant and absolute_lift > 0:
    decision = "Treatment performed significantly better"
elif statistically_significant and absolute_lift < 0:
    decision = "Treatment performed significantly worse"
else:
    decision = "No statistically significant difference"

# Build report
results = pd.DataFrame([
    {
        "variant": "A_Control",
        "sample_size": SAMPLE_SIZE,
        "conversions": control_conversions,
        "conversion_rate": control_rate
    },
    {
        "variant": "B_Treatment",
        "sample_size": SAMPLE_SIZE,
        "conversions": treatment_conversions,
        "conversion_rate": treatment_rate
    }
])

results_path = BASE_DIR / "ab_test_results.csv"
results.to_csv(results_path, index=False)

# Track the A/B experiment in MLflow
with mlflow.start_run(run_name="Dashboard_AB_Test"):
    mlflow.log_params({
        "experiment_type": "A/B test",
        "control_variant": "A_Control",
        "treatment_variant": "B_Treatment",
        "sample_size_per_variant": SAMPLE_SIZE,
        "random_seed": SEED,
        "alpha": ALPHA,
        "control_assumed_rate": CONTROL_RATE,
        "treatment_assumed_rate": TREATMENT_RATE
    })

    mlflow.log_metrics({
        "control_conversion_rate": float(control_rate),
        "treatment_conversion_rate": float(treatment_rate),
        "absolute_lift": float(absolute_lift),
        "relative_lift": float(relative_lift),
        "z_statistic": float(z_statistic),
        "p_value": float(p_value),
        "control_conversions": float(control_conversions),
        "treatment_conversions": float(treatment_conversions)
    })

    mlflow.set_tag("decision", decision)
    mlflow.set_tag(
        "statistically_significant",
        str(statistically_significant)
    )
    mlflow.set_tag("data_type", "simulated")

    mlflow.log_artifact(str(results_path))

# Display results
print("\nA/B TEST RESULTS")
print(results.to_string(index=False))
print(f"\nAbsolute lift: {absolute_lift:.4%}")
print(f"Relative lift: {relative_lift:.2%}")
print(f"Z-statistic: {z_statistic:.4f}")
print(f"P-value: {p_value:.6f}")
print(f"Significance level: {ALPHA}")
print(f"Decision: {decision}")
print(f"Report saved to: {results_path}")
print("MLflow experiment: DA_AB_Test_Tracking")
