from PyQt5.QtCore import *
from random import *

text_right = "Правильно!"
text_wrong = "Неправильно!"


class Question:
    def __init__(self, q="НОВЫЙ ВОПРОС", a="", w1="", w2="", w3=""):
        self.question = q
        self.answer = a
        self.wrong_ans1 = w1
        self.wrong_ans2 = w2
        self.wrong_ans3 = w3

        self.attempts = 0
        self.correct = 0

    def got_right(self):
        print("Правильно!")
        self.correct += 1
        self.attempts += 1

    def got_wrong(self):
        print("Неправильно!")
        self.attempts += 1


class QuestionView:
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        self.frm_model = frm_model
        self.question = question
        self.answer = answer
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3

    def change(self, frm_model):
        self.frm_model = frm_model

    def show(self):
        self.question.setText(self.frm_model.question)
        self.answer.setText(self.frm_model.answer)
        self.wrong_answer1.setText(self.frm_model.wrong_ans1)
        self.wrong_answer2.setText(self.frm_model.wrong_ans2)
        self.wrong_answer3.setText(self.frm_model.wrong_ans3)


class AnswerCheck(QuestionView):
    def __init__(self, frm_model, q, a, w1, w2, w3, showed_answer, r):
        super().__init__(frm_model, q, a, w1, w2, w3)
        self.showed_answer = showed_answer
        self.result = r

    def check(self):
        if self.answer.isChecked():
            self.result.setText(text_right)
            self.showed_answer.setText(self.frm_model.answer)
            self.frm_model.got_right()
        else:
            self.result.setText(text_wrong)
            self.showed_answer.setText(self.frm_model.answer)
            self.frm_model.got_wrong()


class QuestionEdit(QuestionView):
    def save_question(self):
        self.frm_model.question = self.question.text()

    def save_answer(self):
        self.frm_model.answer = self.answer.text()

    def save_wrong_answers(self):
        self.frm_model.wrong_answer1 = self.wrong_answer1.text()
        self.frm_model.wrong_answer2 = self.wrong_answer2.text()
        self.frm_model.wrong_answer3 = self.wrong_answer3.text()

    def set_connects(self):
        self.question.editingFinished.connect(self.save_question)
        self.answer.editingFinished.connect(self.save_answer)
        self.wrong_answer1.editingFinished.connect(self.save_wrong_answers)
        self.wrong_answer2.editingFinished.connect(self.save_wrong_answers)
        self.wrong_answer3.editingFinished.connect(self.save_wrong_answers)

    def __init__(self, frm_model, question, answer, w_a1, w_a2, w_a3):
        super().__init__(frm_model, question, answer, w_a1, w_a2, w_a3)

        self.set_connects()


class QuestionListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_list = []

    def rowCount(self, index):
        return len(self.form_list)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            form = self.form_list[index.row()]
            return form.question

    def insertRows(self, parent=QModelIndex()):
        position = len(self.form_list)
        self.beginInsertRows(parent, position, position)
        self.form_list.append(Question())
        self.endInsertRows()
        QModelIndex()
        return True

    def removeRows(self, position, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position)
        self.form_list.pop(position)
        self.endRemoveRows()
        return True

    def random_question(self):
        total = len(self.form_list)
        current = randint(0, total - 1)
        return self.form_list[current]


def random_AnswerCheck(list_model, w_question, widgets_list, w_showed_answer, w_result):
    frm = list_model.random_question()
    shuffle(widgets_list)
    frm_card = AnswerCheck(
        frm, w_question, widgets_list[0], widgets_list[1], widgets_list[2], widgets_list[3], w_showed_answer, w_result)
    return frm_card
