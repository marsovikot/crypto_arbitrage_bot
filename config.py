import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

EXCHANGE_CONFIG = {
    'binance': {
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_SECRET_KEY'),
    },
    'kucoin': {
        'apiKey': os.getenv('KUCOIN_API_KEY'),
        'secret': os.getenv('KUCOIN_SECRET_KEY'),
    },
    'bybit': {
        'apiKey': os.getenv('BYBIT_API_KEY'),
        'secret': os.getenv('BYBIT_SECRET_KEY'),
    },
    'okx': {
        'apiKey': os.getenv('OKX_API_KEY'),
        'secret': os.getenv('OKX_SECRET_KEY'),
    },
    'mexc': {
        'apiKey': os.getenv('MEXC_API_KEY'),
        'secret': os.getenv('MEXC_SECRET_KEY'),
    },
}
