from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox
)
from ui.change_password_dialog import ChangePasswordDialog
from ui.users_dialog import UsersDialog
from ui.theme import apply_theme


class DashboardWindow(QMainWindow):
    def __init__(self, auth_service, user, app, settings, logout_callback):
        super().__init__()
        self.auth = auth_service
        self.user = user
        self.app = app
        self.settings = settings
        self.logout_callback = logout_callback

        self.setWindowTitle("AuthorizationApp — Личный кабинет")
        self.setMinimumSize(480, 300)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(30, 28, 30, 28)
        layout.setSpacing(14)

        title = QLabel(f"Добро пожаловать, {user['username']}!")
        title.setStyleSheet("font-size: 24px; font-weight: 700;")
        role = "Администратор" if user["role"] == "admin" else "Пользователь"
        details = QLabel(
            f"ID аккаунта: {user['id']}\n"
            f"Роль: {role}\n"
            f"Дата регистрации: {user['created_at']}"
        )
        details.setWordWrap(True)

        password_button = QPushButton("Сменить пароль")
        password_button.clicked.connect(self.open_change_password)

        layout.addWidget(title)
        layout.addWidget(details)
        layout.addSpacing(8)
        layout.addWidget(password_button)

        if user["role"] == "admin":
            users_button = QPushButton("Управление пользователями")
            users_button.clicked.connect(self.open_users)
            layout.addWidget(users_button)

        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("Оформление"))
        theme_button = QPushButton("Переключить тему")
        theme_button.clicked.connect(self.toggle_theme)
        theme_row.addWidget(theme_button)
        layout.addLayout(theme_row)

        logout_button = QPushButton("Выйти из аккаунта")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)
        layout.addStretch()
        self.setCentralWidget(central)

    def open_change_password(self):
        dialog = ChangePasswordDialog(self.auth, self.user, self)
        dialog.exec()

    def open_users(self):
        UsersDialog(self.auth, self.user, self).exec()

    def toggle_theme(self):
        self.settings["theme"] = "dark" if self.settings["theme"] == "light" else "light"
        apply_theme(self.app, self.settings["theme"])

    def logout(self):
        answer = QMessageBox.question(
            self, "Выход", "Выйти из аккаунта?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.close()
        self.logout_callback()
