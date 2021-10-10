import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QPushButton, QVBoxLayout, QFileDialog, QLabel, QTextEdit

class SecondWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.setWindowTitle("MS Tool")
        self.setFixedSize(700, 500)
        layout = QVBoxLayout()

        HelloWorld = QLabel("NEW WINDOW GOES HERE")

        HelloWorld.setAlignment(Qt.AlignCenter)
        HelloWorld.setFont(QFont('Arial', 50))

        layout.addWidget(HelloWorld)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.

        self.setWindowTitle("MS Tool")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()

        Choose_label = QLabel("Choose from the following")
        choose_tp1 = QPushButton("Only Single Timepoint")
        choose_tp2 = QPushButton("Longitudinal Analysis")

        Choose_label.setAlignment(Qt.AlignCenter)
        Choose_label.setFont(QFont('Arial', 20))

        choose_tp1.clicked.connect(self.show_new_window)

        layout.addWidget(Choose_label)
        layout.addWidget(choose_tp1)
        layout.addWidget(choose_tp2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def show_new_window(self, checked):
        if self.w is None:
            self.w = SecondWindow()
            self.w.show()
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

