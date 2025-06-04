import asyncio
from typing import Dict, List

from exchanges.factory import get_exchange
from core.executor import Executor


class ArbitrageBot:
    """Simple arbitrage bot fetching prices and generating trade signals."""

    def __init__(self, exchanges: List[str], symbol: str = "BTC/USDT", threshold: float = 0.5, interval: int = 5):
        self.symbol = symbol
        self.threshold = threshold
        self.interval = interval
        self.exchanges = {name: get_exchange(name) for name in exchanges}
        self.executor = Executor()

    async def fetch_prices(self) -> Dict[str, float]:
        """Fetch ticker prices from all configured exchanges."""
        prices: Dict[str, float] = {}
        for name, ex in self.exchanges.items():
            try:
                ticker = await asyncio.to_thread(ex.fetch_ticker, self.symbol)
                prices[name] = ticker["last"]
            except Exception as exc:
                print(f"[{name.upper()}] Failed to fetch price: {exc}")
        return prices

    def evaluate_spread(self, prices: Dict[str, float]):
        """Compare spread across exchanges and generate trade signal."""
        if len(prices) < 2:
            return
        buy_exchange = min(prices, key=prices.get)
        sell_exchange = max(prices, key=prices.get)
        buy_price = prices[buy_exchange]
        sell_price = prices[sell_exchange]
        spread = (sell_price - buy_price) / buy_price * 100
        print(
            f"Prices: {prices} | Best buy: {buy_exchange} {buy_price} | Best sell: {sell_exchange} {sell_price} | Spread: {spread:.2f}%"
        )
        if spread >= self.threshold:
            print(f"Arbitrage opportunity detected: {spread:.2f}% spread")
            self.executor.place_order(buy_exchange, "buy", self.symbol, 1, buy_price)
            self.executor.place_order(sell_exchange, "sell", self.symbol, 1, sell_price)

    async def run(self):
        """Main loop fetching prices and checking for arbitrage."""
        while True:
            prices = await self.fetch_prices()
            self.evaluate_spread(prices)
            await asyncio.sleep(self.interval)
