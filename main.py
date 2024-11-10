from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from UI import Window
import sys
from os import path
    
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(resource_path('Objects/western_formula_sae_logo.jpg')))
app.setApplicationDisplayName('Computational Battery Model')
window = Window()
window.show()
app.exec()