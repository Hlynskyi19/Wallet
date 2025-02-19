import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
)


class WalletApp(QWidget):
    def __init__(self):
        super().__init__()

        self.balance = 0  # Початковий баланс

        # Налаштування інтерфейсу
        self.setWindowTitle("Гаманець")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.balance_label = QLabel(f"Баланс: {self.balance} грн", self)
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
            self.balance += amount
            self.update_balance()

    def add_expense(self):
        amount = self.get_amount()
        if amount is not None:
            if amount > self.balance:
                QMessageBox.warning(self, "Помилка", "Недостатньо коштів!")
            else:
                self.balance -= amount
                self.update_balance()

    def get_amount(self):
        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                QMessageBox.warning(self, "Помилка", "Сума має бути більшою за 0!")
                return None
            return amount
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Введіть коректне число!")
            return None

    def update_balance(self):
        self.balance_label.setText(f"Баланс: {self.balance} грн")
        self.amount_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WalletApp()
    window.show()
    sys.exit(app.exec_())
