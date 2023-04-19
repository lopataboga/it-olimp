from requests import get, patch
from json import loads
from time import sleep
from kivy.config import Config

url = "http://dt.miet.ru/ppo_it/api"
min_temp, min_hum_earth, min_hum_air = 25.0, 30.0, 30.0
average_temp, average_hum_earth, average_hum_air = 0.0, 0.0, 0.0
count_open = 0
water_all = 0
hydration_all = 0
atoken = 'djdj'

import sqlite3 as sql
import random
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.fitimage import FitImage
from kivy.metrics import dp
from kivy.lang import Builder

db = sql.connect("tableinfo.db")
cursor = db.cursor()


def splitting_for(s):
    return loads(s)


leftmenu = """
MDNavigationLayout:
    MDScreenManager:
        MDScreen:

            MDTopAppBar:
                id: mainset
                pos_hint: {"top": 1, "x":0}
                adaptive_height: True
                use_overflow: True
                title: 'Умная теплица'
                anchor_title: "left"
                left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                right_action_items: [["align-vertical-bottom", lambda x: app.popup("open")]]

            Widget:

    MDNavigationDrawer:
        id: nav_drawer
        radius: 0, 0, 0, 0


        BoxLayout:
            orientation: "vertical"



            MDRectangleFlatIconButton:
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "home"
                text: "Главная"
                on_release:
                    nav_drawer.set_state("close")
                    app.main_call()

            MDRectangleFlatIconButton:
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "lightning-bolt"
                halign: "center"
                text: "Управление теплицей"
                on_release:
                    nav_drawer.set_state("close")
                    app.extra_mode()

            MDRectangleFlatIconButton:
                id: edit_locate
                line_color: 0, 0, 0, 0
                size_hint: (1, .5)
                icon: "pencil"
                text: "Ограничения"
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


"""


class LeftMenu(Screen):
    def __init__(self):
        super().__init__()
        self.add_widget(Builder.load_string(leftmenu))


class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Main"

        self.button_value = []
        for i in range(1, 4 + 1):
            res = get(f"{url}/temp_hum/{i}")
            self.button_value.append(
                f"""Датчик {i}:\nТемпература: {splitting_for(res.text)["temperature"]}\nВлажность: {splitting_for(res.text)["humidity"]}""")
        self.fl = FloatLayout()
        self.dp = LeftMenu()
        self.Init()

    def Init(self):
        self.layou = GridLayout(cols=2, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=[.5, .5])
        for i in range(0, 4):
            self.layou.add_widget(MDRectangleFlatButton(text=self.button_value[i],
                                                        size_hint=(0.25, .25),
                                                        on_release=self.update
                                                        ))
        self.mainl = MDLabel(text='Температура и влажность воздуха',
                             halign='center',
                             pos_hint={'center_x': .5, 'center_y': 0.85})

        self.dat = MDLabel(text='Датчик1', halign='center', pos_hint={'center_x': .25, 'center_y': 0.80})

        self.btn_next = MDRectangleFlatButton(
            text="Далее",
            size_hint=(.2, .2),
            pos_hint={"center_x": .5, "y": 0},
            on_press=self.next
        )
        self.fl.add_widget(self.mainl)
        self.fl.add_widget(self.btn_next)
        self.fl.add_widget(self.dp)
        self.add_widget(self.layou)
        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.current = "Second"

    def update(self, instance):
        id_btn = instance.text[7:8]
        res = get(f"{url}/temp_hum/{id_btn}")
        txt = f"""Датчик {id_btn}:\nТемпература: {splitting_for(res.text)["temperature"]}\nВлажность: {splitting_for(res.text)["humidity"]}"""
        instance.text = txt


class SecondScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Second"

        self.button_value = []
        for i in range(1, 6 + 1):
            res = get(f"{url}/hum/{i}")
            self.button_value.append(
                f"""Датчик {i}:\nВлажность: {splitting_for(res.text)["humidity"]}""")
        self.fl = FloatLayout()
        self.dp = LeftMenu()
        self.Init()

    def Init(self):
        self.layou = GridLayout(cols=2, pos_hint={'center_x': .5, 'center_y': .5}, size_hint=[.5, .5])
        for i in range(0, 6):
            self.layou.add_widget(MDRectangleFlatButton(id=f"{i}", text=self.button_value[i],
                                                        size_hint=(0.25, .2),
                                                        on_press=self.update
                                                        ))
        self.mainl = MDLabel(text='Влажность почвы',
                             halign='center',
                             pos_hint={'center_x': .5, 'center_y': 0.85})
        self.btn_next = MDRectangleFlatButton(
            text="Далее",
            size_hint=(.2, .2),
            pos_hint={"center_x": .5, "y": 0},
            on_press=self.next
        )

        self.fl.add_widget(self.mainl)
        self.fl.add_widget(self.btn_next)
        self.fl.add_widget(self.dp)

        self.add_widget(self.layou)
        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.current = "Main"

    def update(self, instance):
        id_btn = instance.text[7:8]
        res = get(f"{url}/hum/{id_btn}")
        txt = f"""Датчик {id_btn}:\nВлажность: {splitting_for(res.text)["humidity"]}"""
        instance.text = txt

    def doing(self, instance):
        self.manager.current = "Doing"


class ExtraScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = "ExtraMode"
        self.skcheck = 0
        self.dp = LeftMenu()
        self.bx = BoxLayout(orientation="vertical",
                            pos_hint={"x": 0, "y": 0},
                            size_hint=(1, 0.7))
        self.fl = FloatLayout()
        self.Init()

    def on_enter(self):
        global average_temp, min_temp, average_hum_air, min_hum_air
        if average_temp < min_temp:
            self.btn1.disabled = True
        if average_hum_air > min_hum_air:
            self.btn2.disabled = True

    def Init(self):
        self.switch = MDSwitch(
            pos_hint={'center_x': .06, 'center_y': .75},
            width=dp(64)
        )
        self.switch.bind(active=self.skip_check)

        self.switchlb = MDLabel(
            text="Игнорировать ограничения",
            halign="center",
            size_hint=(0.8, .2),
            pos_hint={"center_x": 0.25, "center_y": 0.75},
            font_size=dp(30),
        )
        self.btn1 = MDRectangleFlatButton(text="Открыть форточки",
                                          size_hint=(1, 0.17),
                                          pos_hint={"center_x": 0.5, "center_y": 0.595},
                                          font_size=dp(15),
                                          on_press=self.leaf_move
                                          )
        self.btn2 = MDRectangleFlatButton(text="Начать увлажнение",
                                          size_hint=(1, 0.17),
                                          pos_hint={"center_x": 0.5, "center_y": 0.425},
                                          font_size=dp(15),
                                          on_press=self.start_water
                                          )
        self.fl.add_widget(self.switchlb)
        self.fl.add_widget(self.switch)
        self.fl.add_widget(self.btn1)
        self.fl.add_widget(self.btn2)
        self.fl.add_widget(self.bx)
        self.fl.add_widget(self.dp)
        self.add_widget(self.fl)

    def leaf_move(self, instance):
        global count_open
        if count_open == 0:
            self.btn1.text = "Закрыть форточки"
            count_open = 1
        else:
            self.btn1.text = "Открыть форточки"
            count_open = 0
        patch("https://dt.miet.ru/ppo_it/api/fork_drive", params={"state": count_open})

    def start_water(self, instance):
        global water_all
        if water_all == 0:
            self.btn2.text = "Остановить увлажнение"
            water_all = 1
        else:
            self.btn2.text = "Начать увлажнение"
            water_all = 0
        patch("https://dt.miet.ru/ppo_it/api/total_hum", params={"state": water_all})

    def skip_check(self, instance, value):
        self.skcheck = not self.skcheck
        if self.skcheck == 1:
            self.btn1.disabled = False
            self.btn2.disabled = False
        else:
            global average_temp, min_temp, average_hum_air, min_hum_air
            if average_temp < min_temp:
                self.btn1.disabled = True
            if average_hum_air > min_hum_air:
                self.btn2.disabled = True


