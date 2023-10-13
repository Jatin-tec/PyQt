import cv2
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QScrollArea, QSizePolicy, QWidget
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import Qt, QObject, QEvent, pyqtSignal, QThread
from PyQt5 import QtCore

# Define the RTSP URLs for your 16 cameras.
camera_urls = [
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    "rtsp://happymonk:admin123@streams.ckdr.co.in:3554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif",
    # Add URLs for the remaining cameras...
]

class CaptureIpCameraFramesWorker(QThread):
    ImageUpdated = pyqtSignal(QImage)

    def __init__(self, url):
        super(CaptureIpCameraFramesWorker, self).__init__()
        self.url = url
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False

    def run(self):
        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        self.fps = cap.get(cv2.CAP_PROP_FPS)

        if cap.isOpened():
            while self.__thread_active:
                if not self.__thread_pause:
                    ret, frame = cap.read()
                    if ret:
                        height, width, channels = frame.shape
                        bytes_per_line = width * channels
                        cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        qt_rgb_image_scaled = qt_rgb_image.scaled(1280, 720, Qt.KeepAspectRatio)
                        self.ImageUpdated.emit(qt_rgb_image_scaled)
                    else:
                        break

        cap.release()
        self.quit()

    def stop(self):
        self.__thread_active = False

    def pause(self):
        self.__thread_pause = True

    def unpause(self):
        self.__thread_pause = False

class MultiCameraViewer(QMainWindow):
    def __init__(self):
        super(MultiCameraViewer, self).__init__()

        self.camera_widgets = []
        self.camera_workers = []

        for _ in range(len(camera_urls)):
            camera_widget = QLabel()
            camera_widget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            camera_widget.setScaledContents(True)
            self.camera_widgets.append(camera_widget)

            camera_worker = CaptureIpCameraFramesWorker(camera_urls[_])
            camera_worker.ImageUpdated.connect(self.update_camera_widget)
            self.camera_workers.append(camera_worker)
            camera_worker.start()

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # Assuming you want a 4x4 grid layout for 16 cameras.
        for i, camera_widget in enumerate(self.camera_widgets):
            row = i // 4
            col = i % 4
            grid_layout.addWidget(camera_widget, row, col)

        central_widget = QWidget(self)
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Multi-Camera Viewer")

    def update_camera_widget(self, image):
        sender = self.sender()
        camera_index = self.camera_workers.index(sender)
        camera_widget = self.camera_widgets[camera_index]
        camera_widget.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        for camera_worker in self.camera_workers:
            camera_worker.stop()
            camera_worker.wait()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MultiCameraViewer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()