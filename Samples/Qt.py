# export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1:$LD_PRELOAD

import sys
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkProxyFactory

class MaximizeVideoWidget(QVideoWidget):
    maximizeRequest = pyqtSignal()
    restoreRequest = pyqtSignal()

    def __init__(self, parent=None):
        super(MaximizeVideoWidget, self).__init__(parent)
        self.setMouseTracking(True)

    def mouseDoubleClickEvent(self, event):
        if self.isFullScreen():
            self.restoreRequest.emit()
        else:
            self.maximizeRequest.emit()

class VideoStreamingApp(QMainWindow):
    def __init__(self, video_urls):
        super(VideoStreamingApp, self).__init__()

        num_videos = len(video_urls)
        num_columns = int(num_videos ** 0.5)
        num_rows = (num_videos + num_columns - 1) // num_columns

        layout = QGridLayout()
        self.media_players = []
        self.video_widgets = []

        for idx, url in enumerate(video_urls):
            media_player = QMediaPlayer(self)
            video_widget = MaximizeVideoWidget(self)  # Use the custom MaximizeVideoWidget
            media_player.setVideoOutput(video_widget)

            layout.addWidget(video_widget, idx // num_columns, idx % num_columns)
            self.media_players.append(media_player)
            self.video_widgets.append(video_widget)

            media_content = QMediaContent(QUrl(url))
            media_player.setMedia(media_content)
            media_player.play()

            # Connect the signals for maximizing and restoring video widgets
            video_widget.maximizeRequest.connect(lambda video_widget=video_widget: self.maximize_video(video_widget))
            video_widget.restoreRequest.connect(lambda video_widget=video_widget: self.restore_video(video_widget))

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

    def maximize_video(self, video_widget):
        for widget in self.video_widgets:
            widget.setVisible(widget is video_widget)
            if widget is video_widget:
                widget.showFullScreen()
            else:
                widget.hide()

    def restore_video(self, video_widget):
        for widget in self.video_widgets:
            widget.setVisible(True)
            widget.showNormal()

def main():
    # Add your HLS or RTSP video URLs to this list
    video_urls = ["https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8", "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8"]
    
    # Set up the network proxy factory to support HTTPS requests
    QNetworkProxyFactory.setUseSystemConfiguration(True)


    app = QApplication(sys.argv)
    window = VideoStreamingApp(video_urls)

    # for media_player in window.media_players:
    #     media_player.stateChanged.connect(window.notify)
    
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
