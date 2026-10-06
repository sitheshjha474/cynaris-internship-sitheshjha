from fastapi import FastAPI
from pydantic import BaseModel
import duckdb
import importlib
import ollama
import re



app = FastAPI()

DB_FILE = r"D:\cynaris-internship\projects\weeks\week6\day1\retail.db"

# --------------------------------------------------
# 5 TRAINING EXAMPLES
# --------------------------------------------------

TRAINING_EXAMPLES = [
    {
        "question": "What is the total sales?",
        "sql": "SELECT SUM(Sales_INR) AS total_sales FROM retail_sales;"
    },
    {
        "question": "Which category has the highest sales?",
        "sql": """
SELECT Category, SUM(Sales_INR) AS total_sales
FROM retail_sales
GROUP BY Category
ORDER BY total_sales DESC
LIMIT 1;
"""
    },
    {
        "question": "Which city has the highest sales?",
        "sql": """
SELECT City, SUM(Sales_INR) AS total_sales
FROM retail_sales
GROUP BY City
ORDER BY total_sales DESC
LIMIT 1;
"""
    },
    {
        "question": "What is the average profit?",
        "sql": """
SELECT AVG(Profit_INR) AS average_profit
FROM retail_sales;
"""
    },
    {
        "question": "Which payment method is used most?",
        "sql": """
SELECT Payment_Method, COUNT(*) AS transactions
FROM retail_sales
GROUP BY Payment_Method
ORDER BY transactions DESC
LIMIT 1;
"""
    }
]

# --------------------------------------------------
# DATABASE SCHEMA
# --------------------------------------------------

SCHEMA = """
Table: retail_sales

Columns:
Order_ID
Order_Date
City
State
Category
Quantity
Unit_Price_INR
Discount
Sales_INR
Profit_INR
Payment_Method
Channel
"""

# --------------------------------------------------
# GENERATE SQL
# --------------------------------------------------

def generate_sql(question):

    examples = ""

    for example in TRAINING_EXAMPLES:
        examples += f"""
Question: {example["question"]}
SQL:
{example["sql"]}
"""

    prompt = f"""
You are a SQL analyst.

Database:
DuckDB

Schema:
{SCHEMA}

Here are example question and SQL pairs:
{examples}

Convert the user's question into valid DuckDB SQL.

User question:
{question}

Rules:
- Use only the retail_sales table.
- Use only columns from the schema.
- Return ONLY SQL.
- Do not use markdown.
- Do not explain the SQL.
"""

    response = ollama.chat(
        model="gemma3:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response["message"]["content"].strip()

    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = sql.replace("```", "").strip()

    return sql


# --------------------------------------------------
# EXECUTE SQL
# --------------------------------------------------

def run_sql(sql):

    con = duckdb.connect(DB_FILE)

    result = con.execute(sql).fetchdf()

    con.close()

    return result


# --------------------------------------------------
# API REQUEST
# --------------------------------------------------

class QueryRequest(BaseModel):
    question: str


# --------------------------------------------------
# ENDPOINT
# --------------------------------------------------

@app.post("/cia/sql-analyst")
def sql_analyst(request: QueryRequest):

    try:

        sql = generate_sql(request.question)

        result = run_sql(sql)

        return {
            "question": request.question,
            "sql": sql,
            "result": result.to_dict(orient="records")
        }

    except Exception as e:

        return {
            "question": request.question,
            "error": str(e)
        }


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "CIA SQL Analyst is running"
    }