from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen


class CButton(Button):
    def __init__(self, screen, direction, goal, **kwargs):
        super().__init__(**kwargs)

        self.screen = screen
        self.direction = direction
        self.goal = goal

    def on_press(self):
        self.screen.manager.transition.direction = self.direction
        self.screen.manager.current = self.goal


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        button_vertical_layout = BoxLayout(
            orientation="vertical", padding=8, spacing=8)

        main_horizontal_layout = BoxLayout()

        info_text = Label(text="Обери один з 4 екранів:")

        btn_1 = CButton(self, direction="down",
                        goal="first", text="Перша сторінка")
        btn_2 = CButton(self, direction="left",
                        goal="second", text="Друга сторінка")
        btn_3 = CButton(self, direction="up", goal="third",
                        text="Третя сторінка")
        btn_4 = CButton(self, direction="right", goal="fourth",
                        text="Четверта сторінка")

        button_vertical_layout.add_widget(btn_1)
        button_vertical_layout.add_widget(btn_2)
        button_vertical_layout.add_widget(btn_3)
        button_vertical_layout.add_widget(btn_4)

        main_horizontal_layout.add_widget(info_text)
        main_horizontal_layout.add_widget(button_vertical_layout)

        self.add_widget(main_horizontal_layout)


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        btn_back = CButton(self, direction="up",
                           goal="main", text="До головної")

        main_vertical_layout = BoxLayout(orientation="vertical", spacing=8, size_hint=(
            0.5, 0.5), pos_hint={"center_x": 0.5, "center_y": 0.5})

        btn_test = Button(text="Я нічого не роблю...")

        main_vertical_layout.add_widget(btn_test)
        main_vertical_layout.add_widget(btn_back)

        self.add_widget(main_vertical_layout)


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        btn_back = CButton(self, direction="right",
                           goal="main", text="До головної")

        self.text_result = Label(text="")

        text_info = Label(text="Введіть пароль")

        self.password = TextInput(multiline=False)

        btn_ok = Button(text="Увійти")
        btn_ok.on_press = self.checkPassword

        main_vertical_layout = BoxLayout(orientation="vertical", spacing=16, size_hint=(
            0.5, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.5})

        horizontal_layout = BoxLayout()
        horizontal_layout.add_widget(text_info)
        horizontal_layout.add_widget(self.password)
        horizontal_layout.add_widget(btn_ok)
        horizontal_layout.add_widget(btn_back)

        main_vertical_layout.add_widget(self.text_result)
        main_vertical_layout.add_widget(horizontal_layout)

        self.add_widget(main_vertical_layout)

    def checkPassword(self):
        if self.password.text == "1234":
            self.text_result.text = "Увійшли!"
        else:
            self.text_result.text = "Неправильний пароль!"


class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        btn_back = CButton(self, direction="right",
                           goal="main", text="До головної")

        self.text_result = Label(text="")

        text_info = Label(text="Введіть пароль")

        self.password = TextInput(multiline=False)

        btn_ok = Button(text="Увійти")
        btn_ok.on_press = self.checkPassword

        main_vertical_layout = BoxLayout(orientation="vertical", spacing=16, size_hint=(
            0.5, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.5})

        horizontal_layout = BoxLayout()
        horizontal_layout.add_widget(text_info)
        horizontal_layout.add_widget(self.password)
        horizontal_layout.add_widget(btn_ok)
        horizontal_layout.add_widget(btn_back)

        main_vertical_layout.add_widget(self.text_result)
        main_vertical_layout.add_widget(horizontal_layout)

        self.add_widget(main_vertical_layout)

    def checkPassword(self):
        if self.password.text == "2321":
            self.text_result.text = "Увійшли!"
        else:
            self.text_result.text = "Неправильний пароль!"


class FourthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        btn_back = CButton(self, direction="right",
                           goal="main", text="До головної")

        self.text_result = Label(text="")

        text_info = Label(text="Введіть пароль")

        self.password = TextInput(multiline=False)

        btn_ok = Button(text="Увійти")
        btn_ok.on_press = self.checkPassword

        main_vertical_layout = BoxLayout(orientation="vertical", spacing=16, size_hint=(
            0.5, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.5})

        horizontal_layout = BoxLayout()
        horizontal_layout.add_widget(text_info)
        horizontal_layout.add_widget(self.password)
        horizontal_layout.add_widget(btn_ok)
        horizontal_layout.add_widget(btn_back)

        main_vertical_layout.add_widget(self.text_result)
        main_vertical_layout.add_widget(horizontal_layout)

        self.add_widget(main_vertical_layout)

    def checkPassword(self):
        if self.password.text == "2321":
            self.text_result.text = "Увійшли!"
        else:
            self.text_result.text = "Неправильний пароль!"


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(FirstScreen(name="first"))
        sm.add_widget(SecondScreen(name="second"))
        sm.add_widget(ThirdScreen(name="third"))
        sm.add_widget(FourthScreen(name="fourth"))
        return sm


MyApp().run()
