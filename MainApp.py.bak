from kivy.config import Config

Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 400)
Config.set("graphics", "height", 500)

from webbrowser import open_new_tab
from requests import get, patch
from json import loads
from datetime import datetime as dt
from time import sleep

import sqlite3 as sql

# Основное приложение
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp
from kivy.lang import Builder

min_temp, min_hum_earth, min_hum_air = 0, 0, 0

db = sql.connect("tableinfo.db")
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS tabel(
    id INTEGER,
    temperature FLOAT,
    humidity_air FLOAT
)
""")
db.commit()


# преобразование json в словарь
def splitting_for(s):
    return loads(s)


LeftMenu_KV = """
MDNavigationLayout:

    MDScreenManager:

        MDScreen:

            MDTopAppBar:
                id: main-set
                pos_hint: {"top": 1, "x":0}
                size_hint: (1, .0)
                md_bg_color: 0, 1, 0, 1
                left_action_items: [["menu",lambda x: nav_drawer.set_state("open")]]
                icon_color: 0, 0, 0, 1
                specific_text_color: 0,1,0,1
                color: 0, 0, 0, 1

    MDNavigationDrawer:
        id: nav_drawer
        radius: 0, 0, 0, 0
        

        BoxLayout:
            orientation: "vertical"
            
            MDIconButton:
                icon: "help"
                icon_color: 0, 1, 0, 0.6
                theme_icon_color: "Custom"
                size_hint: (.2, .2)
                pos_hint: {"x": 0.8, "y":0.8}
                on_release:
                    nav_drawer.set_state("close")
                    app.call_help()
            MDLabel:
                text: "Меню"
                size_hint: (1, .5)
                halign: "center"
                theme_text_color: "Custom"
                text_color: 0, 1, 0, 1

            MDRectangleFlatIconButton:
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "home"
                text: "Главная"
                on_release:
                    nav_drawer.set_state("close")
                    app.main_call()

            MDRectangleFlatIconButton:
                id: edit_locate
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "pencil"
                text: "Редактировать"
                on_release:
                    nav_drawer.set_state("close")
                    app.edit_call()

            MDRectangleFlatIconButton:
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "table-large"
                text: "Таблицы"
                on_release:
                    nav_drawer.set_state("close")
                    app.table_info()

            MDRectangleFlatIconButton:
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "lightning-bolt"
                halign: "center"
                text: "Экстра режим"
                on_release:
                    nav_drawer.set_state("close")
                    app.extra_mode()

            MDRectangleFlatIconButton:
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "play"
                halign: "center"
                text: "Авто режим"
                on_release:
                    nav_drawer.set_state("close")
                    app.auto_mode()

            MDRectangleFlatIconButton:
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "lightbulb"
                text: "Темы"
                on_release: app.change_color_sys()

            MDRectangleFlatIconButton:
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "github"
                halign: "center"
                text: "GitHub"
                on_release:
                    nav_drawer.set_state("close")
                    app.git_info()
