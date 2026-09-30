# PropValue Real Estate Analytics

**Data Analyst Internship Project — Cynaris**

## Project Overview

PropValue Real Estate Analytics is an analytics project designed to support data-driven market analysis, valuation, and decision-making.

The original project brief focuses on real-estate analytics, including market trends, micro-market comparison, fair-value estimation, and a valuation API. The data package provided for the initial analysis, however, contains customer, product, and sales transaction data. Therefore, the current implementation establishes a reusable data analytics pipeline and baseline metrics using the supplied datasets while keeping the architecture ready for further real-estate data integration.

## Objectives

The initial implementation focuses on:

* Building a repeatable Python-based data pipeline
* Cleaning and standardizing the supplied datasets
* Creating derived revenue metrics
* Establishing baseline business metrics
* Preparing SQL queries for analytical reporting
* Maintaining the project using Git and GitHub
* Creating a foundation for subsequent analytical and modelling stages

## Dataset

Three CSV datasets were provided:

### 1. Sales Transactions

`da_sales_transactions.csv`

Contains transaction-level information including:

* Transaction ID
* Date
* Customer ID
* Product ID
* Category
* Units
* Unit Price
* Discount Percentage
* Channel
* City
* Return Flag

### 2. Customer Data

`da_customer_data.csv`

Contains customer-level information including:

* Customer ID
* City
* Age Band
* Gender
* Acquisition Channel
* First Purchase Date
* Total Orders
* Total Revenue
* Last Purchase Date
* Churned

### 3. Product Catalogue

`da_product_catalogue.csv`

Contains product-level information including:

* Product ID
* Product Name
* Category
* MRP
* COGS
* Stock Units
* Average Monthly Sales

## Data Pipeline

The project uses Python to create a repeatable data preparation pipeline.

The pipeline:

1. Loads the raw CSV datasets.
2. Converts date columns into appropriate datetime formats.
3. Converts numerical columns into numeric data types.
4. Removes duplicate records.
5. Calculates gross revenue.
6. Calculates discount amount.
7. Calculates net revenue.
8. Saves cleaned datasets into the processed-data directory.

### Derived Metrics

**Gross Revenue**

```text
Gross Revenue = Units × Unit Price
```

**Discount Amount**

```text
Discount Amount = Gross Revenue × Discount Percentage / 100
```

**Net Revenue**

```text
Net Revenue = Gross Revenue − Discount Amount
```

## Baseline Metrics

The baseline analysis calculates key metrics including:

* Total Revenue
* Total Units Sold
* Number of Transactions
* Average Transaction Value
* Return Rate
* Number of Customers
* Customer Churn Rate
* Number of Products
* Average Stock Units

These metrics provide a starting point for future analysis and allow changes in business performance to be measured consistently.

## SQL Analysis

SQL queries have been prepared for common analytical requirements, including:

* Total revenue
* Total units sold
* Transaction count
* Revenue by city
* Revenue by sales channel
* Revenue by product category
* Return rate
* Customer churn
* Product inventory analysis
* Estimated inventory coverage

SQL file:

```text
project1/sql/baseline_queries.sql
```

## Project Structure

```text
cynaris-internship-sitheshjha/
│
├── .gitignore
├── requirements.txt
│
└── project1/
    │
    ├── API/
    ├── dashboard/
    ├── data/
    │   ├── raw/
    │   └── processed/
    │
    ├── model/
    ├── notebook/
    ├── report/
    ├── sql/
    │   └── baseline_queries.sql
    │
    └── src/
        ├── data_pipeline.py
        └── baseline_metrics.py
```

## How to Run

### 1. Create and activate the virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Run the data pipeline

From the project root:

```powershell
python project1/src/data_pipeline.py
```

This processes the raw datasets and creates cleaned files in:

```text
project1/data/processed/
```

### 4. Calculate baseline metrics

```powershell
python project1/src/baseline_metrics.py
```

The script displays the baseline metrics in the terminal.

## Version Control

Git is used to maintain version control for the project.

The repository contains the analytical code, SQL queries, configuration files, and documentation.

Client-provided raw and processed CSV data is excluded from version control using `.gitignore` to avoid publishing the supplied datasets.

## Current Data Limitation

The supplied datasets represent retail sales, customer, and product information rather than property-level real-estate data.

The current datasets do not contain important real-estate attributes such as:

* Property type
* Built-up area
* Number of bedrooms
* Property price
* Property coordinates
* Location-level property attributes

Therefore, the current dataset is suitable for establishing the data pipeline and baseline analytics but is not sufficient to build a valid real-estate price prediction or fair-value model.

Additional real-estate/property data would be required for the valuation and micro-market modelling stages.

## Next Steps

The planned next stages of the project are:

1. Exploratory Data Analysis
2. Micro-market analysis
3. Real-estate data integration, subject to stakeholder clarification
4. Price trend modelling
5. Fair-value estimation
6. Model evaluation using MAPE
7. Valuation API development using FastAPI
8. Interactive dashboard and map visualization
9. Final documentation and deployment

## Technology Stack

* Python
* Pandas
* NumPy
* SciPy
* Scikit-learn
* Matplotlib
* Seaborn
* SQL
* SQLite/PostgreSQL
* FastAPI
* Streamlit
* Git
* GitHub

### Checkpoint 3 – Deep-Dive Analysis

