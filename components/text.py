from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Text():
    def __init__(self, window, text, font_name, font_size, pos_x, pos_y, size_x, size_y, style, alignment=None):
        self.window = window
        self.font_name = font_name
        self.font_size = font_size
        self.object = QLabel(window)
        self.object.setText(text)
        self.object.setFont(QFont(font_name, font_size))
        self.object.resize(size_x, size_y)
        self.object.move(pos_x, pos_y)
        self.object.setStyleSheet(style)
        self.object.setAlignment(alignment)
    
    def set_text(self, text):
        self.object.setText(text)
        self.object.setFont(QFont(self.font_name, self.font_size))

    def show(self):
        self.object.setVisible(True)
    
    def hide(self):
        self.object.setVisible(False)
    