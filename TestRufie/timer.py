from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import BooleanProperty


class Timer(Label):

    done = BooleanProperty(False)

    def __init__(self, total_seconds, **kwargs):
        super().__init__(**kwargs)
        self.done = False
        self.current = 0
        self.total_second = total_seconds

        self.text = "Пройшло секунд: " + str(self.current)

    def start(self):
        Clock.schedule_interval(self.change, 1)

    def restart(self, total_seconds, **kwargs):
        self.done = False
        self.total_second = total_seconds
        self.current = 0
        self.text = "Пройшло секунд: " + str(self.current)

        self.start()

    def change(self, dt):
        self.current += 1
        self.text = "Пройшло секунд: " + str(self.current)
        if self.current >= self.total_second:
            self.done = True
            return False
