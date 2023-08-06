import logging
from abc import abstractmethod
from logging import Logger
from typing import Any

import orjson
from websocket import WebSocketApp

from lime_trader.converters.abstract_converter import AbstractConverter
from lime_trader.models.market import (MarketDataFeedType, MarketDataFeedAggregate, MarketDataFeedTrade,
                                       MarketDataFeedError)


class MarketDataFeedHandler:
    def __init__(self, logger: Logger | None = None):
        self._logger = logger if logger is not None else logging.getLogger()

    def on_market_data_feed_client_internal_error(self, websocket_app: WebSocketApp, error):
        self.on_client_error(error=error)

    def on_message(self, converter: AbstractConverter, websocket_app: WebSocketApp, message: str) -> None:
        self._logger.info("Received message on market data feed")
        decoded = orjson.loads(message)
        message_type = decoded.get("t", None)
        if message_type is None:
            self._logger.error("Error decoding market feed message. Missing message type.")
            return
        decoded_type = MarketDataFeedType(message_type)
        if decoded_type == MarketDataFeedType.TRADE:
            self.on_trade(converter.load_from_dict(decoded, MarketDataFeedTrade))
        elif decoded_type == MarketDataFeedType.AGGREGATE:
            obj = converter.load_from_dict(decoded, MarketDataFeedAggregate)
            obj._as = decoded.get("as")  # required field, cannot set it directly because it is reserved keyword
            self.on_aggregate(obj)
        elif decoded_type == MarketDataFeedType.ERROR:
            self.on_stream_error(converter.load_from_dict(decoded, MarketDataFeedError))
        else:
            raise ValueError(f"Unknown message type={message_type} for market feed!")

    @abstractmethod
    def on_aggregate(self, aggregate: MarketDataFeedAggregate) -> None:
        """
        The server sends a snapshot of current quote data as the first message after successful subscription.
        All subsequent aggregate messages contain only fields changed since last update.

        Args:
            aggregate: Updated aggregate quote data
        """
        self._logger.info(f"Aggregate: {aggregate}")

    @abstractmethod
    def on_trade(self, trade: MarketDataFeedTrade) -> None:
        """
        The server sends executed trades

        Args:
            trade: Executed trade
        """
        self._logger.info(f"Trade: {trade}")

    @abstractmethod
    def on_stream_error(self, error: MarketDataFeedError) -> None:
        """
        Handles error returned as websocket message. This error indicates that message has been received and contains
        error message.

        Args:
            error: Decoded error
        """
        self._logger.info(f"Market data streaming feed error: {error}")

    @abstractmethod
    def on_client_error(self, error: Any) -> None:
        """
        Handles client error, this error indicates error from client or error while decoding message.
        Message is received and cannot be decoded or there was error receiving message.

        Args:
            error: Error description
        """
        self._logger.error(f"Market data streaming feed client error: {error}")
