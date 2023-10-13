import sys
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, QRadioButton, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QGridLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QThread, QTimer, pyqtSlot
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QMouseEvent
import uuid


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, url):
        super().__init__()
        self._run_flag = True
        self.url = url

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.url)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


# Define the RTSP URLs for your 16 cameras.
camera_urls = [
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
]


class VideoPlayerWidget(QWidget):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread(self.url)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()



    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    


class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        focus_stream = VideoPlayerWidget("rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif")
        
        multi_stream_layout = QGridLayout()
        for i in range(0, 4):
            video_player = VideoPlayerWidget("rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif")
            multi_stream_layout.addWidget(video_player, i//2, i%2)

        main_layout = QVBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Focus Stream"))
        left_layout.addWidget(focus_stream)
        left_layout.addWidget(QLabel("Multi Stream"))
        left_layout.addLayout(multi_stream_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Notifications"))

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)


class VideoGridWidget(QWidget):
    def __init__(self, video_urls):
        super().__init__()
        self.video_urls = video_urls
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout(self)
        for row, url in enumerate(self.video_urls):
                video_player = VideoPlayerWidget(url[0])
                grid_layout.addWidget(video_player, row//4, row%4)

        self.setLayout(grid_layout)

    def maximizeVideo(self, video_player):
        for child in self.findChildren(VideoPlayerWidget):
            if child != video_player:
                child.setVisible(False)
        video_player.setFixedSize(self.size())


class VideoWallScreen(QWidget):
    def __init__(self, video_urls):
        super().__init__()
        self.video_urls = video_urls
        self.video_grid = VideoGridWidget(self.video_urls)
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel("Members"))
        self.main_layout.addWidget(self.video_grid)  # Add the VideoGridWidget to the layout
        self.setLayout(self.main_layout)  # Set the main layout for the main window

    # Override resizeEvent to handle resizing of the window
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGridLayout()

    def updateGridLayout(self):
        layout = self.layout()
        if layout is not None:
            # Calculate new size for each video player based on the new dimensions of the widget
            widget_width = self.width() // 4  # 4 columns
            widget_height = self.height() // (len(self.video_urls) // 4 + 1)  # Calculate rows

            # Iterate through video players and update their size
            for row in range(len(self.video_urls)):
                if row < layout.count():
                    video_player = layout.itemAt(row).widget()
                    video_player.setFixedSize(widget_width, widget_height)





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


# Read video URLs from a .txt file
def read_video_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        video_urls = [line.strip().split(',') for line in lines]
    file.close()    
    return video_urls
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    devices = read_video_urls_from_file('devices.txt')
    window = MainWindow(devices)
    window.show()
    sys.exit(app.exec_())
