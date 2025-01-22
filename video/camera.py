# from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, Qt, QObject

import numpy as np
import ffmpeg
import time
import sys
import cv2


def push_camera_stream(rtmp_url):
    # 打开摄像头，0 表示默认摄像头
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    try:
        # 获取摄像头的宽度和高度
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        print("width:", width, "height:", height, "fps:", fps)
        # 创建 ffmpeg 输入流，使用 pipe 模式
        process = (
            ffmpeg.input(
                "pipe:",
                format="rawvideo",
                pix_fmt="bgr24",
                s=f"{width}x{height}",
                r=fps,
            )
            .output(
                rtmp_url,
                vcodec="libx264",
                preset="veryfast",
                video_bitrate="2000k",
                format="flv",
                tune="zerolatency",  # 设置为零延时
                max_delay=0,  # 最大延迟设置为 0
                threads=6,
            )
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = np.array(frame)

            process.stdin.write(frame.tobytes())

            time.sleep(0.04)

    except ffmpeg.Error as e:
        print(f"Error occurred during push stream: {e.stderr}")
    finally:
        cap.release()
        process.stdin.close()
        process.wait()


# if __name__ == "__main__":
# rtmp_url = "rtmp://127.0.0.1:1935/live/obs/"


class Camera(QObject):
    frame_ready = pyqtSignal(np.ndarray)

    signalFrame = pyqtSignal(np.ndarray)
    signalStr = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        # self.start_stream()

    def timerEvent(self):

        if not self.cap.isOpened():
            print("Error: Cannot open camera.")
            return

        ret, frame = self.cap.read()
        if not ret:
            print("Error: Cannot open camera.")
            return

        frame = np.array(frame)
        self.process.stdin.write(frame.tobytes())
        self.signalFrame.emit(frame)
        # self.signalStr.emit("ok")
        return

    def pushStream(self, rtmp_url):
        self.rtmp_url = rtmp_url
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Cannot open camera.")
            return

        try:
            # 获取摄像头的宽度和高度
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))

            # 创建 ffmpeg 输入流，使用 pipe 模式
            self.process = (
                ffmpeg.input(
                    "pipe:",
                    format="rawvideo",
                    pix_fmt="bgr24",
                    s=f"{width}x{height}",
                    r=fps,
                )
                .output(
                    self.rtmp_url,
                    vcodec="libx264",
                    preset="veryfast",
                    video_bitrate="2000k",
                    format="flv",
                    tune="zerolatency",  # 设置为零延时
                    max_delay=0,  # 最大延迟设置为 0
                    threads=6,
                )
                .overwrite_output()
                .run_async(pipe_stdin=True)
            )

        except ffmpeg.Error as e:
            print(f"Error occurred during push stream: {e.stderr}")

        # finally:
        # cap.release()
        # process.stdin.close()
        # process.wait()
