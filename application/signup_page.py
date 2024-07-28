import re
from kivy.uix.screenmanager import Screen
from database.stock_database import connect_db, create_signup_table
from database.database_operations import create_user
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock


class SignUpPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dialog = MDDialog()

        self.conn, self.cursor = connect_db()
        create_signup_table(self.conn, self.cursor)

    def register_user(self, username, email, password):
        result = create_user(username, email, password)
        if self.ids.user2.text == "" and self.ids.email.text == "" and self.ids.psswd1.text == "":
            self.display_message_for_validation("Please provide all the detail")
        elif self.ids.user2.text == "":
            self.display_message_for_validation("username field can not be empty")
        elif self.ids.email.text == "":
            self.display_message_for_validation("Email field can not be empty")
        elif self.ids.psswd1.text == "":
            self.display_message_for_validation("Password field can not be empty")
        elif self.ids.psswd2.text == "":
            self.display_message_for_validation("Password field can not be empty")
        elif self.ids.psswd1.text != self.ids.psswd2.text:
            self.display_message_for_validation("password and confirm password should be same")
        elif result:
            self.display_message("Registration successful")
            self.manager.current = "login_page"
        else:
            self.display_message("User with the same username or email already exists")

    def validate_email(self, email):
        if not email:
            # Empty email field, clear any previous error messages
            self.ids.email_error_label.text = ""
        else:
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(email_pattern, email):
                self.ids.email_error_label.text = ""
            else:
                self.ids.email_error_label.text = "Invalid Email"

    def display_message(self, message):
        self.dialog.text = message
        self.dialog.open()
        Clock.schedule_once(self.close_message, 2)

    def display_message_for_validation(self, message):
        self.dialog.text = message
        self.dialog.open()
        Clock.schedule_once(self.close_message, 3)

    def close_message(self, dt=None):
        self.dialog.dismiss()

    pass
