import os
import numpy as np
import pandas as pd
import plotly.express as px

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


# --------------------------------
# 1. Setup
# --------------------------------

os.makedirs("outputs", exist_ok=True)

np.random.seed(42)

# --------------------------------
# 2. Generate sample sales data
# --------------------------------

months = pd.date_range("2025-01-01", periods=12, freq="MS")
regions = ["North", "South", "East", "West"]
products = ["Electronics", "Clothing", "Furniture"]

records = []

for i, month in enumerate(months):
    for region in regions:
        for product in products:

            base_sales = {
                "Electronics": 60000,
                "Clothing": 40000,
                "Furniture": 50000
            }[product]

            region_factor = {
                "North": 1.15,
                "South": 1.10,
                "East": 0.80,
                "West": 1.00
            }[region]

            sales = (
                base_sales
                * (1 + i * 0.02)
                * region_factor
                + np.random.normal(0, 3000)
            )

            records.append({
                "Month": month,
                "Region": region,
                "Product": product,
                "Sales": round(max(sales, 0), 2)
            })

df = pd.DataFrame(records)
df.to_csv("outputs/sales_data.csv", index=False)


# --------------------------------
# 3. Calculate business KPIs
# --------------------------------

total_sales = df["Sales"].sum()
average_sales = df["Sales"].mean()

monthly_sales = df.groupby("Month", as_index=False)["Sales"].sum()
region_sales = df.groupby("Region", as_index=False)["Sales"].sum()
product_sales = df.groupby("Product", as_index=False)["Sales"].sum()

best_region_row = region_sales.loc[region_sales["Sales"].idxmax()]
worst_region_row = region_sales.loc[region_sales["Sales"].idxmin()]
best_product_row = product_sales.loc[product_sales["Sales"].idxmax()]

first_month_sales = monthly_sales.iloc[0]["Sales"]
last_month_sales = monthly_sales.iloc[-1]["Sales"]

sales_growth = (
    (last_month_sales - first_month_sales) / first_month_sales
) * 100

best_region = best_region_row["Region"]
worst_region = worst_region_row["Region"]
best_product = best_product_row["Product"]

# --------------------------------
# 4. Create Plotly charts
# --------------------------------

# Monthly sales trend
fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig1.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="Sales (INR)"
)

fig1.write_html("outputs/monthly_sales.html")
fig1.write_image("outputs/monthly_sales.png", width=1100, height=550)


# Regional sales comparison
fig2 = px.bar(
    region_sales.sort_values("Sales", ascending=False),
    x="Region",
    y="Sales",
    color="Region",
    title="Sales Performance by Region"
)

fig2.update_layout(
    template="plotly_white",
    showlegend=False,
    yaxis_title="Sales (INR)"
)

fig2.write_html("outputs/regional_sales.html")
fig2.write_image("outputs/regional_sales.png", width=1100, height=550)


# Product sales comparison
fig3 = px.pie(
    product_sales,
    names="Product",
    values="Sales",
    title="Sales Contribution by Product"
)

fig3.update_layout(template="plotly_white")

fig3.write_html("outputs/product_sales.html")
fig3.write_image("outputs/product_sales.png", width=900, height=550)


# --------------------------------
# 5. Create executive PowerPoint
# --------------------------------

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)


def add_title(slide, title, subtitle=None):
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.25), Inches(12), Inches(0.6)
    )
    paragraph = title_box.text_frame.paragraphs[0]
    paragraph.text = title
    paragraph.font.size = Pt(27)
    paragraph.font.bold = True
    paragraph.font.color.rgb = RGBColor(31, 78, 121)

    if subtitle:
        subtitle_box = slide.shapes.add_textbox(
            Inches(0.55), Inches(0.9), Inches(12), Inches(0.35)
        )
        p = subtitle_box.text_frame.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(100, 100, 100)


def add_bullet_slide(title, bullet_points):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, title)

    text_box = slide.shapes.add_textbox(
        Inches(0.9), Inches(1.5), Inches(11.5), Inches(5.2)
    )

    text_frame = text_box.text_frame
    text_frame.word_wrap = True

    for index, point in enumerate(bullet_points):
        if index == 0:
            paragraph = text_frame.paragraphs[0]
        else:
            paragraph = text_frame.add_paragraph()

        paragraph.text = point
        paragraph.font.size = Pt(21)
        paragraph.space_after = Pt(20)

    return slide


# Slide 1: Cover
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(
    slide,
    "Executive Sales Performance Report",
    "Annual Business Performance | January–December 2025"
)

