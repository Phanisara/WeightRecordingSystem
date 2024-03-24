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
from components.table import *
from components.popup import *

font_size_header = 25
font_size_title  = 23
font_size_button = 20
font_size_detail = 18
font_size_weight = 120
input_machine = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setStyleSheet(f"background-color: {Color.white};")
        self.screen = QGuiApplication.primaryScreen()
        self.screen_geometry = self.screen.geometry()
        self.create_component()
    
    def create_component(self):
        """
        FUnction to create and initialize all the UI components required for the application.

        This method initializes various UI components such as fonts, icons, buttons, labels, etc.
        It sets up the appearance and functionality of each component according to the application's requirements.

        Returns:
            None
        """
        # ---------------------------------------------------------- Font ---------------------------------------------------------- 
        QFontDatabase.addApplicationFont("./fonts/Seven Segment.ttf")

        # --------------------------------------------------------- Header --------------------------------------------------------- 
        self.faculty_name = ""
        self.icon = Image(self, "./pics/weight_icon_white.png", 37, 30, 40, 40)
        self.text_header_title = Text(self, f"ระบบชั่งและบันทึกน้ำหนักขยะ: {self.faculty_name}", "TH Sarabun New" , font_size_header,  90, 5, 900, 100, f"color: {Color.white}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignVCenter)
        self.setting_icon = ImageButton(self,"./pics/settings.png", self.screen_geometry.width() - 60, 35, 35, 35)
        self.setting_icon.clicked.connect(self.pop_up_setting)
        self.text_error_machine = Text(self, "กรุณาระบะชื่อเครื่องที่ปุ่มการตั้งค่า (มุมขวาบน) ก่อนเริ่มใช้งานระบบ", "TH Sarabun New" , font_size_detail,  40, 160, 500, 60, f"color: red; background-color: {None}; font-weight: bold;", alignment=Qt.AlignVCenter)

        # -------------------------------------------------------- Date time -------------------------------------------------------- 
        self.updater = DateTimeUpdater()
        self.current_time = "กำลังแสดงวันและเวลาในปัจจุบัน"
        self.text_current_time = Text(self, self.current_time, "TH Sarabun New" , font_size_detail,  40, 120, 500, 60, f"color: {Color.darkgreen}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignVCenter)
        self.updater.date_time_changed.connect(self.on_date_time_changed)

        # ------------------------------------------------------- Wight scale ------------------------------------------------------
        weight_value = "00.000"
        self.text_weight_title = Text(self, "น้ำหนักของขยะ (กิโลกรัม)", "TH Sarabun New" , font_size_title, 100, 325, 700, 60, f"color: {Color.darkgreen}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignCenter)
        self.text_weight_value = Text(self, weight_value, "Seven Segment" , font_size_weight,  100, 390, 700, 300, f"color: {Color.darkgreen}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignCenter)

        # ---------------------------------------------------- Profile of waste ----------------------------------------------------
        self.text_select_profile = Text(self, "เลือกประเภทของขยะ", "TH Sarabun New" , font_size_title,  900, 120, 920, 60, f"color: {Color.darkgreen}; background-color: {None}; font-weight: bold;", alignment=Qt.AlignCenter)

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
        
        self.style_profile_waste_disable = "QPushButton { \
                                                background-color: " + Color.gray + "; \
                                                border: 2px solid " + Color.gray + "; \
                                                border-radius: 10px; \
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

        for button in [self.profile_can_button, self.profile_glass_button, self.profile_paper_button, self.profile_milk_box_button,
                    self.profile_bottle_button, self.profile_straw_button, self.profile_plastic_cup_sell_button,
                    self.profile_plastic_cup_nosell_button, self.profile_plastic_cutlery_button, self.profile_plastic_bag_button,
                    self.profile_foil_bag_button, self.profile_plastic_box_button, self.profile_food_waste_button,
                    self.profile_hazardous_waste_button, self.profile_toilet_waste_button, self.profile_orphan_waste_button,
                    self.profile_normal_waste_button]:
            button.disable()
        
        # Create the button
        # self.history_button = Button(self, "ประวัติการบันทึก", "TH Sarabun New" , font_size_button, 100, 720, 200, 60, self.style_history, Goto=self.gotoHistoryWindow, cursor=QtCore.Qt.PointingHandCursor)
        self.save_button = Button(self, "บันทึก", "TH Sarabun New" , font_size_button, 680, 720, 120, 60, self.style_save, Goto=self.click_save_profile, cursor=QtCore.Qt.PointingHandCursor)
        self.save_button.disable()
        self.text_warning_save_profile = Text(self, "\"กรุณาเลือกประเภทของขยะก่อนกดบันทึก\"", "TH Sarabun New" , font_size_detail, 490, 800, 350, 40, f"color: red; background-color: {None}; font-weight: bold;", alignment=Qt.AlignVCenter)
        self.text_warning_save_profile.hide()

        self.style_button_pop_up = " QPushButton{ \
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

        # --------------------------------------------------- Setting variable -----------------------------------------------------
        self.old_object = None
        self.select_profile_waste = None
        self.input_machine_placeholder = "ชื่อของเครื่อง_หมายเลขเครื่อง"

        self.all_name_profile_waste = {
                                        "กระป๋อง": "can",
                                        "แก้ว"   : "glass",
                                        "กระดาษ": "paper",
                                        "กล่องนม": "milk_box",
                                        "ขวดพลาสติก": "plastic_bottle",
                                        "หลอดพลาสติก": "plastic_straw",
                                        "แก้วน้ำพลาสติก\n(ขายได้)": "plastic_cup_sell",
                                        "แก้วน้ำพลาสติก\n(ขายไม่ได้)" : "plastic_cup_nosell",
                                        "ช้อน - ส้อม\nพลาสติก": "plastic_cutlery",
                                        "ถุงพลาสติก": "plastic_bag",
                                        "ถุงวิบวับ": "foil_bag",
                                        "กล่องอาหาร\nพลาสติก": "plastic_box",
                                        "เศษอาหาร": "food_waste",
                                        "ขยะอันตราย": "hazardous_waste",
                                        "ขยะห้องน้ำ": "toilet_waste",
                                        "ขยะกำพร้า": "orphan_waste",
                                        "ขยะทั่วไป": "normal_waste",
                                    }
        
        self.all_profile_waste_english_to_thai = {
                                                    "can": "กระป๋อง",
                                                    "glass": "แก้ว",
                                                    "paper": "กระดาษ",
                                                    "milk_box": "กล่องนม",
                                                    "plastic_bottle": "ขวดพลาสติก",
                                                    "plastic_straw": "หลอดพลาสติก",
                                                    "plastic_cup_sell": "แก้วน้ำพลาสติก\n(ขายได้)",
                                                    "plastic_cup_nosell": "แก้วน้ำพลาสติก\n(ขายไม่ได้)",
                                                    "plastic_cutlery": "ช้อน - ส้อม\nพลาสติก",
                                                    "plastic_bag": "ถุงพลาสติก",
                                                    "foil_bag": "ถุงวิบวับ",
                                                    "plastic_box": "กล่องอาหาร\nพลาสติก",
                                                    "food_waste": "เศษอาหาร",
                                                    "hazardous_waste": "ขยะอันตราย",
                                                    "toilet_waste": "ขยะห้องน้ำ",
                                                    "orphan_waste": "ขยะกำพร้า",
                                                    "normal_waste": "ขยะทั่วไป",
                                                }

    def paintEvent(self, event):
        painter = QPainter(self)
        self.header_background = Rectangle(painter, PainterColor.darkgreen, PainterColor.darkgreen, 0, 0, self.screen_geometry.width(), 100, 0, 0)
        self.weightscale_background = Rectangle(painter, PainterColor.lightgreen, PainterColor.lightgreen, 100, 390, 700, 300, 10, 10)

    def handle_button_clicked(self, text, object):
        """
        Function to handle the click event of a profile of waste button.

        Args:
            text (str): The text displayed on the clicked button.
            object (ProfileButton): The object representing the clicked button.

        Returns:
            None
        """

        # Hide warning that related to saving profiles when not click the button
        self.text_warning_save_profile.hide()

        # Update currently selected object and text
        self.currently_object = object
        self.currently_text = text

        # Reset style of previously clicked button
        if self.old_object != self.currently_object and self.old_object:
            self.old_object.set_style(self.style_profile_waste, old_object=True)
        
        # Update style of currently clicked button
        self.currently_object.set_style("QPushButton { \
                                            background-color: " + Color.middlegreen + "; \
                                            border: 2px solid " + Color.white + "; \
                                            border-radius: 10px; \
                                        }")
        
        # Update old_object reference to currently clicked button
        self.old_object = self.currently_object
        # Retrieve and store the profile waste corresponding to the clicked button's text
        self.select_profile_waste = self.all_name_profile_waste[text]
    
    def on_date_time_changed(self, formatted_date_time):
        """
        Function to update the current time text based on the formatted date and time string.

        Args:
            formatted_date_time (str): The formatted date and time string to be displayed.

        Returns:
            None
        """
        # Update the text displaying the current date and time
        self.text_current_time.set_text(formatted_date_time)

    def update_profile_waste(self, input_machine):
        """
        Function to update the profile waste buttons based on the input machine name.

        Args:
            input_machine (str): The name of the input machine.

        Returns:
            None
        """
        self.input_machine = input_machine
        print(self.input_machine)
        profile_waste = ["can", "glass", "paper", "milk_box", "plastic_bottle", "plastic_straw", "plastic_cup_sell", "plastic_cup_nosell", "plastic_cutlery"]

        # Convert English profile waste names to Thai
        new_profile_waste = [self.all_profile_waste_english_to_thai[name] for name in profile_waste]

        # Iterate through buttons and disable those whose text is in the list
        for button in [self.profile_can_button, self.profile_glass_button, self.profile_paper_button, self.profile_milk_box_button,
                    self.profile_bottle_button, self.profile_straw_button, self.profile_plastic_cup_sell_button,
                    self.profile_plastic_cup_nosell_button, self.profile_plastic_cutlery_button, self.profile_plastic_bag_button,
                    self.profile_foil_bag_button, self.profile_plastic_box_button, self.profile_food_waste_button,
                    self.profile_hazardous_waste_button, self.profile_toilet_waste_button, self.profile_orphan_waste_button,
                    self.profile_normal_waste_button]:
            if button.text() not in new_profile_waste:
                button.disable(self.style_profile_waste_disable)
            else:
                button.enable()
            self.save_button.enable()
       
    def click_save_profile(self):
        """
        Function to handle the save profile button click event.
        This method displays a popup dialog confirming the completion of the profile saving process.

        Returns:
            None
        """
        # Define the dimensions and position of the popup dialog
        self.width_pop_up = 800
        self.height_pop_up = 300
        self.pos_x_pop_up = int((self.screen_geometry.width()/2) - (self.width_pop_up/2))
        self.pos_y_pop_up = int((self.screen_geometry.height()/2) - (self.height_pop_up/2)+30)

        # Check if a profile waste is selected and a faculty name is provided
        if self.select_profile_waste and self.faculty_name != None:
            # Create and display the popup dialog
            self.popup = PopupDialog(PainterColor.lightgray, PainterColor.darkgreen, PainterColor.white, self.pos_x_pop_up, self.pos_y_pop_up, self.width_pop_up, self.height_pop_up, 10, 10, "การบันทึกเสร็จสมบูรณ์\nคุณสามารถนำขยะที่อยู่บนเครื่องชั่งลงได้", 800, 155, "TH Sarabun New" , font_size_title, 120, 60, self.style_button_pop_up)
            self.popup.move(0, 0)
            self.popup.resize(self.screen_geometry.width(), self.screen_geometry.height())
            self.popup.exec_()
            print("CLick save")
            print("Profile waste button: ", self.select_profile_waste)
        else:
            # Show a warning message if profile waste is not selected but click save button
            self.text_warning_save_profile.show()
            
    def pop_up_setting(self):
        """
        Function to isplays a popup dialog for setting up the machine name.
        This method initializes the style for input text, defines the dimensions and position of the popup dialog, and creates and displays the popup dialog for setting up the machine name.

        Returns:
            None
        """
        self.style_input_text = " QLineEdit { \
                                    background-color: " + Color.white + "; \
                                    border: 2px solid " + Color.middlegreen + "; \
                                    border-radius: 10px; \
                                  } \
                                  QPushButton:focus { \
                                    background-color: " + Color.white + "; \
                                    border: 2px solid " + Color.darkgreen + "; \
                                    border-radius: 10px; \
                                  }"
    
        # Define the dimensions and position of the popup dialog
        self.width_pop_up = 800
        self.height_pop_up = 300
        self.pos_x_pop_up = int((self.screen_geometry.width()/2) - (self.width_pop_up/2))
        self.pos_y_pop_up = int((self.screen_geometry.height()/2) - (self.height_pop_up/2)+30)
        
        # Create and display the popup dialog for setting up the machine name
        self.popup_setting = PopupDialogSetting(PainterColor.lightgray, PainterColor.darkgreen, PainterColor.white, self.pos_x_pop_up, self.pos_y_pop_up, self.width_pop_up, self.height_pop_up, 10, 10, "กรุณากรอกชื่อของเครื่องเพื่อเริ่มต้นการบันทึกค่า", 800, 70, "TH Sarabun New" , font_size_title, 100, 60, self.style_button_pop_up, self.style_input_text, self.input_machine_placeholder, self.click_save_setting)
        self.popup_setting.move(0, 0)
        self.popup_setting.resize(self.screen_geometry.width(), self.screen_geometry.height())
        self.popup_setting.exec_()

    def click_save_setting(self):
        """
        Function to save the input machine name from the popup dialog and updates settings accordingly.
        This method retrieves the input machine name from the popup dialog, checks if it is valid, updates the settings if valid, and shows an error message if not valid.

        Returns:
            None
        """

        # Retrieve the input machine name from the popup dialog
        input_machine = self.popup_setting.get_input()

        # List of valid machine names
        self.list_machine_name = ['FIBO_01']

        # Check if the input machine name is valid
        if input_machine in self.list_machine_name:
            self.popup_setting.close()
            self.faculty_name = 'สถาบันวิทยาการหุ่นยนต์ภาคสนาม'
            self.text_header_title.set_text(f"ระบบชั่งและบันทึกน้ำหนักขยะ: {self.faculty_name}")
            # Update profile waste and hide error message
            self.update_profile_waste(input_machine)
            self.text_error_machine.hide()
        else:
            # Show error message if the input machine name is not valid
            self.popup_setting.show_error_message()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    mainWindow    = MainWindow()
    widget.addWidget(mainWindow)

    # Find the width and height of full screen
    screen = QGuiApplication.primaryScreen()
    widget.showMaximized() 

    # Setting the title and icon of window
    widget.setWindowTitle("ระบบชั่งและบันทึกน้ำหนักขยะ")
    widget.setWindowIcon(QtGui.QIcon("pics/weight_icon.png"))
    sys.exit(app.exec_()) 
    