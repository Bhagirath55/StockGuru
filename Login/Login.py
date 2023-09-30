
import yfinance as yf
from datetime import date,  timedelta
import statsmodels.api as sm
import pmdarima as pm
from database import Database

import re

import kivy
import mysql.connector
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog

kivy.require('2.0.0')

# Database connection (unchanged)

# Define your FirstPage class with corrections


class FirstPage(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
    pass
# Define your SecondPage class with corrections


class SecondPage(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
    pass


class ThirdPage(Screen):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
    pass

    def update_prediction_label(self, prediction_text):

        self.ids.result.text = prediction_text

    pass


# Your main application class


class StockGuru(MDApp):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # Initialize database cursor and dialog

        self.dialog = MDDialog()

    def build(self):
        # Configure app theme (unchanged)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        # Create a ScreenManager and add your login
        screen_manager = ScreenManager()
        screen_manager.add_widget(FirstPage(name="first_page"))
        screen_manager.add_widget(SecondPage(name="second_page"))
        screen_manager.add_widget(ThirdPage(name="third_page"))

        return screen_manager

    def predict_stock(self, ticker):
        end_date = date.today()
        print(end_date)
        start_date = date.today() - timedelta(days=1825)
        print(start_date)
        data = yf.download(ticker, start_date, end_date, progress=False)
        data["Date"] = data.index
        data = data[["Date", "Open", "Low", "Close", "Adj Close", "Volume"]]
        data.reset_index(drop=True, inplace=True)

        model = pm.auto_arima(data['Close'], seasonal=True, m=24,
                              stepwise=True, trace=True)
        p, d, q = model.order

        model = sm.tsa.statespace.SARIMAX(data['Close'], order=(p, d, q), seasonal_order=(p, d, q, 24))
        model = model.fit()
        model.summary()

        prediction_text = model.predict(len(data), len(data) + 10)
        print(prediction_text)
        prediction_text = prediction_text.tolist()
        prediction_text = str(prediction_text)

        self.root.get_screen('third_page').update_prediction_label(prediction_text)

    # Function to show a message  in the dialog

    def show_message(self, message):
        self.dialog.text = message
        self.dialog.open()

    # Function to close the dialog
    def close_message(self):
        self.dialog.dismiss()

    # Function to validate email format
    def validate_email(self, email):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(email_pattern, email):
            self.root.get_screen('second_page').ids.email_error_label.text = ""
        else:
            self.root.get_screen('second_page').ids.email_error_label.text = "Invalid Email"

    # Function to check if a user with the provided username and password exists
    def check_user_sign_in(self, username, password):
        try:
            Database.cursor.execute(f"SELECT * FROM sign_up_credentials WHERE username='{username.text}'"
                                f" AND password='{password.text}'")
            existing_user = Database.cursor.fetchone()
            return existing_user is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    # Function to handle the sign-in process
    def sign_in(self, username, password):
        if self.check_user_sign_in(username, password):
            # User exists, allow sign-in
            self.show_message("Welcome To StockGuru")
            self.root.current = 'third_page'
            # Here, you can navigate to another screen or perform any actions needed for sign-in success.
        else:
            # User doesn't exist or incorrect password, display an error message
            self.show_message("Sign-In Failed: User not found or incorrect password")
            # You can display an error message to the user using your screen structure.

    # Function to handle sign-up
    def sign_up(self, username, email, password, password2):
        try:
            Database.cursor.execute(f"SELECT * FROM sign_up_credentials WHERE username='{username.text}'")
            existing_user = Database.cursor.fetchone()
            if existing_user:
                # Username already exists, display an error message
                self.show_message("Username Already Exists. Please Choose a Different Username")
            else:
                # Insert the new user into the database
                if password.text == password2.text:
                    Database.cursor.execute(f"INSERT INTO login_users (username,password)"
                                        f"VALUES('{username.text}','{password.text}')")
                    Database.cursor.execute(f"INSERT INTO sign_up_credentials(username, email, password)"
                                        f" VALUES ('{username.text}', '{email.text}', '{password.text}')")
                    Database.mydb.commit()
                    self.show_message("Username Added successfully!")
                else:
                    self.show_message("Password Doesn't Matched Please Re-enter")
                    # Here, you can navigate to another screen or perform any actions needed for sign-up success.
        except mysql.connector.Error as err:
            # Handle any database errors here
            print(f"Error: {err}")


if __name__ == "__main__":
    # Set the initial window size and run the app
    Window.size = (360, 640)
    chu
    Builder.load_file("../wedget/login.kv")
    Builder.load_file("../wedget/signup.kv")
    Builder.load_file("../wedget/home.kv")

    #Builder.load_file("signup.kv")
    StockGuru().run()
