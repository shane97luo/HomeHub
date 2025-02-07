import sys
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction


# 定义一个处理菜单动作的类
class ActionsHandler:
    def __init__(self, main_window):
        self.main_window = main_window

    def open_file(self):
        print("执行打开文件操作")

    def exit_app(self):
        self.main_window.close()
