class Executor:
    """Simulate order placement on an exchange."""

    def place_order(self, exchange: str, side: str, symbol: str, amount: float, price: float) -> None:
        print(
            f"[SIMULATED ORDER] {side.upper()} {amount} {symbol} on {exchange.upper()} at {price}"
        )
