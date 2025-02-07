from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import sys
import os

app = QApplication(sys.argv)

# Load the image
pixmap = QPixmap("box.png")
splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
# splash.setWindowOpacity(0.95)  # Adjust opacity if needed
# splash.setWindowOpacity(0.5)  # Adjust opacity if needed
splash.setWindowOpacity(1)  # Adjust opacity if needed
splash.show()

# Close after 3 seconds
QTimer.singleShot(3000, splash.close)
QTimer.singleShot(3000, lambda: app.quit())
app.exec_()