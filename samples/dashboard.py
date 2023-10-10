import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QStackedLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class VideoPlayerWidget(QWidget):
    def __init__(self, rtsp_url):
        super().__init__()
        self.rtsp_url = rtsp_url
        self.initUI()

    def initUI(self):
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        layout = QGridLayout()
        layout.addWidget(self.video_widget, 0, 0, 1, 1)
        self.setLayout(layout)
        self.playVideo()

    def playVideo(self):
        media_content = QMediaContent(QUrl(self.rtsp_url))
        self.media_player.setMedia(media_content)
        self.media_player.play()
        
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        nav_bar_layout = QHBoxLayout()
        self.stacked_layout = QStackedLayout()
        
        #add buttons to nav_bar_layout
        nav_bar_layout.addWidget(QLabel("Logo"))
        nav_bar_layout.addWidget(QLineEdit("Search"))
        
        
        # Connect button clicks to corresponding components
        self.button_functions = {
            "Home": 0,
            "Video Wall": 1,
            "Devices": 2,
            "Members": 3,
            "Reports": 4
        }
        
        for button_text, index in self.button_functions.items():
            button = QPushButton(button_text)
            button.clicked.connect(lambda _, index=index: self.switchLayout(index))
            nav_bar_layout.addWidget(button)

        
        main_layout.addLayout(nav_bar_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Video Player')
        self.setGeometry(100, 100, 800, 600)

    def switchLayout(self, index):
        if index == 0:
            home_layout = self.setupHomeLayout()
            self.stacked_layout.itemAt(0).changeItem(home_layout)
        else:
            # Handle other layouts here if needed
            pass
    
    def setupHomeLayout(self):        
        focus_stream = VideoPlayerWidget("rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4")  # Provide the HLS video stream URL here
        
        multi_stream_layout = QGridLayout()
        for i in range(0, 10):
            multi_stream_layout.addWidget(VideoPlayerWidget("rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4"))  # Provide another HLS video stream URL here

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
        
        return main_section_layout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