cover_text = slide.shapes.add_textbox(
    Inches(0.8), Inches(2.2), Inches(11.5), Inches(2)
)
p = cover_text.text_frame.paragraphs[0]
p.text = "Sales Performance and Business Insights"
p.font.size = Pt(30)
p.font.bold = True

p2 = cover_text.text_frame.add_paragraph()
p2.text = "Prepared using Python, Pandas, Plotly and PowerPoint"
p2.font.size = Pt(18)


# Slide 2: Executive summary
add_bullet_slide(
    "Executive Summary",
    [
        f"Total sales: INR {total_sales:,.2f}",
        f"Average sales per region-product-month record: INR {average_sales:,.2f}",
        f"Sales change from first to last month: {sales_growth:.2f}%",
        f"Highest-performing region: {best_region}",
        f"Lowest-performing region: {worst_region}",
        f"Top product category: {best_product}"
    ]
)


# Slide 3: KPI overview
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Key Performance Indicators")

kpis = [
    ("Total Sales", f"INR {total_sales:,.0f}"),
    ("Average Sales", f"INR {average_sales:,.0f}"),
    ("Sales Change", f"{sales_growth:.2f}%"),
    ("Top Region", best_region)
]

for i, (label, value) in enumerate(kpis):
    x = 0.8 + (i % 2) * 6.1
    y = 1.7 + (i // 2) * 2.2

    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(5.3), Inches(1.5)
    )

    tf = box.text_frame
    tf.text = label
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.bold = True

    p = tf.add_paragraph()
    p.text = value
    p.font.size = Pt(25)
    p.font.color.rgb = RGBColor(31, 78, 121)


# Slide 4: Monthly trend
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Monthly Sales Trend")
slide.shapes.add_picture(
    "outputs/monthly_sales.png",
    Inches(1), Inches(1.3), width=Inches(11)
)


# Slide 5: Regional performance
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Regional Sales Performance")
slide.shapes.add_picture(
    "outputs/regional_sales.png",
    Inches(1), Inches(1.3), width=Inches(11)
)


# Slide 6: Product contribution
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_title(slide, "Product Sales Contribution")
slide.shapes.add_picture(
    "outputs/product_sales.png",
    Inches(1), Inches(1.3), width=Inches(11)
)


# Slide 7: Findings
add_bullet_slide(
    "Key Business Findings",
    [
        f"{best_region} recorded the highest total sales.",
        f"{worst_region} recorded the lowest total sales.",
        f"{best_product} contributed the highest product-category sales.",
        f"Sales changed by {sales_growth:.2f}% between January and December.",
        "Regional performance should be reviewed to identify improvement opportunities."
    ]
)


# Slide 8: Recommendations
add_bullet_slide(
    "Recommendations and Next Steps",
    [
        f"Investigate the reasons for lower sales in the {worst_region} region.",
        f"Study successful sales practices in the {best_region} region.",
        f"Review inventory and marketing opportunities for {best_product}.",
        "Monitor monthly sales KPIs through a recurring executive dashboard.",
        "Validate these findings using actual company sales data before making decisions."
    ]
)


# Slide 9: Conclusion
add_bullet_slide(
    "Conclusion",
    [
        "The analysis summarizes sales performance across months, regions and products.",
        "Visualizations help executives identify patterns and performance gaps.",
        "The recommendations provide areas for further investigation and action.",
        "This report demonstrates an automated Python-based executive reporting workflow."
    ]
)


# --------------------------------
# 6. Save PowerPoint
# --------------------------------

ppt_path = "outputs/executive_sales_report.pptx"
prs.save(ppt_path)


# --------------------------------
# 7. Save KPI summary
# --------------------------------

summary = pd.DataFrame({
    "KPI": [
        "Total Sales",
        "Average Sales",
        "Sales Change (%)",
        "Best Region",
        "Weakest Region",
        "Best Product"
    ],
    "Value": [
        round(total_sales, 2),
        round(average_sales, 2),
        round(sales_growth, 2),
        best_region,
        worst_region,
        best_product
    ]
})

summary.to_csv("outputs/executive_kpi_summary.csv", index=False)


# --------------------------------
# 8. Display completion message
# --------------------------------

print("\nEXECUTIVE REPORT GENERATED SUCCESSFULLY")
print("---------------------------------------")
print(f"Total Sales: INR {total_sales:,.2f}")
print(f"Best Region: {best_region}")
print(f"Weakest Region: {worst_region}")
print(f"Best Product: {best_product}")
print(f"Sales Change: {sales_growth:.2f}%")
print(f"\nPowerPoint saved at: {ppt_path}")
print("All charts and reports saved in outputs/")