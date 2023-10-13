import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QPixmap


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


class VideoPlayerWidget(QWidget):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 0
        self.display_height = 0

        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # create a vertical box layout and add the image label
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)

        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread(self.url)
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def resizeEvent(self, event):
        # Get the size of the widget when it is resized
        self.disply_width = self.image_label.width()
        self.display_height = self.image_label.height()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        if self.disply_width > 0 and self.display_height > 0:
            # Calculate aspect ratio
            aspect_ratio = cv_img.shape[1] / cv_img.shape[0]
            # Calculate new width and height based on aspect ratio
            new_width = int(self.disply_width)
            new_height = int(self.disply_width / aspect_ratio)

            # Resize the image to fit the widget while maintaining aspect ratio
            qt_img = self.convert_cv_qt(cv2.resize(cv_img, (new_width, new_height)))
            self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)