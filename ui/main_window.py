from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLabel, QFileDialog, QMessageBox, QFrame
)
from PyQt5.QtGui import QColor

from models.log_analyzer import LogAnalyzer
from storage.file_storage import FileStorage
from ui.chart_widget import StatsChartWidget
from ui.styles import STYLE

ROW_COLORS = {
    "Error": QColor("#fdecea"),
    "Denied": QColor("#fff8e1"),
    "Failed": QColor("#e3f2fd"),
    "Warning": QColor("#e8f5e9"),
}


class MainWindow(QMainWindow):
    def __init__(self, file_path, patterns):
        super().__init__()
        self.setWindowTitle("Аналізатор лог-файлів — результати")
        self.resize(800, 620)

        self.analyzer = LogAnalyzer()
        self.analyzer.load_file(file_path)
        self.analyzer.analyze(patterns)

        self.build_ui()
        self.fill_table()
        self.update_stats_label()
        self.chart.set_data(self.analyzer.get_statistics())
        self.setStyleSheet(STYLE)

    def build_ui(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        self.stats_label = QLabel()
        self.stats_label.setObjectName("statsLabel")
        layout.addWidget(self.stats_label)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Рядок", "Категорія", "Текст"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        chart_card = QFrame()
        chart_card.setObjectName("chartCard")
        chart_layout = QVBoxLayout(chart_card)
        chart_layout.setContentsMargins(12, 12, 12, 12)
        self.chart = StatsChartWidget()
        chart_layout.addWidget(self.chart)
        layout.addWidget(chart_card)

        button_row = QHBoxLayout()
        save_json_button = QPushButton("Зберегти звіт (JSON)")
        save_json_button.clicked.connect(self.save_report_json)
        save_txt_button = QPushButton("Зберегти звіт (TXT)")
        save_txt_button.setObjectName("secondaryButton")
        save_txt_button.clicked.connect(self.save_report_txt)
        button_row.addWidget(save_json_button)
        button_row.addWidget(save_txt_button)
        layout.addLayout(button_row)

        self.setCentralWidget(central)

    def fill_table(self):
        entries = self.analyzer.get_entries()
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            line_item = QTableWidgetItem()
            line_item.setData(0, entry.line_number)
            level_item = QTableWidgetItem(entry.level)
            text_item = QTableWidgetItem(entry.message)

            color = ROW_COLORS.get(entry.level)
            if color:
                line_item.setBackground(color)
                level_item.setBackground(color)
                text_item.setBackground(color)

            self.table.setItem(row, 0, line_item)
            self.table.setItem(row, 1, level_item)
            self.table.setItem(row, 2, text_item)

        self.table.setSortingEnabled(True)

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
            QMessageBox.information(self, "Готово", f"Звіт збережено: {path}")
        except OSError as error:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти файл: {error}")

    def save_report_txt(self):
        path, _ = QFileDialog.getSaveFileName(self, "Зберегти звіт", "report.txt", "Text (*.txt)")
        if not path:
            return
        try:
            FileStorage.write_txt_report(path, self.analyzer.to_report_dict())
            QMessageBox.information(self, "Готово", f"Звіт збережено: {path}")
        except OSError as error:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти файл: {error}")