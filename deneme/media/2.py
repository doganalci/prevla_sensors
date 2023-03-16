import pandas as pd

df = pd.read_csv("burak.csv",header=0,sep=',')

print(df)

df = df[df.columns[df.columns.str.startswith('x_point')]]
print(df)