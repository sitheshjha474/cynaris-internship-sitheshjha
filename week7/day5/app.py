import uuid
import numbers

import pandas as pd
import pandasai as pai
import plotly.express as px

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pandasai_litellm.litellm import LiteLLM


app = FastAPI(title="CIA CSV Analyst")

# Temporary uploaded CSV storage
dataframes = {}


# --------------------------------------------------
# FRONTEND
# --------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


# --------------------------------------------------
# VALUE FORMATTER
# --------------------------------------------------

def format_value(value):

    if value is None:
        return "No result found."

    if isinstance(value, numbers.Number):

        if pd.isna(value):
            return "No result found."

        if float(value).is_integer():
            return f"{int(value):,}"

        return f"{float(value):,.2f}"

    return str(value)


# --------------------------------------------------
# CSV UPLOAD
# --------------------------------------------------

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    try:

        if not file.filename.lower().endswith(".csv"):
            return {
                "success": False,
                "error": "Please upload a CSV file."
            }

        df = pd.read_csv(file.file)

        session_id = str(uuid.uuid4())

        dataframes[session_id] = df

        return {
            "success": True,
            "session_id": session_id,
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns)
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# --------------------------------------------------
# CIA QUERY
# --------------------------------------------------

@app.post("/cia/sql-analyst")
async def cia_query(
    session_id: str = Form(...),
    question: str = Form(...)
):

    try:

        if session_id not in dataframes:
            return {
                "success": False,
                "error": "Session not found. Please upload the CSV again."
            }

        df = dataframes[session_id]

        # ------------------------------------------
        # Ollama + LiteLLM
        # ------------------------------------------

        llm = LiteLLM(
            model="ollama/gemma3:latest",
            api_base="http://localhost:11434"
        )

        # Register LLM with PandasAI
        pai.config.set({
            "llm": llm
        })

        # Convert Pandas DataFrame to PandasAI DataFrame
        pandasai_df = pai.DataFrame(df)

        # Ask PandasAI
        result = pandasai_df.chat(question)

        # ------------------------------------------
        # CLEAN ANSWER
        # ------------------------------------------

        if isinstance(result, pd.DataFrame):

            if result.shape[0] == 1 and result.shape[1] == 1:

                value = result.iloc[0, 0]

                answer = format_value(value)

            else:

                answer = result.to_string(index=False)

        elif isinstance(result, pd.Series):

            if len(result) == 1:

                answer = format_value(result.iloc[0])

            else:

                answer = result.to_string()

        else:

            answer = format_value(result)

        # ------------------------------------------
        # CREATE CHART
        # ------------------------------------------

        chart = create_chart(df, question)

        return {
            "success": True,
            "question": question,
            "answer": answer,
            "chart": chart
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# --------------------------------------------------
# CREATE PLOTLY JSON
# --------------------------------------------------

def create_chart(df, question):

    q = question.lower()

    category_col = find_column(
        df,
        ["category", "product_category"]
    )

    city_col = find_column(
        df,
        ["city"]
    )

    sales_col = find_column(
        df,
        [
            "sales",
            "sale",
            "amount",
            "revenue",
            "booking_value",
            "sales_inr"
        ]
    )

    payment_col = find_column(
        df,
        [
            "payment_method",
            "payment method",
            "payment"
        ]
    )

    # ------------------------------------------
    # CATEGORY SALES
    # ------------------------------------------

    if "category" in q and "sales" in q:

        if category_col and sales_col:

            chart_df = (
                df.groupby(category_col)[sales_col]
                .sum()
                .reset_index()
                .sort_values(
                    sales_col,
                    ascending=False
                )
            )

            fig = px.bar(
                chart_df,
                x=category_col,
                y=sales_col,
                title="Sales by Category"
            )

            return fig.to_json()

    # ------------------------------------------
    # CITY SALES
    # ------------------------------------------

    if "city" in q and "sales" in q:

        if city_col and sales_col:

            chart_df = (
                df.groupby(city_col)[sales_col]
                .sum()
                .reset_index()
                .sort_values(
                    sales_col,
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                chart_df,
                x=city_col,
                y=sales_col,
                title="Top Cities by Sales"
            )

            return fig.to_json()

    # ------------------------------------------
    # PAYMENT METHOD
    # ------------------------------------------

    if "payment" in q:

        if payment_col:

            chart_df = (
                df[payment_col]
                .value_counts()
                .reset_index()
            )

            chart_df.columns = [
                payment_col,
                "count"
            ]

            fig = px.bar(
                chart_df,
                x=payment_col,
                y="count",
                title="Payment Method Usage"
            )

            return fig.to_json()

    return None


# --------------------------------------------------
# FIND COLUMN
# --------------------------------------------------

def find_column(df, possible_names):

    normalized = {
        str(column)
        .lower()
        .replace("_", " ")
        .strip(): column
        for column in df.columns
    }

    for name in possible_names:

        name = (
            name
            .lower()
            .replace("_", " ")
            .strip()
        )

        if name in normalized:
            return normalized[name]

    return None