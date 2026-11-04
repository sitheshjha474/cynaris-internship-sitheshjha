import duckdb

DB_FILE = r"D:\cynaris-internship\projects\weeks\week6\day1\retail.db"
CSV_FILE = r"D:\cynaris-internship\projects\weeks\week6\day1\indian_dataset_100k.csv"

con = duckdb.connect(DB_FILE)

con.execute("DROP TABLE IF EXISTS retail_sales")

con.execute(f"""
CREATE TABLE retail_sales AS
SELECT *
FROM read_csv_auto('{CSV_FILE}')
""")

print("Database created successfully.")
print("Rows:", con.execute("SELECT COUNT(*) FROM retail_sales").fetchone()[0])
print("Tables:", con.execute("SHOW TABLES").fetchall())

con.close()