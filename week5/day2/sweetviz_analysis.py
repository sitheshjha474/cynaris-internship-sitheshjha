import pandas as pd
import sweetviz as sv

df = pd.read_csv("indian-dataset.csv")

report = sv.analyze(df)

report.show_html(
    "SweetViz_Report.html",
    open_browser=False
)

print("SweetViz report generated successfully.")