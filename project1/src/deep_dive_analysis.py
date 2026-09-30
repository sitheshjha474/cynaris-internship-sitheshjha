import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORT_DIR = os.path.join(BASE_DIR, "report")

os.makedirs(REPORT_DIR, exist_ok=True)

SALES_FILE = os.path.join(DATA_DIR, "sales_cleaned.csv")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers_cleaned.csv")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

print("\nLoading data...")

sales = pd.read_csv(SALES_FILE)
customers = pd.read_csv(CUSTOMER_FILE)

sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
customers["First_Purchase_Date"] = pd.to_datetime(
    customers["First_Purchase_Date"], errors="coerce"
)
customers["Last_Purchase_Date"] = pd.to_datetime(
    customers["Last_Purchase_Date"], errors="coerce"
)

print(f"Sales records: {len(sales)}")
print(f"Customers: {len(customers)}")


# ---------------------------------------------------------
# 1. CUSTOMER SEGMENTATION - RFM
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("CUSTOMER SEGMENTATION - RFM ANALYSIS")
print("=" * 60)

# Use the latest transaction date as the reference date
reference_date = sales["Date"].max() + pd.Timedelta(days=1)

rfm = sales.groupby("Customer_ID").agg(
    Recency=("Date", lambda x: (reference_date - x.max()).days),
    Frequency=("Transaction_ID", "nunique"),
    Monetary=("Net_Revenue", "sum")
).reset_index()

# ---------------------------------------------------------
# RFM SCORES
# ---------------------------------------------------------

# Higher recency score = more recent customer
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    4,
    labels=[4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)


# ---------------------------------------------------------
# CUSTOMER SEGMENTS
# ---------------------------------------------------------

def assign_segment(row):

    if row["R_Score"] >= 3 and row["F_Score"] >= 3 and row["M_Score"] >= 3:
        return "Champions"

    elif row["R_Score"] >= 3 and row["M_Score"] >= 3:
        return "Loyal High Value"

    elif row["R_Score"] <= 2 and row["M_Score"] >= 3:
        return "At Risk High Value"

    elif row["R_Score"] <= 2 and row["F_Score"] <= 2:
        return "At Risk Low Engagement"

    elif row["F_Score"] >= 3:
        return "Frequent Customers"

    else:
        return "Potential Customers"


rfm["Segment"] = rfm.apply(assign_segment, axis=1)


# ---------------------------------------------------------
# MERGE CUSTOMER INFORMATION
# ---------------------------------------------------------

customer_analysis = rfm.merge(
    customers[
        [
            "Customer_ID",
            "City",
            "Age_Band",
            "Gender",
            "Acquisition_Channel",
            "Churned"
        ]
    ],
    on="Customer_ID",
    how="left"
)


# ---------------------------------------------------------
# SAVE RFM RESULTS
# ---------------------------------------------------------

rfm_output = os.path.join(REPORT_DIR, "customer_rfm_segmentation.csv")
customer_analysis.to_csv(rfm_output, index=False)


# ---------------------------------------------------------
# SEGMENT SUMMARY
# ---------------------------------------------------------

segment_summary = customer_analysis.groupby("Segment").agg(
    Customers=("Customer_ID", "count"),
    Total_Revenue=("Monetary", "sum"),
    Average_Revenue=("Monetary", "mean"),
    Average_Orders=("Frequency", "mean"),
    Average_Recency=("Recency", "mean"),
    Churn_Rate=("Churned", "mean")
).reset_index()

segment_summary["Churn_Rate"] = segment_summary["Churn_Rate"] * 100

segment_summary = segment_summary.sort_values(
    "Total_Revenue",
    ascending=False
)

segment_output = os.path.join(REPORT_DIR, "segment_summary.csv")
segment_summary.to_csv(segment_output, index=False)

print("\nCustomer Segmentation Summary:")
print(segment_summary.to_string(index=False))


# ---------------------------------------------------------
# CHART 1 - CUSTOMERS BY SEGMENT
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

segment_counts = (
    customer_analysis["Segment"]
    .value_counts()
    .sort_values(ascending=True)
)

segment_counts.plot(kind="barh")

plt.title("Number of Customers by Segment")
plt.xlabel("Customers")
plt.ylabel("Customer Segment")
plt.tight_layout()

