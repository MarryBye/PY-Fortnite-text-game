from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import json

app = QApplication([])  # віджет "додаток", сама програма

main_window = QWidget()  # віджет "вікно", головне вікно нашої програми
main_window.setWindowTitle("Розумні замітки")  # встановили назву вікна
main_window.resize(900, 600)  # встановили розмір вікна

# ВІДЖЕТИ

list_notes = QListWidget()  # список заміток (права колонка)
list_notes_label = QLabel("Список заміток")  # створення текст

button_note_create = QPushButton("Створити замітку")  # створити кнопку
button_note_del = QPushButton("Видалити замітку")
button_note_save = QPushButton("Зберегти замітку")

field_tag = QLineEdit("")  # поле для введення (1 рядок)
field_tag.setPlaceholderText("Введіть тег...")  # заглушка для поля введеня

field_text = QTextEdit()  # поле для введення (багато рядків)

button_tag_add = QPushButton("Додати тег")
button_tag_del = QPushButton("Видалити тег")
button_tag_search = QPushButton("Шукати за тегами")

tag_list = QListWidget()
tag_list_label = QLabel("Список тегів")


# ============================================

# ЛЕЙАУТИ

main_layout = QHBoxLayout()  # горизонтальна лінія
column_left = QVBoxLayout()  # вертикальна лінія (ліва колонка)
column_right = QVBoxLayout()  # вертикальна лінія (права колонка)

column_left.addWidget(field_text)  # додали в ліву колонку наш QTextEdit

column_right.addWidget(list_notes_label)
column_right.addWidget(list_notes)

buttons_row_1 = QHBoxLayout()
buttons_row_1.addWidget(button_note_create)
buttons_row_1.addWidget(button_note_del)

column_right.addWidget(button_note_save)
column_right.addLayout(buttons_row_1)
column_right.addWidget(tag_list_label)
column_right.addWidget(tag_list)
column_right.addWidget(field_tag)

buttons_row_2 = QHBoxLayout()
buttons_row_2.addWidget(button_tag_add)
buttons_row_2.addWidget(button_tag_del)

column_right.addWidget(button_tag_search)
column_right.addLayout(buttons_row_2)

main_layout.addLayout(column_left, stretch=2)
main_layout.addLayout(column_right, stretch=1)

# ============================================

# ФУНКЦІОНАЛ

notes_copy = {}


def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes_copy[key]["текст"])
    tag_list.clear()
    tag_list.addItems(notes_copy[key]["теги"])


def add_note():
    note_name, ok = QInputDialog.getText(
        main_window, "Додати замітку", "Назва замітки: ")
    if ok and note_name != "":
        notes_copy[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        tag_list.addItems(notes_copy[note_name]["теги"])


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes_copy[key]["текст"] = field_text.toPlainText()

        with open("./notes.json", "w") as file:
            json.dump(notes_copy, file, sort_keys=True,
                      ensure_ascii=False, indent=4)


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes_copy[key]
        list_notes.clear()
        tag_list.clear()
        field_text.clear()
        list_notes.addItems(notes_copy)

        with open("./notes.json", "w") as file:
            json.dump(notes_copy, file, sort_keys=True,
                      ensure_ascii=False, indent=4)


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag != "":
            if not tag in notes_copy[key]["теги"]:
                notes_copy[key]["теги"].append(tag)
                tag_list.addItem(tag)
                field_tag.clear()

                with open("./notes.json", "w") as file:
                    json.dump(notes_copy, file, sort_keys=True,
                              ensure_ascii=False, indent=4)


def del_tag():
    if list_notes.selectedItems():
        if tag_list.selectedItems():
            key = list_notes.selectedItems()[0].text()
            tag = tag_list.selectedItems()[0].text()

            notes_copy[key]["теги"].remove(tag)
            tag_list.clear()
            tag_list.addItems(notes_copy[key]["теги"])

            with open("./notes.json", "w") as file:
                json.dump(notes_copy, file, sort_keys=True,
                          ensure_ascii=False, indent=4)


def find_by_tag():
    tag = field_tag.text()
    if tag != "":
        if button_tag_search.text() == "Шукати за тегами":
            notes_filter = {}
            for note in notes_copy:
                if tag in notes_copy[note]["теги"]:
                    notes_filter[note] = notes_copy[note]
            button_tag_search.setText("Скинути пошук")
            list_notes.clear()
            tag_list.clear()
            list_notes.addItems(notes_filter)
        elif button_tag_search.text() == "Скинути пошук":
            field_tag.clear()
            list_notes.clear()
            tag_list.clear()
            list_notes.addItems(notes_copy)
            button_tag_search.setText("Шукати за тегами")
        else:
            pass


list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(find_by_tag)

# json.load() - завантажує все що написано в файлі
# json.dump() - зберегає щось до файлу
# r - читання, w - запис, a - додати


with open("./notes.json", "r") as file:
    notes_copy = json.load(file)

# addItem, addItems
list_notes.addItems(notes_copy)

# ============================================

# головне вікно буде мати ось таке розташування елементів
main_window.setLayout(main_layout)

main_window.show()  # показати віджет "вікно"
app.exec()  # запуск додатку
