import sys

from PySide6.QtWidgets import QApplication
from database.database import Database
from services.auth_service import AuthService
from ui.login_window import LoginWindow
from ui.theme import apply_theme


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AuthorizationApp")
    app.setOrganizationName("StudyProject")

    database = Database()
    database.initialize()
    auth_service = AuthService(database)

    settings = app.property("theme_settings")
    if settings is None:
        settings = {"theme": "light"}
        app.setProperty("theme_settings", settings)
    apply_theme(app, settings["theme"])

    window = LoginWindow(auth_service, app, settings)
    window.show()

    exit_code = app.exec()
    database.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
