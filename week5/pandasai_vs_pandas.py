import pandas as pd
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

# Ollama + Gemma 3
llm = LiteLLM(
    model="ollama/gemma3:latest",
    api_base="http://localhost:11434"
)

pai.config.set({
    "llm": llm
})

# Load dataset
df = pai.read_csv("indian-dataset.csv")

print("=" * 70)
print("PANDASAI VS MANUAL PANDAS")
print("=" * 70)

questions = [
    "What is the total sales in INR?",
    "Which category has the highest total sales?",
    "Which city has the highest total sales?"
]

# PandasAI
print("\n--- PANDASAI RESULTS ---")

for i, question in enumerate(questions, 1):
    try:
        result = df.chat(question)

        print(f"\nQ{i}: {question}")
        print("PandasAI:", result)

    except Exception as e:
        print(f"\nQ{i} failed:", e)


# Manual Pandas
# Convert PandasAI dataframe to normal Pandas dataframe
normal_df = df.dataframe

print("\n--- MANUAL PANDAS RESULTS ---")

result1 = normal_df["Sales_INR"].sum()

result2 = (
    normal_df.groupby("Category")["Sales_INR"]
    .sum()
    .idxmax()
)

result3 = (
    normal_df.groupby("City")["Sales_INR"]
    .sum()
    .idxmax()
)

print("\nQ1: Total sales")
print("Manual Pandas:", result1)

print("\nQ2: Highest-sales category")
print("Manual Pandas:", result2)

print("\nQ3: Highest-sales city")
print("Manual Pandas:", result3)

print("\n" + "=" * 70)
print("COMPARISON COMPLETED")
print("=" * 70)