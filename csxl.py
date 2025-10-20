import pandas as pd
df = pd.read_csv("ap.csv")
df.to_excel("ap.xlsx", index=False)