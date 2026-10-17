from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


def apply_theme(app, theme_name):
    """Применяет светлую или тёмную цветовую палитру Qt."""
    app.setStyle("Fusion")
    palette = QPalette()

    if theme_name == "dark":
        palette.setColor(QPalette.ColorRole.Window, QColor("#171923"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#edf0f7"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#222635"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#2b3042"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#edf0f7"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#30364a"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#edf0f7"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#5378e5"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#a0a8bb"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#30364a"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#edf0f7"))
    else:
        palette.setColor(QPalette.ColorRole.Window, QColor("#f4f6fb"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#20263a"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#eef1f8"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#20263a"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#e7ebf5"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#20263a"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#4263d8"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#737d94"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#20263a"))

    app.setPalette(palette)
    app.setStyleSheet("""
        QWidget { font-size: 14px; }
        QLineEdit, QComboBox {
            padding: 8px; border: 1px solid palette(mid);
            border-radius: 7px; min-height: 20px;
        }
        QPushButton {
            padding: 8px 14px; border-radius: 7px;
            border: 1px solid palette(mid);
        }
        QPushButton:default { font-weight: bold; }
        QTableWidget { gridline-color: palette(mid); }
    """)
