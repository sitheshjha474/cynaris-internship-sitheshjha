import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PropValue Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


# =========================================================
# LOAD DATA
# =========================================================
 # to run the file in streamlit, you need to use the below command in the terminal
# streamlit run d:/cynaris-internship/projects/cynaris-internship-sitheshjha/project1/dashboard/app.py 

@st.cache_data
def load_data():

    sales = pd.read_csv("cynaris-internship-sitheshjha\project1\dashboard\sales_cleaned.csv")
    customers = pd.read_csv("cynaris-internship-sitheshjha\project1\dashboard\customers_cleaned.csv")
    products = pd.read_csv("cynaris-internship-sitheshjha\project1\dashboard\products_cleaned.csv")

    sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")

    return sales, customers, products


try:
    sales, customers, products = load_data()

except Exception as e:

    st.error("Unable to load the processed datasets.")

    st.code(str(e))

    st.info(
        "Make sure the processed CSV files exist inside "
        "project1/data/processed/"
    )

    st.stop()


# =========================================================
# PREPARE SALES DATA
# =========================================================

sales["Gross_Revenue"] = (
    sales["Units"] * sales["Unit_Price"]
)

sales["Discount_Amount"] = (
    sales["Gross_Revenue"] *
    sales["Discount_Pct"] / 100
)

sales["Net_Revenue"] = (
    sales["Gross_Revenue"] -
    sales["Discount_Amount"]
)

sales["Month"] = sales["Date"].dt.to_period("M").astype(str)


# =========================================================
# CUSTOMER SEGMENT DATA
# =========================================================

reference_date = sales["Date"].max() + pd.Timedelta(days=1)

customer_rfm = (
    sales.groupby("Customer_ID")
    .agg(
        Recency=(
            "Date",
            lambda x: (reference_date - x.max()).days
        ),
        Frequency=("Transaction_ID", "nunique"),
        Monetary=("Net_Revenue", "sum")
    )
    .reset_index()
)


# =========================================================
# RFM SCORES
# =========================================================

def safe_qcut(series, ascending=True):

    try:

        if series.nunique() < 4:
            return pd.Series(
                3,
                index=series.index
            )

        if ascending:
            return pd.qcut(
                series.rank(method="first"),
                4,
                labels=[1, 2, 3, 4]
            ).astype(int)

        return pd.qcut(
            series.rank(method="first"),
            4,
            labels=[4, 3, 2, 1]
        ).astype(int)

    except Exception:

        return pd.Series(
            3,
            index=series.index
        )


customer_rfm["R_Score"] = safe_qcut(
    customer_rfm["Recency"],
    ascending=False
)

customer_rfm["F_Score"] = safe_qcut(
    customer_rfm["Frequency"],
    ascending=True
)

customer_rfm["M_Score"] = safe_qcut(
    customer_rfm["Monetary"],
    ascending=True
)


# =========================================================
# CUSTOMER SEGMENTS
# =========================================================

def assign_segment(row):

    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 3 and f >= 3 and m >= 3:
        return "Champions"

    elif r >= 3 and m >= 3:
        return "Loyal High Value"

    elif r <= 2 and m >= 3:
        return "At Risk High Value"

    elif r <= 2 and f <= 2:
        return "At Risk Low Engagement"

    elif f >= 3:
        return "Frequent Customers"

    else:
        return "Potential Customers"


customer_rfm["Segment"] = customer_rfm.apply(
    assign_segment,
    axis=1
)


# =========================================================
# MERGE CUSTOMER INFORMATION
# =========================================================

