import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set window size and position.
        self.setGeometry(100, 100, 400, 300)
        
        # Remove the title bar from the window.
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        # Make the window background transparent.
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create a QVBoxLayout instance for managing widgets vertically.
        layout = QVBoxLayout()

        # Create a label and a button.
        self.label = QLabel('Click the button...', self)
        self.button = QPushButton('Click Me', self)

        # Connect the button's click signal to the changeText method.
        self.button.clicked.connect(self.changeText)

        # Add the label and button to the layout.
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Set the layout for the QWidget.
        self.setLayout(layout)
        
        # This is optional: enable window dragging.
        self.oldPos = self.pos()

    def changeText(self):
        # Change the text of the label.
        self.label.setText('Hello, PyQt5!')

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.oldPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TransparentWindow()
    win.show()
    sys.exit(app.exec_())
