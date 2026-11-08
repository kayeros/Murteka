import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from login import LoginWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.png'))
    ex = LoginWindow()
    ex.show()
    sys.exit(app.exec())