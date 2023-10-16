from numpy import arange
from math import exp

training_set = [
    [1, 1, 1,
     1, 0, 1,
     1, 0, 1,
     1, 0, 1,
     1, 1, 1],
    [0, 0, 1,
     0, 0, 1,
     0, 0, 1,
     0, 0, 1,
     0, 0, 1],
    [1, 1, 1,
     0, 0, 1,
     1, 1, 1,
     1, 0, 0,
     1, 1, 1],
    [1, 1, 1,
     0, 0, 1,
     1, 1, 1,
     0, 0, 1,
     1, 1, 1],
    [1, 0, 1,
     1, 0, 1,
     1, 1, 1,
     0, 0, 1,
     0, 0, 1],
    [1, 1, 1,
     1, 0, 0,
     1, 1, 1,
     0, 0, 1,
     1, 1, 1],
    [1, 1, 1,
     1, 0, 0,
     1, 1, 1,
     1, 0, 1,
     1, 1, 1],
    [1, 1, 1,
     0, 0, 1,
     0, 0, 1,
     0, 0, 1,
     0, 0, 1],
    [1, 1, 1,
     1, 0, 1,
     1, 1, 1,
     1, 0, 1,
     1, 1, 1],
    [1, 1, 1,
     1, 0, 1,
     1, 1, 1,
     0, 0, 1,
     1, 1, 1]
]

test_set = [
    [1, 1, 1,
     1, 0, 0,
     1, 1, 1,
     0, 0, 1,
     1, 1, 1],
    [1, 1, 1,
     1, 0, 0,
     1, 1, 1,
     0, 0, 0,
     1, 1, 1],
    [1, 1, 1,
     1, 0, 0,
     0, 1, 0,
     0, 0, 1,
     1, 1, 1],
    [1, 1, 1,
     1, 0, 0,
     0, 1, 1,
     0, 0, 1,
     1, 1, 1],
    [1, 1, 0,
     1, 0, 0,
     1, 1, 1,
     0, 0, 1,
     1, 1, 1],
    [1, 1, 0,
     1, 0, 0,
     1, 1, 1,
     0, 0, 1,
     0, 1, 1],
    [1, 1, 1,
     1, 0, 0,
     1, 0, 1,
     0, 0, 1,
     1, 1, 1]
]


class NumericNeuron:
    # Инициализирую нейрон, стандартные значения
    def __init__(self, train_set: list, max_inputs: int = 15) -> None:
        self.max_inputs = max_inputs
        self.inputs = [inp for inp in arange(max_inputs)]
        self.weights = [wgt for wgt in arange(max_inputs)]
        self.numbers_train_set = train_set

    # Персептрон проверяет результат, задействованніе входы умножает на их веса и делает решение
    def get_result(self) -> bool:
        net = 0
        for input_num in arange(self.max_inputs):
            net += self.inputs[input_num] * self.weights[input_num]
        out = 1 / (exp(-1 * net))  # сигмоидальная функция, т.к. единичный скачок очень плохо работает
        return out >= 0.75

    # То же получение результата, просто сокращен момент замены входов на другие
    def check_for(self, inputs: list) -> bool:
        self.inputs = inputs
        return self.get_result()

    # Тренируем нейрон определять число
    def train_for(self, number_train) -> None:
        correct_answers = 0
        print("Тренировка начата")
        while True:
            if correct_answers == 10:
                print("Успешно натренировали")
                break

            correct_answers += 1

            for number in arange(10):  # всего 10 цифр, мы это знаем
                result = self.check_for(self.numbers_train_set[number])

                if result and number != number_train:
                    correct_answers = 0
                    for weight in arange(self.max_inputs):
                        if self.numbers_train_set[number][weight] == 1:
                            self.weights[weight] -= 1

                if not result and number == number_train:
                    correct_answers = 0
                    for weight in arange(self.max_inputs):
                        if self.numbers_train_set[number][weight] == 1:
                            self.weights[weight] += 1


MainNeuron = NumericNeuron(training_set)
MainNeuron.train_for(5)

i = 0
for num in test_set:
    i += 1
    print("Пятерка", i, MainNeuron.check_for(num))

i = 0
for num in training_set:
    print(i, ":", MainNeuron.check_for(num))
    i += 1
