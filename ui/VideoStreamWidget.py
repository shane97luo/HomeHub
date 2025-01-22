from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QImage, QPixmap

import cv2
import ffmpeg
import numpy as np
import sys


class VideoStreamWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RTMP Video Stream")
        self.layout = QVBoxLayout()

        self.video_label = QLabel(self)
        # self.video_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        self.setLayout(self.layout)

    def convert_frame_to_qimage(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = np.require(frame, np.uint8, "C")
        q_image = QImage(
            q_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888
        )
        return q_image

    def update(self, frame):

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = self.convert_frame_to_qimage(frame)

        self.video_label.setPixmap(QPixmap.fromImage(image))
