from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QFileDialog, QMessageBox,
    QFrame, QSplitter, QMenu, QApplication, QAbstractItemView,
    QGraphicsOpacityEffect
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QEvent, QPropertyAnimation, QTimer

from storage.file_storage import FileStorage
from ui.chart_widget import StatsChartWidget
from ui.copy_button import CopyButton
from ui.colors import get_category_color
from ui.styles import STYLE

ROW_TINT = {
    "Error": QColor("#fdecea"),
    "Denied": QColor("#fff8e1"),
    "Failed": QColor("#e3f2fd"),
    "Warning": QColor("#e8f5e9"),
}


class MainWindow(QMainWindow):
    def __init__(self, analyzer):
        super().__init__()
        self.setWindowTitle("Аналізатор лог-файлів — результати")
        self.resize(920, 760)
        self.setMinimumSize(700, 560)

        self.start_window = None
        self.active_filter = None
        self.filter_buttons = {}
        self.hover_row = -1

        self.analyzer = analyzer

        self.build_ui()
        self.fill_table()
        self.update_stats_label()
        self.chart.set_data(self.analyzer.get_statistics())
        self.setStyleSheet(STYLE)

    def build_ui(self):
        central = QWidget()
        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setSpacing(16)

        top_row = QHBoxLayout()
        self.stats_label = QLabel()
        self.stats_label.setObjectName("statsLabel")
        top_row.addWidget(self.stats_label, stretch=1)

        new_analysis_button = QPushButton("Новий аналіз")
        new_analysis_button.setObjectName("ghostButton")
        new_analysis_button.clicked.connect(self.start_new_analysis)
        top_row.addWidget(new_analysis_button)
        outer_layout.addLayout(top_row)

        table_card = self.make_card("Знайдені записи")
        table_card_layout = table_card.layout()

        filter_row = QHBoxLayout()
        filter_row.setSpacing(8)
        filter_row.addWidget(QLabel("Фільтр:"))
        for category in self.analyzer.get_statistics().keys():
            button = QPushButton(category)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, c=category: self.toggle_filter(c))
            self.filter_buttons[category] = button
            self.style_filter_button(button, category, active=False)
            filter_row.addWidget(button)
        filter_row.addStretch()
        table_card_layout.addLayout(filter_row)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Рядок", "Категорія", "Текст"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(32)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_table_context_menu)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setMouseTracking(True)
        self.table.viewport().setMouseTracking(True)
        self.table.cellEntered.connect(self.on_cell_entered)
        self.table.viewport().installEventFilter(self)
        table_card_layout.addWidget(self.table)

        self.hover_copy_button = CopyButton(self.table.viewport())
        self.hover_copy_button.setToolTip("Копіювати рядок")
        self.hover_copy_button.hide()
        self.hover_copy_button.clicked.connect(self.copy_hover_row)

        chart_card = self.make_card("Статистика за категоріями")
        chart_card_layout = chart_card.layout()
        self.chart = StatsChartWidget()
        chart_card_layout.addWidget(self.chart)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(table_card)
        splitter.addWidget(chart_card)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        splitter.setChildrenCollapsible(False)
        outer_layout.addWidget(splitter, stretch=1)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)
        button_row.addStretch()
        save_txt_button = QPushButton("Зберегти звіт (TXT)")
        save_txt_button.setObjectName("secondaryButton")
        save_txt_button.clicked.connect(self.save_report_txt)
        save_json_button = QPushButton("Зберегти звіт (JSON)")
        save_json_button.clicked.connect(self.save_report_json)
        button_row.addWidget(save_txt_button)
        button_row.addWidget(save_json_button)
        outer_layout.addLayout(button_row)

        self.setCentralWidget(central)

        self.toast_label = QLabel("", self)
        self.toast_label.setObjectName("toastLabel")
        self.toast_label.setAlignment(Qt.AlignCenter)
        self.toast_opacity = QGraphicsOpacityEffect(self.toast_label)
        self.toast_label.setGraphicsEffect(self.toast_opacity)
        self.toast_opacity.setOpacity(0)
        self.toast_label.hide()

    def style_filter_button(self, button, category, active):
        colors = get_category_color(category)
        if active:
            style = f"""
                QPushButton {{
                    background-color: {colors['border']};
                    color: white;
                    border: 1px solid {colors['border']};
                    border-radius: 14px;
                    padding: 6px 14px;
                    font-size: 12px;
                    font-weight: 600;
                }}
            """
        else:
            style = f"""
                QPushButton {{
                    background-color: #ffffff;
                    color: {colors['text']};
                    border: 1px solid {colors['border']};
                    border-radius: 14px;
                    padding: 6px 14px;
                    font-size: 12px;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {colors['bg']};
                }}
            """
        button.setStyleSheet(style)

    def make_card(self, title_text):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel(title_text)
        title.setObjectName("cardTitle")
        layout.addWidget(title)

        return card

    def fill_table(self):
        entries = self.analyzer.get_entries()

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            line_item = QTableWidgetItem()
            line_item.setData(0, entry.line_number)
            level_item = QTableWidgetItem(entry.level)
            text_item = QTableWidgetItem(entry.message)

            colors = get_category_color(entry.level)
            tint = ROW_TINT.get(entry.level)
            if tint:
                line_item.setBackground(tint)
                text_item.setBackground(tint)

            level_item.setBackground(QColor(colors["bg"]))
            level_item.setForeground(QColor(colors["text"]))
            bold_font = level_item.font()
            bold_font.setBold(True)
            level_item.setFont(bold_font)

            self.table.setItem(row, 0, line_item)
            self.table.setItem(row, 1, level_item)
            self.table.setItem(row, 2, text_item)

        self.table.setSortingEnabled(True)

    def toggle_filter(self, category):
        if self.active_filter == category:
            self.active_filter = None
        else:
            self.active_filter = category

        for name, button in self.filter_buttons.items():
            is_active = name == self.active_filter
            button.setChecked(is_active)
            self.style_filter_button(button, name, active=is_active)

        self.apply_filter()

    def apply_filter(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.table.setUpdatesEnabled(False)
        self.table.setSortingEnabled(False)

        for row in range(self.table.rowCount()):
            level_item = self.table.item(row, 1)
            if level_item is None:
                continue
            should_hide = (
                self.active_filter is not None and level_item.text() != self.active_filter
            )
            self.table.setRowHidden(row, should_hide)

        self.table.setSortingEnabled(True)
        self.table.setUpdatesEnabled(True)
        QApplication.restoreOverrideCursor()

    def on_cell_entered(self, row, column):
        if self.table.isRowHidden(row):
            self.hover_copy_button.hide()
            return

        self.hover_row = row
        last_column = self.table.columnCount() - 1
        rect = self.table.visualRect(self.table.model().index(row, last_column))

        button_size = 30
        x = rect.right() - button_size - 8
        y = rect.top() + (rect.height() - button_size) // 2

        self.hover_copy_button.move(x, y)
        self.hover_copy_button.show()
        self.hover_copy_button.raise_()

    def eventFilter(self, source, event):
        if source is self.table.viewport() and event.type() == QEvent.Leave:
            self.hover_copy_button.hide()
        return super().eventFilter(source, event)

    def copy_hover_row(self):
        if self.hover_row < 0:
            return
        self.copy_row_to_clipboard(self.hover_row)

    def copy_row_to_clipboard(self, row):
        values = []
        for column in range(self.table.columnCount()):
            item = self.table.item(row, column)
            values.append(item.text() if item else "")
        QApplication.clipboard().setText("  |  ".join(values))
        self.show_toast("Скопійовано")

    def show_toast(self, message):
        self.toast_label.setText(message)
        self.toast_label.adjustSize()

        x = (self.width() - self.toast_label.width()) // 2
        y = self.height() - self.toast_label.height() - 36
        self.toast_label.move(x, y)
        self.toast_label.show()
        self.toast_label.raise_()

        self.fade_in = QPropertyAnimation(self.toast_opacity, b"opacity")
        self.fade_in.setDuration(180)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()

        QTimer.singleShot(1300, self.fade_out_toast)

    def fade_out_toast(self):
        self.fade_out = QPropertyAnimation(self.toast_opacity, b"opacity")
        self.fade_out.setDuration(350)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.finished.connect(self.toast_label.hide)
        self.fade_out.start()

    def show_table_context_menu(self, position):
        row = self.table.rowAt(position.y())
        if row < 0:
            return

        menu = QMenu(self)
        copy_action = menu.addAction("Копіювати рядок")
        action = menu.exec_(self.table.viewport().mapToGlobal(position))

        if action == copy_action:
            self.copy_row_to_clipboard(row)

    def start_new_analysis(self):
        from ui.start_window import StartWindow

        self.start_window = StartWindow()
        self.start_window.show()
        self.close()

    def update_stats_label(self):
        stats = self.analyzer.get_statistics()
        if not stats:
            self.stats_label.setText("Підозрілих записів не знайдено.")
            return
        parts = [f"{level}: {count}" for level, count in stats.items()]
        self.stats_label.setText("Знайдено — " + "   ".join(parts))

    def save_report_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "Зберегти звіт", "report.json", "JSON (*.json)")
        if not path:
            return
        try:
            FileStorage.write_json_report(path, self.analyzer.to_report_dict())
            self.show_toast("Звіт збережено")
        except OSError as error:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти файл: {error}")

    def save_report_txt(self):
        path, _ = QFileDialog.getSaveFileName(self, "Зберегти звіт", "report.txt", "Text (*.txt)")
        if not path:
            return
        try:
            FileStorage.write_txt_report(path, self.analyzer.to_report_dict())
            self.show_toast("Звіт збережено")
        except OSError as error:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти файл: {error}")