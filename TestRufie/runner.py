from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, NumericProperty


class Runner(BoxLayout):

    valueChanged = NumericProperty(0)
    finished = BooleanProperty(False)

    def __init__(self, total=10, stepTime=1, autoRepeat=True,
                 color=(0.5, 0.25, 0.15, 1), text="Присідання...", **kwargs):
        super().__init__(**kwargs)

        self.total = total
        self.autoRepeat = autoRepeat
        self.color = color
        self.text = text

        self.animation = (Animation(pos_hint={"top": 0.1}, duration=stepTime/2)
                          + Animation(pos_hint={"top": 1.0}, duration=stepTime/2))

        self.animation.on_progress = self.next

        self.btn = Button(size_hint=(1, 0.1), pos_hint={
                          "top": 1.0}, background_color=color)

        self.add_widget(self.btn)

    def start(self):
        self.valueChanged = 0
        self.finished = False
        self.btn.text = self.text
        if self.autoRepeat:
            self.animation.repeat = True
        self.animation.start(self.btn)

    def next(self, widget, step):
        if step == 1.0:
            self.valueChanged += 1
            if self.valueChanged >= self.total:
                self.animation.repeat = False
                self.finished = True
