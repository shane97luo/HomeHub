from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, Qt, QObject

import cv2
import ffmpeg
import numpy as np
import time
import sys


from ui.MainWindow import MainWindow
from ui.VideoStreamWidget import VideoStreamWidget
from video.camera import Camera
from predict.predict_image import Predict


class VideoStream(QThread):

    signalFrame = pyqtSignal(np.ndarray)

    prodict = Predict()

    def __init__(self, video_url, parent=None):
        super(VideoStream, self).__init__(parent)
        # 创建 ffmpeg 进程
        self.video_url = video_url
        self.running = True

    def run(self):

        try:
            self.cap = cv2.VideoCapture(self.video_url)
            if not self.cap.isOpened():
                print("Error: Cannot open camera.")
                return
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Cannot open camera.")
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.video_url)
                    continue

                frame = np.array(frame)

                result_image, _ = self.prodict.predict_and_detect(
                    self.prodict.model, frame, classes=[], conf=0.5
                )

                self.signalFrame.emit(result_image)
                # self.signalFrame.emit(frame)
        except Exception as e:
            print(f"Error occurred while opening video source: {e}")
        finally:
            if self.cap is not None:
                self.cap.release()

    # def capture_img(self):

    #     if not self.cap.isOpened():
    #         print("Error: Cannot open camera.")
    #         self.cap.release()
    #         self.cap = cv2.VideoCapture(self.rtmp_url)
    #         return
    #     ret, frame = self.cap.read()
    #     if not ret:
    #         print("Error: Cannot open camera.")
    #         # self.cap = cv2.VideoCapture(rtmp_url)

    #         return
    #     frame = np.array(frame)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    camera = Camera()
    rtmp_url = "rtmp://127.0.0.1:1935/live/obs/"

    camera.pushStream(rtmp_url)
    camera.signalFrame.connect(window.updateOriFrame)

    timer = QTimer()
    timer.timeout.connect(camera.timerEvent)
    timer.start(100)

    v_stream = VideoStream(rtmp_url)
    v_stream.signalFrame.connect(window.updateRtmp)
    v_stream.start()

    window.show()

    sys.exit(app.exec())
