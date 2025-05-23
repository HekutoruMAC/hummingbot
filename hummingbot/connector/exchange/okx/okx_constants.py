import sys

from hummingbot.core.api_throttler.data_types import RateLimit
from hummingbot.core.data_type.common import OrderType
from hummingbot.core.data_type.in_flight_order import OrderState

CLIENT_ID_PREFIX = "93027a12dac34fBC"
MAX_ID_LEN = 32
SECONDS_TO_WAIT_TO_RECEIVE_MESSAGE = 30 * 0.8

# URL mapping based on where account is registered:
# sourced from https://app.okx.com/docs-v5/en/#overview-account-mode and https://my.okx.com/docs-v5/en/#overview-account-mode

subdomain_to_api_subdomain = {
    "www": "www",
    "app": "us",
    "my": "eea"
}


def get_okx_base_url(sub_domain: str) -> str:
    """Returns OKX REST base URL based on API subdomain ("www", "us", "eea")"""
    return f"https://{subdomain_to_api_subdomain[sub_domain]}.okx.com/"


def get_ws_url(sub_domain: str) -> str:
    """Returns OKX WebSocket base URL based on API subdomain ("www", "us", "eea")"""
    if sub_domain == "www":
        return "wss://ws.okx.com:8443"
    else:
        return f"wss://ws{subdomain_to_api_subdomain[sub_domain]}.okx.com:8443"


DEFAULT_DOMAIN = get_okx_base_url("www")


def get_okx_ws_uri_public(sub_domain):
    return f"{get_ws_url(sub_domain)}/ws/v5/public"


def get_okx_ws_uri_private(sub_domain):
    return f"{get_ws_url(sub_domain)}/ws/v5/private"


# REST API endpoints
OKX_SERVER_TIME_PATH = '/api/v5/public/time'
OKX_INSTRUMENTS_PATH = '/api/v5/public/instruments'
OKX_TICKER_PATH = '/api/v5/market/ticker'
OKX_TICKERS_PATH = '/api/v5/market/tickers'
OKX_ORDER_BOOK_PATH = '/api/v5/market/books'

# Auth required
OKX_PLACE_ORDER_PATH = "/api/v5/trade/order"
OKX_ORDER_DETAILS_PATH = '/api/v5/trade/order'
OKX_ORDER_CANCEL_PATH = '/api/v5/trade/cancel-order'
OKX_BATCH_ORDER_CANCEL_PATH = '/api/v5/trade/cancel-batch-orders'
OKX_BALANCE_PATH = '/api/v5/account/balance'
OKX_TRADE_FILLS_PATH = "/api/v5/trade/fills"

# WebSocket channels
OKX_WS_ACCOUNT_CHANNEL = "account"
OKX_WS_ORDERS_CHANNEL = "orders"
OKX_WS_PUBLIC_TRADES_CHANNEL = "trades"
OKX_WS_PUBLIC_BOOKS_CHANNEL = "books"

OKX_WS_CHANNELS = {
    OKX_WS_ACCOUNT_CHANNEL,
    OKX_WS_ORDERS_CHANNEL
}

# Rate limiting
WS_CONNECTION_LIMIT_ID = "WSConnection"
WS_REQUEST_LIMIT_ID = "WSRequest"
WS_SUBSCRIPTION_LIMIT_ID = "WSSubscription"
WS_LOGIN_LIMIT_ID = "WSLogin"

ORDER_STATE = {
    "live": OrderState.OPEN,
    "filled": OrderState.FILLED,
    "partially_filled": OrderState.PARTIALLY_FILLED,
    "canceled": OrderState.CANCELED,
}

ORDER_TYPE_MAP = {
    OrderType.LIMIT: "limit",
    OrderType.MARKET: "market",
    OrderType.LIMIT_MAKER: "post_only",
}

NO_LIMIT = sys.maxsize

RATE_LIMITS = [
    RateLimit(WS_CONNECTION_LIMIT_ID, limit=3, time_interval=1),
    RateLimit(WS_REQUEST_LIMIT_ID, limit=100, time_interval=10),
    RateLimit(WS_SUBSCRIPTION_LIMIT_ID, limit=240, time_interval=60 * 60),
    RateLimit(WS_LOGIN_LIMIT_ID, limit=1, time_interval=15),
    RateLimit(limit_id=OKX_SERVER_TIME_PATH, limit=10, time_interval=2),
    RateLimit(limit_id=OKX_INSTRUMENTS_PATH, limit=20, time_interval=2),
    RateLimit(limit_id=OKX_TICKER_PATH, limit=20, time_interval=2),
    RateLimit(limit_id=OKX_TICKERS_PATH, limit=20, time_interval=2),
    RateLimit(limit_id=OKX_ORDER_BOOK_PATH, limit=20, time_interval=2),
    RateLimit(limit_id=OKX_PLACE_ORDER_PATH, limit=20, time_interval=2),
    RateLimit(limit_id=OKX_ORDER_DETAILS_PATH, limit=20, time_interval=2),
    RateLimit(limit_id=OKX_ORDER_CANCEL_PATH, limit=20, time_interval=2),
    RateLimit(limit_id=OKX_BATCH_ORDER_CANCEL_PATH, limit=300, time_interval=2),
    RateLimit(limit_id=OKX_BALANCE_PATH, limit=10, time_interval=2),
    RateLimit(limit_id=OKX_TRADE_FILLS_PATH, limit=60, time_interval=2),
]
