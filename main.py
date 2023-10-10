import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QGridLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QMouseEvent
import uuid


class VideoPlayerWidget(QWidget):
    def __init__(self, rtsp_url):
        super().__init__()
        self.rtsp_url = rtsp_url
        self.initUI()

    def initUI(self):
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        self.setLayout(layout)
        self.playVideo()

    def playVideo(self):
        media_content = QMediaContent(QUrl(self.rtsp_url))
        self.media_player.setMedia(media_content)
        self.media_player.play()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.parent().maximizeVideo(self)

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        focus_stream = VideoPlayerWidget("rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif")
        multi_stream_layout = QGridLayout()
        for i in range(0, 10):
            multi_stream_layout.addWidget(VideoPlayerWidget("rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"))

        main_section_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Focus Stream"))
        left_layout.addWidget(focus_stream)
        left_layout.addWidget(QLabel("Multi Stream"))
        left_layout.addLayout(multi_stream_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Notifications"))

        main_section_layout.addLayout(left_layout)
        main_section_layout.addLayout(right_layout)

        self.setLayout(main_section_layout)


class VideoGridWidget(QWidget):
    def __init__(self, video_urls):
        super().__init__()
        self.video_urls = video_urls
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout(self)
        for row, urls in enumerate(self.video_urls):
            for col, url in enumerate(urls):
                video_player = VideoPlayerWidget(url)
                grid_layout.addWidget(video_player, row, col)
        self.setLayout(grid_layout)

    def maximizeVideo(self, video_player):
        for child in self.findChildren(VideoPlayerWidget):
            if child != video_player:
                child.setVisible(False)
        video_player.setFixedSize(self.size())

class VideoWallScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.video_urls = [
        ['rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif', 'rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif'],
        ['rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif', 'rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif']
    ]
        self.video_grid = VideoGridWidget(self.video_urls)
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel("Members"))
        self.main_layout.addWidget(self.video_grid)  # Add the VideoGridWidget to the layout
        self.setLayout(self.main_layout)  # Set the main layout for the main window

class DevicesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel("Devices"))
        
        self.setLayout(self.main_layout)


class MembersScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel("Members"))

        self.setLayout(self.main_layout)


# The code defines a GUI application with a navigation bar and multiple screens, including a Reports
# screen with a table and download functionality.
class ReportsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(["", "Activity ID", "Type", "Activity", "Date", "Time", "Latitude", "Longitude", "Tags", "Device ID", "Media Gallery", ""])
        
         # Set columns to stretch and fill available space
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Resize first column to fit content
        header.setSectionResizeMode(11, QHeaderView.ResizeToContents)  # Resize last column to fit content
        for i in range(1, 11):
            header.setSectionResizeMode(i, QHeaderView.Stretch)  # Stretch other columns
        
        # Set table size policy to make it expand in both directions
        tableSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setSizePolicy(tableSizePolicy)

        layout.addWidget(self.table)

        # Adding sample data to the table (you can replace this with your actual data)
        for row in range(10):
            self.table.insertRow(row)
            radio_button = QRadioButton()
            self.table.setCellWidget(row, 0, radio_button)
            self.table.setItem(row, 1, QTableWidgetItem(str(uuid.uuid4())))
            self.table.setItem(row, 2, QTableWidgetItem("Type"))
            self.table.setItem(row, 3, QTableWidgetItem("Activity"))
            self.table.setItem(row, 4, QTableWidgetItem("DD/MM/YYYY"))
            self.table.setItem(row, 5, QTableWidgetItem("HH:MM"))
            self.table.setItem(row, 6, QTableWidgetItem("Latitude"))
            self.table.setItem(row, 7, QTableWidgetItem("Longitude"))
            self.table.setItem(row, 8, QTableWidgetItem("Tags"))
            self.table.setItem(row, 9, QTableWidgetItem("Device ID"))
            self.table.setItem(row, 10, QTableWidgetItem("Image Path"))

            download_button = QPushButton("Download")
            download_button.clicked.connect(lambda _, r=row: self.download_row(r))
            self.table.setCellWidget(row, 11, download_button)
                    
        self.setLayout(layout)

    def download_row(self, row):
        # Implement your download logic here, using row variable to identify the clicked row
        print(f"Downloading data from row {row}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.stacked_layout = QStackedLayout()

        self.home_screen = HomeScreen()
        self.video_wall_screen = VideoWallScreen()
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
