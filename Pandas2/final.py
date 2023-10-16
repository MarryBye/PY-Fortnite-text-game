import pandas as pd

df = pd.read_csv('./datasets/Space_Corrected.csv')

df.info()


def split_date(date):
    return date.split(" ")[3]


df["Year"] = df["Datum"].apply(split_date)

print(df["Year"])
