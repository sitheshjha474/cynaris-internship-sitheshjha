# Full Demo Script — AI Data Analyst Platform

Suggested duration: 7–10 minutes.

## 1. Introduction
Introduce the project as a platform that allows users to explore CSV datasets, generate visualizations, and ask analytical questions through a simple interface.

## 2. Launch the Application
Open VS Code, activate the virtual environment, and run:

`streamlit run app.py`

Show the application in the browser.

## 3. Upload Dataset
Upload a sample CSV file.

Explain that the application reads the file into a Pandas DataFrame.

## 4. Dataset Overview
Show:
- Total rows
- Total columns
- Missing values
- Duplicate rows
- Dataset preview

## 5. Automated Data Analysis
Show column data types, unique values, missing-value counts, and statistical summaries.

## 6. Visualizations
Demonstrate:
- Histogram
- Bar chart
- Line chart
- Box plot
- Correlation heatmap, when at least two numeric columns exist

## 7. Ask the Data Analyst
Try questions such as:
- How many rows are in the dataset?
- What is the average sales?
- What is the maximum sales?
- Show total sales by region.

Explain that the built-in engine handles supported analytical questions using Pandas.

## 8. Optional AI Integration
If Ollama is installed and running, enable the local AI option and demonstrate a question.

If it is unavailable, explain that the built-in analysis engine works independently.

## 9. Automated Insights and Export
Show the generated numeric insights and download the CSV file.

## 10. Conclusion
Summarize the platform's capabilities and mention future improvements such as advanced natural-language analysis, authentication, database connectivity, and cloud deployment.