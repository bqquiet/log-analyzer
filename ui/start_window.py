from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit,
    QCheckBox, QLabel, QFileDialog, QFrame, QStackedWidget,
    QProgressBar, QWidget, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer
from ui.styles import STYLE
from ui.colors import get_category_color
from ui.analysis_worker import AnalysisWorker


class StartWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналізатор лог-файлів — вибір файлу")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.resize(520, 440)
        self.setAcceptDrops(True)

        self.file_path = None
        self.main_window = None
        self.worker = None

        self.build_ui()
        self.setStyleSheet(STYLE)

    def build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        outer_layout.addWidget(self.stack)

        self.stack.addWidget(self.build_form_page())
        self.stack.addWidget(self.build_progress_page())

        self.toast_label = QLabel("", self)
        self.toast_label.setObjectName("toastWarning")
        self.toast_label.setAlignment(Qt.AlignCenter)
        self.toast_opacity = QGraphicsOpacityEffect(self.toast_label)
        self.toast_label.setGraphicsEffect(self.toast_opacity)
        self.toast_opacity.setOpacity(0)
        self.toast_label.hide()

    def show_toast(self, message, duration=1800, error=False):
        self.toast_label.setObjectName("toastError" if error else "toastWarning")
        self.toast_label.style().unpolish(self.toast_label)
        self.toast_label.style().polish(self.toast_label)
        self.toast_label.setText(message)
        self.toast_label.setWordWrap(True)
        self.toast_label.adjustSize()

        button_top_left = self.start_button.mapTo(self, self.start_button.rect().topLeft())
        x = (self.width() - self.toast_label.width()) // 2
        y = button_top_left.y() - self.toast_label.height() - 12
        self.toast_label.move(x, y)
        self.toast_label.show()
        self.toast_label.raise_()

        self.fade_in = QPropertyAnimation(self.toast_opacity, b"opacity")
        self.fade_in.setDuration(180)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()

        QTimer.singleShot(duration, self.fade_out_toast)

    def fade_out_toast(self):
        self.fade_out = QPropertyAnimation(self.toast_opacity, b"opacity")
        self.fade_out.setDuration(350)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.finished.connect(self.toast_label.hide)
        self.fade_out.start()

    def build_form_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
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

        layout.addWidget(pattern_card)

        self.start_button = QPushButton("Аналізувати")
        self.start_button.clicked.connect(self.start_clicked)
        layout.addWidget(self.start_button)

        return page

    def build_progress_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(6)

        icon_label = QLabel("🔍")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 40px;")
        layout.addWidget(icon_label)
        layout.addSpacing(12)

        title = QLabel("Аналізуємо файл")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        self.progress_status_label = QLabel("Читання файлу...")
        self.progress_status_label.setAlignment(Qt.AlignCenter)
        self.progress_status_label.setStyleSheet("color: #607d8b; font-size: 12px;")
        layout.addWidget(self.progress_status_label)
        layout.addSpacing(18)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setFixedWidth(320)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        layout.addSpacing(14)

        hint = QLabel("Великі файли можуть аналізуватись кілька секунд")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #b0bec5; font-size: 11px;")
        layout.addWidget(hint)

        return page

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

        return patterns

    def start_clicked(self):
        if not self.file_path:
            self.show_toast("Спочатку оберіть лог-файл")
            return

        patterns = self.get_patterns()
        if not patterns:
            self.show_toast("Оберіть хоча б один патерн пошуку")
            return

        self.progress_bar.setValue(0)
        self.progress_status_label.setText("Читання файлу...")
        self.stack.setCurrentIndex(1)

        self.worker = AnalysisWorker(self.file_path, patterns)
        self.worker.progress_changed.connect(self.on_progress_changed)
        self.worker.finished_successfully.connect(self.on_analysis_finished)
        self.worker.failed.connect(self.on_analysis_failed)
        self.worker.start()

    def on_progress_changed(self, percent, status_text):
        self.progress_bar.setValue(percent)
        self.progress_status_label.setText(status_text)

    def on_analysis_finished(self, analyzer):
        from ui.main_window import MainWindow

        self.main_window = MainWindow(analyzer)
        self.main_window.show()
        self.close()

    def on_analysis_failed(self, message):
        self.stack.setCurrentIndex(0)
        self.show_toast(message, duration=3500, error=True)