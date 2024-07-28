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
            start_date = date.today() - timedelta(days=1825)
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
