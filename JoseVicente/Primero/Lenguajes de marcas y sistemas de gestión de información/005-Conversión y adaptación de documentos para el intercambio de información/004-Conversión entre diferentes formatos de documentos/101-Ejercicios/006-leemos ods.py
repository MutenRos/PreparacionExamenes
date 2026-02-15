import pandas as pd

df = pd.read_excel("empresa.ods", engine="odf")
print(df.head())
