# A/B Test Tracking with MLflow

## Objective

Build an A/B testing workflow that compares a control variant with a treatment variant and records experiment results in MLflow.

## Technologies

- Python
- MLflow
- Pandas
- NumPy
- SciPy
- SQLite

## Implementation

1. Simulated control and treatment groups with reproducible random data.
2. Used conversion rate as the primary metric.
3. Calculated absolute lift and relative lift.
4. Performed a two-proportion z-test using a significance level of 0.05.
5. Logged experiment parameters, metrics, and decision tags in MLflow.
6. Exported variant-level results to `ab_test_results.csv`.
7. Logged the CSV report as an MLflow artifact.

## How to Run

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the experiment:

```bash
python ab_test_tracking.py
```

Launch the MLflow UI:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

Open `http://127.0.0.1:5000` and select `DA_AB_Test_Tracking`.

## Deliverables

- `ab_test_tracking.py` — experiment simulation and statistical analysis.
- `requirements.txt` — dependencies.
- `ab_test_results.csv` — conversion results by variant.
- `mlflow.db` — local experiment-tracking database.
- `evidence/` — screenshots of logged parameters, metrics, and output.

## Limitations

The experiment uses simulated data and assumed conversion probabilities. Its findings must not be interpreted as real customer behavior or a real product improvement. A production A/B test would require randomized assignment of eligible users, appropriate sample-size planning, data-quality checks, and monitoring for experiment bias.

## Conclusion

The workflow demonstrates how MLflow can track A/B test configurations, conversion metrics, statistical results, and a report in one experiment run.
