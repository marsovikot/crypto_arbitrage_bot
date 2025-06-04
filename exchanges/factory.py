import ccxt
import logging
from config import EXCHANGE_CONFIG


def get_exchange(name: str):
    """Instantiate a ccxt exchange with sane defaults."""
    name = name.lower()
    if name not in EXCHANGE_CONFIG:
        raise ValueError(f"Exchange config not found: {name}")

    exchange_class = getattr(ccxt, name)
    config = EXCHANGE_CONFIG[name]

    exchange = exchange_class({
        'apiKey': config['apiKey'],
        'secret': config['secret'],
        'enableRateLimit': True,
        'options': {'adjustForTimeDifference': True},
    })

    try:
        exchange.load_time_difference()
    except Exception as exc:
        logging.warning(f"[{name.upper()}] Could not sync time: {exc}")

    return exchange
