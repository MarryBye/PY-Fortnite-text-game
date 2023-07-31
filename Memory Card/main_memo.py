from memo_data import *
from memo_card_layout import *
from memo_menu_layout import *
from PyQt5.QtWidgets import QWidget, QApplication
from random import shuffle

# Стандартные параметры
card_width, card_height = 600, 500
menu_width, menu_height = 1000, 450

# Список вопросов
questions_listmodel = QuestionListModel()
frm_edit = QuestionEdit(0, txt_Question, txt_Answer,
                        txt_Wrong1, txt_Wrong2, txt_Wrong3)
radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]

# Создание таймера для отдыха
timer = QTimer()

# Создание окон
win_card = QWidget()
win_menu = QWidget()

# Функция, которая запускается когда мы идем отдыхать


def sleep_card():
    win_card.hide()
    timer.setInterval(box_minutes.value() * 60000)
    timer.start()

# Функция, которая запускается когда мы отдохнули


def stop_sleep():
    win_card.show()
    timer.stop()

# Создать стандартные вопросы


def question_list():
    frm = Question("День вшанування захисників Донецького аеропорту-",
                   "20 січня", "23 січня", "28 вересня", "25 липня")
    questions_listmodel.form_list.append(frm)
    frm = Question("Акт проголошення незалежності України був -",
                   "24 серпня 1991", "27 серпня 1991", "28 серпня 1991", "22 сепрня 1991")
    questions_listmodel.form_list.append(frm)
    frm = Question("Міжнародний день пам'яті жертв Голокосту-",
                   "27 січня", "29 січня", "1 січня", "28 січня")
    questions_listmodel.form_list.append(frm)
    frm = Question("День пам'яті Героїв Крут-",
                   "9 січня", "10 січня", "5 лютого", "8 грудня")
    questions_listmodel.form_list.append(frm)
    frm = Question("День Героїв Небесної Сотні",
                   "20 лютого", "24 лютого", "21 червня", "1 листопада")
    questions_listmodel.form_list.append(frm)
    frm = Question("Міжнародний день рідної мови-",
                   "21 лютого", "9 січня", "6 серпня", "8 червня")
    questions_listmodel.form_list.append(frm)
    frm = Question("День кримського спротиву російській окупації-",
                   "26 лютого", "3 лютого", "4 липня", "28 травня")
    questions_listmodel.form_list.append(frm)
    frm = Question("День Служби безпеки України-",
                   "25 березня", "27 лютого", "3 червня", "1 травня")
    questions_listmodel.form_list.append(frm)
    frm = Question("День пам'яток історії та культури-",
                   "18 квітня", "5 лютого", "25 січня", "8 лютого")
    questions_listmodel.form_list.append(frm)
    frm = Question("Міжнародний день пам'яті про чорнобильську катастрофу-",
                   "26 квітня", "29 серпня", "7 квітня", "20 квітня")
    questions_listmodel.form_list.append(frm)


# Установка вида главного окна


def set_card():
    win_card.resize(card_width, card_height)
    win_card.move(300, 300)
    win_card.setWindowTitle("Memory Card")

    win_card.setLayout(layout_card)

# Установка вида меню


def set_menu():
    win_menu.resize(menu_width, menu_height)
    win_menu.move(100, 100)
    win_menu.setWindowTitle('Список вопросов')
    win_menu.setLayout(layout_menu)

# Показать случайный вопрос


def show_random():
    global frm_card
    frm_card = random_AnswerCheck(
        questions_listmodel, lb_question, radio_list, lb_Correct, lb_Result)
    frm_card.show()
    show_question()


# Нажатие на кнопку
def click():
    if btn_ok.text() != "Следующий вопрос":
        frm_card.check()
        show_result()
    else:
        show_random()

# Показать меню


def back_to_menu():
    win_card.hide()
    win_menu.showNormal()

# Начало теста


def start_test():
    show_random()
    win_card.show()
    win_menu.showMinimized()

# Редактирование вопроса


def edit_question(index):
    if index.isValid():
        i = index.row()
        frm = questions_listmodel.form_list[i]
        frm_edit.change(frm)
        frm_edit.show()

# Добавление вопроса


def add_question():
    questions_listmodel.insertRows()
    last = questions_listmodel.rowCount(0) - 1

    index = questions_listmodel.index(last)
    list_question.setCurrentIndex(index)
    edit_question(index)

    txt_Question.setFocus(Qt.TabFocusReason)

# Удаление вопроса


def del_question():
    questions_listmodel.removeRows(list_question.currentIndex().row())
    edit_question(list_question.currentIndex())

# Соединить между собой элементы


def connects():
    list_question.setModel(questions_listmodel)
    list_question.clicked.connect(edit_question)
    btn_add.clicked.connect(add_question)
    btn_delete.clicked.connect(del_question)
    btn_start.clicked.connect(start_test)
    btn_ok.clicked.connect(click)
    btn_menu.clicked.connect(back_to_menu)
    btn_sleep.clicked.connect(sleep_card)
    timer.timeout.connect(stop_sleep)


# Запуск всех частей программы
question_list()
set_card()
set_menu()
connects()

win_menu.show()
app.exec_()
