STYLE = """
QDialog, QMainWindow {
    background-color: #f4f6f8;
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

QLabel#statsLabel {
    font-size: 14px;
    font-weight: bold;
    color: white;
    background-color: #2c3e50;
    border-radius: 8px;
    padding: 10px 14px;
}

QLabel#dropZone {
    border: 2px dashed #90a4ae;
    border-radius: 8px;
    padding: 20px;
    color: #607d8b;
    font-size: 13px;
    background-color: #ffffff;
}

QGroupBox {
    font-weight: bold;
    border: 1px solid #cfd8dc;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 14px;
    background-color: #ffffff;
}

QPushButton {
    background-color: #2e86de;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 18px;
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

QLineEdit {
    border: 1px solid #cfd8dc;
    border-radius: 5px;
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
    border: 1px solid #cfd8dc;
    border-radius: 8px;
    gridline-color: #eceff1;
    font-size: 13px;
}

QHeaderView::section {
    background-color: #2c3e50;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QFrame#chartCard {
    background-color: white;
    border: 1px solid #cfd8dc;
    border-radius: 8px;
}
"""