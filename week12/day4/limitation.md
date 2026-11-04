# Limitations and Future Improvements

## 1. Time Series Analysis
Limitation:
The demonstration uses synthetic monthly sales data.

Future improvements:
- Use actual business sales data.
- Compare multiple forecasting models.
- Tune model parameters.
- Include external factors affecting sales.

## 2. Prophet Forecasting
Limitation:
Historical market prices do not guarantee future performance.
The forecast does not account for every market event or trading holiday.

Future improvements:
- Add exchange holiday calendars.
- Compare Prophet with ARIMA and other models.
- Evaluate multiple forecast horizons.
- Monitor forecast errors over time.

## 3. Anomaly Detection
Limitation:
The sample dataset contains artificially introduced anomalies.
The methods do not independently establish fraud.

Future improvements:
- Use real transaction data.
- Evaluate against labelled anomalies.
- Tune contamination and detection thresholds.
- Compare with additional anomaly detection algorithms.

## 4. Data Storytelling
Limitation:
The example uses synthetic retail sales data.

Future improvements:
- Use verified business data.
- Add customer segmentation.
- Include business-specific KPIs.
- Collect stakeholder feedback.

## 5. Executive Reporting
Limitation:
The report is generated locally and uses sample data.

Future improvements:
- Connect to a database.
- Add interactive filters.
- Introduce scheduled report generation.
- Add user authentication and access control.

## 6. Production Architecture
Limitation:
The work is an architecture design review rather than a live
infrastructure assessment.

Future improvements:
- Build the proposed modular architecture.
- Containerize the application.
- Implement CI/CD.
- Add automated testing and monitoring.
- Conduct load and recovery testing.

## 7. Security Audit
Limitation:
The scanner uses static pattern matching and may produce
false positives or miss vulnerabilities.

Future improvements:
- Integrate dependency vulnerability scanning.
- Review Git history for exposed credentials.
- Perform infrastructure and access-control reviews.
- Conduct authorized penetration testing.

## Conclusion

Future development should prioritize real data integration,
automated testing, security, monitoring, and deployment validation.