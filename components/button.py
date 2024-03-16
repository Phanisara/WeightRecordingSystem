from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from components.color import *

class Button():
   def __init__(self, window, text, font_name, font_size, pos_x, pos_y, size_x, size_y, style, Goto=None, cursor=None):
      self.style = style
      self.object = QPushButton(window)
      self.object.setText(text)
      self.object.setFont(QFont(font_name, font_size))
      self.object.resize(size_x, size_y)
      self.object.move(pos_x, pos_y)
      self.object.setStyleSheet(style)
      if Goto:
         self.object.clicked.connect(Goto)
      self.object.setCursor(QCursor(cursor))
      self.pressed = False
      self.ready = False

   def Icon(self, pic):
      self.object.setIcon(pic)

   def disable(self, style_disable):
      self.object.setStyleSheet(style_disable)

class ProfileButton(QGraphicsObject):
   clicked_text = pyqtSignal(str, object)
   def __init__(self, window, text, font_name, font_size, pos_x, pos_y, size_x, size_y, style, blur_radius, blur_color, width_text, width_icon, Goto=None, cursor=None):
      super().__init__() 
      self.style = style
      self.text_font_name = font_name
      self.text_font_size = font_size
      self.object = QPushButton(window)
      self.object.resize(size_x, size_y)
      self.object.move(pos_x, pos_y)
      self.object.setStyleSheet(style)
      self.object.setCursor(QCursor(cursor))

      # Create a layout for the button
      layout = QHBoxLayout()
      layout.setAlignment(Qt.AlignCenter)
      layout.setContentsMargins(0, 0, 0, 0)
      self.object.setLayout(layout) 

      # Create a label for the icon
      self.icon_label = QLabel()
      self.icon_label.setFixedWidth(width_icon)
      self.icon_label.setFixedHeight(size_y)
      layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

      # Create a label for the text
      self.text_label = QLabel(text)
      self.text_label.setFixedWidth(width_text)
      self.text_label.setFixedHeight(size_y)
      self.text_label.setFont(QFont(self.text_font_name, self.text_font_size))
      self.text_label.setAlignment(Qt.AlignCenter)
      self.text_label.setStyleSheet(f"color: {Color.darkgreen}; background-color: transparent; font-weight: bold;")
      layout.addWidget(self.text_label, alignment=Qt.AlignCenter)
      layout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

      # creating a QGraphicsDropShadowEffect object 
      shadow = QGraphicsDropShadowEffect() 
      shadow.setBlurRadius(blur_radius) 
      shadow.setColor(blur_color) 
      self.object.setGraphicsEffect(shadow) 

      self.object.enterEvent = self.enterEvent
      self.object.leaveEvent = self.leaveEvent

      # Connect clicked signal to slot
      self.object.clicked.connect(self.on_clicked)

      self.click_flag = False

   def set_icon(self, icon_path, icon_width, icon_height):
      icon = QIcon(icon_path)
      self.icon_label.setAlignment(Qt.AlignCenter)
      self.icon_label.setPixmap(icon.pixmap(QSize(icon_width, icon_height)))
      self.icon_label.setStyleSheet("background-color: transparent;")
   
   def set_style(self, style, old_object=False):
      self.object.setStyleSheet(style)
      if old_object:
         self.click_flag = False
         self.text_label.setStyleSheet(f"color: {Color.darkgreen}; background-color: transparent; font-weight: bold;")
      
   def enterEvent(self, event):
      if not self.click_flag:
            self.text_label.setStyleSheet(f"color: {Color.white}; background-color: transparent; font-weight: bold;")

   def leaveEvent(self, event):
      if not self.click_flag:
            self.text_label.setStyleSheet(f"color: {Color.darkgreen}; background-color: transparent; font-weight: bold;")

   def on_clicked(self):
      text = self.text_label.text()
      self.click_flag = True
      self.clicked_text.emit(text, self) 

   def disable(self, style_disable):
      self.object.setStyleSheet(style_disable)