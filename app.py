from PyQt6.QtWidgets import QApplication  # , QWidget, QMainWindow
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, Qt, QObject

import sys


from ui.MainWindow import MainWindow
from ui.WebView import WebView

from ui.menu_bar import MenuManager
from actions.menu_action_handle import ActionsHandler


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    # 创建菜单栏
    action_handler = ActionsHandler(window)

    menu_manger = MenuManager(window, action_handler)

    window.setMenuBar(menu_manger.menuBar())

    window.show()

    sys.exit(app.exec())
