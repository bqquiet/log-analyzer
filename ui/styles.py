STYLE = """
QDialog, QMainWindow {
    background-color: #eef1f4;
}

QLabel {
    font-size: 13px;
    color: #2c3e50;
}

QLabel#sectionTitle {
    font-size: 15px;
    font-weight: bold;
    color: #2c3e50;
    padding-top: 4px;
}

QLabel#cardTitle {
    font-size: 12px;
    font-weight: bold;
    color: #90a4ae;
    letter-spacing: 1px;
    padding-bottom: 2px;
}

QLabel#statsLabel {
    font-size: 14px;
    font-weight: bold;
    color: white;
    background-color: #2c3e50;
    border-radius: 10px;
    padding: 14px 18px;
}

QLabel#dropZone {
    border: 2px dashed #90a4ae;
    border-radius: 10px;
    padding: 22px;
    color: #607d8b;
    font-size: 13px;
    background-color: #ffffff;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #dde3e8;
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 14px;
    background-color: #ffffff;
}

QPushButton {
    background-color: #2e86de;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 11px 20px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #256ba8;
}

QPushButton:pressed {
    background-color: #1c5588;
}

QPushButton#secondaryButton {
    background-color: #ffffff;
    color: #2e86de;
    border: 1px solid #2e86de;
}

QPushButton#secondaryButton:hover {
    background-color: #eaf2fb;
}

QPushButton#ghostButton {
    background-color: transparent;
    color: #607d8b;
    border: 1px solid #cfd8dc;
    padding: 8px 16px;
}

QPushButton#ghostButton:hover {
    background-color: #f4f6f8;
    color: #2c3e50;
}

QPushButton#filterButton {
    background-color: #ffffff;
    color: #607d8b;
    border: 1px solid #dde3e8;
    border-radius: 14px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton#filterButton:hover {
    background-color: #f4f6f8;
}

QPushButton#filterButton:checked {
    background-color: #2c3e50;
    color: white;
    border: 1px solid #2c3e50;
}

QLineEdit {
    border: 1px solid #dde3e8;
    border-radius: 6px;
    padding: 8px;
    background-color: white;
    font-size: 13px;
}

QCheckBox {
    padding: 5px;
    font-size: 13px;
}

QTableWidget {
    background-color: white;
    border: none;
    gridline-color: #f1f3f5;
    font-size: 13px;
}

QTableWidget::item {
    padding: 6px;
}

QTableWidget::item:selected {
    background-color: #d6e6f8;
    color: #2c3e50;
}

QHeaderView::section {
    background-color: #2c3e50;
    color: white;
    padding: 10px;
    border: none;
    font-weight: bold;
}

QFrame#card {
    background-color: white;
    border: 1px solid #dde3e8;
    border-radius: 12px;
}

QSplitter::handle {
    background-color: #eef1f4;
    height: 14px;
}

QLabel#toastLabel {
    background-color: #2c3e50;
    color: white;
    border-radius: 18px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
}

QMenu {
    background-color: white;
    border: 1px solid #dde3e8;
    border-radius: 6px;
    padding: 4px;
}

QMenu::item {
    padding: 6px 20px;
    border-radius: 4px;
}

QMenu::item:selected {
    background-color: #eaf2fb;
    color: #2c3e50;
}
"""