class TabelScreen(Screen):
    def __init__(self):
        super().__init__()
        self.name = "Table"

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
        self.Init()

    def Init(self):
        self.txt1 = MDTextField(hint_text=f"Температура",
                                size_hint=(0.90, 0.3),
                                mode="rectangle",
                                pos_hint={"center_x": 0.5, "center_y": .7}
                                )
        self.txt2 = MDTextField(hint_text=f"Влажность воздуха",
                                mode="rectangle",
                                size_hint=(0.90, 0.3),
                                pos_hint={"center_x": 0.5, "center_y": 0.55},
                                )
        self.txt3 = MDTextField(hint_text=f"Влажность почвы",
                                mode="rectangle",
                                size_hint=(0.90, 0.3),
                                pos_hint={"center_x": 0.5, "center_y": 0.4}
                                )
        btn_save_data = MDRaisedButton(
            text="Сохранить",
            size_hint=(1, .2),
            pos_hint={"x": 0, "y": 0},
            on_release=self.save_data
        )
        self.fl.add_widget(self.txt1)
        self.fl.add_widget(self.txt2)
        self.fl.add_widget(self.txt3)
        self.fl.add_widget(btn_save_data)

        self.fl.add_widget(self.dp)

        self.add_widget(self.fl)

    def next(self, instance):
        self.manager.current = "Main"

    def save_data(self, instance):
        global min_temp, min_hum_air, min_hum_earth
        if self.txt1.text is not None and self.txt1.text != "":
            min_temp = float(self.txt1.text)

        if self.txt2.text is not None and self.txt2.text != "":
            min_hum_air = float(self.txt2.text)

        if self.txt3.text is not None and self.txt3.text != "":
            min_hum_earth = float(self.txt3.text)


class MainApp(MDApp, Screen):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.sm = ScreenManager(transition=NoTransition())

    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Dark"
        self.title = 'Умная теплица'

        self.sm.add_widget(MainScreen())
        self.sm.add_widget(TabelScreen())

        self.sm.add_widget(ExtraScreen())
        self.sm.add_widget(EditScreen())
        self.sm.add_widget(SecondScreen())
        Clock.schedule_once(self.updateAppData, 0)
        Clock.schedule_interval(self.updateAppData, 10)
        return self.sm

    def updateAppData(self, *args):
        for i in range(0, 6):
            pass
        new_data_row = []
        average_temp1 = 0
        average_hum_air1 = 0
        for i in range(1, 4 + 1):
            res = get(f"{url}/temp_hum/{i}").text
            temp = splitting_for(res)["temperature"]
            average_temp1 += temp
            hum = splitting_for(res)["humidity"]
            average_hum_air1 += hum
            new_data_row.append(
                (i,
                 temp,
                 hum,
                 ))
            cursor.execute(f"""INSERT INTO tabel(id, temperature, humidity_air) 
            VALUES("{i}", "{temp}", "{hum}");
        """)
            global average_temp, average_hum_air
            average_temp = average_temp1 // 4
            average_hum_air = average_temp1 // 4
            print(min_temp, min_hum_earth, min_hum_air)
            print(average_temp, average_hum_earth, average_hum_air)
            print("  ")
            db.commit()

    def main_call(self):
        self.sm.current = "Main"

    def edit_call(self):
        self.sm.current = "Edit"

    def extra_mode(self):
        self.sm.current = "ExtraMode"

    def table_info(self):
        self.sm.current = "Table"

    def popup(self, text1):
        layout = GridLayout(cols=1, padding=5)

        popupLabel = MDLabel(
            text=f"ср. влж. возуха: {average_hum_air} огр. влж. воздуха: {min_hum_air}\nср. температура: {average_temp} огр. температура: {min_temp}")
        closeButton = MDRectangleFlatButton(text="Ок")

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        popup = Popup(title='Дата', content=layout,
                      auto_dismiss=False)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)


if __name__ == "__main__":
    MainApp().run()
