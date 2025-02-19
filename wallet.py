import sys
import pytest
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
)


class Wallet:
    """Клас гаманця для управління балансом."""

    def __init__(self):
        self.balance = 0

    def add_income(self, amount: float):
        if amount <= 0:
            raise ValueError("Сума має бути більшою за 0!")
        self.balance += amount

    def add_expense(self, amount: float):
        if amount <= 0:
            raise ValueError("Сума має бути більшою за 0!")
        if amount > self.balance:
            raise ValueError("Недостатньо коштів!")
        self.balance -= amount

    def get_balance(self):
        return self.balance


class WalletApp(QWidget):
    """Графічний інтерфейс PyQt5 для гаманця."""

    def __init__(self):
        super().__init__()
        self.wallet = Wallet()

        self.setWindowTitle("Гаманець")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.balance_label = QLabel(f"Баланс: {self.wallet.get_balance()} грн", self)
        layout.addWidget(self.balance_label)

        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Введіть суму")
        layout.addWidget(self.amount_input)

        self.income_button = QPushButton("Додати дохід", self)
        self.income_button.clicked.connect(self.add_income)
        layout.addWidget(self.income_button)

        self.expense_button = QPushButton("Додати витрату", self)
        self.expense_button.clicked.connect(self.add_expense)
        layout.addWidget(self.expense_button)

        self.setLayout(layout)

    def add_income(self):
        amount = self.get_amount()
        if amount is not None:
            try:
                self.wallet.add_income(amount)
                self.update_balance()
            except ValueError as e:
                QMessageBox.warning(self, "Помилка", str(e))

    def add_expense(self):
        amount = self.get_amount()
        if amount is not None:
            try:
                self.wallet.add_expense(amount)
                self.update_balance()
            except ValueError as e:
                QMessageBox.warning(self, "Помилка", str(e))

    def get_amount(self):
        try:
            amount = float(self.amount_input.text())
            return amount
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Введіть коректне число!")
            return None

    def update_balance(self):
        self.balance_label.setText(f"Баланс: {self.wallet.get_balance()} грн")
        self.amount_input.clear()


def run_app():
    app = QApplication(sys.argv)
    window = WalletApp()
    window.show()
    sys.exit(app.exec_())


# --- Pytest тести ---
def test_initial_balance():
    wallet = Wallet()
    assert wallet.get_balance() == 0


def test_add_income():
    wallet = Wallet()
    wallet.add_income(100)
    assert wallet.get_balance() == 100


def test_add_expense():
    wallet = Wallet()
    wallet.add_income(200)
    wallet.add_expense(50)
    assert wallet.get_balance() == 150


def test_expense_exceeds_balance():
    wallet = Wallet()
    wallet.add_income(50)
    with pytest.raises(ValueError, match="Недостатньо коштів!"):
        wallet.add_expense(100)


def test_negative_income():
    wallet = Wallet()
    with pytest.raises(ValueError, match="Сума має бути більшою за 0!"):
        wallet.add_income(-10)


def test_negative_expense():
    wallet = Wallet()
    with pytest.raises(ValueError, match="Сума має бути більшою за 0!"):
        wallet.add_expense(-5)


# Запуск застосунку
if __name__ == "__main__":
    run_app()
