txt_file = "first.txt"

with open(txt_file, "r", encoding="utf-8") as file:  # відкрити файл
    data = file.read()  # read() - прочитати файл та отримати зміст
    print(data)

author = input("Введіть автора цитати:")
with open(txt_file, "a", encoding="utf-8") as file:
    file.write("\n(" + author + ")")  # команда запису в файл


while True:  # цикл, який працює доки не відповіли "ні"
    # запросили відповідь маленькими літерами
    ans = input("Чи хочете ви додати нову цитати? (так/ні)").lower()
    if ans == "так":  # умова перевірки відповіді
        quote = input("Введіть цитату:")
        author = input("Введіть автора вашої цитати:")
        with open(txt_file, "a", encoding="utf-8") as file:  # відкрили файл для дозапису
            file.write("\n\n" + quote + "\n(" + author + ")")
    elif ans == "ні":
        break  # зупинити цикл у разі відповіді "ні"
    else:
        print("Такої відповіді нема!")

with open(txt_file, "r", encoding="utf-8") as file:  # відкрити файл
    data = file.read()  # read() - прочитати файл та отримати зміст
    print(data)