plt.savefig(
    os.path.join(REPORT_DIR, "customers_by_segment.png"),
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# CHART 2 - REVENUE BY SEGMENT
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

revenue_segment = (
    segment_summary
    .set_index("Segment")["Total_Revenue"]
    .sort_values()
)

revenue_segment.plot(kind="barh")

plt.title("Total Revenue by Customer Segment")
plt.xlabel("Revenue")
plt.ylabel("Customer Segment")
plt.tight_layout()

plt.savefig(
    os.path.join(REPORT_DIR, "revenue_by_segment.png"),
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# CHART 3 - CHURN RATE BY SEGMENT
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

churn_segment = (
    segment_summary
    .set_index("Segment")["Churn_Rate"]
    .sort_values()
)

churn_segment.plot(kind="barh")

plt.title("Churn Rate by Customer Segment")
plt.xlabel("Churn Rate (%)")
plt.ylabel("Customer Segment")
plt.tight_layout()

plt.savefig(
    os.path.join(REPORT_DIR, "churn_by_segment.png"),
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# 2. COHORT ANALYSIS
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("COHORT ANALYSIS")
print("=" * 60)

sales_cohort = sales[
    [
        "Customer_ID",
        "Date",
        "Net_Revenue"
    ]
].copy()

sales_cohort["Purchase_Month"] = (
    sales_cohort["Date"]
    .dt.to_period("M")
)

customer_first_purchase = (
    sales_cohort
    .groupby("Customer_ID")["Date"]
    .min()
    .reset_index()
)

customer_first_purchase["Cohort_Month"] = (
    customer_first_purchase["Date"]
    .dt.to_period("M")
)

sales_cohort = sales_cohort.merge(
    customer_first_purchase[
        ["Customer_ID", "Cohort_Month"]
    ],
    on="Customer_ID",
    how="left"
)

# Calculate months since first purchase
sales_cohort["Cohort_Index"] = (
    (sales_cohort["Purchase_Month"].dt.year -
     sales_cohort["Cohort_Month"].dt.year) * 12
    +
    (sales_cohort["Purchase_Month"].dt.month -
     sales_cohort["Cohort_Month"].dt.month)
)

# ---------------------------------------------------------
# COHORT RETENTION
# ---------------------------------------------------------

cohort_data = (
    sales_cohort
    .groupby(
        ["Cohort_Month", "Cohort_Index"]
    )["Customer_ID"]
    .nunique()
    .reset_index()
)

cohort_pivot = cohort_data.pivot(
    index="Cohort_Month",
    columns="Cohort_Index",
    values="Customer_ID"
)

cohort_sizes = (
    cohort_pivot[0]
    if 0 in cohort_pivot.columns
    else pd.Series(dtype=float)
)

cohort_retention = cohort_pivot.divide(
    cohort_sizes,
    axis=0
) * 100


# ---------------------------------------------------------
# SAVE COHORT RESULTS
# ---------------------------------------------------------

cohort_output = os.path.join(
    REPORT_DIR,
    "cohort_retention.csv"
)

cohort_retention.to_csv(cohort_output)

print("\nCohort Retention:")
print(cohort_retention.round(2).to_string())


# ---------------------------------------------------------
# CHART 4 - COHORT RETENTION HEATMAP
# ---------------------------------------------------------

plt.figure(figsize=(12, 7))

plt.imshow(
    cohort_retention,
    aspect="auto"
)

plt.colorbar(label="Retention (%)")

plt.title("Customer Cohort Retention")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")

plt.xticks(
    range(len(cohort_retention.columns)),
    cohort_retention.columns
)

plt.yticks(
    range(len(cohort_retention.index)),
    cohort_retention.index.astype(str)
)

plt.tight_layout()

plt.savefig(
    os.path.join(REPORT_DIR, "cohort_retention_heatmap.png"),
    dpi=300
)

plt.close()


# ---------------------------------------------------------
# 3. CITY ANALYSIS
# ---------------------------------------------------------

city_summary = sales.groupby("City").agg(
    Transactions=("Transaction_ID", "nunique"),
    Units=("Units", "sum"),
    Revenue=("Net_Revenue", "sum")
).reset_index()

city_summary = city_summary.sort_values(
    "Revenue",
    ascending=False
)

city_summary.to_csv(
    os.path.join(REPORT_DIR, "city_deep_dive.csv"),
    index=False
)


# ---------------------------------------------------------
# 4. CHANNEL ANALYSIS
# ---------------------------------------------------------

channel_summary = sales.groupby("Channel").agg(
    Transactions=("Transaction_ID", "nunique"),
    Units=("Units", "sum"),
    Revenue=("Net_Revenue", "sum")
).reset_index()

channel_summary = channel_summary.sort_values(
    "Revenue",
    ascending=False
)

channel_summary.to_csv(
    os.path.join(REPORT_DIR, "channel_deep_dive.csv"),
    index=False
)


# ---------------------------------------------------------
# FINAL OUTPUT
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("DEEP-DIVE ANALYSIS COMPLETED")
print("=" * 60)

print("\nGenerated files:")
print("1. customer_rfm_segmentation.csv")
print("2. segment_summary.csv")
print("3. customers_by_segment.png")
print("4. revenue_by_segment.png")
print("5. churn_by_segment.png")
print("6. cohort_retention.csv")
print("7. cohort_retention_heatmap.png")
print("8. city_deep_dive.csv")
print("9. channel_deep_dive.csv")

print(f"\nFiles saved in: {REPORT_DIR}")