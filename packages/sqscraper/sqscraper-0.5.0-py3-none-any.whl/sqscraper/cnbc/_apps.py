"""
"""

import bs4
import pandas as pd
import requests


class Apps:
    """
    """
    _address = "https://apps.cnbc.com/view.asp"

    def __init__(self, symbol: str, uid: str):
        self.symbol, self.uid = symbol, uid

        self._params = {"symbol": self.symbol, "uid": self.uid}
        self._response = requests.get(self._address, params=self._params, timeout=100)
        self._url = self._response.url

        self._soup = bs4.BeautifulSoup(self._response.text, features="lxml")
        self._dataframes = pd.read_html(self._url)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(symbol={self.symbol}, uid={self.uid})"


class PageSection:
    """
    """
    def __init__(self, symbol: str, soup: bs4.BeautifulSoup):
        self.symbol, self._soup = symbol, soup

    def __repr__(self) -> str:
        return f"{type(self).__name__}(symbol={self.symbol})"
