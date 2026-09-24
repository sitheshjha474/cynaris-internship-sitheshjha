import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

# -------------------------------------------------
# 1. Configure local Ollama + Gemma 3
# -------------------------------------------------

llm = LiteLLM(
    model="ollama/gemma3:latest",
    api_base="http://localhost:11434"
)

pai.config.set({
    "llm": llm
})

# -------------------------------------------------
# 2. Load Indian  dataset
# -------------------------------------------------

df = pai.read_csv("indian-dataset.csv")

print("=" * 70)
print("PANDASAI - INDIAN data SALES ANALYSIS")
print("=" * 70)

# -------------------------------------------------
# 3. Natural-language queries
# -------------------------------------------------

queries = [
    "What is the total sales in INR?",
    "What is the average sales per order?",
    "Which category has the highest total sales?",
    "Which city has the highest total sales?",
    "What is the total quantity sold?",
    "Which payment method is used most often?",
    "What is the average profit per order?",
    "Which category has the lowest total sales?",
    "Show the top 5 cities by total sales.",
    "What percentage of total sales comes from the Online channel?"
]

# -------------------------------------------------
# 4. Run all 10 queries
# -------------------------------------------------

for i, query in enumerate(queries, 1):

    print(f"\n{'-' * 70}")
    print(f"QUERY {i}")
    print(f"{'-' * 70}")
    print("Question:", query)

    try:
        result = df.chat(query)

        print("Result:", result)

    except Exception as e:

        print("Query failed.")
        print("Error:", e)

print("\n" + "=" * 70)
print("ANALYSIS COMPLETED")
print("=" * 70)