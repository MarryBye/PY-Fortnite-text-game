import pandas as pd

df = pd.read_csv('./datasets/GooglePlayStore_wild.csv')

# pd.isnull() - чи є нульовим

# 2

# temp = df[pd.isnull(df["Rating"])]
# print(len(temp))

# 3

# print(len(df[df["Size"] == "Varies with device"]))

# str[початок:кінець:шаг]


# def make_size(size):
#     if size[len(size) - 1] == "K":
#         return float(size[0:len(size) - 1])
#     elif size[len(size) - 1] == "M":
#         return float(size[0:len(size) - 1])
#     else:
#         return 0


# df["Size"] = df["Size"].apply(make_size)

# print(df[df["Category"] == "TOOLS"]["Size"].max())

# # temp = df[df["Category"] == "TOOLS"]["Size"].max()
# # print(temp)


# 2 кружок
# "$4.99"
# "10,000+"

# def make_price(price):
#     if price[0] == "$":
#         return float(price[1:])
#     return 0


# def make_installs(installs):
#     if installs == "0":
#         return 0
#     return int(installs[:-1].replace(",", ""))


# df["Installs"] = df["Installs"].apply(make_installs)
# df["Price"] = df["Price"].apply(make_price)

# df["Profit"] = df["Installs"] * df["Price"]

# print(df[df["Type"] == "Paid"]["Profit"].max())

# Яка максимальна кількість жанрів (Number of genres) для одного додатка є в датасеті?

def genres_to_list(genres_str):
    return genres_str.split(";")  # "1;2;3;4;5" -> ["1", "2", "3", "4", "5"]


df["Genres"] = df["Genres"].apply(genres_to_list)
df["Number of genres"] = df["Genres"].apply(len)

print(df["Number of genres"])
