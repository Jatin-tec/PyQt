import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl

class VideoPlayer(QWidget):
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

if __name__ == '__main__':
    rtsp_links = [
        "rtsp://example.com/video1",
        "rtsp://example.com/video2",
        # Add more RTSP links as needed
    ]

    app = QApplication(sys.argv)
    main_window = QWidget()
    main_layout = QGridLayout()

    row = 0
    col = 0

    for rtsp_link in rtsp_links:
        video_player = VideoPlayer(rtsp_link)
        main_layout.addWidget(video_player, row, col)
        col += 1
        if col > 3:  # Change the number of columns as per your preference
            col = 0
            row += 1

    main_window.setLayout(main_layout)
    main_window.setWindowTitle('Multi-Video Player')
    main_window.show()

    sys.exit(app.exec_())
