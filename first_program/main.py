from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import randint

app = QApplication([])
win = QWidget()
win.setWindowTitle("Генератор победителя")
win.resize(450, 175)

lbl_info = QLabel("Для выбора победителя нажмите на кнопку")
lbl_random = QLabel("?")
btn_choose = QPushButton("Сгенерировать!")

# QVBoxLayout, QHBoxLayout

window_layout = QVBoxLayout()

window_layout.addWidget(lbl_info, alignment=Qt.AlignCenter)
window_layout.addWidget(lbl_random, alignment=Qt.AlignCenter)
window_layout.addWidget(btn_choose, alignment=Qt.AlignCenter)

win.setLayout(window_layout)

# Событие - это то, что происходит и требует какую-то реакцию на себе


def on_click():
    lbl_info.setText("Выпал номер:")
    lbl_random.setText(str(randint(1, 100)))


btn_choose.clicked.connect(on_click)


win.show()
app.exec()
