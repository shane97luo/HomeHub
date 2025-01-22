from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtCore import pyqtSignal, QObject
import sys
import cv2

from ui.VideoStreamWidget import VideoStreamWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(1024, 768)

        self.setWindowTitle("Monitor System")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        # 创建一个垂直布局
        self.layout = QGridLayout(self.central_widget)
        # 创建一个标签
        self.label_00 = VideoStreamWidget()
        self.label_01 = VideoStreamWidget()
        self.label_10 = VideoStreamWidget()
        self.label_11 = VideoStreamWidget()

        self.layout.addWidget(self.label_00, 0, 0)
        self.layout.addWidget(self.label_01, 0, 1)
        self.layout.addWidget(self.label_10, 1, 0)
        self.layout.addWidget(self.label_11, 1, 1)

        # 创建一个按钮
        self.button = QPushButton("Click Me", self.central_widget)
        self.layout.addWidget(self.button)
        # 连接按钮的点击信号到槽函数
        self.button.clicked.connect(self.on_button_click)

        # 设置布局
        self.central_widget.setLayout(self.layout)

    def updateOriFrame(self, frame):
        # print("111")
        self.label_00.update(frame)
        # self.label_01.update(cv2.flip(frame, 1))
        # self.label_10.update(cv2.flip(frame, -1))

    def updateRtmp(self, frame):
        self.label_01.update(frame)

    def on_button_click(self):
        self.label.setText("Button Clicked!")

    def timerEvent(self):
        print("111")
