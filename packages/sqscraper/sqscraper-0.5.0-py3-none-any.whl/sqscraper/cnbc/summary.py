"""
"""

import datetime
import decimal
import operator
import re
import typing
import urllib.parse
import warnings

import bs4
import numpy as np
import pandas as pd
import requests

from ._apps import Apps
from ._apps import PageSection
from ._serializer import Serializer
from sqscraper.utils import expand_value
from sqscraper.utils import normalize_value


class StockSummary(Apps):
    """
    """
    def __init__(self, symbol: str):
        super().__init__(symbol, "stocks/summary")

        self.pricing_momentum = _PricingMomentum(self.symbol, self._soup)
        self.growth_rates = _GrowthRates(self.symbol, self._soup)
        self.key_measures = _KeyMeasures(self.symbol, self._soup)

    @property
    def shares(self) -> pd.Series:
        """
        """
        data = {
            "Shares Outstanding": self.shares_outstanding,
            "Institutional Ownership": self.institutional_ownership,
            "Market Cap": self.market_cap,
            "Last Stock Split (Date)": self.last_stock_split_date,
            "Last Stock Split (Ratio)": self.last_stock_split_ratio
        }
        return pd.Series(data, name="Shares")

    @property
    def shares_outstanding(self) -> int:
        """
        """
        element = self._soup.select_one("table#shares tr:nth-child(1) > td:nth-child(2)")
        return expand_value(element.text)

    @property
    def institutional_ownership(self) -> float:
        """
        """
        element = self._soup.select_one("table#shares tr:nth-child(2) > td:nth-child(2)")
        return float(element.text.strip("%"))
    
    @property
    def market_cap(self) -> int:
        """
        """
        element = self._soup.select_one("table#shares tr:nth-child(3) > td:nth-child(2)")
        return expand_value(element.text)
    
    @property
    def last_stock_split_date(self) -> typing.Optional[datetime.datetime]:
        """
        """
        element = self._soup.select_one("table#shares tr:nth-child(4) > td:nth-child(1)")
        try:
            return datetime.datetime.strptime(element.text, "Last Stock Split %m/%d/%Y")
        except ValueError:
            return np.nan
        
    @property
    def last_stock_split_ratio(self) -> typing.Optional[float]:
        """
        """
        element = self._soup.select_one("table#sharestr:nth-child(4) > td:nth-child(2)")
        regex = re.compile(r"^(.*):(.*)$")
        try:
            return float(
                operator.truediv(
                    *[decimal.Decimal(x) for x in regex.search(element.text).groups()]
                )
            )
        except AttributeError:
            return np.nan
        
    @property
    def analyst_consensus(self) -> typing.Optional[pd.Series]:
        """
        """
        element = self._soup.select_one("div#trends > img")
        if element is None:
            return

        url_components = urllib.parse.urlparse(element.attrs.get("desturl"))
        query_parameters = dict(x.split("=") for x in url_components.query.split("&"))

        ratings = ("Strong Buy", "Buy", "Hold", "Sell", "Underperform")
        return pd.Series(dict(zip(ratings, map(int, query_parameters["data"].split(",")))))


