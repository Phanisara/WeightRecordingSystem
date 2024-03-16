from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Rectangle(QWidget):  
    def __init__(self, painter, line_color, background_color, x, y, w, h, x_radius, y_radius):
        super().__init__()  # Call the superclass constructor
        self.line_color = line_color
        self.background_color = background_color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x_radius = x_radius
        self.y_radius = y_radius
        painter.setPen(QPen(self.line_color))
        painter.setBrush(QBrush(self.background_color, Qt.SolidPattern))
        painter.drawRoundedRect(self.x, self.y, self.w, self.h, self.x_radius, self.y_radius)