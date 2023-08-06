# screener.py

import warnings
import datetime as dt
import time
from abc import ABCMeta
import threading
from typing import (
    Optional, Union, Dict, Iterable, Any, List
)

import pandas as pd

from represent import BaseModel, Modifiers

from multithreading import Caller, multi_threaded_call

from crypto_screening.dataset import (
    DATE_TIME, save_dataset, load_dataset
)
from crypto_screening.hints import Number
from crypto_screening.symbols import Separator
from crypto_screening.process import find_string_value
from crypto_screening.validate import (
    validate_exchange, validate_symbol
)

__all__ = [
    "BaseScreener",
    "wait_for_update",
    "wait_for_initialization",
    "WaitingState",
    "DataCollector",
    "wait_for_dynamic_update",
    "wait_for_dynamic_initialization",
    "BaseMultiScreener",
    "create_market_dataframe",
    "MarketRecorder",
    "structure_screeners_datasets",
    "structure_screener_datasets",
    "validate_market",
    "gather_screeners"
]

class WaitingState(BaseModel):
    """A class to represent the waiting state of screener objects."""

    modifiers = Modifiers(hidden=["screeners"], properties=["time"])

    __slots__ = (
        "screeners", "delay", "count",
        "canceled", "cancel", "start", "end"
    )

    def __init__(
            self,
            screeners: Iterable,
            start: dt.datetime,
            end: dt.datetime,
            stop: Optional[bool] = None,
            delay: Optional[Number] = None,
            count: Optional[int] = None,
            canceled: Optional[bool] = None,
            cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param screeners: The screener objects.
        :param start: The start time.
        :param end: The end time.
        :param stop: The stop value.
        :param delay: The waiting delay.
        :param count: The iterations count.
        :param canceled: The value for the waiting being canceled.
        :param cancel: The time to cancel the waiting.
        """

        self.screeners: Iterable[Union[BaseScreener, BaseMultiScreener]] = screeners

        self.start = start
        self.end = end
        self.cancel = cancel

        self.stop = stop or False
        self.canceled = canceled or False
        self.delay = delay or 0
        self.count = count or 0
    # end __init__

    @property
    def time(self) -> dt.timedelta:
        """
        Returns the amount of waited time.

        :return: The waiting time.
        """

        return self.end - self.start
    # end time
# end WaitingState

class DataCollector(BaseModel, metaclass=ABCMeta):
    """A class to represent an abstract parent class of data collectors."""

    modifiers = Modifiers(**BaseModel.modifiers)
    modifiers.excluded.extend(
        [
            'screening_process', 'timeout_process',
            'saving_process', 'update_process'
        ]
    )

    __slots__ = (
        'screening_process', 'timeout_process',
        'saving_process', 'update_process',
        'location', 'cancel', 'delay', 'market'
    )

    LOCATION = "datasets"

    DELAY = 0.0
    CANCEL = 0

    def __init__(
            self,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        if delay is None:
            delay = self.DELAY
        # end if

        if cancel is None:
            cancel = self.CANCEL
        # end if

        self.cancel = cancel
        self.delay = delay

        self.location = location or self.LOCATION

        self.screening = False
        self.block = False
        self.saving = False
        self.updating = False

        self.screening_process = None
        self.timeout_process = None
        self.saving_process = None
        self.update_process = None
    # end __init__

    def __getstate__(self) -> Dict[str, Any]:
        """
        Returns the data of the object.

        :return: The state of the object.
        """

        data = self.__dict__.copy()

        for key, value in data.items():
            if isinstance(value, threading.Thread):
                data[key] = None
            # end if
        # end for

        return data
    # end __getstate__

    def blocking(self) -> bool:
        """
        returns the value of the process being blocked.

        :return: The value.
        """

        return self.block
    # end blocking

    def screening_loop(self) -> None:
        """Runs the process of the price screening."""
    # end screening_loop

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""
    # end saving_loop

    def update_loop(self) -> None:
        """Updates the state of the screeners."""
    # end update_loop

    def wait_for_initialization(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

        self: Union[BaseScreener, BaseMultiScreener]

        return wait_for_initialization(
            self, delay=delay, stop=stop,
            cancel=cancel or self.cancel
        )
    # end wait_for_initialization

    def wait_for_update(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

        self: Union[BaseScreener, BaseMultiScreener]

        return wait_for_update(
            self, delay=delay, stop=stop,
            cancel=cancel or self.cancel
        )
    # end wait_for_update

    def start_blocking(self) -> None:
        """Starts the blocking process."""

        if self.saving:
            warnings.warn(f"Blocking process of {self} is already running.")
        # end if

        self.block = True

        while self.blocking():
            time.sleep(0.005)
        # end while
    # end start_blocking

    def start_screening(self) -> None:
        """Starts the screening process."""

        if self.screening:
            warnings.warn(f"Screening process of {self} is already running.")

            return
        # end if

        self.screening = True

        self.screening_process = threading.Thread(
            target=self.screening_loop
        )

        self.screening_process.start()
    # end start_screening

    def start_saving(self) -> None:
        """Starts the saving process."""

        if self.saving:
            warnings.warn(f"Saving process of {self} is already running.")
        # end if

        self.saving = True

        self.saving_process = threading.Thread(
            target=self.saving_loop
        )

        self.saving_process.start()
    # end start_saving

    def start_updating(self) -> None:
        """Starts the updating process."""

        if self.updating:
            warnings.warn(f"Updating process of {self} is already running.")
        # end if

        self.updating = True

        self.update_process = threading.Thread(
            target=self.update_loop
        )

        self.update_process.start()
    # end start_updating

    def start_waiting(
            self, wait: Union[Number, dt.timedelta, dt.datetime]
    ) -> None:
        """
        Runs a waiting for the process.

        :param wait: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()
        # end if

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()
        # end if

        if isinstance(wait, bool) and wait:
            self.wait_for_initialization()

        elif isinstance(wait, (int, float)):
            time.sleep(wait)
        # end if
    # end start_waiting

    def start_timeout(
            self, duration: Union[Number, dt.timedelta, dt.datetime]
    ) -> None:
        """
        Runs a timeout for the process.

        :param duration: The duration of the start_timeout.

        :return: The start_timeout process.
        """

        if (
            isinstance(self.timeout_process, threading.Thread) and
            self.timeout_process.is_alive()
        ):
            warnings.warn(f"Timeout process of {self} is already running.")

            return
        # end if

        if isinstance(duration, dt.datetime):
            duration = duration - dt.datetime.now()
        # end if

        if isinstance(duration, dt.timedelta):
            duration = duration.total_seconds()
        # end if

        self.timeout_process = threading.Thread(
            target=lambda: (time.sleep(duration), self.terminate())
        )

        self.timeout_process.start()
    # end start_timeout

    def run(
            self,
            screen: Optional[bool] = True,
            save: Optional[bool] = True,
            block: Optional[bool] = False,
            update: Optional[bool] = True,
            wait: Optional[Union[bool, Number, dt.timedelta, dt.datetime]] = False,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param screen: The value to start the screening.
        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param update: The value to update the screeners.
        :param timeout: The valur to add a start_timeout to the process.
        """

        if screen:
            self.start_screening()
        # end if

        if save:
            self.start_saving()
        # end if

        if update:
            self.start_updating()
        # end if

        if timeout:
            self.start_timeout(timeout)
        # end if

        if wait:
            self.start_waiting(wait)
        # end if

        if block:
            self.start_blocking()
        # end if
    # end run

    def terminate(self) -> None:
        """Stops the trading process."""

        self.stop()
    # end terminate

    def stop(self) -> None:
        """Stops the screening process."""

        if (
            self.screening and
            isinstance(self.screening_process, threading.Thread) and
            self.screening_process.is_alive()
        ):
            self.screening_process = None

            self.screening = False
        # end if

        if (
            self.saving and
            isinstance(self.saving_process, threading.Thread) and
            self.saving_process.is_alive()
        ):
            self.saving_process = None

            self.saving = False
        # end if

        if self.block:
            self.block = False
        # end if
    # end stop
# end DataCollector

def create_market_dataframe(columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :param columns: The dataset columns.

    :return: The dataframe.
    """

    market = pd.DataFrame(
        {column: [] for column in columns or []}, index=[]
    )
    market.index.name = DATE_TIME

    return market
# end create_market_dataframe

class BaseScreener(DataCollector):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The name of the exchange platform to screen data from.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.
    """

    modifiers = Modifiers(**DataCollector.modifiers)
    modifiers.hidden.append("market")

    __slots__ = "symbol", "exchange", "market"

    def __init__(
            self,
            symbol: str,
            exchange: str,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            market: Optional[pd.DataFrame] = None,
    ) -> None:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param market: The data for the market.
        """

        super().__init__(location=location, cancel=cancel, delay=delay)

        self.exchange = self.validate_exchange(exchange=exchange)
        self.symbol = self.validate_symbol(
            exchange=self.exchange, symbol=symbol
        )

        if market is None:
            market = create_market_dataframe()
        # end if

        self.market = market
    # end __init__

    @staticmethod
    def validate_exchange(exchange: str) -> str:
        """
        Validates the symbol value.

        :param exchange: The exchange name.

        :return: The validates symbol.
        """

        return validate_exchange(exchange=exchange)
    # end validate_exchange

    @staticmethod
    def validate_symbol(exchange: str, symbol: Any) -> str:
        """
        Validates the symbol value.

        :param exchange: The exchange name.
        :param symbol: The name of the symbol.

        :return: The validates symbol.
        """

        return validate_symbol(exchange=exchange, symbol=symbol)
    # end validate_symbol

    def dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        location = location or self.location

        if location is None:
            location = "."
        # end if

        return (
            f"{location}/"
            f"{self.exchange.lower()}/"
            f"{self.symbol.replace(Separator.value, '-')}.csv"
        )
    # end dataset_path

    def save_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        if len(self.market) == 0:
            return
        # end if

        save_dataset(
            dataset=self.market,
            path=self.dataset_path(location=location)
        )
    # end save_dataset

    def load_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.market.loc[index] = data
        # end for
    # end load_dataset

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

        self.saving = True

        delay = self.delay

        if isinstance(self.delay, dt.timedelta):
            delay = delay.total_seconds()
        # end if

        while self.saving:
            start = time.time()

            self.save_dataset()

            end = time.time()

            time.sleep(max(delay - (end - start), 1))
        # end while
    # end saving_loop
# end BaseScreener

Market = Dict[str, Dict[str, pd.DataFrame]]

def validate_market(data: Any) -> Market:
    """
    Validates the data.

    :param data: The data to validate.

    :return: The valid data.
    """

    if data is None:
        return {}
    # end if

    try:
        if not isinstance(data, dict):
            raise ValueError
        # end if

        for exchange, values in data.items():
            if not (
                isinstance(exchange, str) and
                (
                    (
                        isinstance(values, dict) and
                        all(
                            isinstance(symbol, str) and
                            isinstance(dataset, pd.DataFrame)
                            for symbol, dataset in values.items()
                        )
                    ) or (all(isinstance(value, str) for value in values))
                )
            ):
                raise ValueError
            # end if

            if not isinstance(values, dict):
                data[exchange] = {
                    symbol: create_market_dataframe()
                    for symbol in values
                }
            # end if
        # end for

    except (TypeError, ValueError):
        raise ValueError(
            f"Data must be of type {Market}, not: {data}."
        )
    # end try

    return data
# end validate_market

class MarketRecorder(BaseModel):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - market:
        The market structure of the data to store the fetched data in.
        This structure is a dictionary with exchange names as keys
        and dictionaries as values, where their keys are symbols,
        and their values are the dataframes to record the data.

    >>> from crypto_screening.screener import MarketRecorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = MarketRecorder(data=market)

    """

    modifiers = Modifiers(**BaseModel.modifiers)
    modifiers.hidden.append("market")

    __slots__ = "market"

    def __init__(self, market: Optional[Market] = None) -> None:
        """
        Defines the class attributes.

        :param market: The object to fill with the crypto feed record.
        """

        self.market = self.validate_market(data=market)
    # end __init__

    @staticmethod
    def validate_market(data: Any) -> Market:
        """
        Validates the data.

        :param data: The data to validate.

        :return: The valid data.
        """

        return validate_market(data=data)
    # end validate_market

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: list(symbols.keys())
            for exchange, symbols in self.market.items()
        }
    # end structure

    def data(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        exchange = find_string_value(
            value=exchange, values=self.market.keys()
        )

        validate_exchange(
            exchange=exchange,
            exchanges=self.market.keys(),
            provider=self
        )

        validate_symbol(
            symbol=symbol,
            exchange=exchange,
            exchanges=self.market.keys(),
            symbols=self.market[exchange],
            provider=self
        )

        return self.market[exchange][symbol]
    # end data

    def in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        try:
            self.data(exchange=exchange, symbol=symbol)

            return True

        except ValueError:
            return False
        # end try
    # end in_market
# end MarketRecorder

class BaseMultiScreener(DataCollector):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.
    """

    modifiers = Modifiers(**DataCollector.modifiers)
    modifiers.hidden.extend(["screeners", 'market'])

    screeners: List[BaseScreener]

    __slots__ = "screeners", "location", "cancel", "delay", 'recorder'

    def __init__(
            self,
            screeners: Optional[Iterable[BaseScreener]] = None,
            recorder: Optional[MarketRecorder] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        super().__init__(location=location, cancel=cancel, delay=delay)

        self.screeners = list(screeners or [])

        self.recorder = recorder or MarketRecorder(
            market=structure_screener_datasets(screeners=self.screeners)
        )
    # end __init__

    @property
    def market(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.recorder.market
    # end market

    def connect_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        for screener in self.screeners:
            screener.market = self.recorder.data(
                exchange=screener.exchange, symbol=screener.symbol
            )
        # end for
    # end connect_screeners

    def in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.in_market(exchange=exchange, symbol=symbol)
    # end in_market

    def save_datasets(self, location: Optional[str] = None) -> None:
        """
        Runs the data handling loop.

        :param location: The saving location.
        """

        callers = []

        for screener in self.screeners:
            location = location or screener.location or self.location

            callers.append(
                Caller(
                    target=screener.save_dataset,
                    kwargs=dict(location=location)
                )
            )
        # end for

        multi_threaded_call(callers=callers)
    # end save_datasets

    def load_datasets(self, location: Optional[str] = None) -> None:
        """
        Runs the data handling loop.

        :param location: The saving location.
        """

        callers = []

        for screener in self.screeners:
            location = location or screener.location or self.location

            callers.append(
                Caller(
                    target=screener.load_dataset,
                    kwargs=dict(location=location)
                )
            )
        # end for

        multi_threaded_call(callers=callers)
    # end load_datasets
# end BaseScreener

def gather_screeners(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]]
) -> List[BaseScreener]:
    """
    Gathers the base screeners.

    :param screeners: The screeners to process.

    :return: The gathered base screeners.
    """

    checked_screeners = []

    for screener in screeners:
        if isinstance(screener, BaseScreener):
            checked_screeners.append(screener)

        elif isinstance(screener, BaseMultiScreener):
            checked_screeners.extend(screener.screeners)
        # end if
    # end for

    return checked_screeners
# end gather_screeners

def wait_for_dynamic_initialization(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]],
        stop: Optional[bool] = None,
        delay: Optional[Union[Number, dt.timedelta]] = None,
        cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    if cancel is None:
        cancel = 0
    # end if

    if delay is None:
        delay = 0
    # end if

    if isinstance(cancel, (int, float)):
        cancel = dt.timedelta(seconds=cancel)
    # end if

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()
    # end if

    start = dt.datetime.now()
    count = 0
    canceled = False

    while screeners:
        checked_screeners = gather_screeners(screeners=screeners)

        if all(
            len(screener.market) > 0
            for screener in checked_screeners
        ):
            break
        # end if

        if (
            isinstance(cancel, dt.timedelta) and
            (canceled := ((dt.datetime.now() - start) > cancel))
        ):
            break
        # end if

        count += 1

        if isinstance(delay, (int, float)):
            time.sleep(delay)
        # end if
    # end while

    if stop:
        for screener in screeners:
            screener.stop()
        # end for
    # end if

    return WaitingState(
        screeners=screeners, delay=delay,
        count=count, end=dt.datetime.now(), start=start,
        cancel=cancel, canceled=canceled
    )
# end wait_for_dynamic_initialization

def wait_for_initialization(
        *screeners: Union[BaseScreener, BaseMultiScreener],
        stop: Optional[bool] = False,
        delay: Optional[Union[Number, dt.timedelta]] = None,
        cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    return wait_for_dynamic_initialization(
        screeners, delay=delay,
        stop=stop, cancel=cancel
    )
# end wait_for_initialization

def wait_for_dynamic_update(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]],
        stop: Optional[bool] = False,
        delay: Optional[Union[Number, dt.timedelta]] = None,
        cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    if cancel is None:
        cancel = 0
    # end if

    if delay is None:
        delay = 0
    # end if

    if isinstance(cancel, (int, float)):
        cancel = dt.timedelta(seconds=cancel)
    # end if

    if isinstance(delay, dt.timedelta):
        delay = delay.total_seconds()
    # end if

    start = dt.datetime.now()
    count = 0
    canceled = False

    wait = wait_for_dynamic_initialization(
        screeners, delay=delay, cancel=cancel, stop=stop
    )

    if not screeners:
        return wait
    # end if

    while screeners:
        checked_screeners = gather_screeners(screeners=screeners)

        indexes = {
            screener: len(screener.market)
            for screener in checked_screeners
        }

        if (
            isinstance(cancel, dt.timedelta) and
            (canceled := ((dt.datetime.now() - start) > cancel))
        ):
            break
        # end if

        if isinstance(delay, (int, float)):
            time.sleep(delay)
        # end if

        count += 1

        new_indexes = {
            screener: len(screener.market)
            for screener in checked_screeners
        }

        if indexes == new_indexes:
            break
        # end if
    # end while

    if stop:
        for screener in screeners:
            screener.stop()
        # end for
    # end if

    return WaitingState(
        screeners=screeners, delay=delay,
        count=count, end=dt.datetime.now(), start=start,
        cancel=cancel, canceled=canceled
    )
# end wait_for_dynamic_update

def wait_for_update(
        *screeners: Union[BaseScreener, BaseMultiScreener],
        stop: Optional[bool] = False,
        delay: Optional[Union[Number, dt.timedelta]] = None,
        cancel: Optional[Union[Number, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    return wait_for_dynamic_update(
        screeners, delay=delay,
        stop=stop, cancel=cancel
    )
# end wait_for_update

def structure_screeners_datasets(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, List[pd.DataFrame]]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, [])
        ).append(screener.market)
    # end for

    return structure
# end structure_screeners_datasets

def structure_screener_datasets(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, pd.DataFrame]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, screener.market)
        )
    # end for

    return structure
# end structure_screener_datasets