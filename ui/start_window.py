from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QCheckBox, QLabel, QFileDialog, QMessageBox, QGroupBox
)


class StartWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналізатор лог-файлів — вибір файлу")
        self.resize(480, 260)

        self.file_path = None
        self.main_window = None

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("1. Оберіть лог-файл (.log / .txt):"))

        file_row = QHBoxLayout()
        self.file_field = QLineEdit()
        self.file_field.setReadOnly(True)
        browse_button = QPushButton("Обрати файл...")
        browse_button.clicked.connect(self.choose_file)
        file_row.addWidget(self.file_field)
        file_row.addWidget(browse_button)
        layout.addLayout(file_row)

        pattern_box = QGroupBox("2. Патерни пошуку")
        pattern_layout = QVBoxLayout()

        self.check_error = QCheckBox("Error")
        self.check_denied = QCheckBox("Denied")
        self.check_failed = QCheckBox("Failed")
        self.check_warning = QCheckBox("Warning")

        for box in (self.check_error, self.check_denied, self.check_failed, self.check_warning):
            box.setChecked(True)
            pattern_layout.addWidget(box)

        custom_row = QHBoxLayout()
        custom_row.addWidget(QLabel("Власний шаблон:"))
        self.custom_field = QLineEdit()
        self.custom_field.setPlaceholderText("напр. timeout|refused")
        custom_row.addWidget(self.custom_field)
        pattern_layout.addLayout(custom_row)

        pattern_box.setLayout(pattern_layout)
        layout.addWidget(pattern_box)

        start_button = QPushButton("Аналізувати")
        start_button.clicked.connect(self.start_clicked)
        layout.addWidget(start_button)

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Оберіть лог-файл", "", "Log/Text files (*.log *.txt);;Усі файли (*)"
        )
        if path:
            self.file_path = path
            self.file_field.setText(path)

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