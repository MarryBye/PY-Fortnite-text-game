import pandas as pd

df = pd.read_csv('GoogleApps.csv')

# 1 кружок

# .value_count() - порахувати кількість значень в стовпці

# Скільки всього програм з категорією 'BUSINESS'? 246
print(df["Category"].value_counts())
# print((df['Category'] == 'BUSINESS').sum())

# Чому рівне співвідношення кількості додатків для підлітків ('Teen') і для дітей старше 10 ('Everyone 10+')?
# 2.73
apps_count = df["Content Rating"].value_counts()
print(round(apps_count["Teen"] / apps_count["Everyone 10+"], 2))

# 1. Чому дорівнює середній рейтинг платних програм? 4.25
# 2. На скільки середній рейтинг безкоштовних додатків менший за середній рейтинг платних? 0.08

paid_rating = round(df[df["Type"] == "Paid"]["Rating"].mean(), 2)
free_rating = round(df[df["Type"] == "Free"]["Rating"].mean(), 2)

print(paid_rating - free_rating)

# Чому дорівнює мінімальний та максимальний розмір додатків у категорії 'COMICS'? 0.43, 40.0

max_size = df[df["Category"] == "COMICS"]["Size"].max()
min_size = df[df["Category"] == "COMICS"]["Size"].min()

print(max_size, min_size)

# 2 кружок

# .groupby - згрупувати дані в якомусь стовпці

# Чому дорівнює мінімальний, середній та максимальний рейтинг ('Rating') платних та безкоштовних додатків ('Type')?

temp = df.groupby(by="Type")["Rating"].agg(["max", "mean", "min"])
print(temp)

# Групування за мінімальною, медіанною (median) та максимальною ціною ('Price') платних додатків (Type == 'Paid') для різних цільових аудиторій ('Content Rating').
temp = df[df["Type"] == "Paid"].groupby(by="Content Rating")[
    "Price"].agg(["min", "median", "max"])
print(temp)

# .pivot_table() - команда для зведення таблиці

# 1. У якій віковій групі найбільше відгуків отримала програма з категорії 'EDUCATION'? Everyone
# 2. У якій віковій групі найбільше відгуків отримала програма з категорії 'FAMILY'? Everyone 10+
# 3. У якій віковій групі найбільше відгуків отримала програма з категорії 'GAME'? Everyone 10+

temp = df.pivot_table(columns="Content Rating",
                      index="Category", values="Reviews", aggfunc="max")
print(temp)
