from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"


def calculate_metrics():

    sales = pd.read_csv(
        DATA_DIR / "sales_cleaned.csv"
    )

    customers = pd.read_csv(
        DATA_DIR / "customers_cleaned.csv"
    )

    products = pd.read_csv(
        DATA_DIR / "products_cleaned.csv"
    )

    # ---------------------------------------------
    # Sales metrics
    # ---------------------------------------------

    total_revenue = sales["Net_Revenue"].sum()

    total_units = sales["Units"].sum()

    total_transactions = sales["Transaction_ID"].nunique()

    average_transaction_value = (
        total_revenue / total_transactions
    )

    return_rate = (
        sales["Return_Flag"].mean() * 100
    )

    # ---------------------------------------------
    # Customer metrics
    # ---------------------------------------------

    total_customers = customers["Customer_ID"].nunique()

    churn_rate = (
        customers["Churned"].mean() * 100
    )

    # ---------------------------------------------
    # Product metrics
    # ---------------------------------------------

    total_products = products["Product_ID"].nunique()

    average_stock = products["Stock_Units"].mean()

    # ---------------------------------------------
    # Output
    # ---------------------------------------------

    print("\n========== BASELINE METRICS ==========\n")

    print(f"Total Revenue       : {total_revenue:,.2f}")
    print(f"Total Units Sold    : {total_units:,.0f}")
    print(f"Transactions        : {total_transactions:,}")
    print(
        f"Average Transaction : "
        f"{average_transaction_value:,.2f}"
    )

    print(f"Return Rate         : {return_rate:.2f}%")

    print(f"Customers           : {total_customers:,}")
    print(f"Customer Churn Rate : {churn_rate:.2f}%")

    print(f"Products            : {total_products:,}")
    print(f"Average Stock       : {average_stock:.2f}")


if __name__ == "__main__":
    calculate_metrics()