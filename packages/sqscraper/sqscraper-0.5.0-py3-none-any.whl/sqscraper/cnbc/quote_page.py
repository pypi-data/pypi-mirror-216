"""
"""

import datetime
import math
import typing

import numpy as np
import pandas as pd
import requests

from sqscraper.utils import expand_value
from sqscraper.utils import normalize_value


class Quote:
    """
    :param data:
    """
    def __init__(self, data: typing.Dict[str, typing.Any]):
        self.data = data

        self.quote_strip = QuoteStrip(self.symbol, self.data)
        try:
            self.ext_quote_strip = ExtQuoteStrip(self.symbol, self.data["ExtendedMktQuote"])
        except KeyError:
            self.ext_quote_strip = None

        self.key_stats = KeyStats(self.symbol, self.data)
        self.ratios = Ratios(self.symbol, self.data)
        self.events = Events(self.symbol, self.data["EventData"])

    def __repr__(self) -> str:
        argnames = ("symbol", "name", "exchange")
        arguments = ", ".join(f"{x}={self.__getattribute__(x)}" for x in argnames)

        return f"{type(self).__name__}({arguments})"

    def __getitem__(self, key: str) -> str:
        return self.data[key]

    @property
    def symbol(self) -> str:
        """
        """
        return self["symbol"]

    @property
    def name(self) -> str:
        """
        """
        return self["name"]

    @property
    def exchange(self) -> str:
        """
        """
        return self["exchange"]


class StockQuotes:
    """
    :param symbols: Ticker symbols to look up
    """
    _address = "https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol"

    def __init__(self, *symbols: str):
        self.symbols = tuple(set(symbols))

        self._params = {
            "symbols": "|".join(self.symbols), "fund": 1, "exthrs": 1, "events": 1
        }
        self._response = requests.get(self._address, params=self._params, timeout=100)

        self._url = self._response.url
        self._json = self._response.json()
        self._result = self._json["FormattedQuoteResult"]["FormattedQuote"]

    def __repr__(self) -> str:
        return f"{type(self).__name__}(symbols={self.symbols})"

    def __len__(self) -> int:
        return len(self.symbols)

    def __getitem__(self, key: str) -> str:
        return self.quotes[key]

    def __contains__(self, item: str) -> bool:
        return item in self.symbols

    @classmethod
    def get_quote(cls, symbol: str, **kwargs) -> Quote:
        """
        :param symbol:
        :param kwargs:
        :return:
        """
        return cls(symbol, **kwargs)[symbol]

    @property
    def data(self) -> typing.Dict[str, typing.Any]:
        """
        """
        return dict(zip(self.symbols, self._result))

    @property
    def quotes(self) -> typing.Dict[str, Quote]:
        """
        """
        return dict(zip(self.symbols, map(Quote, self._result)))


