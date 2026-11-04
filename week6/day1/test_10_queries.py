import requests

url = "http://127.0.0.1:8000/cia/sql-analyst"

questions = [
    "What is the total sales?",
    "Which category has the highest sales?",
    "Which city has the highest sales?",
    "What is the average profit?",
    "Which payment method is used most?",
    "What is the total quantity sold?",
    "Which state has the highest sales?",
    "What is the total profit?",
    "Which channel has the highest sales?",
    "What is the average sales per order?"
]

for i, question in enumerate(questions, 1):

    print("\n" + "=" * 70)
    print(f"QUERY {i}: {question}")
    print("=" * 70)

    try:
        response = requests.post(
            url,
            json={"question": question}
        )

        print(response.json())

    except Exception as e:
        print("ERROR:", e)


## test outputs
##10-query verification summary
#	Question	Result
# 1	Total sales	₹457,117,635.60
# 2	Highest-sales category	Electronics — ₹195,527,550.00
# 3	Highest-sales city	Mumbai — ₹48,138,252.00
# 4	Average profit	₹1,204.62
# 5	Most-used payment method	UPI — 42,920 transactions
# 6	Total quantity sold	307,040
# 7	Highest-sales state	Maharashtra — ₹95,600,570.80
# 8	Total profit	₹120,461,597.80
# 9	Highest-sales channel	Online — ₹263,345,386.00
# 10	Average sales per order	₹4,571.18#