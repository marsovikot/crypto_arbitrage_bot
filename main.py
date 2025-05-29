from exchanges.factory import get_exchange
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
)

def test_exchange_connection(exchange_name: str):
    try:
        exchange = get_exchange(exchange_name)
        ticker = exchange.fetch_ticker('BTC/USDT')
        logging.info(f"[{exchange_name.upper()}] Connected. BTC/USDT price: {ticker['last']}")
    except Exception as e:
        logging.error(f"[{exchange_name.upper()}] Connection failed: {e}")

if __name__ == "__main__":
    exchanges = ['binance', 'kucoin', 'bybit', 'okx', 'mexc']

    for ex in exchanges:
        test_exchange_connection(ex)
