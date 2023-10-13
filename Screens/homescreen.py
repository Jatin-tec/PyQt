from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from Components.videoplayer import VideoPlayerWidget

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
