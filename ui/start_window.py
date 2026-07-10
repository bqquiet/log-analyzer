from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
    QCheckBox, QLabel, QFileDialog, QMessageBox, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui.styles import STYLE
from ui.colors import get_category_color


class StartWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналізатор лог-файлів — вибір файлу")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(520, 420)
        self.setAcceptDrops(True)

        self.file_path = None
        self.main_window = None

        self.build_ui()
        self.setStyleSheet(STYLE)

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("1. Оберіть лог-файл")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        self.drop_label = QLabel("📂  Перетягніть .log / .txt файл сюди\nабо натисніть кнопку нижче")
        self.drop_label.setObjectName("dropZone")
        self.drop_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.drop_label)

        file_row = QHBoxLayout()
        self.file_field = QLineEdit()
        self.file_field.setReadOnly(True)
        self.file_field.setPlaceholderText("Файл не обрано")
        browse_button = QPushButton("Обрати файл...")
        browse_button.setObjectName("secondaryButton")
        browse_button.clicked.connect(self.choose_file)
        file_row.addWidget(self.file_field)
        file_row.addWidget(browse_button)
        layout.addLayout(file_row)

        pattern_title = QLabel("2. Патерни пошуку")
        pattern_title.setObjectName("sectionTitle")
        layout.addWidget(pattern_title)

        pattern_card = QFrame()
        pattern_card.setObjectName("card")
        pattern_layout = QVBoxLayout(pattern_card)
        pattern_layout.setContentsMargins(18, 16, 18, 18)
        pattern_layout.setSpacing(14)

        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(10)

        self.check_error = self.make_category_checkbox("Error")
        self.check_denied = self.make_category_checkbox("Denied")
        self.check_failed = self.make_category_checkbox("Failed")
        self.check_warning = self.make_category_checkbox("Warning")

        grid.addWidget(self.check_error, 0, 0)
        grid.addWidget(self.check_denied, 0, 1)
        grid.addWidget(self.check_failed, 1, 0)
        grid.addWidget(self.check_warning, 1, 1)
        pattern_layout.addLayout(grid)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #eceff1;")
        pattern_layout.addWidget(divider)

        custom_label = QLabel("Власний регулярний вираз (необов'язково)")
        custom_label.setStyleSheet("font-weight: 600; font-size: 12px;")
        pattern_layout.addWidget(custom_label)

        self.custom_field = QLineEdit()
        self.custom_field.setPlaceholderText("напр. timeout|refused")
        self.custom_field.setFont(QFont("Consolas", 10))
        pattern_layout.addWidget(self.custom_field)

        layout.addWidget(pattern_card)

        start_button = QPushButton("Аналізувати")
        start_button.clicked.connect(self.start_clicked)
        layout.addWidget(start_button)

    def make_category_checkbox(self, category):
        colors = get_category_color(category)
        checkbox = QCheckBox(category)
        checkbox.setChecked(True)
        checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {colors['text']};
                font-weight: 600;
                font-size: 13px;
                padding: 4px;
            }}
        """)
        return checkbox

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            path = event.mimeData().urls()[0].toLocalFile()
            if path.lower().endswith((".log", ".txt")):
                event.acceptProposedAction()

    def dropEvent(self, event):
        path = event.mimeData().urls()[0].toLocalFile()
        self.file_path = path
        self.file_field.setText(path)
        file_name = path.replace(chr(92), "/").split("/")[-1]
        self.drop_label.setText(f"✅  Обрано: {file_name}")

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Оберіть лог-файл", "", "Log/Text files (*.log *.txt);;Усі файли (*)"
        )
        if path:
            self.file_path = path
            self.file_field.setText(path)
            file_name = path.replace(chr(92), "/").split("/")[-1]
            self.drop_label.setText(f"✅  Обрано: {file_name}")

    def get_patterns(self):
        patterns = {}
        if self.check_error.isChecked():
            patterns["Error"] = r"\berror\b"
        if self.check_denied.isChecked():
            patterns["Denied"] = r"\bdenied\b"
        if self.check_failed.isChecked():
            patterns["Failed"] = r"\bfailed\b|authentication failure"
        if self.check_warning.isChecked():
            patterns["Warning"] = r"\bwarning\b"

        custom = self.custom_field.text().strip()
        if custom:
            patterns["Custom"] = custom

        return patterns

    def start_clicked(self):
        if not self.file_path:
            QMessageBox.warning(self, "Помилка", "Спочатку оберіть лог-файл.")
            return

        patterns = self.get_patterns()
        if not patterns:
            QMessageBox.warning(self, "Помилка", "Оберіть хоча б один патерн пошуку.")
            return

        from ui.main_window import MainWindow

        try:
            self.main_window = MainWindow(self.file_path, patterns)
        except Exception as error:
            QMessageBox.critical(self, "Помилка аналізу", str(error))
            return

        self.main_window.show()
        self.close()