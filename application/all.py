from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from application.login_page import LoginPage
from application.signup_page import SignUpPage
from application.home_page import HomePage
from application.prediction_page import PredictionPage
import re
from database.stock_database import connect_db, create_signup_table
from database.database_operations import create_user
from database.database_operations import authenticate_user
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import SlideTransition
import yfinance as yf
from kivy.uix.screenmanager import Screen
from datetime import date, timedelta
import statsmodels.api as sm
import pmdarima as pm
import matplotlib.pyplot as plt
from kivy.clock import Clock
from kivy.uix.image import Image
import pandas as pd
import pytz
import time
import os
from kivymd.uix.dialog import MDDialog


class StockGuru(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        # Configure app theme (unchanged)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        # Create a ScreenManager and add your login
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginPage(name="login_page"))
        screen_manager.add_widget(SignUpPage(name="signup_page"))
        # screen_manager.add_widget(HomePage(name="home_page"))
        screen_manager.add_widget(HomePage(name="home_page"))
        screen_manager.add_widget(PredictionPage(name="prediction_page"))
        screen_manager.add_widget(HomePage(name="screen3"))

        return screen_manager


class SignUpPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dialog = MDDialog()

        self.conn, self.cursor = connect_db()
        create_signup_table(self.conn, self.cursor)

    def register_user(self, username, email, password):
        result = create_user(username, email, password)
        if result:
            self.display_message("Registration successful")
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

    def close_message(self, dt=None):
        self.dialog.dismiss()

    pass


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog()

    def login(self, username, password):
        if authenticate_user(username, password):
            self.display_message("Login successful")
            self.manager.current = 'home_page'
        else:
            self.display_message("Invalid username or password")

    def display_message(self, message):
        self.dialog.text = message
        self.dialog.open()
        Clock.schedule_once(self.close_message, 1)

    def close_message(self, dt=None):
        self.dialog.dismiss()

    pass


class Screen1(Screen):
    pass


class Screen3(Screen):
    pass


class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = None

    def on_tab_switch(self, tab_name):
        screen_manager = self.manager
        if tab_name == 'screen1':
            screen_manager.transition = SlideTransition(direction="right")
            screen_manager.current = 'screen1'
        elif tab_name == 'prediction_page':
            screen_manager.transition = SlideTransition(direction="left")
            screen_manager.current = 'prediction_page'
        elif tab_name == 'screen3':
            screen_manager.transition = SlideTransition(direction="up")
            screen_manager.current = 'screen3'

    def on_start(self):
        self.dropdown = MDDropdownMenu(
            caller=self.ids.custom_dropdown_button,
            items=[
                {"text": "Logout", "viewclass": "OneLineListItem", "on_release": self.handle_logout},
                {"text": "Profile", "viewclass": "OneLineListItem", "on_release": self.handle_profile},
                {"text": "Settings", "viewclass": "OneLineListItem", "on_release": self.handle_settings},
            ], width_mult=2
        )
        self.dropdown.open()

    def close_logout_confirmation(self, instance):
        self.logout_dialog.dismiss()

    def handle_logout(self, instance):
        print("Logout selected")
        self.dropdown.dismiss()

    def handle_profile(self, instance):
        print("Profile selected")
        self.dropdown.dismiss()

    def handle_settings(self, instance):
        print("Settings selected")
        self.dropdown.dismiss()

    def fetch_stock_prices(self, dt=None):
        try:
            nifty50_ticker = "^NSEI"
            banknifty_ticker = "^NSEBANK"
            sensex_ticker = "^BSESN"
            reliance_ticker = "RELIANCE.NS"
            itc_ticker = "ITC.NS"
            infosys_ticker = "INFY.NS"

            # Fetch NIFTY 50 data
            nifty50_data = yf.Ticker(nifty50_ticker).history(period="1d")
            if not nifty50_data.empty:
                nifty50_close_price = nifty50_data["Close"].iloc[0]
                self.ids.nifty50.price_label = f"NIFTY50 {nifty50_close_price:.1f}"
            else:
                self.ids.nifty50.price_label = "NIFTY 50 Data not available"

            # Fetch Bank NIFTY data
            banknifty_data = yf.Ticker(banknifty_ticker).history(period="1d")
            if not banknifty_data.empty:
                banknifty_close_price = banknifty_data["Close"].iloc[0]
                self.ids.banknifty.price_label = f"BankNifty {banknifty_close_price:.1f}"
            else:
                self.ids.banknifty.price_label = "Bank NIFTY Data not available"

            # Fetch SENSEX data
            sensex_data = yf.Ticker(sensex_ticker).history(period="1d")
            if not sensex_data.empty:
                sensex_close_price = sensex_data["Close"].iloc[0]
                self.ids.sensex.price_label = f"SENSEX {sensex_close_price:.1f}"
            else:
                self.ids.sensex.price_label = "SENSEX Data not available"

            # Fetch Reliance Industries Limited data
            reliance_data = yf.Ticker(reliance_ticker).history(period="1d")
            if not reliance_data.empty:
                reliance_close_price = reliance_data["Close"].iloc[0]
                self.ids.reliance.price_label = f"Reliance {reliance_close_price:.1f}"
            else:
                self.ids.reliance.price_label = "Reliance Data not available"

            # Fetch ITC Limited data
            itc_data = yf.Ticker(itc_ticker).history(period="1d")
            if not itc_data.empty:
                itc_close_price = itc_data["Close"].iloc[0]
                self.ids.itc.price_label = f"ITC {itc_close_price:.1f}"
            else:
                self.ids.itc.price_label = "ITC Data not available"

            # Fetch Infosys Limited data
            infosys_data = yf.Ticker(infosys_ticker).history(period="1d")
            if not infosys_data.empty:
                infosys_close_price = infosys_data["Close"].iloc[0]
                self.ids.infosys.price_label = f"Infosys {infosys_close_price:.1f}"
            else:
                self.ids.infosys.price_label = "Infosys Data not available"

        except Exception as e:
            print(f"Error: {e}")

    def on_pre_enter(self):
        self.fetch_stock_prices()
        Clock.schedule_interval(self.fetch_stock_prices, 120)


class PredictionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.previous_image_path = None
        self.dialog = MDDialog()
        self.predictions = None

    def predict_stock(self):
        stock_ticker = self.ids.stock_ticker.text
        no_of_days = self.ids.no_of_days.text
        if not stock_ticker:
            self.display_message("Please enter a valid stock ticker.")
        elif not no_of_days:
            self.display_message("Please enter a valid number of days.")
        else:
            try:
                no_of_days = int(no_of_days)
                if no_of_days <= 0:
                    self.display_message("Please start from 1 day.")
                elif no_of_days >= 16:
                    self.display_message("You can predict a maximum of 15 days.")
                else:
                    self.display_stock_predictions(stock_ticker, no_of_days, self.ids.graph_layout)
            except ValueError:
                self.display_message("Please enter a valid number of days.")

    def display_stock_predictions(self, stock_ticker, no_of_days, graph_layout=None):
        try:
            no_of_days = int(no_of_days)
            end_date = date.today()
            start_date = date.today() - timedelta(days=1095)
            data = yf.download(stock_ticker, start_date, end_date, progress=False)
            data["Date"] = data.index
            data = data[["Date", "Open", "Low", "Close", "Adj Close", "Volume"]]
            data.reset_index(drop=True, inplace=True)
            data.set_index("Date", inplace=True)
            data = data[["Close"]]

            # Display "Processing Graph Image" message with a slight delay
            self.update_message("Processing Graph Image...")
            Clock.schedule_once(lambda dt: self.process_image(data, no_of_days, graph_layout),
                                0.1)  # Delay for 0.1 seconds

        except Exception as e:
            print(f"Error:{e}")

    def process_image(self, data, no_of_days, graph_layout):
        try:
            model = pm.auto_arima(data['Close'], seasonal=True, m=36, stepwise=True, trace=True)
            p, d, q = model.order

            model = sm.tsa.statespace.SARIMAX(data['Close'], order=(p, d, q), seasonal_order=(p, d, q, 36))
            model = model.fit()
            self.predictions = model.predict(len(data), len(data) + no_of_days)

            fig, ax = plt.subplots(figsize=(12, 6))
            indian_tz = pytz.timezone('Asia/Kolkata')
            data.index = data.index.tz_localize(pytz.utc).tz_convert(indian_tz)
            data["Close"].plot(legend=True, label="Training Data", linestyle='--', ax=ax)
            ax.set_xlabel('Date and Time (IST)')
            ax.set_ylabel('Closing Price')
            last_date = data.index[-1]
            prediction_dates = pd.date_range(start=last_date + timedelta(days=1), periods=len(self.predictions))
            self.predictions.index = prediction_dates
            self.predictions.plot(legend=True, label="Predictions", linestyle='--', ax=ax)

            timestamp = str(int(time.time()))
            image_path = f'kivy_files/prediction_graph_{timestamp}.png'
            fig.savefig(image_path)

            if graph_layout is not None:
                # Update the source of the prediction_image
                prediction_image = self.ids.prediction_image
                prediction_image.source = image_path

                for widget in graph_layout.children[:]:
                    if isinstance(widget, Image):
                        graph_layout.remove_widget(widget)

                image_size = (800, 800)
                image = Image(source=image_path, size=image_size)
                graph_layout.add_widget(image)

                # Remove the previous image if it exists
                if self.previous_image_path:
                    try:
                        os.remove(self.previous_image_path)
                    except OSError:
                        pass

                # Update the previous_image_path
                self.previous_image_path = image_path

                # Schedule the message update to run in the next frame
                Clock.schedule_once(lambda dt: self.update_message("Graph Image Processed Successfully"))

        except:
            self.display_message(f"Error: Please Enter A Valid Stock-Ticker(www.yahoofinance.com)")

    def show_predicted_prices(self):
        # Check if predictions exist
        if self.predictions is not None and self.predictions.any():
            # Create a dialog to display the predicted prices
            predicted_prices = "\n".join([f"Predicted Price: {price:.2f}" for price in self.predictions])
            dialog = MDDialog(title="Predicted Prices", text=predicted_prices, size_hint=(0.8, 0.8))
            dialog.open()
        else:
            self.display_message("No predictions available.")

    def update_message(self, text):
        self.ids.message_label.text = text
        self.ids.message_label.opacity = 1

    def display_message(self, message):
        self.dialog.text = message
        self.dialog.open()
        Clock.schedule_once(self.close_message, 5)

    def close_message(self, dt=None):
        self.dialog.dismiss()


if __name__ == "__main__":
    # Set the initial window size and run the app
    # Window.size = (360, 640)
    Builder.load_file('kivy_files/login.kv')
    Builder.load_file('kivy_files/signup.kv')
    Builder.load_file('kivy_files/home.kv')
    Builder.load_file('kivy_files/prediction.kv')
    StockGuru().run()
