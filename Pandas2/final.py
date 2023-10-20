import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./datasets/Space_Corrected.csv')

# TODO Дослідження популярності додатків різних категорій
# ! 1. Яку частину ринку займають бізнес додатки?
# ? Бізнес додатки мають невисоку популярність
# ? Кількість завантажень бізнес додатків менша ніж у ігор в середньому
# ? Більшість бізнес додатків мають невисокий рейтинг в середньому

df.info()

all_missions = df["Status Mission"].value_counts().sum()
spacex_missions = df[df["Company Name"] ==
                     "SpaceX"]["Status Mission"].value_counts().sum()

dt_custom = pd.Series(
    data=[spacex_missions, all_missions - spacex_missions], index=["SpaceX", "Other"])

dt_custom.plot(kind="barh", grid=True)

plt.show()

dt_custom.plot(kind="pie")

plt.show()

print(all_missions)
