import json
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

app = QApplication([])  # Создаем приложение

main_window = QWidget()  # Создали окно приложения
main_window.setWindowTitle("Заметки")  # Назвали окно
main_window.resize(1000, 700)  # Задали размер окна

# Создаем все элементы программы, но еще не располагаем их
note_text_field = QTextEdit() # Большое текстовое поле под текст заметки
notes_list = QListWidget()  # Список заметок
tags_list = QListWidget()  # Список тегов

add_note_button = QPushButton("Добавить заметку")
delete_note_button = QPushButton("Удалить заметку")
edit_note_button = QPushButton("Редактировать заметку")

add_tag_button = QPushButton("Добавить тег")
delete_tag_button = QPushButton("Удалить тег")
find_by_tag_button = QPushButton("Искать по тегу")

notes_list_label = QLabel("Список заметок")
tags_list_label = QLabel("Список тегов")

find_by_tag_input = QLineEdit()
find_by_tag_input.setPlaceholderText("Введите тег...")

# Располагаем все элементы по местам
# Главный лейаут, в котором все объединим
main_layout = QHBoxLayout()

# Левая часть программы
left_col = QVBoxLayout()
left_col.addWidget(note_text_field)

# Правая часть программы
right_col = QVBoxLayout()
right_col.addWidget(notes_list_label)
right_col.addWidget(notes_list)

buttons_layout_1 = QHBoxLayout()
buttons_layout_1.addWidget(add_note_button)
buttons_layout_1.addWidget(delete_note_button)
buttons_layout_2 = QHBoxLayout()
buttons_layout_2.addWidget(edit_note_button)

right_col.addLayout(buttons_layout_1)
right_col.addLayout(buttons_layout_2)

right_col.addWidget(tags_list_label)
right_col.addWidget(tags_list)
right_col.addWidget(find_by_tag_input)

buttons_layout_3 = QHBoxLayout()
buttons_layout_3.addWidget(add_tag_button)
buttons_layout_3.addWidget(delete_tag_button)
buttons_layout_4 = QHBoxLayout()
buttons_layout_4.addWidget(find_by_tag_button)

right_col.addLayout(buttons_layout_3)
right_col.addLayout(buttons_layout_4)

# Объединили правую и левую часть программы
main_layout.addLayout(left_col)
main_layout.addLayout(right_col)

# Логика программы
path_to_json = "C:\\Users\\vikto\\Documents\\Projects\\Zametki\\"

notes = {}

for filename in os.listdir(path_to_json): # Получаем все файлы в папке
    if ".json" in filename:
        fname, fext = os.path.splitext(filename) # Отделили название от расширения
        with open(path_to_json + fname + fext, "r", encoding="UTF-8") as file:
            note = json.load(file) # Загрузили файл
            notes[fname] = note[fname] # Скопировали заметку из файла
            
notes_list.addItems(notes) # Загрузили в список в программе заметки

# При нажатии на заметку из списка
def open_note_info():
    # Ключ заметки, к которой обращаемся в Json файле
    key = notes_list.selectedItems()[0].text()
    # Добавляем текст заметки в большое текстовое поле
    note_text_field.setText(notes[key]["текст"])
    # Очищаем старые теги от прошлой заметки (если есть)
    tags_list.clear()
    # Добавляем теги текущей заметки
    tags_list.addItems(notes[key]["теги"])
    
# Функция добавления заметки
def add_note():
    note_name, ok = QInputDialog.getText(main_window, "Добавить заметку", "Название: ")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        notes_list.addItem(note_name)
        tags_list.addItems(notes[note_name]["теги"])
        
# Редактирование заметок
def edit_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        notes[key]["текст"] = note_text_field.toPlainText()
        new_note = { # Создали образец заметки
            key: {
                "текст": notes[key]["текст"],
                "теги": notes[key]["теги"]
            }
        }
        with open(path_to_json + key + ".json", "w", encoding="UTF-8") as file:
            json.dump(new_note, file, sort_keys=True, ensure_ascii=False, indent=4)
    else:
        print("Заметка для редактирования не выбрана!")
        
def delete_note():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        del notes[key]
        tags_list.clear()
        note_text_field.clear()
        notes_list.clear()
        notes_list.addItems(notes)
        os.remove(path_to_json + key + ".json") # Удаление файла с компьютера
    else:
        print("Вы не выбрали заметку для удаления!")
        
def add_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        tag = find_by_tag_input.text()
        if tag != "" and not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            tags_list.addItem(tag)
            find_by_tag_input.clear()
            new_note = {
                key: {
                    "текст": notes[key]["текст"],
                    "теги": notes[key]["теги"]
                }
            }
            with open(path_to_json + key + ".json", "w", encoding="UTF-8") as file:
                json.dump(new_note, file, sort_keys=True, ensure_ascii=False, indent=4)
        else:
            print("Такой тег уже существует у данной заметки!")
    else:
        print("Заметка, которой надо добавить тег не выбрана!")
        
def delete_tag():
    if notes_list.selectedItems():
        key = notes_list.selectedItems()[0].text()
        if tags_list.selectedItems():
            tag = tags_list.selectedItems()[0].text()
            notes[key]["теги"].remove(tag)
            tags_list.clear()
            tags_list.addItems(notes[key]["теги"])
            new_note = {
                key: {
                    "текст": notes[key]["текст"],
                    "теги": notes[key]["теги"]
                }
            }
            with open(path_to_json + key + ".json", "w", encoding="UTF-8") as file:
                json.dump(new_note, file, sort_keys=True, ensure_ascii=False, indent=4)
        else:
            print("Вы не выбрали тег, который хотите удалить!")
    else:
        print("Вы не выбрали заметку, у которой надо удалить тег!")
        
def find_by_tag():
    tag = find_by_tag_input.text()
    if find_by_tag_button.text() == "Искать по тегу" and tag != "":
        find_by_tag_button.setText("Сбросить фильтр")
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note]=notes[note]
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(notes_filtered)
        find_by_tag_input.clear()
    elif find_by_tag_button.text() == "Сбросить фильтр":
        find_by_tag_button.setText("Искать по тегу")
        notes_list.clear()
        tags_list.clear()
        notes_list.addItems(notes)
        find_by_tag_input.clear()
    else:
        pass
        
        
# Когда нажали на одну из заметок в списке
notes_list.itemClicked.connect(open_note_info)
# Нажали на кнопку добавить заметку
add_note_button.clicked.connect(add_note)
# Нажали на кнопку редактировать заметку
edit_note_button.clicked.connect(edit_note)
# Нажали на кнопку удалить заметку
delete_note_button.clicked.connect(delete_note)
# Нажали на кнопку добавить тег
add_tag_button.clicked.connect(add_tag)
# Нажали на кнопку удалить тег
delete_tag_button.clicked.connect(delete_tag)
# Нажали на кнопку искать по тегу
find_by_tag_button.clicked.connect(find_by_tag)

main_window.setLayout(main_layout) # Установили расположение элементов в окне

main_window.show() # Показать главное окно
app.exec_()  # Запускаем приложение
