from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient
from PyQt5.QtCore import Qt, QRectF

BAR_COLORS = {
    "Error": ("#ef5350", "#c62828"),
    "Denied": ("#ffca28", "#f57f17"),
    "Failed": ("#42a5f5", "#1565c0"),
    "Warning": ("#66bb6a", "#2e7d32"),
}
DEFAULT_COLOR = ("#9e9e9e", "#616161")


class StatsChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}
        self.setMinimumHeight(240)

    def set_data(self, data):
        self.data = data or {}
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        margin_bottom = 44
        margin_top = 30
        margin_side = 24

        if not self.data:
            painter.setPen(QPen(QColor("#9e9e9e")))
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, "Немає даних для відображення")
            return

        max_value = max(self.data.values()) or 1
        n = len(self.data)
        bar_area_width = width - margin_side * 2
        gap = bar_area_width / n
        bar_width = min(gap * 0.55, 90)

        grid_pen = QPen(QColor("#e8ecef"))
        grid_pen.setStyle(Qt.DashLine)
        painter.setPen(grid_pen)
        steps = 4
        for i in range(steps + 1):
            y = margin_top + (height - margin_top - margin_bottom) * i / steps
            painter.drawLine(margin_side, int(y), width - margin_side, int(y))

        painter.setPen(QPen(QColor("#cfd8dc")))
        painter.drawLine(margin_side, height - margin_bottom, width - margin_side, height - margin_bottom)

        label_font = QFont()
        label_font.setPointSize(10)
        label_font.setBold(True)
        value_font = QFont()
        value_font.setPointSize(11)
        value_font.setBold(True)

        for i, (label, value) in enumerate(self.data.items()):
            bar_height = (value / max_value) * (height - margin_top - margin_bottom)
            x = margin_side + i * gap + (gap - bar_width) / 2
            y = height - margin_bottom - bar_height

            light, dark = BAR_COLORS.get(label, DEFAULT_COLOR)
            gradient = QLinearGradient(0, y, 0, height - margin_bottom)
            gradient.setColorAt(0, QColor(light))
            gradient.setColorAt(1, QColor(dark))

            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            rect = QRectF(x, y, bar_width, bar_height)
            painter.drawRoundedRect(rect, 8, 8)

            painter.setFont(value_font)
            painter.setPen(QPen(QColor("#2c3e50")))
            painter.drawText(int(x), int(y) - 22, int(bar_width), 20, Qt.AlignCenter, str(value))

            painter.setFont(label_font)
            painter.setPen(QPen(QColor("#607d8b")))
            painter.drawText(
                int(x - gap * 0.15), height - margin_bottom + 10, int(gap * 1.3), 20,
                Qt.AlignCenter, label
            )