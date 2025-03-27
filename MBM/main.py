from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from UI import Window
import sys
from os import path

app = QApplication(sys.argv)
app.setWindowIcon(QIcon('Objects/Images/Logo.ico'))
app.setApplicationDisplayName('Computational Battery Model')
window = Window()
window.setWindowIcon(QIcon('Objects/Images/Logo.ico'))
window.show()
app.exec()