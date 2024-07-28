from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from application.login_page import LoginPage
from application.signup_page import SignUpPage
from application.home_page import HomePage
from application.prediction_page import PredictionPage
from application.stock_news import StockNews


class StockGuru(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginPage(name="login_page"))
        screen_manager.add_widget(SignUpPage(name="signup_page"))
        screen_manager.add_widget(HomePage(name="home_page"))
        screen_manager.add_widget(PredictionPage(name="prediction_page"))
        screen_manager.add_widget(StockNews(name="stock_news"))

        return screen_manager


if __name__ == "__main__":
    Builder.load_file('kivy_files/login.kv')
    Builder.load_file('kivy_files/signup.kv')
    Builder.load_file('kivy_files/home.kv')
    Builder.load_file('kivy_files/prediction.kv')
    Builder.load_file('kivy_files/stock_news.kv')
    StockGuru().run()
