import threading
import time
from logging import Logger

from orjson import orjson
from websocket import WebSocketApp

from lime_trader.converters.cattr_converter import converter
from lime_trader.models.market import MarketDataFeedAction, MarketDataFeedActionType


class MarketDataFeedClient(threading.Thread):
    """
    Client used to subscribe to market data feed.
    Should not be instantiated by end-user.
    """

    def __init__(self, websocket_app: WebSocketApp, logger: Logger):
        super().__init__()
        self._websocket_app = websocket_app
        self._logger = logger
        self._available = False

    def run(self):
        self._logger.info("Starting market data feed thread")
        self._websocket_app.run_forever()

    def stop(self) -> None:
        self._logger.info("Stopping market data feed thread")
        self._websocket_app.close()

    def on_market_feed_streaming_feed_open(self, web_socket_app: WebSocketApp) -> None:
        self._logger.info("Market data feed client connection opened")
        self._available = True

    def on_market_feed_streaming_feed_close(self, web_socket_app: WebSocketApp) -> None:
        self._logger.info("Market data feed client connection closed")
        self._available = False

    def _send_action(self, action: MarketDataFeedAction) -> None:
        self._logger.info(f"Market data feed - sending action {action}")
        while not self._available or not self._websocket_app.sock:
            time.sleep(1)
        self._websocket_app.send(data=orjson.dumps(converter.dump_to_dict(action)))

    def subscribe_symbols(self, symbols: list[str]) -> None:
        """
        Subscribe to changes for specific symbols

        Args:
            symbols: List of symbols to watch
        """
        action = MarketDataFeedAction(action=MarketDataFeedActionType.SUBSCRIBE, symbols=symbols)
        self._send_action(action=action)

    def unsubscribe_symbols(self, symbols: list[str]) -> None:
        """
        Unsubscribe from changes for specific symbols

        Args:
            symbols: List of symbols to unwatch
        """
        action = MarketDataFeedAction(action=MarketDataFeedActionType.UNSUBSCRIBE, symbols=symbols)
        self._send_action(action=action)
