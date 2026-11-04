import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import re

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="AI Data Analyst Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyst Platform")
st.write(
    "Upload a CSV file, explore your data, generate insights, "
    "and ask questions about your dataset."
)

# ---------------- SESSION STATE ----------------
if "df" not in st.session_state:
    st.session_state.df = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:
    if uploaded_file.name != st.session_state.file_name:
        try:
            new_df = pd.read_csv(uploaded_file)
            st.session_state.df = new_df
            st.session_state.file_name = uploaded_file.name
        except Exception as error:
            st.error(f"Could not read CSV: {error}")
            st.stop()

df = st.session_state.df

if df is None:
    st.info("👈 Upload a CSV file from the sidebar to begin.")
    st.stop()

if df.empty:
    st.error("The uploaded dataset is empty.")
    st.stop()

# ---------------- DATA OVERVIEW ----------------
st.header("1. Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Rows", f"{df.shape[0]:,}")
c2.metric("Total Columns", df.shape[1])
c3.metric("Missing Values", f"{df.isna().sum().sum():,}")
c4.metric("Duplicate Rows", f"{df.duplicated().sum():,}")

with st.expander("Preview Uploaded Data", expanded=True):
    st.dataframe(df.head(20), use_container_width=True)

# ---------------- DATA PROFILE ----------------
st.header("2. Automated Data Analysis")

left, right = st.columns(2)

