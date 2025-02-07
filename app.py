from PyQt6.QtWidgets import QApplication  # , QWidget, QMainWindow

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

from ui.WebView import WebView

from ui.menu_bar import MenuManager
from actions.menu_action_handle import ActionsHandler


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
                print("Error: Cannot open video  stream.")
                return
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Cannot open  video  stream.")
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.video_url)
                    continue

                frame = np.array(frame)

                begin_t = time.perf_counter()

                # pridict
                # result_image, _ = self.prodict.predict_and_detect(
                #     self.prodict.model, frame, classes=[], conf=0.5
                # )
                end_t = time.perf_counter()

                # print("predict time:", (end_t - begin_t))
                # self.signalFrame.emit(result_image)
                self.signalFrame.emit(frame)

        except Exception as e:
            print(f"Error occurred while opening video source: {e}")
        finally:
            if self.cap is not None:
                self.cap.release()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    # 创建菜单栏
    action_handler = ActionsHandler(window)

    menu_manger = MenuManager(window, action_handler)

    window.setMenuBar(menu_manger.menuBar())

    camera = Camera()
    # rtmp_url = "rtmp://127.0.0.1:1935/live/obs/"
    # rtmp_url = "rtmp://10.255.255.254:1935/live/obs/"
    rtmp_url = "rtmp://172.26.222.211:1935/live/obs/"

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
