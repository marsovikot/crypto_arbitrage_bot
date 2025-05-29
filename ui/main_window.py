import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from config import EXCHANGE_CONFIG


class ExchangeWidget(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name

        self.checkbox = QCheckBox()
        self.name_label = QLabel(name.capitalize())
        self.status = QLabel("❌")
        self.status.setFont(QFont("Arial", 18))

        logo = QLabel()
        path = os.path.join("assets", f"{name}.png")
        if os.path.exists(path):
            pixmap = QPixmap(path).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio)
            logo.setPixmap(pixmap)
        else:
            logo.setText("[Logo]")

        layout = QHBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.status)
        self.setLayout(layout)

    def set_status(self, connected: bool):
        self.status.setText("✅" if connected else "❌")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arbitrage Bot")
        self.setGeometry(100, 100, 500, 500)

        self.exchanges = {}
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        layout = QVBoxLayout()

        for name in EXCHANGE_CONFIG.keys():
            ex_widget = ExchangeWidget(name)
            layout.addWidget(ex_widget)
            self.exchanges[name] = ex_widget

        self.connect_button = QPushButton("Подключиться")
        self.connect_button.clicked.connect(self.connect_exchanges)
        layout.addWidget(self.connect_button, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(QLabel("Лог:"))
        layout.addWidget(self.logs)

        self.setLayout(layout)

    def log(self, message: str):
        self.logs.append(message)
        print(message)

    def connect_exchanges(self):
        from exchanges.factory import get_exchange

        for name, widget in self.exchanges.items():
            if widget.checkbox.isChecked():
                try:
                    exchange = get_exchange(name)
                    ticker = exchange.fetch_ticker('BTC/USDT')
                    widget.set_status(True)
                    self.log(f"[{name.upper()}] Подключение успешно. Цена BTC/USDT: {ticker['last']}")
                except Exception as e:
                    widget.set_status(False)
                    self.log(f"[{name.upper()}] ❌ Ошибка подключения: {e}")
            else:
                widget.set_status(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
