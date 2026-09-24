# Week 5 - PandasAI Practical Task

## Project Overview

This task demonstrates the use of PandasAI for natural-language
analysis of an Indian retail sales dataset.

The project uses:

- Python
- Pandas
- PandasAI
- LiteLLM
- Ollama
- Gemma 3

Ollama and Gemma 3 are used locally, so an OpenAI API key is not
required.

---

## Task 1 - PandasAI Analysis

The Indian retail sales CSV dataset was loaded into PandasAI.

The following 10 natural-language questions were tested:

1. What is the total sales in INR?
2. What is the average sales per order?
3. Which category has the highest total sales?
4. Which city has the highest total sales?
5. What is the total quantity sold?
6. Which payment method is used most often?
7. What is the average profit per order?
8. Which category has the lowest total sales?
9. Show the top 5 cities by total sales.
10. What percentage of total sales comes from the Online channel?

The analysis was performed using the locally installed Ollama
`gemma3:latest` model.

Main file:

`pd_ai.py`

---

## Task 2 - PandasAI vs Manual Pandas

PandasAI and Manual Pandas were compared using the same three
business questions:

1. Total sales in INR
2. Category with the highest total sales
3. City with the highest total sales

Manual Pandas was treated as the reference result.

Main file:

`pandasai_vs_manual.py`

Evidence file:

`comparison_output.txt`

Run the comparison using:

```powershell
python pandasai_vs_manual.py