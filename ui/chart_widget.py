from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt

BAR_COLORS = {
    "Error": QColor("#D9534F"),
    "Denied": QColor("#F0AD4E"),
    "Failed": QColor("#5BC0DE"),
    "Warning": QColor("#5CB85C"),
}
DEFAULT_COLOR = QColor("#777777")


class StatsChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}
        self.setMinimumHeight(220)

    def set_data(self, data):
        self.data = data or {}
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        margin_bottom = 40
        margin_top = 20

        if not self.data:
            painter.setPen(QPen(QColor("#999999")))
            painter.drawText(self.rect(), Qt.AlignCenter, "Немає даних для відображення")
            return

        max_value = max(self.data.values()) or 1
        n = len(self.data)
        bar_area_width = width - 40
        bar_width = bar_area_width / n * 0.6
        gap = bar_area_width / n

        painter.setPen(QPen(QColor("#CCCCCC")))
        painter.drawLine(20, height - margin_bottom, width - 20, height - margin_bottom)

        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)

        for i, (label, value) in enumerate(self.data.items()):
            bar_height = (value / max_value) * (height - margin_top - margin_bottom)
            x = 20 + i * gap + (gap - bar_width) / 2
            y = height - margin_bottom - bar_height

            color = BAR_COLORS.get(label, DEFAULT_COLOR)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRect(int(x), int(y), int(bar_width), int(bar_height))

            painter.setPen(QPen(QColor("#000000")))
            painter.drawText(int(x), int(y) - 5, int(bar_width), 20, Qt.AlignCenter, str(value))
            painter.drawText(
                int(x - gap / 4), height - margin_bottom + 5, int(gap), 20, Qt.AlignCenter, label
            )