with left:
    st.subheader("Column Information")

    profile = pd.DataFrame({
        "Column": df.columns.astype(str),
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isna().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(profile, use_container_width=True)

with right:
    st.subheader("Statistical Summary")

    st.dataframe(
        df.describe(include="all").T,
        use_container_width=True
    )

# ---------------- DATA QUALITY ----------------
st.subheader("Data Quality Checks")

quality = pd.DataFrame({
    "Check": ["Missing Values", "Duplicate Rows"],
    "Count": [
        int(df.isna().sum().sum()),
        int(df.duplicated().sum())
    ]
})

st.dataframe(quality, use_container_width=True)

# ---------------- COLUMN TYPES ----------------
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

categorical_cols = df.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

# ---------------- VISUALIZATION ----------------
st.header("3. Interactive Data Visualization")

if numeric_cols:

    chart_type = st.selectbox(
        "Choose Chart Type",
        ["Histogram", "Bar Chart", "Line Chart", "Box Plot"]
    )

    selected_column = st.selectbox(
        "Select Numeric Column",
        numeric_cols
    )

    fig = None

    if chart_type == "Histogram":

        fig = px.histogram(
            df,
            x=selected_column,
            title=f"Distribution of {selected_column}"
        )

    elif chart_type == "Bar Chart":

        if categorical_cols:

            category = st.selectbox(
                "Choose Category",
                categorical_cols
            )

            chart_data = (
                df.groupby(category, dropna=False)[selected_column]
                .sum()
                .reset_index()
            )

            chart_data[category] = chart_data[category].astype(str)

            fig = px.bar(
                chart_data,
                x=category,
                y=selected_column,
                title=f"{selected_column} by {category}"
            )

        else:
            st.warning("No categorical columns available.")

    elif chart_type == "Line Chart":

        fig = px.line(
            df,
            y=selected_column,
            title=f"{selected_column} Trend"
        )

    elif chart_type == "Box Plot":

        fig = px.box(
            df,
            y=selected_column,
            title=f"{selected_column} Box Plot"
        )

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No numeric columns found.")

# ---------------- CORRELATION ----------------
if len(numeric_cols) >= 2:

    st.subheader("Correlation Analysis")

    correlation = df[numeric_cols].corr()

    fig = px.imshow(
        correlation,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap",
        color_continuous_scale="RdBu_r"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- RULE-BASED ANALYST ----------------
def answer_question(data, question):

    q = question.lower().strip()

    numeric = data.select_dtypes(include=np.number).columns.tolist()

    categorical = data.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    # Identify mentioned column
    mentioned_column = None

    for column in data.columns:
        if str(column).lower() in q:
            mentioned_column = column
            break

    # Row count
    if any(word in q for word in [
        "how many rows", "number of rows", "row count"
    ]):
        return f"Total rows: {len(data):,}"

    # Column count
    if any(word in q for word in [
        "how many columns", "number of columns", "column count"
    ]):
        return f"Total columns: {len(data.columns)}"

    # Missing values
    if "missing" in q or "null" in q:

        missing = data.isna().sum()
        missing = missing[missing > 0]

        if missing.empty:
            return "There are no missing values."

        return "Missing values by column:\n" + missing.to_string()

    # Duplicate rows
    if "duplicate" in q:
        return f"Duplicate rows: {data.duplicated().sum():,}"

    # Numeric column analysis
    if mentioned_column in numeric:

        series = data[mentioned_column].dropna()

        if series.empty:
            return f"No valid numeric values in {mentioned_column}."

        if any(word in q for word in ["average", "mean"]):
            return f"Average {mentioned_column}: {series.mean():,.2f}"

        if any(word in q for word in ["total", "sum"]):
            return f"Total {mentioned_column}: {series.sum():,.2f}"

        if any(word in q for word in [
            "maximum", "highest", "largest", "max"
        ]):
            return f"Maximum {mentioned_column}: {series.max():,.2f}"

        if any(word in q for word in [
            "minimum", "lowest", "smallest", "min"
        ]):
            return f"Minimum {mentioned_column}: {series.min():,.2f}"

        if "median" in q:
            return f"Median {mentioned_column}: {series.median():,.2f}"

        if "standard deviation" in q or "std" in q:
            return f"Standard deviation of {mentioned_column}: {series.std():,.2f}"

    # Grouped analysis
    if mentioned_column in numeric and " by " in q:

        group_column = None

        for column in categorical:
            if str(column).lower() in q:
                group_column = column
                break

        if group_column is not None:

            result = (
                data.groupby(group_column, dropna=False)[mentioned_column]
                .sum()
                .sort_values(ascending=False)
            )

            return (
                f"Total {mentioned_column} by {group_column}:\n"
                f"{result.to_string()}"
            )

    # Categorical column analysis
    if mentioned_column in categorical:

        return (
            f"Unique values in {mentioned_column}: "
            f"{data[mentioned_column].nunique()}\n\n"
            f"Most common values:\n"
            f"{data[mentioned_column].value_counts().head(5).to_string()}"
        )

    return (
        "I could not understand the question.\n\n"
        "Try questions like:\n"
        "- What is the average sales?\n"
        "- What is the total profit?\n"
        "- What is the maximum sales?\n"
        "- How many rows are there?\n"
        "- Are there missing values?\n"
        "- Show total sales by region."
    )

# ---------------- OPTIONAL OLLAMA ----------------
def ask_ollama(data, question, model):

    context = data.head(10).to_string()

    prompt = f"""
You are a data analyst.

Dataset shape: {data.shape}
Columns: {list(data.columns)}

Sample data:
{context}

Question: {question}

Answer using only the supplied information.
Do not invent numerical results.
If the sample is insufficient, explain that.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=90
    )

    response.raise_for_status()

    return response.json().get("response", "No response returned.")

# ---------------- QUESTION ANSWERING ----------------
st.header("4. Ask Your Data Analyst")

question = st.text_input(
    "Ask a question about your dataset",
    placeholder="Example: What is the average sales?"
)

use_ollama = st.checkbox(
    "Use local Ollama AI if available",
    value=False
)

if use_ollama:
    model = st.text_input(
        "Ollama Model",
        value="gemma3:latest"
    )
else:
    model = None

if st.button("Analyze Question"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Analyzing your data..."):

            if use_ollama:

                try:
                    result = ask_ollama(df, question, model)
                    st.success("Ollama AI Response")

                except Exception as error:

                    st.warning(
                        f"Ollama unavailable. Using built-in analysis. "
                        f"Details: {error}"
                    )

                    result = answer_question(df, question)

            else:

                result = answer_question(df, question)

        st.subheader("Analyst Response")
        st.write(result)

# ---------------- AUTOMATED INSIGHTS ----------------
st.header("5. Automated Insights")

st.write(
    f"- Dataset contains **{len(df):,} rows** "
    f"and **{len(df.columns)} columns**."
)

st.write(
    f"- Missing values: **{df.isna().sum().sum():,}**."
)

st.write(
    f"- Duplicate rows: **{df.duplicated().sum():,}**."
)

if numeric_cols:

    for column in numeric_cols[:5]:

        series = df[column].dropna()

        if not series.empty:

            st.write(
                f"- **{column}**: Average = {series.mean():,.2f}, "
                f"Minimum = {series.min():,.2f}, "
                f"Maximum = {series.max():,.2f}."
            )

# ---------------- DOWNLOAD ----------------
st.header("6. Export")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Analyzed Dataset",
    data=csv_data,
    file_name="analyzed_dataset.csv",
    mime="text/csv"
)

st.success("Your dataset analysis is complete!")

st.caption(
    "Built-in answers use Pandas calculations. "
    "Ollama uses only a sample of the dataset, so verify important results."
)