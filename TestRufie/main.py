from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits
from ruffier import test

age = 7
name = "Вася"
p1, p2, p3 = 0, 0, 0


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lbl_info = Label(text=txt_instruction)
        self.lbl_name = Label(text="Введіть ім'я: ")
        self.lbl_age = Label(text="Скільки вам років: ")

        self.input_name = TextInput(multiline=False)
        self.input_age = TextInput(multiline=False)

        self.btn_next = Button(text="Почати тест!")
        self.btn_next.on_press = self.next

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.line_1 = BoxLayout()
        self.line_2 = BoxLayout()

        self.line_1.add_widget(self.lbl_name)
        self.line_1.add_widget(self.input_name)

        self.line_2.add_widget(self.lbl_age)
        self.line_2.add_widget(self.input_age)

        self.main_layout.add_widget(self.lbl_info)
        self.main_layout.add_widget(self.line_1)
        self.main_layout.add_widget(self.line_2)
        self.main_layout.add_widget(self.btn_next)

        self.add_widget(self.main_layout)

    def next(self):
        global name, age

        name = self.input_name.text
        age = int(self.input_age.text)

        self.manager.current = "P1"


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lbl_info = Label(text=txt_test1)
        self.lbl_result = Label(text="Введіть результат:")

        self.input_result = TextInput(multiline=False)

        self.btn_next = Button(text="Продовжити")
        self.btn_next.on_press = self.next

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.line = BoxLayout()
        self.line.add_widget(self.lbl_result)
        self.line.add_widget(self.input_result)

        self.main_layout.add_widget(self.lbl_info)
        self.main_layout.add_widget(self.line)
        self.main_layout.add_widget(self.btn_next)

        self.add_widget(self.main_layout)

    def next(self):
        global p1

        p1 = int(self.input_result.text)

        self.manager.current = "P2"


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lbl_info = Label(text=txt_sits)

        self.btn_next = Button(text="Продовжити")
        self.btn_next.on_press = self.next

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.main_layout.add_widget(self.lbl_info)
        self.main_layout.add_widget(self.btn_next)

        self.add_widget(self.main_layout)

    def next(self):
        self.manager.current = "P3"


class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lbl_info = Label(text=txt_test3)
        self.lbl_p2 = Label(text="Результат: ")
        self.lbl_p3 = Label(text="Результат після відпочинку: ")

        self.input_p2 = TextInput(multiline=False)
        self.input_p3 = TextInput(multiline=False)

        self.btn_next = Button(text="Продовожити")
        self.btn_next.on_press = self.next

        self.main_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        self.line_1 = BoxLayout()
        self.line_2 = BoxLayout()

        self.line_1.add_widget(self.lbl_p2)
        self.line_1.add_widget(self.input_p2)

        self.line_2.add_widget(self.lbl_p3)
        self.line_2.add_widget(self.input_p3)

        self.main_layout.add_widget(self.lbl_info)
        self.main_layout.add_widget(self.line_1)
        self.main_layout.add_widget(self.line_2)
        self.main_layout.add_widget(self.btn_next)

        self.add_widget(self.main_layout)

    def next(self):
        global p2, p3

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

        self.lbl_info.text = name + "\n" + test(p1, p2, p3, age)


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
