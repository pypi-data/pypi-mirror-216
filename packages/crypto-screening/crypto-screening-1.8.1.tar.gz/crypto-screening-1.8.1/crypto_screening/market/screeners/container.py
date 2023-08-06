# container.py

from typing import Iterable, List

from represent import Modifiers

from crypto_screening.collect.assets import exchanges_symbols_quote_assets
from crypto_screening.market.screeners.base import (
    BaseScreener, structure_screener_datasets
)
from crypto_screening.market.screeners.recorder import MarketRecorder

class ScreenersContainer(MarketRecorder):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

    - data:
        The structure of the screeners, by exchanges and symbols.

    >>> from crypto_screening.market.screeners.container import ScreenersContainer
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> dynamic_screener = ScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    >>>
    >>> dynamic_screener.screener(exchange="binance", symbol="BTC/USDT"))
    >>> dynamic_screener.data(exchange="binance", symbol="BTC/USDT", length=10))
    """

    modifiers = Modifiers(hidden=["screeners", "currencies"], excluded=["structure"])

    def __init__(self, screeners: Iterable[BaseScreener]) -> None:
        """
        Defines the class attributes.

        :param screeners: The data screener object.
        """

        super().__init__(market=structure_screener_datasets(screeners=screeners))

        self.screeners = screeners

        self.currencies = exchanges_symbols_quote_assets(data=self.market)
        self.exchanges = list(self.market.keys())
    # end __init__

    def screener(self, exchange: str, symbol: str) -> BaseScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        if not self.in_market(exchange=exchange, symbol=symbol):
            raise ValueError(
                f"Screener object for symbol - {symbol} and "
                f"exchange - {exchange} cannot be found in {self}."
            )
        # end if

        for screener in self.screeners:
            if (screener.exchange == exchange) and (screener.symbol == symbol):
                return screener
            # end if
        # end for
    # end screener

    def screeners(self, exchange: str, symbol: str) -> List[BaseScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        if not self.in_market(exchange=exchange, symbol=symbol):
            raise ValueError(
                f"Screener object for symbol - {symbol} and "
                f"exchange - {exchange} cannot be found in {self}."
            )
        # end if

        screeners = []

        for screener in self.screeners:
            if (screener.exchange == exchange) and (screener.symbol == symbol):
                screeners.append(screener)
            # end if
        # end for

        return screeners
    # end screener
# end ScreenersContainer