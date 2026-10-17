from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from services.auth_service import AuthError


class RegisterDialog(QDialog):
    def __init__(self, auth_service, parent=None):
        super().__init__(parent)
        self.auth = auth_service
        self.setWindowTitle("Регистрация")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel("Создание аккаунта")
        title.setStyleSheet("font-size: 20px; font-weight: 700;")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Логин (3–32 символа)")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль (не менее 8 символов)")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Повторите пароль")
        self.confirm.setEchoMode(QLineEdit.EchoMode.Password)

        button = QPushButton("Зарегистрироваться")
        button.clicked.connect(self.register)

        layout.addWidget(title)
        layout.addWidget(QLabel("Логин"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Пароль"))
        layout.addWidget(self.password)
        layout.addWidget(QLabel("Повтор пароля"))
        layout.addWidget(self.confirm)
        layout.addWidget(button)

    def register(self):
        if self.password.text() != self.confirm.text():
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return
        try:
            user = self.auth.register(self.username.text(), self.password.text())
        except AuthError as error:
            QMessageBox.warning(self, "Не удалось зарегистрироваться", str(error))
            return

        role_text = "администратор" if user["role"] == "admin" else "пользователь"
        QMessageBox.information(
            self, "Успех",
            f"Аккаунт «{user['username']}» создан.\nРоль: {role_text}."
        )
        self.accept()
