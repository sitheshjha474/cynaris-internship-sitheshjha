import pandas as pd
import duckdb
import polars as pl
import time
import os

INPUT_FILE = "indian-dataset.csv"
CSV_FILE = "indian_dataset_100k.csv"

# --------------------------------------------------
# CREATE 100K ROW DATASET
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

if len(df) < 100000:
    repeats = (100000 // len(df)) + 1
    df_100k = pd.concat([df] * repeats, ignore_index=True).head(100000)
else:
    df_100k = df.head(100000)

df_100k.to_csv(CSV_FILE, index=False)

print("=" * 70)
print("100K ROW DATASET CREATED")
print("=" * 70)
print("Rows:", len(df_100k))
print("File:", CSV_FILE)


# --------------------------------------------------
# PANDAS
# --------------------------------------------------

print("\n" + "=" * 70)
print("PANDAS BENCHMARK")
print("=" * 70)

pandas_df = pd.read_csv(CSV_FILE)

pandas_times = []

start = time.perf_counter()
pandas_q1 = pandas_df["Sales_INR"].sum()
pandas_times.append(time.perf_counter() - start)

start = time.perf_counter()
pandas_q2 = pandas_df.groupby("Category")["Sales_INR"].sum().sort_values(ascending=False)
pandas_times.append(time.perf_counter() - start)

start = time.perf_counter()
pandas_q3 = pandas_df.groupby("City")["Profit_INR"].mean().sort_values(ascending=False)
pandas_times.append(time.perf_counter() - start)

start = time.perf_counter()
pandas_q4 = pandas_df["Payment_Method"].value_counts()
pandas_times.append(time.perf_counter() - start)

start = time.perf_counter()
pandas_q5 = pandas_df.groupby("Order_Date")["Sales_INR"].sum()
pandas_times.append(time.perf_counter() - start)

print("Q1 Total Sales:", pandas_q1)
print("Q2 Category Sales:")
print(pandas_q2)
print("Q3 Average Profit by City:")
print(pandas_q3)
print("Q4 Payment Method Count:")
print(pandas_q4)
print("Q5 Sales by Date:")
print(pandas_q5.head())

print("\nPandas total query time:", sum(pandas_times))


# --------------------------------------------------
# DUCKDB
# --------------------------------------------------

print("\n" + "=" * 70)
print("DUCKDB BENCHMARK")
print("=" * 70)

con = duckdb.connect()

duckdb_times = []

start = time.perf_counter()
duck_q1 = con.execute("""
    SELECT SUM(Sales_INR)
    FROM read_csv_auto('indian_dataset_100k.csv')
""").fetchone()[0]
duckdb_times.append(time.perf_counter() - start)

start = time.perf_counter()
duck_q2 = con.execute("""
    SELECT Category, SUM(Sales_INR) AS total_sales
    FROM read_csv_auto('indian_dataset_100k.csv')
    GROUP BY Category
    ORDER BY total_sales DESC
""").fetchdf()
duckdb_times.append(time.perf_counter() - start)

start = time.perf_counter()
duck_q3 = con.execute("""
    SELECT City, AVG(Profit_INR) AS average_profit
    FROM read_csv_auto('indian_dataset_100k.csv')
    GROUP BY City
    ORDER BY average_profit DESC
""").fetchdf()
duckdb_times.append(time.perf_counter() - start)

start = time.perf_counter()
duck_q4 = con.execute("""
    SELECT Payment_Method, COUNT(*) AS transaction_count
    FROM read_csv_auto('indian_dataset_100k.csv')
    GROUP BY Payment_Method
    ORDER BY transaction_count DESC
""").fetchdf()
duckdb_times.append(time.perf_counter() - start)

start = time.perf_counter()
duck_q5 = con.execute("""
    SELECT Order_Date, SUM(Sales_INR) AS total_sales
    FROM read_csv_auto('indian_dataset_100k.csv')
    GROUP BY Order_Date
    ORDER BY Order_Date
""").fetchdf()
duckdb_times.append(time.perf_counter() - start)

print("Q1 Total Sales:", duck_q1)
print("Q2 Category Sales:")
print(duck_q2)
print("Q3 Average Profit by City:")
print(duck_q3)
print("Q4 Payment Method Count:")
print(duck_q4)
print("Q5 Sales by Date:")
print(duck_q5.head())

print("\nDuckDB total query time:", sum(duckdb_times))


# --------------------------------------------------
# POLARS
# --------------------------------------------------

print("\n" + "=" * 70)
print("POLARS BENCHMARK")
print("=" * 70)

polars_df = pl.read_csv(CSV_FILE)

polars_times = []

start = time.perf_counter()
polars_q1 = polars_df.select(pl.col("Sales_INR").sum())
polars_times.append(time.perf_counter() - start)

start = time.perf_counter()
polars_q2 = (
    polars_df
    .group_by("Category")
    .agg(pl.col("Sales_INR").sum().alias("total_sales"))
    .sort("total_sales", descending=True)
)
polars_times.append(time.perf_counter() - start)

start = time.perf_counter()
polars_q3 = (
    polars_df
    .group_by("City")
    .agg(pl.col("Profit_INR").mean().alias("average_profit"))
    .sort("average_profit", descending=True)
)
polars_times.append(time.perf_counter() - start)

start = time.perf_counter()
polars_q4 = (
    polars_df
    .group_by("Payment_Method")
    .agg(pl.len().alias("transaction_count"))
    .sort("transaction_count", descending=True)
)
polars_times.append(time.perf_counter() - start)

start = time.perf_counter()
polars_q5 = (
    polars_df
    .group_by("Order_Date")
    .agg(pl.col("Sales_INR").sum().alias("total_sales"))
    .sort("Order_Date")
)
polars_times.append(time.perf_counter() - start)

print("Q1 Total Sales:")
print(polars_q1)

print("Q2 Category Sales:")
print(polars_q2)

print("Q3 Average Profit by City:")
print(polars_q3)

print("Q4 Payment Method Count:")
print(polars_q4)

print("Q5 Sales by Date:")
print(polars_q5.head())

print("\nPolars total query time:", sum(polars_times))


# --------------------------------------------------
# FINAL COMPARISON
# --------------------------------------------------

print("\n" + "=" * 70)
print("FINAL SPEED COMPARISON")
print("=" * 70)

print(f"Pandas :  {sum(pandas_times):.6f} seconds")
print(f"DuckDB :  {sum(duckdb_times):.6f} seconds")
print(f"Polars :  {sum(polars_times):.6f} seconds")

print("\nBenchmark completed successfully.")