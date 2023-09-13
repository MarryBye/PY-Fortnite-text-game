from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.image import Image


from instructions import txt_instruction, txt_test1, txt_test3, txt_sits
from ruffier import test
from runner import *
from sits import *
from timer import Timer

age = 7
name = "Вася"
p1, p2, p3 = 0, 0, 0

Window.clearcolor = (0.25, 0.15, 0.35, 1)
Window.size = (1280, 720)


def checkInt(val):
    try:
        val = int(val)
        if val < 0:
            return False
        else:
            return True
    except:
        return False


class FirstScreen(Screen):

    global age, name

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            Color(0.23, 0.5, 0, 1)
            self.rect = Rectangle(source="1.jpg", pos=(0, 0), size=(1280, 720))

        self.lbl_info = Label(text=txt_instruction,
                              halign="center", valign="middle")

        self.logo = VideoPlayer(state='play', options={'eos': 'loop'})
        self.logo.remove_widget(self.logo.children[0])

        self.image_logo = Image(source="1.jpg")

        self.lbl_info.font_size = 16
        self.lbl_info.outline_color = (0.55, 0.35, 0.55, 1)
        self.lbl_info.outline_width = 1

        self.lbl_name = Label(text="Введіть ім'я: ")
        self.lbl_name.outline_color = (0.55, 0.35, 0.55, 1)
        self.lbl_name.outline_width = 1

        self.lbl_age = Label(text="Скільки вам років: ")
        self.lbl_age.outline_color = (0.55, 0.35, 0.55, 1)
        self.lbl_age.outline_width = 1

        self.input_name = TextInput(text=name, multiline=False)
        self.input_name.foreground_color = (1, 0, 0, 1)
        self.input_age = TextInput(text=str(age), multiline=False)

        self.btn_next = Button(text="[i] Почати тест! [/i]", size_hint=(
            0.35, 0.15), pos_hint={"center_x": 0.5}, markup=True)
        self.btn_next.outline_color = (0.55, 0.35, 0.55, 1)
        self.btn_next.outline_width = 1
        self.btn_next.background_color = (0, 0, 0, 1)
        self.btn_next.on_press = self.next

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.line_1 = BoxLayout(size_hint=(1, 0.15))
        self.line_2 = BoxLayout(size_hint=(1, 0.15))

        self.line_1.add_widget(self.lbl_name)
        self.line_1.add_widget(self.input_name)

        self.line_2.add_widget(self.lbl_age)
        self.line_2.add_widget(self.input_age)

        self.main_layout.add_widget(self.logo)
        self.main_layout.add_widget(self.image_logo)
        self.main_layout.add_widget(self.lbl_info)
        self.main_layout.add_widget(self.line_1)
        self.main_layout.add_widget(self.line_2)
        self.main_layout.add_widget(self.btn_next)

        self.add_widget(self.main_layout)

    def next(self):

        global age, name

        if checkInt(self.input_age.text):
            name = self.input_name.text
            age = int(self.input_age.text)

            self.manager.current = "P1"


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lbl_info = Label(text=txt_test1, halign="center", valign="middle")

        self.timer_lbl = Timer(1)
        self.timer_lbl.bind(done=self.on_timer_done)

        self.lbl_result = Label(text="Введіть результат:")

        self.input_result = TextInput(multiline=False)
        self.input_result.set_disabled(True)

        self.btn_next = Button(text="Продовжити")
        self.btn_next.on_press = self.next
        self.btn_next.set_disabled(True)

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.line = BoxLayout()
        self.line.add_widget(self.lbl_result)
        self.line.add_widget(self.input_result)

        self.main_layout.add_widget(self.lbl_info)
        self.main_layout.add_widget(self.timer_lbl)
        self.main_layout.add_widget(self.line)
        self.main_layout.add_widget(self.btn_next)

        self.add_widget(self.main_layout)

        self.on_enter = self.timer_lbl.start

        # **kwargs: name = "Viktor", age = 8, ...
        # *args: name, age, ...

    def on_timer_done(self, *args):
        self.input_result.set_disabled(False)
        self.btn_next.set_disabled(False)

    def next(self):
        global p1

        if checkInt(self.input_result.text):
            p1 = int(self.input_result.text)

            self.manager.current = "P2"


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lbl_info = Label(text=txt_sits)

        self.lbl_sits = Sits(30)
        self.run = Runner(total=30, stepTime=1.75)
        self.run.bind(valueChanged=self.lbl_sits.next)
        self.run.bind(finished=self.on_timer_done)

        self.btn_next = Button(text="Продовжити")
        self.btn_next.on_press = self.next
        self.btn_next.set_disabled(True)

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.main_layout.add_widget(self.lbl_info)
        self.main_layout.add_widget(self.lbl_sits)
        self.main_layout.add_widget(self.run)
        self.main_layout.add_widget(self.btn_next)

        self.add_widget(self.main_layout)

        self.on_enter = self.run.start

    def on_timer_done(self, *args):
        self.btn_next.set_disabled(False)

    def next(self):
        self.manager.current = "P3"