customer_analysis = customer_rfm.merge(
    customers,
    on="Customer_ID",
    how="left"
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("Dashboard Filters")

min_date = sales["Date"].min().date()
max_date = sales["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

cities = sorted(
    sales["City"].dropna().unique()
)

selected_cities = st.sidebar.multiselect(
    "City",
    cities,
    default=cities
)

channels = sorted(
    sales["Channel"].dropna().unique()
)

selected_channels = st.sidebar.multiselect(
    "Sales Channel",
    channels,
    default=channels
)

categories = sorted(
    sales["Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)


# =========================================================
# APPLY FILTERS
# =========================================================

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

else:

    start_date = pd.Timestamp(min_date)
    end_date = pd.Timestamp(max_date)


filtered_sales = sales[
    (sales["Date"] >= start_date)
    &
    (sales["Date"] <= end_date)
    &
    (sales["City"].isin(selected_cities))
    &
    (sales["Channel"].isin(selected_channels))
    &
    (sales["Category"].isin(selected_categories))
].copy()


# =========================================================
# HEADER
# =========================================================

st.title("📊 PropValue Analytics Dashboard")

st.markdown(
    """
    ### Dashboard v1

    Interactive sales, customer, product and segmentation
    analysis based on the available project datasets.
    """
)

st.divider()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = filtered_sales["Net_Revenue"].sum()

total_units = filtered_sales["Units"].sum()

total_transactions = filtered_sales["Transaction_ID"].nunique()

average_transaction_value = (
    total_revenue / total_transactions
    if total_transactions > 0
    else 0
)

return_rate = (
    filtered_sales["Return_Flag"].astype(str).str.lower().isin(
        ["1", "true", "yes", "returned"]
    ).mean() * 100
    if len(filtered_sales) > 0
    else 0
)

total_customers = filtered_sales["Customer_ID"].nunique()

total_products = filtered_sales["Product_ID"].nunique()


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Units Sold",
        f"{total_units:,.0f}"
    )

with col3:
    st.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

with col4:
    st.metric(
        "Average Transaction Value",
        f"₹{average_transaction_value:,.0f}"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Return Rate",
        f"{return_rate:.2f}%"
    )

with col6:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col7:

    churned = customers["Churned"].sum()

    customer_count = len(customers)

    churn_rate = (
        churned / customer_count * 100
        if customer_count > 0
        else 0
    )

    st.metric(
        "Customer Churn Rate",
        f"{churn_rate:.2f}%"
    )

with col8:
    st.metric(
        "Products",
        f"{total_products:,}"
    )


# =========================================================
# MONTHLY REVENUE
# =========================================================

st.divider()

st.subheader("Sales Performance")

monthly_revenue = (
    filtered_sales
    .groupby("Month")["Net_Revenue"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots()

ax.plot(
    monthly_revenue["Month"],
    monthly_revenue["Net_Revenue"],
    marker="o"
)

ax.set_title("Monthly Revenue Trend")

ax.set_xlabel("Month")

ax.set_ylabel("Net Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)


# =========================================================
# CITY + CHANNEL
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("Revenue by City")

    city_revenue = (
        filtered_sales
        .groupby("City")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(city_revenue)


with col2:

    st.subheader("Revenue by Sales Channel")

    channel_revenue = (
        filtered_sales
        .groupby("Channel")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(channel_revenue)


# =========================================================
# CATEGORY ANALYSIS
# =========================================================

st.divider()

col1, col2 = st.columns(2)


with col1:

    st.subheader("Revenue by Category")

    category_revenue = (
        filtered_sales
        .groupby("Category")["Net_Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_revenue)


with col2:

    st.subheader("Units Sold by Category")

    category_units = (
        filtered_sales
        .groupby("Category")["Units"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_units)


# =========================================================
# CUSTOMER SEGMENTATION
# =========================================================

st.divider()

st.subheader("Customer Segmentation")

segment_summary = (
    customer_analysis
    .groupby("Segment")
    .agg(
        Customers=("Customer_ID", "count"),
        Revenue=("Monetary", "sum")
    )
    .reset_index()
)

segment_summary["Percentage"] = (
    segment_summary["Customers"] /
    segment_summary["Customers"].sum() * 100
)

col1, col2 = st.columns(2)


with col1:

    st.write("Customers by Segment")

    segment_customers = (
        segment_summary
        .set_index("Segment")["Customers"]
        .sort_values(ascending=False)
    )

    st.bar_chart(segment_customers)


with col2:

    st.write("Revenue by Segment")

    segment_revenue = (
        segment_summary
        .set_index("Segment")["Revenue"]
        .sort_values(ascending=False)
    )

    st.bar_chart(segment_revenue)


# =========================================================
# CHURN BY SEGMENT
# =========================================================

st.divider()

st.subheader("Churn Rate by Customer Segment")

segment_churn = (
    customer_analysis
    .groupby("Segment")
    .agg(
        Customers=("Customer_ID", "count"),
        Churned=("Churned", "sum")
    )
    .reset_index()
)

segment_churn["Churn_Rate"] = (
    segment_churn["Churned"] /
    segment_churn["Customers"] * 100
)

st.bar_chart(
    segment_churn.set_index("Segment")["Churn_Rate"]
)


# =========================================================
# PRODUCT PERFORMANCE
# =========================================================

st.divider()

st.subheader("Product Performance")

product_sales = (
    filtered_sales
    .groupby("Product_ID")
    .agg(
        Units=("Units", "sum"),
        Revenue=("Net_Revenue", "sum")
    )
    .reset_index()
)

product_sales = product_sales.merge(
    products[
        [
            "Product_ID",
            "Name",
            "Category",
            "Stock_Units",
            "Avg_Monthly_Sales"
        ]
    ],
    on="Product_ID",
    how="left"
)

top_products = (
    product_sales
    .sort_values("Revenue", ascending=False)
    .head(10)
)

st.dataframe(
    top_products[
        [
            "Product_ID",
            "Name",
            "Category",
            "Units",
            "Revenue",
            "Stock_Units",
            "Avg_Monthly_Sales"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# =========================================================
# INVENTORY ANALYSIS
# =========================================================

st.subheader("Inventory Risk Overview")

inventory = products.copy()

inventory["Estimated_Months_Stock"] = np.where(
    inventory["Avg_Monthly_Sales"] > 0,
    inventory["Stock_Units"] /
    inventory["Avg_Monthly_Sales"],
    np.nan
)

inventory_display = (
    inventory
    .sort_values(
        "Estimated_Months_Stock",
        ascending=True
    )
    .head(10)
)

st.dataframe(
    inventory_display[
        [
            "Product_ID",
            "Name",
            "Category",
            "Stock_Units",
            "Avg_Monthly_Sales",
            "Estimated_Months_Stock"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DASHBOARD FOOTER
# =========================================================

st.divider()

st.caption(
    "Checkpoint 4 – Dashboard v1 | "
    "Cynaris Data Analyst Internship"
)

st.caption(
    "Data source: supplied sales transactions, "
    "customer data and product catalogue."
)