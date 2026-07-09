import sys
from PyQt5.QtWidgets import QApplication

from ui.start_window import StartWindow


def main():
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()