class _PricingMomentum(PageSection):
    """
    :param symbol:
    :param soup:
    """
    _post_url = "https://apps.cnbc.com/resources/asp/getBufferedChart.asp"

    def __init__(self, symbol: str, soup: bs4.BeautifulSoup):
        super().__init__(symbol, soup)

    @property
    def quote(self) -> pd.Series:
        """
        """
        data = {
            "Last": self.last,
            "Change": self.change,
            "Percent Change": self.change_pct,
            "Open": self.open,
            "Day High": self.day_high,
            "Day Low": self.day_low,
            "Volume": self.volume
        }
        return pd.Series(data, name="Quote")

    @property
    def last(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_last")
        return float(element.text)

    @property
    def change(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_chg > span")
        if element is None:
            return np.nan

        if "colUnch" in element.attrs.get("class"):
            return np.nan
        if "colPos" in element.attrs.get("class"):
            return float(element.text)
        if "colNeg" in element.attrs.get("class"):
            return -float(element.text)
        raise ValueError

    @property
    def change_pct(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_chgPct > span")
        if element is None:
            return np.nan

        if "colUnch" in element.attrs.get("class"):
            return np.nan
        return float(element.text.strip("%"))

    @property
    def open(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_open")
        return float(element.text)

    @property
    def day_high(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_high")
        return float(element.text)

    @property
    def day_low(self) -> float:
        """
        """
        element = self._soup.select_one("span#quoteTable_low")
        return float(element.text)

    @property
    def volume(self) -> int:
        """
        """
        element = self._soup.select_one("span#quoteTable_volume")
        return int("".join(element.text.split(",")))

    @property
    def performance(self) -> typing.Dict[str, str]:
        """
        """
        return {
            "spx-on": self._get_performance_chart(spx=True),
            "spx-off": self._get_performance_chart(spx=False)
        }

    @property
    def wsod_issue_symbol(self) -> str:
        """
        """
        return re.search(r"var wsodIssueSymbol = \"(\d+)\";", str(self._soup)).group(1)

    def _get_performance_chart(self, *, spx: bool = True, sma: typing.Tuple[int] = (50, 100, 200)) -> str:
        """
        :param spx:
        :param sma:
        :return:
        """
        regex = re.compile(r"^setPerformanceChartImg\('(.*)'\);$")

        params = {
            "symbol": f"{self.wsod_issue_symbol},spx" if spx else self.wsod_issue_symbol,
            "timeFrame": 365, "width": 600, "height": 120,
            "indicators": ",".join(f"sma:{x}" for x in sma)
        }
        data = {
            "params": "&".join(f"{k}={v}" for k, v in params.items()), "cht": "performance",
            "callback": "setPerformanceChartImg", "returnVars": "File.Name",
            "..contenttype..": "text/javascript", "..requester..": "ContentBuffer"
        }

        with requests.post(self._post_url, data=data, timeout=100) as response:
            return f"https://apps.cnbc.com{regex.search(response.text).group(1)}"


class _GrowthRates(PageSection):
    """
    """
    def __init__(self, symbol: str, soup: bs4.BeautifulSoup):
        super().__init__(symbol, soup)

        self._dataframes = self._scrape_chart_data()

    @property
    def earnings_per_share(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframes[0].copy()
        if dataframe.empty:
            return dataframe

        dataframe.iloc[[0, 1, 2, 4], :] = dataframe.iloc[[0, 1, 2, 4], :].applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else np.nan
        )
        dataframe.iloc[3, :] = pd.Series(dataframe.iloc[3, :], dtype="Int64")

        return dataframe

    @property
    def revenue(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframes[1].copy()
        if dataframe.empty:
            return dataframe

        dataframe.iloc[[0, 4], :] = dataframe.iloc[[0, 4], :].applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else np.nan
        )
        dataframe.iloc[1, :] = pd.Series(
            dataframe.iloc[1, :].apply(
                lambda x: int(float(normalize_value(x))) if isinstance(x, str) else np.nan
            ),
            dtype="Int64"
        )
        dataframe.iloc[2, :] = pd.Series(
            dataframe.iloc[2, :].apply(
                lambda x: int(float(normalize_value(x))) if isinstance(x, str) else np.nan
            ),
            dtype="Int64"
        )
        dataframe.iloc[3, :] = pd.Series(dataframe.iloc[3, :], dtype="Int64")

        return dataframe

    @property
    def dividend(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframes[2].copy()
        if dataframe.empty:
            return dataframe

        dataframe.iloc[[0, 1, 2, 4], :] = dataframe.iloc[[0, 1, 2, 4], :].applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else np.nan
        )
        dataframe.iloc[3, :] = pd.Series(dataframe.iloc[3, :], dtype="Int64")

        return dataframe
    
    @property
    def _javascript(self) -> str:
        """
        """
        for element in self._soup.select(
            "div#category > div.subsection > script[type='text/javascript']"
        ):
            if re.search(r"j1=\[\];.*var growthData=j1;", element.text) is not None:
                return element.text.strip()
        raise ValueError

    def _scrape_chart_data(self) -> typing.List[pd.DataFrame]:
        """
        :return:
        """
        data = []
        regex = [
            re.compile(r"^j1=\[\]$"),
            re.compile(r"^j1\[\d\]=\{\}$"),
            re.compile(r"^j1\[(\d)\]\.name=(.*?)$"),
            re.compile(r"^j1\[(\d)\]\.prefix=(.*?)$"),
            re.compile(r"^j1\[(\d)\]\.years=\[\]$"),
            re.compile(r"^j1\[(\d)\]\.years\[\d\]=\{\}$"),
            re.compile(r"^j1\[(\d)\]\.years\[(\d)\]\.(.*?)=(.*?)$")
        ]
        for statement in self._javascript.split(";"):
            results = [r.search(statement) for r in regex]
            nonnull_results = [(i, x) for i, x in enumerate(results) if x is not None]
            if len(nonnull_results) != 1:
                continue
            idx, res = nonnull_results[0]

            if idx == 0:
                continue
            elif idx == 1:
                data.append({})
            elif idx == 2:
                data[int(res.group(1))].setdefault("name", res.group(2).strip("\""))
            elif idx == 3:
                data[int(res.group(1))].setdefault("profile", res.group(2).strip("\""))
            elif idx == 4:
                data[int(res.group(1))].setdefault("years", [])
            elif idx == 5:
                data[int(res.group(1))]["years"].append({})
            elif idx == 6:
                data[int(res.group(1))]["years"][int(res.group(2))].setdefault(
                    res.group(3), res.group(4).strip("\"")
                )

        dataframes = []
        for i, record in enumerate(data):
            dataframes.append(
                pd.DataFrame({int(x["FiscalYear"]): x for x in record["years"]})
            )
            if dataframes[i].empty:
                continue
            
            dataframes[i].drop(index=["FiscalYear"], inplace=True)
            dataframes[i].index = [
                "Growth Rate", "Growth", "Mean Estimate", "Number of Estimates",
                "Industry Growth Rate"
            ]
            dataframes[i].replace("--", np.nan, inplace=True)
            
        return dataframes


class _KeyMeasures(PageSection):
    """
    """
    _post_url = "https://apps.cnbc.com/resources/asp/getKeyMeasuresBuffer.asp"

    def __init__(self, symbol: str, soup: bs4.BeautifulSoup):
        super().__init__(symbol, soup)

        self._dataframes = self._scrape_table_data()

    @property
    def valuation(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframes[0].copy()
        dataframe = dataframe.applymap(float)

        return dataframe
    
    @property
    def financial_strength(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframes[1].copy()
        dataframe = dataframe.applymap(float)

        return dataframe
    
    @property
    def assets(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframes[2].copy()
        dataframe.iloc[[0, 2], :] = dataframe.iloc[[0, 2], :].applymap(float)
        dataframe.iloc[1, :] = pd.Series(
            dataframe.iloc[1, :].apply(
                lambda x: expand_value(x.strip("$")) if isinstance(x, str) else np.nan
            ), dtype="Int64"
        )

        return dataframe

    @property
    def profitability(self) -> pd.DataFrame:
        """
        """
        dataframe = self._dataframes[3].copy()
        dataframe.iloc[0, :] = pd.Series(
            dataframe.iloc[0, :].apply(
                lambda x: expand_value(x.strip("$")) if isinstance(x, str) else np.nan
            ), dtype="Int64"
        )
        dataframe.iloc[1:, :] = dataframe.iloc[1:, :].applymap(
            lambda x: float(normalize_value(x)) if isinstance(x, str) else np.nan
        )

        return dataframe
    
    @property
    def _issue_type(self) -> str:
        """
        """
        return re.search(r"var issueType = \"(.*?)\";", str(self._soup)).group(1)
    
    @property
    def _wsid(self) -> str:
        """
        """
        return re.search(r"var wsid = \"(.*?)\";", str(self._soup)).group(1)
    
    @property
    def _wsod_company(self) -> str:
        """
        """
        return re.search(r"var wsodCompany = \"(.*?)\";", str(self._soup)).group(1)

    def _scrape_table_data(self) -> typing.List[pd.DataFrame]:
        """
        :return:
        """
        tab_view = {
          "title": "Show All", "value": "*", "issueType": self._issue_type, "symbol": self._wsid,
          "wsodCompany": self._wsod_company
        }
        data = {
            "data": Serializer().seralize(tab_view), "..contenttype..": "text/html",
            "..requester..": "ContentBuffer"
        }

        with requests.post(self._post_url, data, timeout=100) as response:
            json_data = response.json()

        columns = [x["title"] for x in json_data["columns"]]
        columns[columns.index("S&amp;P 500")] = "S&P 500"

        dataframes = []
        for section in json_data["sections"]:
            content = [x["values"] for x in section["rows"]]

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                index = [bs4.BeautifulSoup(x[0], features="lxml").text for x in content]
            data = [x[1:] for x in content]

            dataframes.append(
                pd.DataFrame(data, index=index, columns=columns).replace("--", np.nan)
            )

        return dataframes
