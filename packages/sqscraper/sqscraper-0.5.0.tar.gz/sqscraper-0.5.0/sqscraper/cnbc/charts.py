"""
"""

import datetime
import json
import re
import typing

import bs4
import pandas as pd
import requests

from ._apps import Apps
from sqscraper.utils import YTD


class StockCharts(Apps):
    """
    :param symbol:
    """
    _post_url = "https://apps.cnbc.com/resources/asp/getBufferedChart.asp"

    def __init__(self, symbol: str):
        super().__init__(symbol, "stocks/charts")

    @property
    def _chart(self) -> typing.Dict[str, typing.Any]:
        """
        """
        return json.loads(re.search(r"var chart = (\{.*?\});", str(self._soup)).group(1))

    @property
    def _symbol(self) -> str:
        """
        """
        return re.search(r"var symbol = \"(.*?)\";", str(self._soup)).group(1)

    @property
    def _symbol_ibes(self) -> str:
        """
        """
        return re.search(r"var symbolIBES = \"(.*?)\";", str(self._soup)).group(1)

    @property
    def _symbol_ilx(self) -> str:
        """
        """
        return re.search(r"var symbolILX= \"(.*?)\";", str(self._soup)).group(1)

    @property
    def _exchange_id(self) -> str:
        """
        """
        return re.search(r"var exchangeId = \"(.*?)\";", str(self._soup)).group(1)

    @property
    def _wsod_issue(self) -> int:
        """
        """
        return int(self._chart["params"]["WSODIssue"])

    def _scrape_chart_data(
        self, *, symbols: typing.List[int], timeframe: int, interval: typing.Union[int, str],
        style: str, yscaling: str, indicators: typing.List[str], events: typing.List[str]
    ) -> typing.Dict[str, typing.Any]:
        """
        :param symbols:
        :param timeframe:
        :param interval:
        :param style:
        :param yscaling:
        :param indicators:
        :param events:
        :return:
        """
        regex = re.compile(r"^setChartImgUpper\((.*?)\);$")

        params = {
            "symbol": "".join(map(str, symbols)), "symbolIBES": self._symbol_ibes,
            "symbolILX": self._symbol_ilx, "WSODIssue": self._wsod_issue,
            "exchangeId": self._exchange_id, "timeFrame": timeframe, "width": 606,
            "height": 220, "showLower": 1, "heightLower": 50, "realtime": False,
            "interval": interval, "style": style, "yscaling": yscaling,
            "symbolBridge": self._wsod_issue, "isWSODIssue": True, "intraday": False,
            "indicators": ",".join(indicators), "events": ",".join(events)
        }
        return_vars = [
            "File.Name", "earningsExport", "dividendExport", "splitExport", "indicatorExport",
            "datesExport", "symbolExport", "rangeExport", "chartCoords", "chartCoordsVol",
            "chartYAxisBottom"
        ]
        data = {
            "params": "&".join(f"{k}={v}" for k, v in params.items()), "cht": "basic",
            "callback": "setChartImgUpper", "returnVars": ",".join(return_vars),
            "..contenttype..": "text/javascript", "..requester..": "ContentBuffer"
        }

        with requests.post(self._post_url, data=data, timeout=100) as response:
            chart_data = dict(
                zip(return_vars, re.findall(r"'(.*?)'", regex.search(response.text).group(1)))
            )

        return {
            "url": f"https://apps.cnbc.com{chart_data['File.Name']}",
            "earnings": self._unflatten_data(chart_data["earningsExport"]),
            "dividends": self._unflatten_data(chart_data["dividendExport"]),
            "splits": self._unflatten_data(chart_data["splitExport"]),
            "indicators": self._unflatten_data(chart_data["indicatorExport"]),
            "dates": [
                (int(x.split(":")[0]), float(x.split(":")[1]))
                for x in chart_data["datesExport"].split(",")
            ],
            "symbols": self._unflatten_data(chart_data["symbolExport"]),
            "range": [float(x) for x in chart_data["rangeExport"].split(",")],
            "price": self._parse_coordinates(chart_data["chartCoords"]),
            "volume": self._parse_coordinates(chart_data["chartCoordsVol"]),
            "y-axis": int(chart_data["chartYAxisBottom"])
        }

    def _unflatten_data(self, data: str) -> typing.List[typing.Dict[str, str]]:
        """
        :param data:
        :return:
        """
        keys = {
            "earnings": [
                "x0", "y0", "x1", "y1", "DateAnnounced", "Amount", "val2", "val3", "val4", "val5",
                "val6", "val7"
            ],
            "dividend": [
                "x0", "y0", "x1", "y1", "DatePayable", "DateAnnounced", "DateOwned", "date4",
                "Amount", "val2", "val3"
            ],
            "split": ["x0", "y0", "x1", "y1", "DateAnnounced", "Ratio"],
            "indicator": ["UID", "Name", "x0", "y0", "x1", "y1"],
            "symbols": ["Name", "Symbol", "x0", "y0", "x1", "y1"]
        }
        components = data.split("&")
        try:
            return [
                dict(zip(keys[components[0]], v))
                for v in zip(*[x.split("~") for x in components[1:]])
            ]
        except KeyError:
            return []

    def _parse_coordinates(self, data: str) -> pd.DataFrame:
        """
        :param data:
        :return:
        """
        dataframe = pd.DataFrame([x.split("*") for x in data.split("|")])

        if len(dataframe.columns) == 7:
            dataframe.columns = ["Date", "Open", "High", "Low", "Close", "x", "y"]
            dataframe.iloc[:, 0] = dataframe.iloc[:, 0].apply(
                lambda x: datetime.datetime.strptime(x, "%m/%d/%y %I:%M%p")
            )
            dataframe.iloc[:, 1:5] = dataframe.iloc[:, 1:5].applymap(float)
            dataframe.iloc[:, 5:] = dataframe.iloc[:, 5:].applymap(int)
        elif len(dataframe.columns) == 4:
            dataframe.columns = ["Date", "Volume", "x", "y"]
            dataframe.iloc[:, 0] = dataframe.iloc[:, 0].apply(
                lambda x: datetime.datetime.strptime(x, "%m/%d/%y %H:%M")
            )
            dataframe.iloc[:, 1] = dataframe.iloc[:, 1].apply(
                lambda x: int("".join(x.replace("^", ",").split(",")))
            )
            dataframe.iloc[:, 2:] = dataframe.iloc[:, 2:].applymap(int)
        else:
            raise ValueError
        
        return dataframe
    
    def _parse_earnings(self, data: typing.List[typing.Dict[str, str]]) -> pd.DataFrame:
        """
        :param data:
        :return:
        """
        dataframe = pd.DataFrame(data)
        if dataframe.empty:
            return dataframe

        dataframe.iloc[:, :4] = dataframe.iloc[:, :4].applymap(int)
        dataframe.iloc[:, 4] = dataframe.iloc[:, 4].apply(
            lambda x: datetime.datetime.strptime("%b %d, %Y", x)
        )
        dataframe.iloc[:, 5] = dataframe.iloc[:, 5].apply(float)
        dataframe.iloc[:, 6:8] = dataframe.iloc[:, 6:8].applymap(int)
        dataframe.iloc[:, 8:] = dataframe.iloc[:, 8:].applymap(float)

        return dataframe

    def _parse_dividends(self, data: typing.List[typing.Dict[str, str]]) -> pd.DataFrame:
        """
        :param data:
        :return:
        """
        dataframe = pd.DataFrame(data)
        if dataframe.empty:
            return dataframe

        dataframe.iloc[:, :4] = dataframe.iloc[:, :4].applymap(int)
        dataframe.iloc[:, 4:8] = dataframe.iloc[:, 4:7].applymap(
            lambda x: datetime.datetime.strptime("%b %d, %Y", x)
        )
        dataframe.iloc[:, 8] = dataframe.iloc[:, 8].apply(float)
        dataframe.iloc[:, 9] = dataframe.iloc[:, 9].apply(int)
        dataframe.iloc[:, 10] = dataframe.iloc[:, 10].apply(float)

        return dataframe

    def _parse_splits(self, data: typing.List[typing.Dict[str, str]]) -> pd.DataFrame:
        """
        :param data:
        :return:
        """
        dataframe = pd.DataFrame(data)
        if dataframe.empty:
            return dataframe

        dataframe.iloc[:, :4] = dataframe.iloc[:, :4].applymap(int)
        dataframe.iloc[:, 4] = dataframe.iloc[:, 4].apply(
            lambda x: datetime.datetime.strptime("%b %d, %Y", x)
        )
        dataframe.iloc[:, 5] = dataframe.iloc[:, 5].apply(float)

        return dataframe

    def chart_options(self, **kwargs: typing.Union[str, typing.List[str]]) -> "_ChartOptions":
        """
        :param kwargs:
        :return:
        """
        return _ChartOptions(self._soup, **kwargs)

    def chart_data(
        self, options: typing.Optional["_ChartOptions"] = None
    ) -> typing.Dict[str, typing.Any]:
        """
        :param timeframe:
        :param interval:
        :param options:
        :return:
        """
        options = self.chart_options() if options is None else options
        chart_data = self._scrape_chart_data(
            symbols=list({self._wsod_issue, *[options.symbol_value(x) for x in options.symbols]}),
            timeframe=options.timeframe_value(options.timeframe),
            interval=options.interval_value(options.interval),
            style=options.style,
            yscaling=options.yscaling,
            indicators=[options.indicator_value(x) for x in options.indicators], events=options.events
        )

        return {
            "url": chart_data["url"],
            "earnings": self._parse_earnings(chart_data["earnings"]),
            "dividends": self._parse_dividends(chart_data["dividends"]),
            "splits": self._parse_splits(chart_data["splits"]),
            "price": chart_data["price"],
            "volume": chart_data["volume"]
        }


