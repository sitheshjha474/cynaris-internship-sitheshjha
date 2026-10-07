import pandas as pd
from autoviz import AutoViz_Class

df = pd.read_csv("indian-dataset.csv")

AV = AutoViz_Class()

AV.AutoViz(
    filename="",
    dfte=df,
    depVar="Sales_INR",
    verbose=2,
    chart_format="html"
)

print("AutoViz report generated successfully.")