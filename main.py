import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QComboBox, QHBoxLayout
from components.color import *
from components.text import *
from components.shape import *
from components.image import *
from components.button import *
from components.date_time import *

font_size_header = 25
font_size_title  = 23
font_size_button = 20
font_size_detail = 18
font_size_weight = 120
faculty_name = "สถาบันวิทยาการหุ่นยนต์ภาคสนาม"
all_profile_waste = ["can", "glass", "paper", ""]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setStyleSheet(f"background-color: {Color.white};")
        self.create_component()
        self.screen = QGuiApplication.primaryScreen()
        self.screen_geometry = self.screen.geometry()
    
    def create_component(self):
        # ---------------------------------------------------------- Font ---------------------------------------------------------- 
        QFontDatabase.addApplicationFont("./fonts/Seven Segment.ttf")

        # --------------------------------------------------------- Header --------------------------------------------------------- 
        self.icon = Image(self, "./pics/weight_icon_white.png", 37, 30, 40, 40)
        self.text_header_title = Text(self, f"ระบบชั่งและบันทึกน้ำหนักขยะ: {faculty_name}", "TH Sarabun New" , font_size_header,  90, 5, 900, 100, f"color: {Color.white}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignVCenter)
        
        # -------------------------------------------------------- Date time -------------------------------------------------------- 
        self.updater = DateTimeUpdater()
        self.current_time = "กำลังแสดงวันและเวลาในปัจจุบัน"
        self.text_current_time = Text(self, self.current_time, "TH Sarabun New" , font_size_detail,  40, 120, 500, 60, f"color: {Color.darkgreen}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignVCenter)
        self.updater.date_time_changed.connect(self.onDateTimeChanged)

        # ------------------------------------------------------- Wight scale ------------------------------------------------------
        weight_value = "00.000"
        self.text_weight_title = Text(self, "น้ำหนักของขยะ (กิโลกรัม)", "TH Sarabun New" , font_size_title, 100, 325, 700, 60, f"color: {Color.darkgreen}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignCenter)
        self.text_weight_value = Text(self, weight_value, "Seven Segment" , font_size_weight,  100, 390, 700, 300, f"color: {Color.darkgreen}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignCenter)


        # ---------------------------------------------------- Profile of waste ----------------------------------------------------
        self.text_select_profile = Text(self, "เลือกประเภทของขยะ", "TH Sarabun New" , font_size_title,  900, 100, 920, 115, f"color: {Color.darkgreen}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignCenter)


        # --------------------------------------------------------- Button ---------------------------------------------------------
        # Set style of the button
        self.style_history = "  QPushButton{ \
                                    color: " + Color.birch + "; \
                                    background-color:" + Color.lightbrown + "; \
                                    border-radius: 10; \
                                    font-weight: Bold; \
                                    text-align: center; \
                                }\
                                QPushButton:hover { \
                                    color:" + Color.white + "; \
                                    background-color: " + Color.browngreen + "; \
                            }"
        
        self.style_save = " QPushButton{ \
                                color: " + Color.darkgreen + " ; \
                                background-color:" + Color.lightgreen + "; \
                                border-radius: 10; \
                                font-weight: Bold; \
                                text-align: center; \
                                } \
                            QPushButton:hover { \
                                color:" + Color.white + "; \
                                background-color: " + Color.green + "; \
                            }"

        self.style_profile_waste = "QPushButton { \
                                        background-color: " + Color.white + "; \
                                        border: 2px solid " + Color.darkgreen + "; \
                                        border-radius: 10px; \
                                        font-weight: bold; \
                                        text-align: center; \
                                    } \
                                    QPushButton:hover { \
                                        color: " + Color.white + "; \
                                        background-color: " + Color.middlegreen + "; \
                                        border: 3px solid " + Color.white + "; \
                                        font-weight: bold; \
                                    }"

        # Create the profile of waste
        self.profile_can_button = ProfileButton(self, "กระป๋อง", "TH Sarabun New" , font_size_detail, 910, 200, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_can_button.set_icon('./pics/profile_waste/can.png', 70, 70)
        self.profile_can_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_glass_button = ProfileButton(self, "แก้ว", "TH Sarabun New" , font_size_detail, 1230, 200, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_glass_button.set_icon('./pics/profile_waste/glass.png', 70, 70)
        self.profile_glass_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_paper_button = ProfileButton(self, "กระดาษ", "TH Sarabun New" , font_size_detail, 1540, 200, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_paper_button.set_icon('./pics/profile_waste/paper.png', 70, 70)
        self.profile_paper_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_milk_box_button = ProfileButton(self, "กล่องนม", "TH Sarabun New" , font_size_detail, 910, 330, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_milk_box_button.set_icon('./pics/profile_waste/milk_box.png', 70, 70)
        self.profile_milk_box_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_bottle_button = ProfileButton(self, "ขวดพลาสติก", "TH Sarabun New" , font_size_detail, 1230, 330, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_bottle_button.set_icon('./pics/profile_waste/bottle.png', 90, 90)
        self.profile_bottle_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_straw_button = ProfileButton(self, "หลอดพลาสติก", "TH Sarabun New" , font_size_detail, 1540, 330, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_straw_button.set_icon('./pics/profile_waste/straw.png', 70, 70)
        self.profile_straw_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_plastic_cup_sell_button = ProfileButton(self, "แก้วน้ำพลาสติก\n(ขายได้)", "TH Sarabun New", font_size_detail, 910, 460, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_plastic_cup_sell_button.set_icon('./pics/profile_waste/plastic_cup_sell.png', 70, 70)
        self.profile_plastic_cup_sell_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_plastic_cup_nosell_button = ProfileButton(self, "แก้วน้ำพลาสติก\n(ขายไม่ได้)", "TH Sarabun New", font_size_detail, 1230, 460, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_plastic_cup_nosell_button.set_icon('./pics/profile_waste/plastic_cup_nosell.png', 70, 70)
        self.profile_plastic_cup_nosell_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_plastic_cutlery_button = ProfileButton(self, "ช้อน - ส้อม\nพลาสติก", "TH Sarabun New", font_size_detail, 1540, 460, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_plastic_cutlery_button.set_icon('./pics/profile_waste/cutlery.png', 60, 60)
        self.profile_plastic_cutlery_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_plastic_bag_button = ProfileButton(self, "ถุงพลาสติก", "TH Sarabun New", font_size_detail, 910, 590, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_plastic_bag_button.set_icon('./pics/profile_waste/plastic_bag.png', 60, 60)
        self.profile_plastic_bag_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_foil_bag_button = ProfileButton(self, "ถุงวิบวับ", "TH Sarabun New", font_size_detail, 1230, 590, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_foil_bag_button.set_icon('./pics/profile_waste/foil_bag.png', 70, 70)
        self.profile_foil_bag_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_plastic_box_button = ProfileButton(self, "กล่องอาหาร\nพลาสติก", "TH Sarabun New", font_size_detail, 1540, 590, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_plastic_box_button.set_icon('./pics/profile_waste/plasticbox.png', 70, 70)
        self.profile_plastic_box_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_food_waste_button = ProfileButton(self, "เศษอาหาร", "TH Sarabun New", font_size_detail, 910, 720, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_food_waste_button.set_icon('./pics/profile_waste/food_waste.png', 80, 80)
        self.profile_food_waste_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_hazardous_waste_button = ProfileButton(self, "ขยะอันตราย", "TH Sarabun New", font_size_detail, 1230, 720, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_hazardous_waste_button.set_icon('./pics/profile_waste/hazardous_waste.png', 70, 70)
        self.profile_hazardous_waste_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_toilet_waste_button = ProfileButton(self, "ขยะห้องน้ำ", "TH Sarabun New", font_size_detail, 1540, 720, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_toilet_waste_button.set_icon('./pics/profile_waste/toilet_waste.png', 80, 80)
        self.profile_toilet_waste_button.clicked_text.connect(self.handle_button_clicked)
        
        self.profile_orphan_waste_button = ProfileButton(self, "ขยะกำพร้า", "TH Sarabun New", font_size_detail, 1065, 850, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_orphan_waste_button.set_icon('./pics/profile_waste/orphan_waste.png', 80, 80)
        self.profile_orphan_waste_button.clicked_text.connect(self.handle_button_clicked)

        self.profile_normal_waste_button = ProfileButton(self, "ขยะทั่วไป", "TH Sarabun New", font_size_detail, 1375, 850, 280, 100, self.style_profile_waste, 20, PainterColor.middlegreen, 170, 100, cursor=QtCore.Qt.PointingHandCursor)
        self.profile_normal_waste_button.set_icon('./pics/profile_waste/normal_waste.png', 70, 70)
        self.profile_normal_waste_button.clicked_text.connect(self.handle_button_clicked)

        # Create the button
        self.history_button = Button(self, "ประวัติการบันทึก", "TH Sarabun New" , font_size_button, 100, 720, 200, 60, self.style_history, Goto=self.gotoHistoryWindow, cursor=QtCore.Qt.PointingHandCursor)
        self.save_button = Button(self, "บันทึก", "TH Sarabun New" , font_size_button, 700, 720, 100, 60, self.style_save, cursor=QtCore.Qt.PointingHandCursor)

        self.old_object = None

    def paintEvent(self, event):
        painter = QPainter(self)
        self.header_background = Rectangle(painter, PainterColor.darkgreen, PainterColor.darkgreen, 0, 0, self.screen_geometry.width(), 100, 0, 0)
        self.weightscale_background = Rectangle(painter, PainterColor.lightgreen, PainterColor.lightgreen, 100, 390, 700, 300, 10, 10)

    def handle_button_clicked(self, text, object):
        print("Clicked button text:", text)
        self.currently_object = object
        self.currently_text = text

        if self.old_object != self.currently_object and self.old_object:
            self.old_object.set_style(self.style_profile_waste, old_object=True)
        
        self.currently_object.set_style("QPushButton { \
                                            background-color: " + Color.middlegreen + "; \
                                            border: 2px solid " + Color.white + "; \
                                            border-radius: 10px; \
                                        }")
        self.old_object = self.currently_object
    
    def onDateTimeChanged(self, formatted_date_time):
        self.text_current_time.set_text(formatted_date_time)

    def gotoHistoryWindow(self):
        historyWindow = HistoryWindow()
        widget.addWidget(historyWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)        


class HistoryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {Color.white};")
        self.create_component()
        self.screen = QGuiApplication.primaryScreen()
        self.screen_geometry = self.screen.geometry()
    
    def create_component(self):
        # --------------------------------------------------------- Header --------------------------------------------------------- 
        self.icon = Image(self, "./pics/weight_icon_white.png", 37, 30, 40, 40)
        self.text_header_title = Text(self, f"ระบบชั่งและบันทึกน้ำหนักขยะ: {faculty_name}", "TH Sarabun New" , font_size_header,  90, 5, 900, 100, f"color: {Color.white}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignVCenter)

        # --------------------------------------------------------- Button ---------------------------------------------------------
        # Set style of the button
        self.style_back = " QPushButton{ color: " + Color.birch + " ; background-color:" + Color.lightbrown + """; 
                                    border-radius: 10; 
                                    font-weight: Bold; 
                                    text-align: center;}
                            QPushButton:hover { 
                                    color: """ + Color.white + "; background-color: " + Color.browngreen + ";}"
        
        # Create the button
        self.back_button = Button(self, "ย้อนกลับ", "TH Sarabun New" , font_size_detail, 50, 95, 100, 40, self.style_back, Goto=self.gotoMainWindow, cursor=QtCore.Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.header_background = Rectangle(painter, PainterColor.darkgreen, PainterColor.darkgreen, 0, 0, self.screen_geometry.width(), 100, 0, 0)
    
    def gotoMainWindow(self):
        mainWindow    = MainWindow()
        widget.addWidget(mainWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def setFixedSizeFromScreen(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setFixedSize(screen_geometry.width(), screen_geometry.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    mainWindow    = MainWindow()
    widget.addWidget(mainWindow)

    # Find the width and height of full screen
    screen = QGuiApplication.primaryScreen()
    # screen_geometry = screen.geometry()
    # widget.setFixedSize(screen_geometry.width(), screen_geometry.height())
    widget.showMaximized() 

    # Setting the title and icon of window
    widget.setWindowTitle("ระบบชั่งและบันทึกน้ำหนักขยะ")
    widget.setWindowIcon(QtGui.QIcon("pics/weight_icon.png"))
    # widget.statusTip().setFixedHeight(70)
    sys.exit(app.exec_()) 
    