class QuoteStrip:
    """
    :param data:
    """
    def __init__(self, symbol: str, data: typing.Dict[str, typing.Any]):
        self.symbol = symbol
        self._data = data
        
    def __repr__(self) -> str:
        argnames = (
            "symbol", "market_status", "last", "last_time", "change", "change_pct", "volume"
        )
        arguments = ", ".join(f"{x}={self.__getattribute__(x)}" for x in argnames)

        return f"{type(self).__name__}({arguments})"

    def __str__(self) -> str:
        return "{}: {} {} ({})".format(
            self.symbol,
            self.last,
            "UNCH" if math.isnan(self.change) else f"{self.change_type}{self.change}",
            "UNCH" if math.isnan(self.change_pct) else f"{self.change_type}{self.change_pct}",
        )

    def __getitem__(self, key: str) -> str:
        return self._data[key]

    @property
    def market_status(self) -> str:
        """
        """
        return self["curmktstatus"]

    @property
    def last(self) -> float:
        """
        """
        return float(self["last"])

    @property
    def last_time(self) -> datetime.datetime:
        """
        """
        try:
            return datetime.datetime.strptime(self["last_time"], "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            return datetime.datetime.strptime(self["last_time"], "%Y-%m-%d")

    @property
    def change_type(self) -> str:
        """
        """
        return {"UP": "+", "DOWN": "-", "UNCH": "="}[self["changetype"]]

    @property
    def change(self) -> float:
        """
        """
        if self["change"] == "UNCH":
            return np.nan
        return float(self["change"])

    @property
    def change_pct(self) -> float:
        """
        """
        if self["change_pct"] == "UNCH":
            return np.nan
        return float(normalize_value(self["change_pct"]))

    @property
    def volume(self) -> int:
        """
        """
        return int(normalize_value(self["volume"]))


class ExtQuoteStrip(QuoteStrip):
    """
    :param data:
    """
    @property
    def market_status(self) -> str:
        """
        """
        return self["type"]


class QuotePageSection:
    """
    """
    def __init__(self, symbol: str, data: typing.Dict[str, typing.Any]):
        self.symbol = symbol
        self._data = data

    def __repr__(self) -> str:
        return f"{type(self).__name__}(symbol={self.symbol})"

    def __getitem__(self, key: str) -> str:
        return self._data[key]

    @property
    def series(self) -> pd.Series:
        """
        """
        raise NotImplementedError

    @staticmethod
    def quote_data(
        method: typing.Callable[["QuotePageSection"], typing.Union[int, float, datetime.datetime]]
    ) -> typing.Callable[["QuotePageSection"], typing.Union[int, float, datetime.datetime]]:
        """
        :param method:
        :return:
        """
        def wrapper(self: "QuotePageSection") -> typing.Union[int, float, datetime.datetime]:
            """
            :param self:
            :return:
            """
            try:
                return method(self)
            except KeyError:
                return np.nan
        return wrapper


class KeyStats(QuotePageSection):
    """
    """
    @property
    def series(self) -> pd.Series:
        """
        """
        data = {
            "Open": self.open,
            "Day High": self.day_high,
            "Day Low": self.day_low,
            "Previous Close": self.prev_close,
            "10 Day Average Volume": self.ten_day_average_volume,
            "52 Week High": self.fiftytwo_week_high,
            "52 Week High Date": self.fiftytwo_week_high_date,
            "52 Week Low": self.fiftytwo_week_low,
            "52 Week Low Date": self.fiftytwo_week_low_date,
            "Beta": self.beta,
            "Shares Out": self.shares_out,
            "Dividend": self.dividend,
            "Dividend Yield": self.dividend_yield,
            "YTD % Change": self.ytd_pct_change
        }
        return pd.Series(data, name="Key Stats")

    @property
    @QuotePageSection.quote_data
    def open(self) -> float:
        """
        """
        return float(self["open"])

    @property
    @QuotePageSection.quote_data
    def day_high(self) -> float:
        """
        """
        return float(self["high"])

    @property
    @QuotePageSection.quote_data
    def day_low(self) -> float:
        """
        """
        return float(self["low"])

    @property
    @QuotePageSection.quote_data
    def prev_close(self) -> float:
        """
        """
        return float(self["previous_day_closing"])

    @property
    @QuotePageSection.quote_data
    def ten_day_average_volume(self) -> int:
        """
        """
        return expand_value(self["tendayavgvol"])

    @property
    @QuotePageSection.quote_data
    def fiftytwo_week_high(self) -> float:
        """
        """
        return float(self["yrhiprice"])

    @property
    @QuotePageSection.quote_data
    def fiftytwo_week_high_date(self) -> datetime.datetime:
        """
        """
        return datetime.datetime.strptime(self["yrhidate"], "%m/%d/%y")

    @property
    @QuotePageSection.quote_data
    def fiftytwo_week_low(self) -> float:
        """
        """
        return float(self["yrloprice"])

    @property
    @QuotePageSection.quote_data
    def fiftytwo_week_low_date(self) -> datetime.datetime:
        """
        """
        return datetime.datetime.strptime(self["yrlodate"], "%m/%d/%y")

    @property
    @QuotePageSection.quote_data
    def beta(self) -> float:
        """
        """
        return float(self["beta"])

    @property
    @QuotePageSection.quote_data
    def market_cap(self) -> int:
        """
        """
        return expand_value(self["mktcapView"])

    @property
    @QuotePageSection.quote_data
    def shares_out(self) -> int:
        """
        """
        return expand_value(self["sharesout"])

    @property
    @QuotePageSection.quote_data
    def dividend(self) -> float:
        """
        """
        return float(self["dividend"])

    @property
    @QuotePageSection.quote_data
    def dividend_yield(self) -> float:
        """
        """
        return float(normalize_value(self["dividendyield"]))

    @property
    @QuotePageSection.quote_data
    def ytd_pct_change(self) -> float:
        """
        """
        return np.nan


class Ratios(QuotePageSection):
    """
    """
    @property
    def series(self) -> pd.Series:
        """
        """
        data = {
            "EPS (TTM)": self.eps, "P/E (TTM)": self.pe, "Fwd P/E (NTM)": self.fwd_pe,
            "Revenue (TTM)": self.revenue, "ROE (TTM, %)": self.roe, "EBITDA (TTM)": self.ebitda,
            "Gross Margin (TTM, %)": self.gross_margin, "Net Margin (TTM, %)": self.net_margin,
            "Debt To Equity (TTM, %)": self.debt_to_equity
        }
        return pd.Series(data, name="Ratios/Profitability")

    @property
    @QuotePageSection.quote_data
    def eps(self) -> float:
        """
        """
        return float(self["eps"])

    @property
    @QuotePageSection.quote_data
    def pe(self) -> float:
        """
        """
        return float(self["pe"])

    @property
    @QuotePageSection.quote_data
    def fwd_pe(self) -> float:
        """
        """
        return float(self["fpe"])

    @property
    @QuotePageSection.quote_data
    def revenue(self) -> int:
        """
        """
        return expand_value(self["revenuettm"])

    @property
    @QuotePageSection.quote_data
    def roe(self) -> float:
        """
        """
        return float(normalize_value(self["ROETTEM"]))

    @property
    @QuotePageSection.quote_data
    def ebitda(self) -> int:
        """
        """
        return expand_value(self["TTMEBITD"])

    @property
    @QuotePageSection.quote_data
    def gross_margin(self) -> float:
        """
        """
        return float(normalize_value(self["GROSMGNTTM"]))

    @property
    @QuotePageSection.quote_data
    def net_margin(self) -> float:
        """
        """
        return float(normalize_value(self["NETPROFTTM"]))

    @property
    @QuotePageSection.quote_data
    def debt_to_equity(self) -> float:
        """
        """
        return float(normalize_value(self["DEBTEQTYQ"]))


class Events(QuotePageSection):
    """
    """
    @property
    def series(self) -> pd.Series:
        """
        """
        data = {
            "Earnings Date": self.earnings_date, "Split Date": self.split_date,
            "Ex Div Date": self.ex_div_date, "Split Factor": self.split_factor,
            "Div Amount": self.div_amount
        }
        return pd.Series(data, name="Events")

    @property
    @QuotePageSection.quote_data
    def earnings_date(self) -> datetime.datetime:
        """
        """
        try:
            return datetime.datetime.strptime(self["next_earnings_date"], "%m/%d/%Y(est)")
        except ValueError:
            return datetime.datetime.strptime(self["next_earnings_date"], "%m/%d/%Y")

    @property
    @QuotePageSection.quote_data
    def split_date(self) -> datetime.datetime:
        """
        """
        return datetime.datetime.strptime(self["split_ex_date"], "%m/%d/%Y")

    @property
    @QuotePageSection.quote_data
    def ex_div_date(self) -> datetime.datetime:
        """
        """
        return datetime.datetime.strptime(self["div_ex_date"], "%m/%d/%Y")

    @property
    @QuotePageSection.quote_data
    def split_factor(self) -> float:
        """
        """
        return float(self["split_factor"])

    @property
    @QuotePageSection.quote_data
    def div_amount(self) -> float:
        """
        """
        return float(self["div_amount"])
