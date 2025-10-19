import pandas as pd

df = pd.read_csv('dados/carf_julgamentos_2024.csv')
print(df.head())
print(df.columns)
print(df.dtypes)
print(df.shape)
print(df.info())
print(df.describe())