"""


url = "http://192.168.0.19:5000"

# Класс для Выпадающего меню
class LeftMenu(Screen):
    def __init__(self):
        super().__init__()
        self.add_widget(Builder.load_string(LeftMenu_KV))


class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        # имя экрана
        self.name = "Main"

        self.button_value = []
        for i in range(1, 4 + 1):
            res = get(f"{url}/temp_hum/{i}")
            self.button_value.append(
                f"""Сенсор {i}:\nТемпература: {splitting_for(res.text)["temperature"]}\nВлажность: {splitting_for(res.text)["humidity"]}""")
        self.fl = FloatLayout()
        self.dp = LeftMenu()
        # запускаем функцию Init()
        self.Init()

    def Init(self):
        # создаем обьекты кнопки
        self.btn1 = MDRectangleFlatButton(text=self.button_value[0],
                                          size_hint=(0.25, .25),
                                          # pos=(.5, .5),
                                          pos_hint={'center_x': 0.3, 'center_y': 0.7},
                                          # md_bg_color=(0, 1, 0, 0.1),
                                          on_release=self.update
                                          )
        btn2 = MDRectangleFlatButton(text=self.button_value[1],
                                     size_hint=(0.25, .25),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.7},
                                     on_release=self.update
                                     )
        btn3 = MDRectangleFlatButton(text=self.button_value[2],
                                     size_hint=(0.25, .25),
                                     pos_hint={'center_x': 0.3, 'center_y': 0.4},
                                     on_release=self.update
                                     )
        btn4 = MDRectangleFlatButton(text=self.button_value[3],
                                     size_hint=(0.25, .25), pos_hint={'center_x': 0.7, 'center_y': 0.4},
                                     on_release=self.update
                                     )
        self.btn_doing = MDRectangleFlatButton(
            text="Другие действия",
            size_hint=(.4, .2),
            pos_hint={'center_x': 0.71, 'center_y': 0.1},
            md_bg_color=(0, 1, 0, 0.1),
            on_press=self.doing
        )

        self.btn_next = MDRectangleFlatButton(text="Информация о почве",
                                              size_hint=(.4, .2),
                                              pos_hint={"center_x": 0.29, "center_y": 0.1},
                                              md_bg_color=(0, 1, 0, 0.1),
                                              on_release=self.next
                                              )
        # задаем фоновое изображение
        background_image = FitImage(
            source="icon/main-dark.jpg",
            opacity=0.05
        )

        self.fl.add_widget(background_image)
        self.fl.add_widget(self.btn_doing)
        self.fl.add_widget(self.btn_next)
        self.fl.add_widget(self.btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)
        self.fl.add_widget(btn4)
        self.fl.add_widget(self.dp)

        # добавляем все эллементы текущему обьекту
        self.add_widget(self.fl)

    # другой экран
    def next(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "Second"

    # обновляем текст
    def update(self, instance):
        id_btn = instance.text[7:8]
        res = get(f"{url}/temp_hum/{id_btn}")
        txt = f"""Сенсор {id_btn}:\nТемпература: {splitting_for(res.text)["temperature"]}\nВлажность: {splitting_for(res.text)["humidity"]}"""
        instance.text = txt

    def doing(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "Doing"


class DoingScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Doing"

        self.water_all = 0

        self.dp = LeftMenu()
        self.fl = FloatLayout()

        self.Init()

    def average_value(self, x):
        return sum(x) // len(x)

    # функция для пасчета среднего
    def temp_hum(self):
        res_temp = []
        res_air = []
        res_eath = []
        for i in range(1, 4 + 1):
            res_temp.append(
                splitting_for(get(f"{url}/temp_hum/{i}").text)["temperature"])
            res_air.append(splitting_for(get(f"{url}/temp_hum/{i}").text)["humidity"])
        for i in range(1, 6 + 1):
            res_eath.append(splitting_for(get(f'{url}/hum/{i}').text)["humidity"])
        return [self.average_value(res_temp),
                self.average_value(res_air),
                self.average_value(res_eath)]

    def Init(self):
        self.btn_open = MDRectangleFlatButton(
            text="Открыть форточки",
            font_size=dp(20),
            size_hint=(.9, .2),
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            disabled=False,
            on_release=self.move_luck
        )
        self.btn_start_water = MDRectangleFlatButton(
            text="Начать\nобщий полив",
            font_size=dp(20),
            size_hint=(.9, .2),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            disabled=False,
            on_release=self.start_all_water
        )

        self.btn_stop_water = MDRectangleFlatButton(
            text="Останость полив",
            font_size=dp(20),
            size_hint=(.9, .2),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            disabled=False,
        )

        background_image = FitImage(
            source="icon/doing-dark.jpg",
            opacity=0.05
        )

        self.fl.add_widget(background_image)
        self.fl.add_widget(self.btn_open)
        self.fl.add_widget(self.btn_start_water)
        self.fl.add_widget(self.btn_stop_water)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    # отправляем patch запрос на старт полива всех грядок
    def start_all_water(self, instance):
        if instance.text == "Начать\nОбщий полив":
            instance.text = "Остановить полив"
            res = patch("{url}/total_hum",
                        params={"state": 0}
                        )
            print(res.status_code)
        else:
            instance.text = "Начать\nОбщий полив"
            res = patch("{url}/total_hum",
                        params={"state": 1}
                        )

    # отправляем patch запрос на открытие/закрытие форточки
    def move_luck(self, instance):
        if instance.text == "Открыть":
            instance.text = "Закрыть"
            res = get("{url}/fork_drive")
            print(res.status_code)
        else:
            instance.text = "Открыть"
            res = get("{url}/fork_drive")

    def watering_one(self, instance):
        pass


class SecondScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Second"

        self.button_value = []
        for i in range(1, 6 + 1):
            res = get(f"{url}/hum/{i}")
            self.button_value.append(
                f"""Сенсор {i}:\nВлажность: {splitting_for(res.text)["humidity"]}""")
        self.fl = FloatLayout()
        self.dp = LeftMenu()
        self.Init()

    def Init(self):
        btn1 = MDRectangleFlatButton(text=self.button_value[0],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.3, 'center_y': 0.8},
                                     on_press=self.update
                                     )
        btn2 = MDRectangleFlatButton(text=self.button_value[1],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.8},
                                     on_press=self.update
                                     )
        btn3 = MDRectangleFlatButton(text=self.button_value[2],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.3, 'center_y': 0.55},
                                     on_press=self.update
                                     )
        btn4 = MDRectangleFlatButton(text=self.button_value[3],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.55},
                                     on_press=self.update
                                     )
        btn5 = MDRectangleFlatButton(text=self.button_value[4],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.3, 'center_y': 0.35},
                                     on_press=self.update
                                     )
        btn6 = MDRectangleFlatButton(text=self.button_value[5],
                                     size_hint=(0.25, .2),
                                     pos_hint={'center_x': 0.7, 'center_y': 0.35},
                                     on_press=self.update
                                     )
        self.btn_next = MDRectangleFlatButton(
            text="Назад",
            size_hint=(.4, .2),
            pos_hint={'x': 0.52, 'y': 0},
            md_bg_color=(0, 1, 0, 0.1),
            on_press=self.next
        )
        self.btn_doing = MDRectangleFlatButton(
            text="Другие действия",
            size_hint=(.4, .2),
            pos_hint={'x': 0.08, 'y': 0},
            md_bg_color=(0, 1, 0, 0.1),
            on_press=self.doing
        )
        background_image = FitImage(
            source="icon/second-dark.jpg",
            opacity=0.05
        )

        self.fl.add_widget(background_image)
        self.fl.add_widget(self.btn_doing)
        self.fl.add_widget(self.btn_next)
        self.fl.add_widget(btn1)
        self.fl.add_widget(btn2)
        self.fl.add_widget(btn3)
        self.fl.add_widget(btn4)
        self.fl.add_widget(btn5)
        self.fl.add_widget(btn6)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Main"

    # обновляем текст
    def update(self, instance):
        id_btn = instance.text[7:8]
        res = get(f"{url}/hum/{id_btn}")
        txt = f"""Сенсор {id_btn}:\nВлажность: {splitting_for(res.text)["humidity"]}"""
        instance.text = txt

    def doing(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = "Doing"


class ExtraScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = "ExtraMode"

        self.count_open = 0
        self.water_all = 0

        # создаем обьект переключателя
        self.switch = MDSwitch(
            pos_hint={'center_x': .5, 'center_y': .75},
            thumb_color_active=(255, 0, 0, 1),
            track_color_active=(255, 0, 0, 0.3),
            width=dp(64)
        )
        self.switch.bind(active=self.warning)

        self.dp = LeftMenu()
        self.bx = BoxLayout(orientation="vertical",
                            pos_hint={"x": 0, "y": 0},
                            size_hint=(1, 0.7))
        self.fl = FloatLayout()
        self.lbl = MDLabel(
            text="Внимание\nИспользуя данный режим, вы берете на себя всю ответственность за состояние ваших растений",
            halign="center",
            size_hint=(0.8, .2),
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            line_color=(1, 0, 0, 1),
            font_size=dp(30),
        )
        self.Init()

    def Init(self):
        self.btn1 = MDRectangleFlatButton(text="Открыть форточки",
                                          disabled=True,
                                          size_hint=(1, 0.17),
                                          pos_hint={"center_x": 0.5, "center_y": 0.595},
                                          font_size=dp(15),
                                          theme_text_color="Custom",
                                          line_color=(1, 0, 0, 0.8),
                                          text_color=(1, 0, 0, 1),
                                          on_press=self.leaf_move
                                          )
        self.btn2 = MDRectangleFlatButton(text="Начать полив",
                                          disabled=True,
                                          size_hint=(1, 0.17),
                                          pos_hint={"center_x": 0.5, "center_y": 0.425},
                                          font_size=dp(15),
                                          theme_text_color="Custom",
                                          line_color=(1, 0, 0, 0.8),
                                          text_color=(1, 0, 0, 1),
                                          on_press=self.water_run
                                          )
        self.btn3 = MDRectangleFlatButton(text="Остановить полив",
                                          disabled=True,
                                          size_hint=(1, 0.17),
                                          pos_hint={"center_x": 0.5, "center_y": 0.255},
                                          font_size=dp(15),
                                          theme_text_color="Custom",
                                          line_color=(1, 0, 0, 0.8),
                                          text_color=(1, 0, 0, 1),
                                          on_press=self.water_all_run

                                          )
        background_image = FitImage(
            source="icon/extra-dark.jpg",
            opacity=0.065
        )
        self.fl.add_widget(background_image)
        self.fl.add_widget(self.lbl)
        self.fl.add_widget(self.switch)
        self.fl.add_widget(self.btn1)
        self.fl.add_widget(self.btn2)
        self.fl.add_widget(self.btn3)
        self.fl.add_widget(self.bx)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    def leaf_move(self, instance):
        self.count_open = (1 if self.count_open == 0 else 0)
        get("{url}/fork_drive")

    def water_run(self, instance):
        get("{url}/watering")

    def water_all_run(self, instance):
        if self.water_all == 0:
            self.water_all = 1
        else:
            self.water_all = 0
        res = get("{url}/total_hum")

    def warning(self, instance, value):
        if value:
            self.lbl.text_color = (1, 1, 1, 0.4)
            self.lbl.line_color = (1, 1, 1, 0.4)
            self.btn1.disabled = False
            self.btn2.disabled = False
            self.btn3.disabled = False
        else:
            self.lbl.text_color = (1, 0, 0, 1)
            self.lbl.line_color = (1, 0, 0, 1)
            self.btn1.disabled = True
            self.btn2.disabled = True
            self.btn3.disabled = True


class AutomodeScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "AutoMode"

        self.lbl = MDLabel(
            text="Это автоматический режим\nЗдесь вы можете задать время для самополива ваших растений",
            halign="center",
            pos_hint={"x": 0.1, "y": 0.8},
            size_hint=(0.8, 0.2),
            theme_text_color="Custom",
            text_color=(1, 1, 0, 1),
            font_size=dp(40),
            line_color=(1, 1, 0, 0.8),
        )

        self.fl = FloatLayout()
        self.dp = LeftMenu()

        self.Init()

    def Init(self):
        # BLOCK №1
        self.text1 = MDLabel(text="Авто-полив",
                             pos_hint={"center_x": 0.6,
                                       "center_y": 0.5},
                             theme_text_color="Custom",
                             text_color=(1, 1, 0, 1),
                             )
        self.time1 = MDRaisedButton(
            text="Установить время",
            pos_hint={"center_x": 0.8, "center_y": 0.5},
            disabled=True,
            md_bg_color=(1, 1, 0, 1),
            on_press=self.show_timer_watering
        )
        self.switch1 = MDSwitch(
            pos_hint={'center_x': .5, 'center_y': .5},
            thumb_color_active=(255, 255, 0, 1),
            track_color_active=(255, 255, 0, 0.3),
            width=dp(64)
        )
        self.switch1.bind(active=self.sw_press1)

        # BLOKC №2
        self.text2 = MDLabel(text="Авто-проветривание",
                             pos_hint={"center_x": 0.55,
                                       "center_y": 0.3},
                             theme_text_color="Custom",
                             text_color=(1, 1, 0, 1)
                             )
        self.time2 = MDRaisedButton(
            text="Установить время",
            pos_hint={"center_x": 0.8, "center_y": 0.3},
            disabled=True,
            md_bg_color=(1, 1, 0, 1),
            on_press=self.show_timer_temp
        )
        self.switch2 = MDSwitch(
            pos_hint={'center_x': .5, 'center_y': .3},
            thumb_color_active=(255, 255, 0, 1),
            track_color_active=(255, 255, 0, 0.3),
            width=dp(64),
        )
        self.switch2.bind(active=self.sw_press2)

        background_image = FitImage(
            source="icon/automode-dark.jpg",
            opacity=0.065
        )

        self.fl.add_widget(background_image)
        self.fl.add_widget(self.text1)
        self.fl.add_widget(self.time1)
        self.fl.add_widget(self.switch1)

        self.fl.add_widget(self.text2)
        self.fl.add_widget(self.time2)
        self.fl.add_widget(self.switch2)

        self.fl.add_widget(self.lbl)
        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    # <-----------------Watering----------------->
    def show_timer_watering(self, instance):
        timer = MDTimePicker()
        timer.bind(time=self.get_time_watering)
        timer.open()

    def get_time_watering(self, instance, time):
        self.watering_time = str(time)

    # <-----------------Temperature----------------->
    def show_timer_temp(self, instance):
        timer = MDTimePicker()
        timer.bind(time=self.get_time_watering)
        timer.open()

    def get_time_temp(self, instance, time):
        self.temp_time = str(time)

    # <-----------------Pressed----------------->
    def sw_press1(self, switch, value):
        if value:
            self.time1.disabled = False
        else:
            self.time1.disabled = True

    def sw_press2(self, switch, value):
        if value:
            self.time2.disabled = False
        else:
            self.time2.disabled = True


class TabelScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Table"

        # self.now = datetime.now()

        self.dp = LeftMenu()
        self.fl = FloatLayout()

        self.Init()

    def Init(self):
        self.table = MDDataTable(pos_hint={"center_x": .5,
                                           "center_y": .55},
                                 size_hint=(0.9, 0.6),
                                 column_data=[
                                     ("№ id", dp(10)),
                                     ("temperature", dp(20)),
                                     ("humidity air", dp(25)),

                                 ],
                                 row_data=[
                                 ]
                                 )
        btn = MDRaisedButton(text="Новые данные",
                             pos_hint={"x": 0, "y": 0},
                             size_hint=(1, .2),
                             on_release=self.new_row_table)
        self.fl.add_widget(self.table)
        self.fl.add_widget(btn)
        self.fl.add_widget(self.dp)
        self.add_widget(self.fl)

    def new_row_table(self, instance):
        new_data_row = []
        for i in range(1, 4 + 1):
            res = get(f"{url}/temp_hum/{i}").text
            temp = splitting_for(res)["temperature"]
            hum = splitting_for(res)["humidity"]
            new_data_row.append(
                (i,
                 temp,
                 hum,
                 ))
            cursor.execute(f"""INSERT INTO tabel(id, temperature, humidity_air) 
            VALUES("{i}", "{temp}", "{hum}");
        """)
            db.commit()
        self.table.row_data = new_data_row


class EditScreen(Screen):
    def __init__(self, **kwargs):
        super(EditScreen, self).__init__(**kwargs)
        self.name = "Edit"

        self.fl = FloatLayout()
        self.dp = LeftMenu()
        self.fl = FloatLayout()
        self.lbl = MDLabel(
            text="Редактировать\nЗдесь вы можете задать значения при которых вашим растениям ничего не будет угрожать",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 1, 0, 1),
            line_color=(0, 1, 0, 1),
            size_hint=(.8, 0.2),
            pos_hint={"center_x": .5, "y": 0.8},
        )

        self.Init()

    def Init(self):
        self.txt1 = MDTextField(hint_text=f"Температура",
                                mode="fill",
                                size_hint=(1, 0.3),
                                pos_hint={"center_x": 0.5, "center_y": .6}
                                )
        self.txt2 = MDTextField(hint_text=f"Влажность воздуха",
                                mode="fill",
                                size_hint=(1, 0.3),
                                pos_hint={"center_x": 0.5, "center_y": 0.45},
                                )
        self.txt3 = MDTextField(hint_text=f"Влажность почвы",
                                mode="fill",
                                size_hint=(1, 0.3),
                                pos_hint={"center_x": 0.5, "center_y": 0.3}
                                )

        btn_save_data = MDRaisedButton(
            text="Сохранить",
            size_hint=(1, .2),
            pos_hint={"x": 0, "y": 0},
            on_release=self.save_data
        )
        background_image = FitImage(
            source="icon/edit-dark.jpg",
            opacity=0.065
        )

        self.fl.add_widget(background_image)
        self.fl.add_widget(self.lbl)
        self.fl.add_widget(self.txt1)
        self.fl.add_widget(self.txt2)
        self.fl.add_widget(self.txt3)
        self.fl.add_widget(btn_save_data)

        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = "Main"

    def save_data(self, instance):
        if self.txt1.text is not None and self.txt1.text != "":
            min_temp = float(self.txt1.text)
            do_i = DoingScreen()
            if min_temp < do_i.average_value(do_i.temp_hum()[0]):
                do_i.open_btn = False
            else:
                do_i.open_btn = True

        if self.txt2.text is not None and self.txt2.text != "":
            min_hum_air = float(self.txt2.text)

        if self.txt3.text is not None and self.txt3.text != "":
            min_hum_earth = float(self.txt3.text)


class MainApp(MDApp, Screen):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"

        self.sm.add_widget(MainScreen())
        self.sm.add_widget(TabelScreen())
        self.sm.add_widget(DoingScreen())
        self.sm.add_widget(AutomodeScreen())
        self.sm.add_widget(ExtraScreen())
        self.sm.add_widget(EditScreen())
        self.sm.add_widget(SecondScreen())

        return self.sm

    def main_call(self):
        self.sm.transition.direction = "right"
        self.sm.current = "Main"

    def edit_call(self):
        self.sm.transition.direction = "left"
        self.sm.current = "Edit"

    def extra_mode(self):
        self.sm.transition.direction = "right"
        self.sm.current = "ExtraMode"

    def table_info(self):
        self.sm.transition.direction = "right"
        self.sm.current = "Table"

    def auto_mode(self):
        self.sm.transition.direction = "right"
        self.sm.current = "AutoMode"

    def change_color_sys(self):
        self.theme_cls.theme_style = (
            "Light" if self.theme_cls.theme_style == "Dark" else "Dark"
        )

    def git_info(self):
        open_new_tab("https://github.com/voronov-nikita/teplica_predprof")

    def call_help(self):
        open_new_tab("http://tpgh.ru")


class ErrorApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        fl = FloatLayout()
        fl.add_widget(MDLabel(text="Сервер не отвечает\nПопробуйте позже",
                              font_size=dp(60),
                              size_hint=(1, 1),
                              halign="center"))
        fl.add_widget(FitImage(
            source="icon/error-image.png",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            size_hint=(0.2, 0.2)
        ))
        return fl


if __name__ == "__main__":
    MainApp().run()
    # try:
    #     MainApp().run()
    # except:
    #     ErrorApp().run()
