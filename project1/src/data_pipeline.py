from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data():
    sales = pd.read_csv(
        RAW_DIR / "da_sales_transactions.csv"
    )

    customers = pd.read_csv(
        RAW_DIR / "da_customer_data.csv"
    )

    products = pd.read_csv(
        RAW_DIR / "da_product_catalogue.csv"
    )

    return sales, customers, products


# --------------------------------------------------
# Clean data
# --------------------------------------------------

def clean_data(sales, customers, products):

    # Convert dates
    sales["Date"] = pd.to_datetime(
        sales["Date"],
        errors="coerce"
    )

    customers["First_Purchase_Date"] = pd.to_datetime(
        customers["First_Purchase_Date"],
        errors="coerce"
    )

    customers["Last_Purchase_Date"] = pd.to_datetime(
        customers["Last_Purchase_Date"],
        errors="coerce"
    )

    # Numerical conversions
    sales["Units"] = pd.to_numeric(
        sales["Units"],
        errors="coerce"
    )

    sales["Unit_Price"] = pd.to_numeric(
        sales["Unit_Price"],
        errors="coerce"
    )

    sales["Discount_Pct"] = pd.to_numeric(
        sales["Discount_Pct"],
        errors="coerce"
    )

    products["MRP"] = pd.to_numeric(
        products["MRP"],
        errors="coerce"
    )

    products["COGS"] = pd.to_numeric(
        products["COGS"],
        errors="coerce"
    )

    products["Stock_Units"] = pd.to_numeric(
        products["Stock_Units"],
        errors="coerce"
    )

    products["Avg_Monthly_Sales"] = pd.to_numeric(
        products["Avg_Monthly_Sales"],
        errors="coerce"
    )

    # Remove duplicate records
    sales = sales.drop_duplicates()
    customers = customers.drop_duplicates()
    products = products.drop_duplicates()

    # Calculate transaction revenue
    sales["Gross_Revenue"] = (
        sales["Units"] *
        sales["Unit_Price"]
    )

    sales["Discount_Amount"] = (
        sales["Gross_Revenue"] *
        sales["Discount_Pct"] / 100
    )

    sales["Net_Revenue"] = (
        sales["Gross_Revenue"] -
        sales["Discount_Amount"]
    )

    return sales, customers, products


# --------------------------------------------------
# Save processed data
# --------------------------------------------------

def save_data(sales, customers, products):

    sales.to_csv(
        PROCESSED_DIR / "sales_cleaned.csv",
        index=False
    )

    customers.to_csv(
        PROCESSED_DIR / "customers_cleaned.csv",
        index=False
    )

    products.to_csv(
        PROCESSED_DIR / "products_cleaned.csv",
        index=False
    )


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def main():

    print("Loading datasets...")

    sales, customers, products = load_data()

    print("Cleaning datasets...")

    sales, customers, products = clean_data(
        sales,
        customers,
        products
    )

    print("Saving processed datasets...")

    save_data(
        sales,
        customers,
        products
    )

    print()
    print("Pipeline completed successfully.")
    print(f"Sales records: {len(sales)}")
    print(f"Customers: {len(customers)}")
    print(f"Products: {len(products)}")


if __name__ == "__main__":
    main()