import sys
from PyQt6.QtWidgets import QApplication
from login import LoginWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginWindow()
    ex.show()
    sys.exit(app.exec())