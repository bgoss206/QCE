import math

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from kivy.uix.button import Button
import smtplib, ssl
from kivy.uix.scrollview import ScrollView
from sundry import Sundry
from os.path import join
from datetime import date
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

class CreateAccountWindow(Screen):
    Window.clearcolor = (1, 1, 1, 1)
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    current_user = ''

    def on_enter(self):
        self.reset()

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            self.current_user = db.get_user(self.email.text)
            sm.current = "menu"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class Email:
    def __init__(self, user, password, equipment, supplies, sender):
        self.user = user
        self.password = password
        self.subjectLine = 'Sundries Needed for ' + sender + 'on ' + str(date.today().strftime("%b-%d-%Y"))
        self.equipment = equipment
        self.supplies = supplies
        port = 465
        self.recipients = ['Braxtonagoss@gmail.com']

        messageToSend = """Subject: {subject}

            Supplies: {supplies}
            
            Equipment: {equipment}

            """.format(subject=self.subjectLine, supplies=self.supplies, equipment=self.equipment)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.user, self.password)
            server.sendmail(self.user, self.recipients, messageToSend)

        print("sent email")


class WindowManager(ScreenManager):
    pass


# FIGURE OUT HOW THIS WORKS WITH SMALLER SIZES
def findFontSize(intended_shadow_font_size, container):
    return str((container.width ** 2 + container.height ** 2) / (intended_shadow_font_size ** 4)) + 'dp'


def sendEmail(username, password, equipment, supplies, sender_name):
    Email(username, password, equipment, supplies, sender_name)


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(0.5, 0.5))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(0.5, 0.5))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")



class NavigatorMenu(Screen):

    def logOut(self):
        sm.current = "login"

    def on_enter(self):
        pass


class SupplySelection(Screen):
    # bool to prevent replacing everything in on_enter
    hasBeenEntered = False

    # storage list for btns to grab state
    supplies_list = []

    # selection of lists (no duplicates)
    supply_selection = []

    def logOut(self):
        sm.current = "login"

    def on_leave(self):

        self.hasBeenEntered = True

        for i in self.supplies_list:
            if i.state == 'down' and i.text not in self.supply_selection:
                self.supply_selection.append(i.text)
            else:
                continue

    def on_enter(self):
        if self.hasBeenEntered:
            pass
        else:

            # TODO: RGB OF RED: 237, 24, 32 ::: RGB OF BLUE: 8, 21, 73
            # fetch supplies and equipment from xl file
            sundries = Sundry(join('Sundries.xlsx'))
            supplies = sundries.get_supplies()

            # add title button and make list scrollable
            titleBtnSupplies = Button(text=supplies[0], font_size=findFontSize(18, self),
                                      size_hint=(0.8, 0.2), pos_hint={'x': 0, 'y': 0.8},
                                      background_color=(8 / 255, 21 / 255, 73 / 255, 1))

            rootSupplies = ScrollView(size_hint=(0.8, 0.8))

            layoutForSupplies = GridLayout(cols=1, spacing=1, size_hint=(1, None))
            layoutForSupplies.bind(minimum_height=layoutForSupplies.setter('height'))

            # adds supply buttons to page
            for i in range(1, len(supplies), 1):
                btn = ToggleButton(text=supplies[i], font_size=findFontSize(12, self),
                                   size_hint_x=titleBtnSupplies.size_hint_x, size_hint_y=None,
                                   height=(Window.height / 20), background_normal='QCE-Red.png',
                                   background_down='QCE-Blue.png')
                self.supplies_list.append(btn)
                layoutForSupplies.add_widget(btn)

            rootSupplies.add_widget(layoutForSupplies)

            self.add_widget(rootSupplies)

            self.add_widget(titleBtnSupplies)


class EquipmentSelection(Screen):
    # bool to prevent replacing everything in on_enter
    hasBeenEntered = False

    # storage list for btns to grab state
    equipment_list = []

    def logOut(self):
        sm.current = "login"

    def on_leave(self):
        self.hasBeenEntered = True

    def on_enter(self):
        if self.hasBeenEntered:
            pass
        else:

            # TODO: RGB OF RED: 237, 24, 32 ::: RGB OF BLUE: 8, 21, 73
            # fetch supplies and equipment from xl file
            sundries = Sundry(join('Sundries.xlsx'))
            equipment = sundries.get_equipment()

            # add title button and make list scrollable
            titleBtnEquipment = Button(text=equipment[0], font_size=findFontSize(18, self),
                                       size_hint=(0.8, 0.2), pos_hint={'x': 0, 'y': 0.8},
                                       background_color=(8 / 255, 21 / 255, 73 / 255, 1))

            rootEquipment = ScrollView(size_hint=(0.8, 0.8))

            layoutForEquipment = GridLayout(cols=1, spacing=1, size_hint=(1, None))
            layoutForEquipment.bind(minimum_height=layoutForEquipment.setter('height'))

            # adds supply buttons to page
            for i in range(1, len(equipment), 1):
                btn = ToggleButton(text=equipment[i], font_size=findFontSize(12, self),
                                   size_hint_x=titleBtnEquipment.size_hint_x, size_hint_y=None,
                                   height=(Window.height / 20), background_normal='QCE-Red.png',
                                   background_down='QCE-Blue.png')
                self.equipment_list.append(btn)
                layoutForEquipment.add_widget(btn)

            rootEquipment.add_widget(layoutForEquipment)

            self.add_widget(rootEquipment)

            self.add_widget(titleBtnEquipment)


class SundryConfirmation(Screen):

    def set_screen(self):
        sm.current = 'menu'

    hasBeenEntered = False

    if hasBeenEntered:
        pass
    else:

        def on_enter(self):
            requested_sundries_supplies = []
            requested_sundries_equipment = []
            username = LoginWindow.current_user
            combined_list = requested_sundries_equipment + requested_sundries_supplies

            for j in SupplySelection.supplies_list:
                if j.state == 'down':
                    requested_sundries_supplies.append(j.text)

            for i in EquipmentSelection.equipment_list:
                if i.state == 'down':
                    requested_sundries_equipment.append(i.text)

            if (not requested_sundries_supplies) and (not requested_sundries_equipment):

                noneSelected = Button(text='No Sundries\n  Selected\n  Return to \n  Main Menu',
                                      font_size=findFontSize(15, self),
                                      size_hint=(0.5, 0.5), pos_hint={'x': 0.2, 'y': 0.2},
                                      background_normal='QCE-Red.png',
                                      background_down='QCE-Blue.png', on_release= lambda x: self.set_screen())
                self.add_widget(noneSelected)

            else:

                self.add_widget(Label(text='Selected Items', font_size=findFontSize(15, self),
                                      pos_hint={'x': 0.1, 'y': 0.9}, color=(237 / 255, 24 / 255, 32 / 255, 1)))

                email_button = Button(text='Email Warehouse', font_size=findFontSize(15, self),
                                      size_hint=(0.2, 0.1), pos_hint={'x': 0.8, 'y': 0.5},
                                      background_normal='QCE-Red.png', background_down='QCE-Blue.png')

                email_button.bind(on_release=lambda x: sendEmail('codingBrax@gmail.com', 'codingForPaintWA',
                                                                 requested_sundries_equipment,
                                                                 requested_sundries_supplies,
                                                                 'tester'))
                self.add_widget(email_button)


screens = [CreateAccountWindow(name="create"), LoginWindow(name="login"), NavigatorMenu(name="menu"),
           SupplySelection(name="supplies"), EquipmentSelection(name="equip"), SundryConfirmation(name="confirm")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
