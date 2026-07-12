from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRectF


class CopyButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("background: transparent; border: none;")
        self.hovered = False

    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        bg_color = QColor("#eaf2fb") if self.hovered else QColor("#ffffff")
        border_color = QColor("#2e86de") if self.hovered else QColor("#dde3e8")
        icon_color = QColor("#2e86de") if self.hovered else QColor("#78909c")

        painter.setBrush(bg_color)
        painter.setPen(QPen(border_color, 1))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 9, 9)

        pen = QPen(icon_color, 1.5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(QRectF(12, 9, 10, 12), 2, 2)

        painter.setBrush(bg_color)
        painter.drawRoundedRect(QRectF(8, 12, 10, 12), 2, 2)