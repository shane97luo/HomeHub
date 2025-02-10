import sys
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, Qt, QObject
from ui.VideoStreamWidget import VideoStreamWidget
from predict.predict_image import Predict

from video.camera import Camera

import numpy as np

import cv2
import ffmpeg
import time


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


# 定义一个处理菜单动作的类
class ActionsHandler:
    def __init__(self, main_window):
        self.main_window = main_window

    def open_file(self):
        print("执行打开文件操作")

    def exit_app(self):
        self.main_window.close()

    def action_video_open(self):
        print("执行复制文本操作")
        self.camera = Camera()
        rtmp_url = "rtmp://172.26.222.211:1935/live/obs/"

        self.camera.pushStream(rtmp_url)
        self.camera.signalFrame.connect(self.main_window.updateOriFrame)

        self.timer = QTimer()
        self.timer.timeout.connect(self.camera.timerEvent)
        self.timer.start(100)

        self.v_stream = VideoStream(rtmp_url)
        self.v_stream.signalFrame.connect(self.main_window.updateRtmp)
        self.v_stream.start()

    def action_help(self):
        print("执行帮助操作")

    def action_doc(self):
        print("文档操作")
