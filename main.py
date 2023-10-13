import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit

from Screens.homescreen import HomeScreen
from Screens.videowallscreen import VideoWallScreen
from Screens.devicescreen import DevicesScreen
from Screens.reportscreen import ReportsScreen
from Screens.memberscreen import MembersScreen

from Utils.fetchdevices import read_video_urls_from_file

class MainWindow(QWidget):
    def __init__(self, devices):
        super().__init__()
        self.devices = devices
        self.initUI()

    def initUI(self):
        self.stacked_layout = QStackedLayout()

        self.home_screen = HomeScreen()
        self.video_wall_screen = VideoWallScreen(self.devices)
        self.devices_screen = DevicesScreen()
        self.members_screen = MembersScreen()
        self.reports_screen = ReportsScreen()

        self.stacked_layout.addWidget(self.home_screen)
        self.stacked_layout.addWidget(self.video_wall_screen)
        self.stacked_layout.addWidget(self.devices_screen)
        self.stacked_layout.addWidget(self.members_screen)
        self.stacked_layout.addWidget(self.reports_screen)

        nav_bar_layout = QHBoxLayout()
        nav_bar_layout.addWidget(QLabel("Logo"))
        nav_bar_layout.addWidget(QLineEdit("Search"))

        self.button_functions = {
            "Home": 0,
            "Video Wall": 1,
            "Devices": 2,
            "Members": 3,
            "Reports": 4
        }

        for button_text, index in self.button_functions.items():
            button = QPushButton(button_text)
            button.clicked.connect(lambda _, index=index: self.stacked_layout.setCurrentIndex(index))
            nav_bar_layout.addWidget(button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_bar_layout)
        main_layout.addLayout(self.stacked_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Chokidar Dashboard')
        self.setGeometry(100, 100, 800, 600)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    devices = read_video_urls_from_file('devices.txt')
    window = MainWindow(devices)
    window.show()
    sys.exit(app.exec_())
