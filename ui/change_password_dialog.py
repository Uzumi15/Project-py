from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from services.auth_service import AuthError


class ChangePasswordDialog(QDialog):
    def __init__(self, auth_service, user, parent=None):
        super().__init__(parent)
        self.auth = auth_service
        self.user = user
        self.setWindowTitle("Смена пароля")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        self.old_password = QLineEdit()
        self.old_password.setPlaceholderText("Текущий пароль")
        self.old_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Новый пароль (от 8 символов)")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Повторите новый пароль")
        self.confirm.setEchoMode(QLineEdit.EchoMode.Password)

        button = QPushButton("Изменить пароль")
        button.clicked.connect(self.change_password)

        layout.addWidget(QLabel("Введите текущий и новый пароли."))
        layout.addWidget(self.old_password)
        layout.addWidget(self.new_password)
        layout.addWidget(self.confirm)
        layout.addWidget(button)

    def change_password(self):
        if self.new_password.text() != self.confirm.text():
            QMessageBox.warning(self, "Ошибка", "Новые пароли не совпадают.")
            return
        try:
            self.auth.change_password(
                self.user, self.old_password.text(), self.new_password.text()
            )
        except AuthError as error:
            QMessageBox.warning(self, "Не удалось изменить пароль", str(error))
            return
        QMessageBox.information(self, "Успех", "Пароль успешно изменён.")
        self.accept()
