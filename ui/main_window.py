import sys
import logging
import asyncio
import threading

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

from config import EXCHANGE_CONFIG


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arbitrage Bot")
        self.setGeometry(100, 100, 300, 150)

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_and_start)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.connect_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

    def connect_and_start(self):
        from exchanges.factory import get_exchange

        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

        for name in EXCHANGE_CONFIG.keys():
            try:
                exchange = get_exchange(name)
                ticker = exchange.fetch_ticker('BTC/USDT')
                logging.info(f"[{name.upper()}] Connected. BTC/USDT price: {ticker['last']}")
            except Exception as e:
                logging.error(f"[{name.upper()}] Connection failed: {e}")

        def run_bot():
            from core.arbitrage import ArbitrageBot
            asyncio.run(ArbitrageBot(list(EXCHANGE_CONFIG.keys())).run())

        threading.Thread(target=run_bot, daemon=True).start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

