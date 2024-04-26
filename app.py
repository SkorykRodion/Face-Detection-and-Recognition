import sys
from ui import MainWindow
from PyQt6.QtWidgets import QApplication
if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    window = MainWindow()
    window.show()

    app.exec()
