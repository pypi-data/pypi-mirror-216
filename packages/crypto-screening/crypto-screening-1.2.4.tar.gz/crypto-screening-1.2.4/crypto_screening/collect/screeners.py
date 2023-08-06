# screeners.py

from typing import (
    Optional, Dict, Iterable,
    List, Union, Tuple
)

from crypto_screening.symbols import symbol_to_pair
from crypto_screening.collect.symbols import (
    matching_symbol_pair, MarketSymbolSignature
)
from crypto_screening.screener import BaseScreener, BaseMultiScreener

__all__ = [
    "matching_screener_signatures",
    "matching_screener_pair",
    "matching_screener_pairs",
    "MarketScreenerSignature",
    "find_screeners",
    "structure_screeners",
    "live_screeners",
    "remove_empty_screeners",
    "screeners_exchanges_symbols"
]

AssetMatches = Iterable[Iterable[str]]

def matching_screener_pair(
        screener1: BaseScreener,
        screener2: BaseScreener, /, *,
        matches: Optional[AssetMatches] = None,
        separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbols are valid with the matching currencies.

    :param screener1: The first ticker.
    :param screener2: The second ticker.
    :param matches: The currencies.
    :param separator: The separator of the assets.

    :return: The validation value for the symbols.
    """

    return (
        (screener1.exchange != screener2.exchange) and
        matching_symbol_pair(
            screener1.symbol, screener2.symbol,
            matches=matches, separator=separator
        )
    )
# end matching_screener_pair

ExchangesAssetMatches = Union[Dict[Iterable[str], AssetMatches], AssetMatches]

def matching_screener_pairs(
        screeners: Iterable[BaseScreener],
        matches: Optional[ExchangesAssetMatches] = None,
        separator: Optional[str] = None,
        empty: Optional[bool] = True
) -> List[Tuple[BaseScreener, BaseScreener]]:
    """
    Checks if the screeners are valid with the matching currencies.

    :param screeners: The screeners.
    :param matches: The currencies.
    :param separator: The separator of the assets.
    :param empty: Allows empty screeners.

    :return: The validation value for the symbols.
    """

    pairs = []

    if not empty:
        screeners = remove_empty_screeners(screeners=screeners)
    # end if

    for screener1 in screeners:
        for screener2 in screeners:
            exchanges_matches = (
                matches
                if not isinstance(matches, dict) else
                [
                    *matches.get(screener1.exchange, []),
                    *matches.get(screener2.exchange, [])
                ]
            )

            if matching_screener_pair(
                    screener1, screener2,
                    matches=exchanges_matches or None,
                    separator=separator
            ):
                pairs.append((screener1, screener2))
            # end if
        # end for
    # end for

    return pairs
# end matching_screener_pairs

class MarketScreenerSignature(MarketSymbolSignature):
    """A class to represent the data for the execution of a trade."""

    __slots__ = "screener",

    def __init__(
            self,
            asset: str,
            currency: str,
            exchange: str,
            screener: Optional[BaseScreener] = None
    ) -> None:
        """
        Defines the class attributes.

        :param asset: The traded asset.
        :param currency: The currency to trade the asset with.
        :param exchange: The exchange platform.
        """

        super().__init__(
            asset=asset, currency=currency, exchange=exchange
        )

        self.screener = screener
    # end __init__
# end MarketScreenerSignature

def matching_screener_signatures(
        data: Optional[List[Tuple[BaseScreener, BaseScreener]]] = None,
        screeners: Optional[Iterable[BaseScreener]] = None,
        matches: Optional[ExchangesAssetMatches] = None,
        separator: Optional[str] = None,
        empty: Optional[bool] = True
) -> List[Tuple[MarketScreenerSignature, MarketScreenerSignature]]:
    """
    Checks if the screeners are valid with the matching currencies.

    :param data: The data for the pairs.
    :param screeners: The screeners.
    :param matches: The currencies.
    :param separator: The separator of the assets.
    :param empty: Allows empty screeners.

    :return: The validation value for the symbols.
    """

    if (data is None) and (screeners is None):
        raise ValueError(
            f"One of 'screeners' and 'data' parameters must be given, "
            f"when 'data' is superior to 'screeners'."
        )

    elif (not screeners) and (not data):
        return []
    # end if

    pairs = []

    data = data or matching_screener_pairs(
        screeners=screeners, matches=matches,
        separator=separator, empty=empty
    )

    for screener1, screener2 in data:
        currency1 = symbol_to_pair(screener1.symbol).quote
        currency2 = symbol_to_pair(screener2.symbol).quote

        pairs.append(
            (
                MarketScreenerSignature(
                    asset=currency1, currency=currency1,
                    exchange=screener1.exchange,
                    screener=screener1
                ),
                MarketScreenerSignature(
                    asset=currency2, currency=currency2,
                    exchange=screener2.exchange,
                    screener=screener2
                )
            )
        )
    # end for

    return pairs
# end matching_screener_signatures

def live_screeners(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]]
) -> List[Union[BaseScreener, BaseMultiScreener]]:
    """
    Returns a list of all the live create_screeners.

    :param screeners: The create_screeners to search from.

    :return: A list the live create_screeners.
    """

    return [
        screener for screener in screeners
        if (
            screener.running and (
                isinstance(screener, BaseMultiScreener) or
                len(screener.market) > 0
            )
        )
    ]
# end live_screeners

def structure_screeners(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, List[BaseScreener]]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure: Dict[str, Dict[str, List[BaseScreener]]] = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, [])
        ).append(screener)
    # end for

    return structure
# end structure_screeners

def find_screeners(
        screeners: Iterable[BaseScreener], exchange: str, symbol: str
) -> List[BaseScreener]:
    """
    Finds all the screeners with the matching exchange and symbol name.

    :param screeners: The screeners to process.
    :param exchange: The exchange name for the symbol.
    :param symbol: The pair symbol to search its screeners.

    :return: The matching screeners.
    """

    return [
        screener for screener in screeners
        if (
            (screener.symbol.lower() == symbol.lower()) and
            (exchange.lower() == screener.exchange.lower())
        )
    ]
# end find_screeners

def remove_empty_screeners(screeners: Iterable[BaseScreener]) -> List[BaseScreener]:
    """
    Removes the empty screeners.

    :param screeners: The screeners of the assets and exchanges.
    """

    return [
        screener for screener in screeners
        if len(screener.market) > 0
    ]
# end remove_empty_screeners

def screeners_exchanges_symbols(screeners: Iterable[BaseScreener]) -> Dict[str, List[str]]:
    """
    Collects the structure of the screeners exchanges and symbols.

    :param screeners: The screeners to process.

    :return: The collected structure of exchanges and symbols.
    """

    data = {}

    for screener in screeners:
        data.setdefault(screener.exchange, []).append(screener.symbol)
    # end for

    return {
        exchange: list(set(symbols))
        for exchange, symbols in data.items()
    }
# end screeners_exchanges_symbols