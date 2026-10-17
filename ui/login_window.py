from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QCheckBox
)
from services.auth_service import AuthError
from ui.register_window import RegisterDialog
from ui.dashboard_window import DashboardWindow
from ui.theme import apply_theme


class LoginWindow(QMainWindow):
    def __init__(self, auth_service, app, settings):
        super().__init__()
        self.auth = auth_service
        self.app = app
        self.settings = settings
        self.dashboard = None
        self.setWindowTitle("AuthorizationApp — Вход")
        self.setMinimumWidth(390)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(12)

        title = QLabel("Вход в систему")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        subtitle = QLabel("Войдите или создайте учебную учётную запись")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Логин")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.returnPressed.connect(self.do_login)

        self.show_password = QCheckBox("Показать пароль")
        self.show_password.toggled.connect(
            lambda checked: self.password.setEchoMode(
                QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
            )
        )

        login_button = QPushButton("Войти")
        login_button.setDefault(True)
        login_button.clicked.connect(self.do_login)
        register_button = QPushButton("Создать аккаунт")
        register_button.clicked.connect(self.open_register)

        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("Тема:"))
        self.theme_button = QPushButton(self.theme_label())
        self.theme_button.clicked.connect(self.toggle_theme)
        theme_row.addWidget(self.theme_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(QLabel("Логин"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Пароль"))
        layout.addWidget(self.password)
        layout.addWidget(self.show_password)
        layout.addWidget(login_button)
        layout.addWidget(register_button)
        layout.addSpacing(8)
        layout.addLayout(theme_row)
        self.setCentralWidget(central)

    def theme_label(self):
        return "Тёмная" if self.settings["theme"] == "light" else "Светлая"

    def toggle_theme(self):
        self.settings["theme"] = "dark" if self.settings["theme"] == "light" else "light"
        apply_theme(self.app, self.settings["theme"])
        self.theme_button.setText(self.theme_label())

    def open_register(self):
        dialog = RegisterDialog(self.auth, self)
        dialog.exec()

    def do_login(self):
        try:
            user = self.auth.login(self.username.text(), self.password.text())
        except AuthError as error:
            QMessageBox.warning(self, "Не удалось войти", str(error))
            return

        self.password.clear()
        self.dashboard = DashboardWindow(
            self.auth, user, self.app, self.settings, self.show_login_again
        )
        self.dashboard.show()
        self.hide()

    def show_login_again(self):
        self.username.clear()
        self.password.clear()
        self.show()
        self.raise_()
        self.activateWindow()
