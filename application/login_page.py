from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from database.database_operations import authenticate_user
from kivy.clock import Clock


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog()

    def login(self, username, password):
        if self.ids.user.text == "":
            self.display_message_for_validation("username field can not be empty")
        elif self.ids.psswd.text == "":
            self.display_message_for_validation("password field can not be empty")
        elif authenticate_user(username, password):
            self.display_message("Login successful")
            self.manager.current = 'home_page'
        else:
            self.display_message("Invalid username or password")

    def display_message(self, message):
        self.dialog.text = message
        self.dialog.open()
        Clock.schedule_once(self.close_message, 2)

    def close_message(self, dt=None):
        self.dialog.dismiss()

    def clear_credentials(self):
        self.ids.user.text = ""
        self.ids.psswd.text = ""

    def display_message_for_validation(self, message):
        self.dialog.text = message
        self.dialog.open()
        Clock.schedule_once(self.close_message, 3)