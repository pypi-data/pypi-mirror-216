import datetime
from functools import partial
from logging import Logger
from typing import Callable, Iterator

from lime_trader.api.authenticated_api_client import AuthenticatedApiClient
from lime_trader.clients.market_data_feed_client import MarketDataFeedClient
from lime_trader.converters.cattr_converter import CAttrConverter
from lime_trader.handlers.market_data_feed_handler import MarketDataFeedHandler
from lime_trader.models.accounts import AccountTransaction
from lime_trader.models.market import (Quote, QuoteHistory, Period, Security, SecuritiesPage, Trade, TradesPage,
                                       CurrentSchedule)
from lime_trader.models.page import Page, PageRequest
from lime_trader.constants.urls import (MARKET_DATA_GET_CURRENT_QUOTE, MARKET_DATA_GET_QUOTES,
                                        MARKET_DATA_GET_TRADING_SCHEDULE,
                                        MARKET_DATA_LOOKUP_SECURITIES, MARKET_DATA_GET_TIME_AND_SALES,
                                        MARKET_DATA_GET_QUOTES_HISTORY, MARKET_DATA_STREAMING_FEED)
from lime_trader.utils.pagination import iterate_pages


class MarketDataClient:
    """
    Contains methods related to market data
    """

    def __init__(self, api_client: AuthenticatedApiClient, logger: Logger):
        """
        Args:
            api_client: API client that will be used to execute all requests
            logger: Logger used to submit client log messages
        """
        self._api_client = api_client
        self._logger = logger

    def get_current_quote(self, symbol: str) -> Quote:
        """
        Retrieves current quote for the specified symbol

        Args:
            symbol: Security symbol

        Returns:
            Quote for the symbol
        """
        self._logger.info(f"Getting current quote for symbol {symbol}")
        return self._api_client.get(MARKET_DATA_GET_CURRENT_QUOTE, path_params={},
                                    params={"symbol": symbol}, response_schema=Quote)

    def get_current_quotes(self, symbols: list[str]) -> list[Quote]:
        """
        Retrieves current quotes for all specified symbols

        Args:
            symbols: List of security symbols

        Returns:
            List of quotes for specified symbols
        """
        self._logger.info(f"Getting current quotes for symbols {symbols}")
        return self._api_client.post(MARKET_DATA_GET_QUOTES, path_params={}, json=symbols, response_schema=list[Quote])

    def get_quotes_history(self, symbol: str, period: Period, from_date: datetime.datetime,
                           to_date: datetime.datetime) -> list[QuoteHistory]:
        """
        Returns candle structures aggregated by specified period

        Args:
            symbol: The security symbol, stocks in Nasdaq CMS convention. Options are not supported
            period: Aggregation period.
            from_date: Period start
            to_date: Period end

        Returns:
            Quote history between specified period
        """
        self._logger.info(f"Getting quotes history for symbol={symbol}, period={period}, from_date={from_date},"
                          f"to_date={to_date}")
        return self._api_client.get(MARKET_DATA_GET_QUOTES_HISTORY, path_params={},

                                    params={"symbol": symbol,
                                            "period": period.value,
                                            "from": from_date,
                                            "to": to_date
                                            }, response_schema=list[QuoteHistory])

    def get_trading_schedule(self) -> CurrentSchedule:
        """
        Returns trading session info depending on current date and time:

        Returns:
            Current trading schedule
        """
        self._logger.info(f"Getting current trading schedule")
        return self._api_client.get(MARKET_DATA_GET_TRADING_SCHEDULE, path_params={}, params={},
                                    response_schema=CurrentSchedule)

    def lookup_securities(self, query: str, page: PageRequest) -> Page[Security]:
        """
        Searches the securities reference by the specified criteria. The criteria can be a symbol,
        part of a symbol or part of a company name.

        Args:
            query: Search criteria
            page: Pagination parameters

        Returns:
            Page of security symbols which match criteria
        """
        self._logger.info(f"Looking up securities with query={query}, page={page}")
        response = self._api_client.get(MARKET_DATA_LOOKUP_SECURITIES, path_params={},
                                        params={"query": query,
                                                "limit": page.size,
                                                "skip": page.get_offset()},
                                        response_schema=SecuritiesPage)
        return Page(data=response.securities, number=page.page, size=page.size, total_elements=response.count)

    def time_and_sales(self, symbol: str, from_date: datetime.datetime,
                       to_date: datetime.datetime, page: PageRequest) -> Page[Trade]:
        """
        Retrieves the time and sales history, ordered by descending timestamp. Query parameters are:

        Args:
            symbol: The security symbol, stocks in Nasdaq CMS convention. Options are not supported
            from_date: Period start
            to_date: Period end
            page: Pagination parameters

        Returns:
            Page of historical trades
        """
        self._logger.info(f"Getting time and sales history for symbol={symbol}, from_date={from_date},"
                          f"to_date={to_date}, page={page}")
        response = self._api_client.get(MARKET_DATA_GET_TIME_AND_SALES, path_params={},
                                        params={"symbol": symbol,
                                                "from": from_date,
                                                "to": to_date,
                                                "limit": page.size,
                                                "skip": page.get_offset()},
                                        response_schema=TradesPage)
        return Page(data=response.trades, number=page.page, size=page.size, total_elements=response.count)

    def iterate_time_and_sales(self, symbol: str, from_date: datetime.datetime,
                               to_date: datetime.datetime, start_page: PageRequest,
                               ) -> Iterator[Page[AccountTransaction]]:
        """
        Returns iterator for the time and sales history, ordered by descending timestamp

        Args:
            symbol: The security symbol, stocks in Nasdaq CMS convention. Options are not supported
            from_date: Period start
            to_date: Period end
            start_page: Start page. Iterator starts from this page

        Returns:
            Iterator of pages of historical trades
        """
        for page in iterate_pages(start_page=start_page,
                                  func=partial(self.time_and_sales, symbol=symbol,
                                               from_date=from_date, to_date=to_date)):
            yield page

    def _start_streaming_feed(self, on_message: Callable, on_error: Callable) -> MarketDataFeedClient:
        websocket_app = self._api_client.websocket_connection(url=MARKET_DATA_STREAMING_FEED,
                                                              path_params={}, on_error=on_error, on_message=on_message)
        client = MarketDataFeedClient(websocket_app=websocket_app, logger=self._logger)
        websocket_app.on_open = client.on_market_feed_streaming_feed_open
        websocket_app.on_close = client.on_market_feed_streaming_feed_close
        client.start()
        return client

    def stream_market_data_feed(self, callback_client: MarketDataFeedHandler) -> MarketDataFeedClient:
        return self._start_streaming_feed(
            on_error=callback_client.on_market_data_feed_client_internal_error,
            on_message=partial(callback_client.on_message, CAttrConverter()))
