from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction


class MenuManager:
    def __init__(self, main_window, action_handler):
        self.main_window = main_window
        self.action_handler = action_handler

        self.action_map = {}

        self.create_menu_bar()

    def menuBar(self):
        return self.menubar

    # 创建菜单栏
    def create_menu_bar(self):
        self.menubar = QMenuBar(self.main_window)

        # 创建“文件”菜单
        file_menu = QMenu("文件", self.main_window)
        self.menubar.addMenu(file_menu)

        # 创建“打开”菜单项
        open_action = QAction("打开", self.main_window)
        open_action.triggered.connect(lambda: print("执行打开文件操作"))
        file_menu.addAction(open_action)
        self.action_map["file_open"] = open_action

        # 创建“退出”菜单项
        exit_action = QAction("退出", self.main_window)
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)
        self.action_map["file_quit"] = exit_action

        # 创建“编辑”菜单
        edit_menu = QMenu("编辑", self.main_window)
        self.menubar.addMenu(edit_menu)

        # 创建“复制”菜单项
        copy_action = QAction("复制", self.main_window)
        copy_action.triggered.connect(lambda: print("执行复制文本操作"))
        edit_menu.addAction(copy_action)
        self.action_map["file_copy"] = copy_action

        # 创建“粘贴”菜单项
        paste_action = QAction("粘贴", self.main_window)
        paste_action.triggered.connect(lambda: print("执行粘贴文本操作"))
        edit_menu.addAction(paste_action)
        self.action_map["file_paste"] = paste_action

        # 创建“视频”菜单
        video_menu = QMenu("视频", self.main_window)
        self.menubar.addMenu(video_menu)

        # 创建“打开摄像头”菜单项
        open_video_action = QAction("打开视频", self.main_window)

        # action_video_open
        open_video_action.triggered.connect(self.action_handler.action_video_open)
        video_menu.addAction(open_video_action)
        self.action_map["video_open"] = open_video_action

        # 创建“关闭摄像头”菜单项
        close_video_action = QAction("关闭视频", self.main_window)
        close_video_action.triggered.connect(lambda: print("执行关闭视频操作"))
        video_menu.addAction(close_video_action)
        self.action_map["video_close"] = close_video_action

        # 创建“拉流”菜单项
        pull_stream_action = QAction("拉流", self.main_window)
        pull_stream_action.triggered.connect(lambda: print("执行拉流操作"))
        video_menu.addAction(pull_stream_action)
        self.action_map["video_pull"] = pull_stream_action

        # 创建“推流”菜单项
        push_stream_action = QAction("推流", self.main_window)
        push_stream_action.triggered.connect(lambda: print("执行推流操作"))
        video_menu.addAction(push_stream_action)
        self.action_map["video_push"] = push_stream_action

        # 创建“帮助”菜单
        help_menu = QMenu("帮助", self.main_window)
        self.menubar.addMenu(help_menu)

        help_action = QAction("帮助", self.main_window)
        help_action.triggered.connect(self.action_handler.action_help)
        help_menu.addAction(help_action)
        self.action_map["help"] = help_action

        help_doc_action = QAction("文档", self.main_window)
        help_doc_action.triggered.connect(self.action_handler.action_doc)
        help_menu.addAction(help_doc_action)
        self.action_map["help_doc"] = help_doc_action

        # return menubar