Customer Segmentation, RFM Analysis & Cohort Analysis

1. Overview

This checkpoint focuses on conducting a deeper analysis of customer behavior using segmentation, RFM analysis, cohort analysis, and customer-level performance analysis.

The analysis was performed using the available sales transaction and customer datasets. The objective was to identify valuable customer groups, understand customer retention patterns, and identify customers that may require retention attention.

2. Objectives

Segment customers based on purchasing behavior.
Identify high-value and at-risk customer groups.
Analyze customer revenue contribution across segments.
Measure customer churn across different segments.
Analyze customer retention using cohort analysis.
Compare customer behavior across cities and sales channels.
Document assumptions and limitations of the analysis.

3. Methodology

The analysis followed these steps:

Loaded the processed sales and customer datasets.
Calculated customer-level purchasing metrics.
Performed RFM-style customer segmentation.
Classified customers into behavioral segments.
Compared revenue and churn across segments.
Created monthly customer cohorts based on first purchase month.
Calculated retention rates for each cohort.
Performed additional city and channel-level analysis.
Generated CSV summaries and visualization outputs.

4. RFM Analysis

RFM analysis was used to evaluate customers using:

Recency – how recently a customer made a purchase.
Frequency – customer purchasing activity.
Monetary – total customer revenue contribution.

Customers were scored and grouped into the following segments:

Champions
Loyal High Value
At Risk High Value
At Risk Low Engagement
Frequent Customers
Potential Customers

5. Customer Segmentation Results

The analysis segmented 200 customers into six groups:

Segment	Customers	Percentage
Frequent Customers	55	27.5%
At Risk High Value	52	26.0%
Loyal High Value	25	12.5%
Champions	23	11.5%
At Risk Low Engagement	23	11.5%
Potential Customers	22	11.0%

The largest customer group was Frequent Customers, representing 27.5% of the customer base. The At Risk High Value group represented 26% of customers and contributed a substantial portion of total revenue.

6. Revenue Analysis by Segment

Approximate revenue contribution by segment:

Segment	Revenue
At Risk High Value	₹2.58M
Frequent Customers	₹1.62M
Loyal High Value	₹1.27M
Champions	₹1.16M
At Risk Low Engagement	₹0.71M
Potential Customers	₹0.67M

The At Risk High Value segment generated the highest revenue contribution. This indicates that customers with high historical value but lower recent engagement represent an important retention area.

7. Churn Analysis

Approximate churn rates by segment were:

Segment	Churn Rate
Potential Customers	4.5%
Champions	4.3%
At Risk High Value	3.8%
Frequent Customers	3.6%
At Risk Low Engagement	0%
Loyal High Value	0%

The results show differences in churn across customer segments. High-value customers should be monitored separately because churn among these customers can have a larger revenue impact.

8. Cohort Analysis

Customers were grouped into cohorts based on their first purchase month.

For each cohort, monthly retention was calculated by tracking whether customers made purchases in subsequent months.

The cohort analysis showed:

Initial cohort retention is 100% because customers are counted in their first purchase month.
Older cohorts show decreasing retention over subsequent months.
Newer cohorts contain fewer observed future months.
Blank cells in the cohort matrix represent periods that have not yet occurred for newer cohorts and should not be interpreted as zero retention.

The cohort heatmap provides a visual representation of customer retention over time.

9. City and Channel Analysis

Customer and sales data were also analyzed by:

City
Acquisition channel
Sales channel

These comparisons provide additional context about where customers are located and how they interact with the business.

The analysis can be used to identify differences in customer value and engagement across geographic and acquisition groups.

10. Key Findings

The customer base contains six distinct behavioral segments.
Frequent Customers form the largest segment with 55 customers.
At Risk High Value customers represent 52 customers and contribute the highest segment-level revenue.
Champions and Loyal High Value customers show relatively low observed churn.
Cohort analysis indicates that retention generally decreases as the time from the first purchase increases.
Customer and channel-level analysis provides additional context for understanding revenue and engagement patterns.
11. Assumptions and Limitations

The supplied datasets are retail/customer/product datasets rather than property-market datasets.
Therefore, this checkpoint focuses on customer and sales analytics rather than real-estate valuation.
The sales transaction dataset contains exactly five transactions per customer, so transaction frequency has limited differentiation between customers.
RFM segmentation should therefore be interpreted mainly through recency and monetary behavior, with customer-level order information used as additional context.
Cohort retention is limited to the available transaction period.
The analysis is based on historical data and does not represent live customer behavior.

12. Output Files

The analysis generated the following outputs:

project1/report/
├── customer_rfm_segmentation.csv
├── segment_summary.csv
├── segment_revenue.png
├── segment_churn.png
├── cohort_retention.csv
├── cohort_retention_heatmap.png
├── city_summary.csv
└── channel_summary.csv
13. Technologies Used

Python
Pandas
NumPy
Matplotlib
Seaborn
Statistical and exploratory analysis techniques
Git and GitHub

14. Conclusion

Checkpoint 3 extends the baseline analysis by providing customer-level segmentation, revenue and churn analysis, and cohort-based retention analysis.

The results provide a deeper understanding of customer behavior and identify high-value and potentially at-risk customer groups. These insights can support future customer retention analysis and business decision-making.

Checkpoint 3 Status: Completed
