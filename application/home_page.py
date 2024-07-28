import yfinance as yf
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton


class LogoutDialog(MDDialog):
    def __init__(self, home_page, **kwargs):
        self.home_page = home_page
        super().__init__(
            type="confirmation",
            title="Logout",
            text="Are you sure you want to logout?",
            buttons=[
                MDRaisedButton(text="No", on_release=self.dismiss),
                MDRaisedButton(text="Yes", on_release=lambda instance: self.handle_logout()),
            ],
            **kwargs
        )

    def handle_logout(self, *args):
        self.home_page.manager.get_screen('login_page').clear_credentials()
        self.home_page.manager.current = 'login_page'
        self.home_page.clear_dropdown()
        self.dismiss()


class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = None
        self.logout_dialog = LogoutDialog(self)

    def on_tab_switch(self, tab_name):
        screen_manager = self.manager
        if tab_name == 'screen1':
            screen_manager.transition = SlideTransition(direction="right")
            screen_manager.current = 'screen1'
        elif tab_name == 'prediction_page':
            screen_manager.transition = SlideTransition(direction="left")
            screen_manager.current = 'prediction_page'
        elif tab_name == 'stock_news':
            screen_manager.transition = SlideTransition(direction="up")
            screen_manager.current = 'stock_news'

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

    def close_logout_confirmation(self):
        self.logout_dialog.dismiss()

    def handle_logout(self):
        self.logout_dialog.open()
        print("Logout selected")

    def clear_dropdown(self):
        self.dropdown.items = []
        self.ids.custom_dropdown_button.text = ""
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
        Clock.schedule_interval(self.fetch_stock_prices, 300)