class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.stage = 0

        self.lbl_info = Label(text=txt_test3)
        self.timer_lbl = Timer(3)
        self.timer_lbl.bind(done=self.on_timer_done)

        self.lbl_p2 = Label(text="Результат: ")
        self.lbl_p3 = Label(text="Результат після відпочинку: ")

        self.input_p2 = TextInput(multiline=False)
        self.input_p2.set_disabled(True)
        self.input_p3 = TextInput(multiline=False)
        self.input_p3.set_disabled(True)

        self.btn_next = Button(text="Продовожити")
        self.btn_next.on_press = self.next
        self.btn_next.set_disabled(True)

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.line_1 = BoxLayout()
        self.line_2 = BoxLayout()

        self.line_1.add_widget(self.lbl_p2)
        self.line_1.add_widget(self.input_p2)

        self.line_2.add_widget(self.lbl_p3)
        self.line_2.add_widget(self.input_p3)

        self.main_layout.add_widget(self.lbl_info)
        self.main_layout.add_widget(self.timer_lbl)
        self.main_layout.add_widget(self.line_1)
        self.main_layout.add_widget(self.line_2)
        self.main_layout.add_widget(self.btn_next)

        self.add_widget(self.main_layout)

        self.on_enter = self.timer_lbl.start

    def on_timer_done(self, *args):
        if self.timer_lbl.done:
            if self.stage == 0:
                self.stage = 1
                self.lbl_info.text = "Відпочивайте"
                self.timer_lbl.restart(3)
                self.input_p2.set_disabled(False)
            elif self.stage == 1:
                self.stage = 2
                self.lbl_info.text = "Рахуйте пульс"
                self.timer_lbl.restart(3)
                self.input_p3.set_disabled(False)
            elif self.stage == 2:
                self.lbl_info.text = "Запишіть дані"
                self.btn_next.set_disabled(False)

    def next(self):
        global p2, p3

        if checkInt(self.input_p2.text) and checkInt(self.input_p3.text):
            p2 = int(self.input_p2.text)
            p3 = int(self.input_p3.text)

            self.manager.current = "Result"


class FifthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lbl_info = Label(text="")

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.main_layout.add_widget(self.lbl_info)

        self.add_widget(self.main_layout)

        self.on_enter = self.loadPage

    def loadPage(self):
        global name, p1, p2, p3, age

        self.lbl_info.text = name + "\n" + text


class RufieApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(FirstScreen(name="Main"))
        self.screen_manager.add_widget(SecondScreen(name="P1"))
        self.screen_manager.add_widget(ThirdScreen(name="P2"))
        self.screen_manager.add_widget(FourthScreen(name="P3"))
        self.screen_manager.add_widget(FifthScreen(name="Result"))
        return self.screen_manager


app = RufieApp()
app.run()
