import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create output folder
os.makedirs("outputs", exist_ok=True)

# -------------------------------
# 1. Create sample sales dataset
# -------------------------------

np.random.seed(42)

months = pd.date_range("2025-01-01", periods=12, freq="MS")
regions = ["North", "South", "East", "West"]
products = ["Electronics", "Clothing", "Furniture"]

records = []

for month_index, month in enumerate(months):
    for region in regions:
        for product in products:
            base_sales = {
                "Electronics": 50000,
                "Clothing": 35000,
                "Furniture": 40000
            }[product]

            # Create a gradual overall growth pattern
            growth = 1 + (month_index * 0.025)

            # Create a weaker sales pattern in the East region
            region_factor = {
                "North": 1.15,
                "South": 1.10,
                "East": 0.75,
                "West": 1.00
            }[region]

            sales = base_sales * growth * region_factor
            sales += np.random.normal(0, 2500)

            records.append({
                "Month": month,
                "Region": region,
                "Product": product,
                "Sales": round(max(sales, 0), 2)
            })

df = pd.DataFrame(records)

df.to_csv("outputs/sales_data.csv", index=False)

# -------------------------------
# 2. Analyze the data
# -------------------------------

total_sales = df["Sales"].sum()
average_sales = df["Sales"].mean()

monthly_sales = df.groupby("Month")["Sales"].sum()
region_sales = df.groupby("Region")["Sales"].sum()
product_sales = df.groupby("Product")["Sales"].sum()

best_month = monthly_sales.idxmax()
worst_month = monthly_sales.idxmin()

best_region = region_sales.idxmax()
worst_region = region_sales.idxmin()

best_product = product_sales.idxmax()

growth_percentage = (
    (monthly_sales.iloc[-1] - monthly_sales.iloc[0])
    / monthly_sales.iloc[0]
) * 100

# -------------------------------
# 3. Create visualizations
# -------------------------------

# Monthly sales trend
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/monthly_sales_trend.png")
plt.close()

# Sales by region
plt.figure(figsize=(8, 5))
region_sales.sort_values().plot(kind="bar")
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("outputs/region_sales.png")
plt.close()

# Sales by product
plt.figure(figsize=(8, 5))
product_sales.sort_values().plot(kind="bar")
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("outputs/product_sales.png")
plt.close()

# -------------------------------
# 4. Generate business narrative
# -------------------------------

report = f"""
# Retail Sales Data Story

## 1. Context — What is happening?

This analysis examines retail sales across four regions and three
product categories over 12 months.

Total sales during the period were ₹{total_sales:,.2f}.
Average sales per transaction-group record were ₹{average_sales:,.2f}.

## 2. Key Findings — What does the data show?

- The strongest sales month was {best_month.strftime('%B %Y')}.
- The weakest sales month was {worst_month.strftime('%B %Y')}.
- The {best_region} region generated the highest total sales.
- The {worst_region} region generated the lowest total sales.
- {best_product} was the highest-selling product category.
- Sales changed by {growth_percentage:.2f}% between the first and last months.

## 3. Business Challenge — Why does it matter?

The difference between the strongest and weakest regions suggests
that sales performance is not uniform across the business.

The weaker region may need further investigation into customer demand,
product availability, pricing, and marketing effectiveness.

## 4. Recommendation — What should happen next?

1. Investigate the reasons behind lower sales in the {worst_region} region.
2. Review the sales strategies used in the {best_region} region.
3. Identify opportunities to expand sales of {best_product}.
4. Monitor monthly sales trends to identify changes early.

## 5. Conclusion

The analysis highlights differences in regional and product performance
and shows how monthly sales change over time.

The findings can help management prioritize regional improvements
and make more informed sales decisions.

## Important Note

This project uses a synthetic dataset created for learning purposes.
The findings are illustrative and do not represent actual company sales.
"""

with open("outputs/business_story.md", "w", encoding="utf-8") as file:
    file.write(report)

# -------------------------------
# 5. Save summary
# -------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Average Sales",
        "Best Month",
        "Worst Month",
        "Best Region",
        "Weakest Region",
        "Best Product",
        "Sales Change (%)"
    ],
    "Value": [
        round(total_sales, 2),
        round(average_sales, 2),
        best_month.strftime("%B %Y"),
        worst_month.strftime("%B %Y"),
        best_region,
        worst_region,
        best_product,
        round(growth_percentage, 2)
    ]
})

summary.to_csv("outputs/business_summary.csv", index=False)

print("DATA STORYTELLING ANALYSIS COMPLETED")
print("-----------------------------------")
print(f"Total Sales: ₹{total_sales:,.2f}")
print(f"Best Region: {best_region}")
print(f"Weakest Region: {worst_region}")
print(f"Best Product: {best_product}")
print(f"Sales Change: {growth_percentage:.2f}%")
print("\nFiles saved in the outputs folder.")