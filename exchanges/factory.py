import ccxt
from config import EXCHANGE_CONFIG


def get_exchange(name: str):
    name = name.lower()
    if name not in EXCHANGE_CONFIG:
        raise ValueError(f"Exchange config not found: {name}")

    exchange_class = getattr(ccxt, name)
    config = EXCHANGE_CONFIG[name]

    return exchange_class({
        'apiKey': config['apiKey'],
        'secret': config['secret'],
        'enableRateLimit': True,
    })
