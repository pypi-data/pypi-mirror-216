# exchanges.py

from typing import (
    Optional, Dict, Iterable,
    Callable, Union, Any
)

from multithreading import Caller, multi_threaded_call

from crypto_screening.exchanges import EXCHANGE_NAMES
from crypto_screening.validate import validate_exchange
from crypto_screening.process import (
    find_string_value, lower_string_values
)

__all__ = [
    "exchanges_data"
]

Collector = Callable[
    [
        str,
        Optional[str],
        Optional[bool],
        Optional[Iterable[str]],
        Optional[Iterable[str]],
        Optional[Iterable[str]]
    ], Any
]

def exchanges_data(
        collector: Collector,
        adjust: Optional[bool] = True,
        separator: Optional[str] = None,
        exchanges: Optional[Iterable[str]] = None,
        bases: Optional[Iterable[str]] = None,
        quotes: Optional[Iterable[str]] = None,
        included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
        excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
) -> Dict[str, Any]:
    """
    Collects the symbols from the exchanges.

    :param collector: The collector function to collect data from an exchange.
    :param exchanges: The exchanges.
    :param bases: The bases of the asset pairs.
    :param adjust: The value to adjust the invalid exchanges.
    :param separator: The separator of the assets.
    :param quotes: The quotes of the asset pairs.
    :param included: The symbols to include.
    :param excluded: The excluded symbols.
    :param bases: The bases of the asset pairs.

    :return: The data of the exchanges.
    """

    excluded_symbols = []

    excluded = excluded or {}

    if not excluded:
        excluded_symbols = excluded
    # end if

    if (
            excluded and
            all(isinstance(value, str) for value in excluded) and
            not isinstance(excluded, dict)
    ):
        excluded = {exchange: excluded_symbols for exchange in exchanges}
    # end if

    exchanges = lower_string_values(exchanges or EXCHANGE_NAMES)

    markets = []

    for exchange in exchanges:
        exchange = find_string_value(value=exchange, values=EXCHANGE_NAMES)

        if exchange not in EXCHANGE_NAMES:
            if adjust:
                continue

            else:
                validate_exchange(exchange=exchange, exchanges=EXCHANGE_NAMES)
            # end if
        # end if

        markets.append(exchange)
    # end for

    callers = []
    data: Dict[str, Caller] = {}

    for exchange in markets:
        exchange = find_string_value(value=exchange, values=exchanges)

        caller = Caller(
            target=collector,
            kwargs=dict(
                exchange=exchange,
                separator=separator,
                quotes=quotes,
                adjust=adjust,
                bases=bases,
                included=included[exchange] if exchange in included else None,
                excluded=excluded[exchange] if exchange in excluded else None
            )
        )

        callers.append(caller)
        data[exchange] = caller
    # end for

    multi_threaded_call(callers=callers)

    return {key: value.results.returns for key, value in data.items() if value}
# end exchanges_data