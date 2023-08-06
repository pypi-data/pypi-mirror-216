import datetime
import enum
from _decimal import Decimal
from dataclasses import dataclass


class Period(enum.Enum):
    MINUTE = "minute"
    MINUTE_5 = "minute_5"
    MINUTE_15 = "minute_15"
    MINUTE_30 = "minute_30"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class TradingSchedule(enum.Enum):
    PRE_MARKET = "pre_market"
    REGULAR_MARKET = "regular_market"
    AFTER_MARKET = "after_market"
    CLOSED = "closed"


class OptionType(enum.Enum):
    CALL = "call"
    PUT = "put"


class MarketDataFeedActionType(enum.Enum):
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"


class MarketDataFeedType(enum.Enum):
    TRADE = "t"
    AGGREGATE = "a"
    ERROR = "e"


@dataclass
class Quote:
    """
    Quote for the specified symbol.

    Attributes:
        symbol: The security symbol
        ask: Ask price
        ask_size: Ask size
        bid: Bid price
        bid_size: Bid size
        last: Last price
        last_size: Last trade size
        volume: Today total volume
        date: Last trade time
        high: Today's high price
        low: Today's low price
        open: Open price
        close: Yesterday's close price
        week52_high: 52-week high
        week52_low: 52-week low
        change: Today's price change
        change_pc: Today's percent price change
        open_interest: Open interest (options)
        implied_volatility: Implied volatility (options)
        theoretical_price: Theoretical price (options)
        delta: Delta value (options)
        gamma: Gamma value (options)
        theta: Theta value (options)
        vega: Vega value (options)
    """
    symbol: str
    ask: Decimal
    ask_size: Decimal
    bid: Decimal
    bid_size: Decimal
    last: Decimal
    last_size: Decimal
    volume: int
    date: datetime.datetime
    high: Decimal
    low: Decimal
    open: Decimal
    close: Decimal
    week52_high: Decimal
    week52_low: Decimal
    change: Decimal
    change_pc: Decimal
    open_interest: Decimal
    implied_volatility: Decimal
    theoretical_price: Decimal
    delta: Decimal
    gamma: Decimal
    theta: Decimal
    vega: Decimal


@dataclass
class QuoteHistory:
    timestamp: datetime.datetime
    period: Period
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


@dataclass
class CurrentSchedule:
    """Trading session info depending on current date and time

    Attributes:
        session: Current session info
    """

    session: TradingSchedule


@dataclass
class Security:
    """Represents security

    Attributes:
        symbol: Security symbol
        description: Description of security
    """

    symbol: str
    description: str


@dataclass
class SecuritiesPage:
    """Page of securities

    Attributes:
        trades: List of securities
        count: Total count of securities
    """

    trades: list[Security]
    count: int

    @property
    def securities(self) -> list[Security]:
        """
        Alias for returned list as API returns it as "trades". Should be used instead of "trades" attribute.

        Returns:
            List of securities
        """
        return self.trades


@dataclass
class Trade:
    timestamp: int
    quantity: int
    price: Decimal
    market: str


@dataclass
class TradesPage:
    """Represents one page of trades

    Attributes:
        trades: List of trades
        count: Total count of trades
    """

    trades: list[Trade]
    count: int


@dataclass
class MarketDataFeedAction:
    """Action that is sent to market data feed websocket

    Attributes:
        action: Type of action
        symbols: List of symbols to track
    """

    action: MarketDataFeedActionType
    symbols: list[str]


@dataclass
class MarketDataFeedTrade:
    """Symbol trade. You should use properties instead of accessing attributes directly as naming is more user-friendly

    Attributes:
        t: Type. Always equal to "t"
        s: Symbol
        ls: Last Size. Trade quantity
        lm: Last Market. Trade market center
        l: Last trade Price
        d: Date
    """

    t: MarketDataFeedType
    s: str
    ls: int
    lm: str
    l: Decimal
    d: datetime.datetime

    @property
    def type(self) -> MarketDataFeedType:
        return self.t

    @property
    def symbol(self) -> str:
        return self.s

    @property
    def last_size(self) -> int:
        return self.ls

    @property
    def last_market(self) -> str:
        return self.lm

    @property
    def last_trade_price(self) -> Decimal:
        return self.l

    @property
    def date(self) -> datetime.datetime:
        return self.d


@dataclass
class MarketDataFeedAggregate:
    """Quote data. You should use properties instead of accessing attributes directly as naming is more user-friendly

    Attributes:
        t: Type. Always equal to "a"
        s: Symbol
        ch: Change
        a: Ask
        _as: Ask size, set after init is done
        b: Bid
        bs: Bid size
        l: Last trade Price
        c: Close price
        v: Volume
        chpc: Change percent
        ls: Last Size, trade quantity
        o: Open price
        h: High
        low: Low price
        d: Date
        iv: Implied volatility (options)
        tp: Theoretical price (options)
        delta: Delta value (options)
        theta: Theta value (options)
        gamma: Gamma value (options)
        vega: Vega value (options)
    """

    t: MarketDataFeedType
    s: str

    ch: Decimal | None = None

    a: Decimal | None = None
    _as: Decimal = None
    b: Decimal | None = None
    bs: Decimal | None = None
    l: Decimal | None = None
    c: Decimal | None = None
    v: int | None = None
    chpc: Decimal | None = None
    ls: int | None = None
    o: Decimal | None = None
    h: Decimal | None = None
    low: Decimal | None = None
    d: datetime.datetime | None = None

    iv: Decimal | None = None
    tp: Decimal | None = None
    delta: Decimal | None = None
    theta: Decimal | None = None
    gamma: Decimal | None = None
    vega: Decimal | None = None

    @property
    def type(self) -> MarketDataFeedType:
        return self.t

    @property
    def symbol(self) -> str:
        return self.s

    @property
    def last_size(self) -> int | None:
        return self.ls

    @property
    def last_trade_price(self) -> Decimal | None:
        return self.l

    @property
    def date(self) -> datetime.datetime | None:
        return self.d

    @property
    def ask(self) -> Decimal | None:
        return self.a

    @property
    def ask_size(self) -> Decimal | None:
        return self._as

    @property
    def bid(self) -> Decimal | None:
        return self.b

    @property
    def bid_size(self) -> Decimal | None:
        return self.bs

    @property
    def open_price(self) -> Decimal | None:
        return self.o

    @property
    def high_price(self) -> Decimal | None:
        return self.h

    @property
    def low_price(self) -> Decimal | None:
        return self.low

    @property
    def close_price(self) -> Decimal | None:
        return self.c

    @property
    def change(self) -> Decimal | None:
        return self.ch

    @property
    def change_percent(self) -> Decimal | None:
        return self.chpc

    @property
    def implied_volatility(self) -> Decimal | None:
        return self.iv

    @property
    def theoretical_price(self) -> Decimal | None:
        return self.tp


@dataclass
class MarketDataFeedError:
    """Error during streaming market feed data

    Attributes:
        t: Type. Always equal to "e"
        code: Error code
        description: Error description
    """
    t: MarketDataFeedType
    code: str
    description: str
