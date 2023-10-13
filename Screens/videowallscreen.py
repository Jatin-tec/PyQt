from PyQt5.QtWidgets import QWidget, QGridLayout, QMainWindow
from PyQt5.QtMultimediaWidgets import QVideoWidget
from Components.videoplayer import VideoPlayerWidget

from PyQt5.QtCore import pyqtSignal

class VideoWallScreen(QMainWindow):
    def __init__(self, video_urls):
        super().__init__()
        self.video_urls = video_urls
        print(self.video_urls)
        self.num_columns = int(len(video_urls) ** 0.5)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        grid_layout = QGridLayout(central_widget)
        self.media_players = []

        for row, url_info in enumerate(self.video_urls):
            url = url_info
            video_player = VideoPlayerWidget(url)
            video_player.setObjectName(f"{row}")  # Set object name for identification
            video_player.autoFillBackground()
            grid_layout.addWidget(video_player, row // self.num_columns, row % self.num_columns)

            # Connect signals for maximizing and restoring the video player
            video_player.mouseDoubleClickEvent = lambda event, video_player=video_player: self.toggle_fullscreen(video_player)

            self.media_players.append(video_player)

    def toggle_fullscreen(self, video_player):
        if video_player.isFullScreen():
            video_player.showNormal()
        else:
            video_player.showFullScreen()