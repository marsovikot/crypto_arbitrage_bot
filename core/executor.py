import logging


class Executor:
    """Simulate order placement on an exchange."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def place_order(self, exchange: str, side: str, symbol: str, amount: float, price: float) -> None:
        self.logger.info(
            "[SIMULATED ORDER] %s %.4f %s on %s at %s",
            side.upper(),
            amount,
            symbol,
            exchange.upper(),
            price,
        )
