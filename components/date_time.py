
from PyQt5.QtCore import *
# import datetime

# # Get the current date and time
# current_time = datetime.datetime.now()

# # Get the day of the week (0: Monday, 1: Tuesday, ..., 6: Sunday)
# day_of_week = current_time.weekday()
# days = ["วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์", "วันอาทิตย์"]
# day_name = days[day_of_week]

# # Dictionary mapping English month names to Thai month names
# month_names_thai = {
#     "January": "มกราคม",
#     "February": "กุมภาพันธ์",
#     "March": "มีนาคม",
#     "April": "เมษายน",
#     "May": "พฤษภาคม",
#     "June": "มิถุนายน",
#     "July": "กรกฎาคม",
#     "August": "สิงหาคม",
#     "September": "กันยายน",
#     "October": "ตุลาคม",
#     "November": "พฤศจิกายน",
#     "December": "ธันวาคม"
# }

# month_name = current_time.strftime("%B")
# month_name_thai = month_names_thai[month_name]

# # Extract year, month, date, hour, and minute
# year = current_time.year
# month = current_time.month
# date = current_time.day
# hour = current_time.hour
# minute = current_time.minute

# current_day_text = day_name + "ที่ " + str(date) + " " + month_name_thai + " พ.ศ. " + str(year + 543) 
# current_time_text = "เวลา " + str(hour) + ":" + str(minute)

class DateTimeUpdater(QObject):
    date_time_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)  # Update every second

    def updateDateTime(self):
        # Create a QLocale object for Thai locale
        thai_locale = QLocale(QLocale.Thai)
        current_datetime = QDateTime.currentDateTime()

        # Extract individual components
        datetime = current_datetime.date()  # Date
        day = datetime.dayOfWeek()  # Day of the week (1: Monday, 2: Tuesday, ..., 7: Sunday)
        month = datetime.month()  # Month (1: January, 2: February, ..., 12: December)
        year = datetime.year() + 543  # Year
        date = current_datetime.toString("dd")
        hour = '{:02d}'.format(current_datetime.time().hour())
        minute = '{:02d}'.format(current_datetime.time().minute())
        second = '{:02d}'.format(current_datetime.time().second())

        # Format the day, month, and year in Thai
        day_thai = thai_locale.dayName(day, QLocale.LongFormat)  # Long format (วันจันทร์, วันอังคาร, etc.)
        month_thai = thai_locale.monthName(month, QLocale.LongFormat)  # Long format (มกราคม, กุมภาพันธ์, etc.)

        current_datetime_text = f"{day_thai}ที่ {str(date)} เดือน{month_thai} พ.ศ.{year}, เวลา {str(hour)}:{str(minute)}:{str(second)}"

        self.date_time_changed.emit(current_datetime_text)