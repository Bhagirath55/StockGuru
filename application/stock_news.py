from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarListItem
from kivymd.uix.list import ImageLeftWidget
from newsapi import NewsApiClient


class NewsListItem(TwoLineAvatarListItem):
    pass


class StockNews(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.news_api_key = "YOUR_NEWS_API_KEY"  # Replace with your News API key
        self.newsapi = NewsApiClient(api_key=self.news_api_key)

    def on_pre_enter(self):
        self.fetch_stock_news()

    def fetch_stock_news(self):
        try:
            # Fetch stock-related news
            news_articles = self.newsapi.get_top_headlines(q="stock", language="en", country="us", page_size=5)
            articles = news_articles["articles"]

            # Display news in the application
            for article in articles:
                news_item = NewsListItem(
                    text=article["title"],
                    secondary_text=article["description"],
                )
                news_item.add_widget(ImageLeftWidget(source=article["urlToImage"]))
                self.ids.news_list.add_widget(news_item)

        except Exception as e:
            print(f"Error: {e}")
