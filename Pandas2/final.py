import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./datasets/StudentsPerformance.csv')


male_math_mark = df[df["gender"] == "male"]["math score"].mean()
female_math_mark = df[df["gender"] == "female"]["math score"].mean()

# bar / barh
# pie

custom_series = pd.Series(data=[male_math_mark, female_math_mark], index=["Male", "Female"])

custom_series.plot(kind="pie", grid=True)

plt.show()