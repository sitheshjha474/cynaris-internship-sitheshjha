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

## Project Status

**Checkpoint 2 — Data Pipeline + Baseline Metrics**

The repeatable data pipeline, baseline metric calculations, SQL analysis queries, and Git-based version control have been established.
