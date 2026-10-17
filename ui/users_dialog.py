from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QComboBox, QLabel
)
from services.auth_service import AuthError


class UsersDialog(QDialog):
    def __init__(self, auth_service, current_user, parent=None):
        super().__init__(parent)
        self.auth = auth_service
        self.current_user = current_user
        self.setWindowTitle("Управление пользователями")
        self.resize(680, 400)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Администрирование учётных записей"))

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Роль", "Дата регистрации"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        controls = QHBoxLayout()
        self.role_box = QComboBox()
        self.role_box.addItem("Пользователь", "user")
        self.role_box.addItem("Администратор", "admin")
        role_button = QPushButton("Изменить роль")
        role_button.clicked.connect(self.change_role)
        delete_button = QPushButton("Удалить пользователя")
        delete_button.clicked.connect(self.delete_user)
        refresh_button = QPushButton("Обновить")
        refresh_button.clicked.connect(self.refresh)
        controls.addWidget(self.role_box)
        controls.addWidget(role_button)
        controls.addWidget(delete_button)
        controls.addWidget(refresh_button)
        layout.addLayout(controls)

        self.refresh()

    def selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Не выбран пользователь", "Сначала выберите строку.")
            return None
        return int(self.table.item(row, 0).text())

    def refresh(self):
        try:
            users = self.auth.list_users(self.current_user)
        except AuthError as error:
            QMessageBox.warning(self, "Ошибка доступа", str(error))
            self.reject()
            return
        self.table.setRowCount(len(users))
        for row_index, user in enumerate(users):
            values = [
                str(user["id"]),
                user["username"],
                "Администратор" if user["role"] == "admin" else "Пользователь",
                user["created_at"],
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_index, column, item)

    def change_role(self):
        target_id = self.selected_id()
        if target_id is None:
            return
        role = self.role_box.currentData()
        try:
            self.auth.set_role(self.current_user, target_id, role)
        except AuthError as error:
            QMessageBox.warning(self, "Не удалось изменить роль", str(error))
            return
        self.refresh()

    def delete_user(self):
        target_id = self.selected_id()
        if target_id is None:
            return
        answer = QMessageBox.question(
            self, "Подтверждение",
            "Удалить выбранного пользователя? Это действие нельзя отменить."
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.auth.delete_user(self.current_user, target_id)
        except AuthError as error:
            QMessageBox.warning(self, "Не удалось удалить пользователя", str(error))
            return
        self.refresh()
