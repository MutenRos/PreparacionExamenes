import pandas as pd

df = pd.read_excel("empresa.xlsx", engine="openpyxl")
print(df.head())
