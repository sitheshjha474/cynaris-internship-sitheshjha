import os
import json
import pandas as pd

os.makedirs("outputs", exist_ok=True)

# Review of the current executive reporting prototype
components = [
    {
        "Component": "Data Source",
        "Current Design": "Synthetic data generated inside Python script",
        "Production Requirement": "Connect to a validated business database or data warehouse",
        "Status": "Needs Improvement",
        "Priority": "High"
    },
    {
        "Component": "Data Validation",
        "Current Design": "Basic data generation and pandas processing",
        "Production Requirement": "Validate schema, missing values, duplicates and invalid records",
        "Status": "Needs Improvement",
        "Priority": "High"
    },
    {
        "Component": "Business Logic",
        "Current Design": "KPIs calculated directly inside one Python script",
        "Production Requirement": "Separate reusable business logic into independent modules",
        "Status": "Needs Improvement",
        "Priority": "Medium"
    },
    {
        "Component": "Visualization",
        "Current Design": "Plotly charts exported as HTML and PNG",
        "Production Requirement": "Centralized chart generation with error handling",
        "Status": "Partially Ready",
        "Priority": "Medium"
    },
    {
        "Component": "Report Generation",
        "Current Design": "PowerPoint generated using python-pptx",
        "Production Requirement": "Template-based report generation with validation",
        "Status": "Partially Ready",
        "Priority": "Medium"
    },
    {
        "Component": "Application Interface",
        "Current Design": "Standalone Python script",
        "Production Requirement": "Provide a controlled web interface or reporting API",
        "Status": "Needs Improvement",
        "Priority": "Medium"
    },
    {
        "Component": "Security",
        "Current Design": "No authentication or role-based access",
        "Production Requirement": "Authentication, authorization and secure secrets management",
        "Status": "Needs Improvement",
        "Priority": "High"
    },
    {
        "Component": "Testing",
        "Current Design": "Manual execution and output checking",
        "Production Requirement": "Unit, integration and automated regression tests",
        "Status": "Needs Improvement",
        "Priority": "High"
    },
    {
        "Component": "Monitoring",
        "Current Design": "Terminal print statements",
        "Production Requirement": "Structured logs, error monitoring and operational alerts",
        "Status": "Needs Improvement",
        "Priority": "High"
    },
    {
        "Component": "Deployment",
        "Current Design": "Runs locally in a Python virtual environment",
        "Production Requirement": "Containerized deployment with CI/CD and environment configuration",
        "Status": "Needs Improvement",
        "Priority": "High"
    },
    {
        "Component": "Scalability",
        "Current Design": "Single-process report generation",
        "Production Requirement": "Background jobs and scalable workers for large reports",
        "Status": "Needs Improvement",
        "Priority": "Medium"
    },
    {
        "Component": "Documentation",
        "Current Design": "Project README and execution instructions",
        "Production Requirement": "Architecture, deployment, recovery and maintenance documentation",
        "Status": "Partially Ready",
        "Priority": "Low"
    }
]

df = pd.DataFrame(components)

# Score each component
scores = {
    "Ready": 1.0,
    "Partially Ready": 0.5,
    "Needs Improvement": 0.0
}

df["Score"] = df["Status"].map(scores)

readiness_score = round(df["Score"].mean() * 100, 2)

# Save detailed review
df.to_csv("outputs/architecture_review.csv", index=False)

# Count status categories
status_counts = df["Status"].value_counts().to_dict()

# Generate summary
summary = {
    "Project": "Executive Sales Reporting System",
    "Review_Type": "Production Architecture Review",
    "Components_Reviewed": len(df),
    "Readiness_Score_Percent": readiness_score,
    "Status_Counts": status_counts,
    "Overall_Assessment": (
        "Prototype - Not Production Ready"
        if readiness_score < 70
        else "Requires Further Validation"
    ),
    "Important_Note": (
        "This is a qualitative review of the current project design, "
        "not a production security audit or deployment certification."
    )
}

with open(
    "outputs/architecture_summary.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(summary, file, indent=4)

# Print results
print("\nPRODUCTION ARCHITECTURE REVIEW")
print("--------------------------------")
print(f"Components reviewed: {len(df)}")
print(f"Readiness score: {readiness_score}%")
print(f"Assessment: {summary['Overall_Assessment']}")

print("\nStatus breakdown:")
for status, count in status_counts.items():
    print(f"{status}: {count}")

print("\nHigh-priority improvements:")
for _, row in df[df["Priority"] == "High"].iterrows():
    if row["Status"] != "Ready":
        print(f"- {row['Component']}: {row['Production Requirement']}")

print("\nReview files saved in outputs/")