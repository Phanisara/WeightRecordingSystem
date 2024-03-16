from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Image():
    def __init__(self, window, image_path, pos_x, pos_y, w, h):
        scale = QSize(w, h)
        self.label = QLabel(window)
        self.pixmap = QPixmap(image_path)
        self.pixmap = self.pixmap.scaled(scale)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.label.move(pos_x, pos_y)