class _ChartOptions:
    """
    :param soup:
    :param kwargs:
    """
    fields = (
        "symbols", "timeframe", "interval", "style", "yscaling", "indicators", "events"
    )

    def __init__(self, soup: bs4.BeautifulSoup, **kwargs):
        self._soup = soup

        self._symbols = []
        self._timeframe = "1D"
        self._interval = "1m"
        self._style = "mountain"
        self._yscaling = "standard"
        self._indicators = []
        self._events = []

        self._defaults = self.values
        self.set_fields(**self._defaults)
        self.set_fields(**kwargs)

    def __getitem__(self, key: str) -> typing.Union[str, typing.List[str]]:
        return self.__getattribute__(key)
    
    def __repr__(self) -> str:
        arguments = ", ".join(f"{k}={self.__getattribute__(k)}" for k in self.fields)
        return f"{type(self).__name__}({arguments})"

    @property
    def _symbol_options(self) -> typing.Dict[str, str]:
        """
        """
        return {
            e.text: int(e.attrs.get("wsodissue")) for e in self._soup.select(
                "select#compareSelect > option[wsodissue]"
            )
        }
    
    @property
    def _timeframe_options(self) -> typing.Dict[str, int]:
        """
        """
        return {
            "1D": 1, "5D": 5, "1M": 30, "3M": 90, "6M": 183, "YTD": YTD, "1Y": 365, "3Y": 1095,
            "5Y": 1825, "10Y": 3650
        }
    
    @property
    def _interval_options(self) -> typing.Dict[str, typing.Union[int, str]]:
        """
        """
        if self.timeframe_value(self.timeframe) in (1, 5):
            return {"1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30}
        elif self.timeframe_value(self.timeframe) <= 90:
            return {"Daily": "Daily", "Weekly": "Weekly"}
        else:
            return {"Daily": "Daily", "Weekly": "Weekly", "Monthly": "Monthly"}
        
    @property
    def _indicator_options(self) -> typing.Dict[str, str]:
        """
        """
        return {
            e.text: e.attrs.get("value") for e in self._soup.select(
                "select#selUpper > option, select#selLower > option"
            ) if e.attrs.get("value") != ""
        }

    @property
    def symbol(self) -> str:
        """
        """
        return re.search(r"var underlyingSymbol = \"(.*?)\";", str(self._soup)).group(1)

    @property
    def defaults(self) -> typing.Dict[str, typing.Union[str, typing.List[str]]]:
        """
        """
        return self._defaults

    @property
    def options(self) -> typing.Dict[str, typing.List[str]]:
        """
        """
        return {
            "symbols": list(self._symbol_options),
            "timeframe": list(self._timeframe_options),
            "interval": list(self._interval_options),
            "style": ["line", "bar", "mountain", "candle"],
            "yscaling": ["standard", "logarithmic"],
            "indicators": list(self._indicator_options),
            "events": ["earnings", "splits", "dividends"]
        }
    
    @property
    def values(self) -> typing.Dict[str, typing.Any]:
        """
        """
        return {k: self.__getattribute__(k) for k in self.fields}

    @property
    def symbols(self) -> typing.List[int]:
        """
        """
        return self._symbols
    
    @symbols.setter
    def symbols(self, value: typing.List[int]) -> None:
        """
        """
        self._symbols = []
        if all(x in self.options["symbols"] for x in value):
            self._symbols = list(set(value))
        else:
            raise ValueError(value)
    
    @property
    def timeframe(self) -> str:
        """
        """
        return self._timeframe
    
    @timeframe.setter
    def timeframe(self, value: str) -> None:
        """
        """
        if value in self.options["timeframe"]:
            self._timeframe = value
        else:
            raise ValueError(value)

    @property
    def interval(self) -> str:
        """
        """
        return self._interval
    
    @interval.setter
    def interval(self, value: str) -> None:
        """
        """
        if value in self.options["interval"]:
            self._interval = value
        else:
            raise ValueError(value)

    @property
    def style(self) -> str:
        """
        """
        return self._style
    
    @style.setter
    def style(self, value: str) -> None:
        """
        """
        if value in self.options["style"]:
            self._style = value
        else:
            raise ValueError(value)
    
    @property
    def yscaling(self) -> str:
        """
        """
        return self._yscaling
    
    @yscaling.setter
    def yscaling(self, value: str) -> None:
        """
        """
        if value in self.options["yscaling"]:
            self._yscaling = value
        else:
            raise ValueError(value)
    
    @property
    def indicators(self) -> typing.List[str]:
        """
        """
        return self._indicators
    
    @indicators.setter
    def indicators(self, value: typing.List[str]) -> None:
        """
        """
        self._indicators = []
        if all(x in self.options["indicators"] for x in value):
            self._indicators = list(set(value))
        else:
            raise ValueError(value)
    
    @property
    def events(self) -> typing.List[str]:
        """
        """
        return self._events
    
    @events.setter
    def events(self, value: typing.List[str]) -> None:
        """
        """
        if all(x in self.options["events"] for x in value):
            self._events = list(set(value))
        else:
            raise ValueError(value)

    def set_fields(self, **kwargs) -> None:
        """
        :param kwargs:
        :raise AttributeError:
        """
        for key, value in kwargs.items():
            if key in self.fields:
                self.__setattr__(key, value)
            else:
                raise AttributeError(key)

    def add_symbols(self, *symbols: str) -> None:
        """
        :param symbols:
        """
        self.symbols += list(symbols)

    def remove_symbols(self, *symbols: str) -> None:
        """
        :param symbols:
        """
        self.symbols = [x for x in self.symbols if x not in symbols]

    def add_indicators(self, *indicators: str) -> None:
        """
        :param indicators:
        """
        self.indicators += list(indicators)

    def remove_indicators(self, *indicators: str) -> None:
        """
        :param indicators:
        """
        self.indicators = [x for x in self.indicators if x not in indicators]

    def add_events(self, *events: str) -> None:
        """
        :param events:
        """
        self.events += list(events)

    def remove_events(self, *events: str) -> None:
        """
        :param events:
        """
        self.events = [x for x in self.events if x not in events]

    def symbol_value(self, symbol: str) -> int:
        """
        :param symbol:
        :return:
        :raise KeyError:
        """
        return self._symbol_options[symbol]
    
    def timeframe_value(self, timeframe: str) -> int:
        """
        :param timeframe:
        :return:
        :raise KeyError:
        """
        return self._timeframe_options[timeframe]
        
    def interval_value(self, interval: str) -> typing.Union[int, str]:
        """
        :param interval:
        :return:
        :raise KeyError:
        """
        return self._interval_options[interval]
    
    def indicator_value(self, indicator: str) -> str:
        """
        :param symbol:
        :return:
        :raise KeyError:
        """
        return self._indicator_options[indicator]
