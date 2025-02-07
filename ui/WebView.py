from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import sys


class WebEngineView(QWebEngineView):

    def __init__(self):
        super(WebEngineView, self).__init__()

    def createWindow(self, QWebEnginePage_WebWindowType):
        return self


class WebView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建 QWebEngineView 实例
        self.web_view = WebEngineView()
        # 禁用上下文菜单
        # self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        # 设置背景颜色为黑色
        self.web_view.setStyleSheet("background-color: #000000;")

        # 创建前进和后退按钮
        self.back_button = QPushButton("后退")
        self.forward_button = QPushButton("前进")

        # 连接按钮的点击信号到相应的槽函数
        self.back_button.clicked.connect(self.web_view.back)
        self.forward_button.clicked.connect(self.web_view.forward)

        # 创建水平布局用于放置按钮
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.forward_button)

        # 创建垂直布局，将按钮布局和 WebView 组合在一起
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.web_view)

        # 设置主布局
        self.setLayout(main_layout)

    def load_url(self, url):
        # 加载指定 URL
        self.web_view.load(QUrl(url))
        # 显示网页
        self.web_view.show()


# # from PyQt6.QtCore import *
# # from PyQt6.QtGui import *

# from PyQt6.QtWebEngineWidgets import QWebEngineView


# class WebView(QWebEngineView):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
#         self.setStyleSheet("background-color: #000000;")

#     def loadUrl(self, url):
#         self.load(QUrl(url))
#         self.show()
