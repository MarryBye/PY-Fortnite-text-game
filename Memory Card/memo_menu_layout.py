from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Правая часть меню
txt_Question = QLineEdit("")
txt_Answer = QLineEdit("")
txt_Wrong1 = QLineEdit("")
txt_Wrong2 = QLineEdit("")
txt_Wrong3 = QLineEdit("")

layout_edit = QFormLayout()
layout_edit.addRow("Вопрос:", txt_Question)
layout_edit.addRow("Правильный ответ:", txt_Answer)
layout_edit.addRow("Неправильный ответ №1", txt_Wrong1)
layout_edit.addRow("Неправильный ответ №2", txt_Wrong2)
layout_edit.addRow("Неправильный ответ №3", txt_Wrong3)

# Левая часть меню
list_question = QListView()
wdgt_edit = QWidget()
wdgt_edit.setLayout(layout_edit)

# Кнопки
btn_add = QPushButton("Новый вопрос")
btn_delete = QPushButton("Удалить вопрос")
btn_start = QPushButton("Начать тестирование")

menu_left_side = QVBoxLayout()
menu_left_side.addWidget(list_question)
menu_left_side.addWidget(btn_add)

menu_right_side = QVBoxLayout()
menu_right_side.addWidget(wdgt_edit)
menu_right_side.addWidget(btn_delete)

menu_both = QHBoxLayout()
menu_both.addLayout(menu_left_side)
menu_both.addLayout(menu_right_side)

menu_start_button_layout = QHBoxLayout()
menu_start_button_layout.addStretch(1)
menu_start_button_layout.addWidget(btn_start)
menu_start_button_layout.addStretch(1)

layout_menu = QVBoxLayout()
layout_menu.addLayout(menu_both)
layout_menu.addLayout(menu_start_button_layout)
