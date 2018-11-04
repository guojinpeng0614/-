# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/8/30 9:12'

import sys

# from PyQt5 import QtWidgets
import cgitb
cgitb.enable(format='error')

from PyQt5.QtWidgets import QApplication,QLabel,QWidget,QPushButton
from PyQt5.QtGui import QPalette,QPixmap,QIcon,QBrush

from SinglePlayer import SinglePlayer
from DoublePlayer import  DoublePlayer
from NetworkPlayer import NetworkPlayer,NetworkConfig

from Base import TDPushButton


class GameStart(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        # 设置窗体图标
        self.setWindowIcon(QIcon("source/icon.ico"))
        # 设置窗体的标题
        self.setWindowTitle("五子棋-PA1801")
        # 设置窗体固定大小
        self.setFixedSize(760,650)
        # 设置窗体的背景图片
        palette = QPalette()
            # setBrush（谁是给谁，设置什么）
        palette.setBrush(self.backgroundRole(),
                         QBrush(QPixmap("source/五子棋界面.png")))
        self.setPalette(palette)

        # 生成三个按钮，移动到对应位置
        self.single_btn = TDPushButton("source/人机对战_normal.png","source/人机对战_hover.png","source/人机对战_press.png",self)
        self.double_btn = TDPushButton("source/双人对战_normal.png",
                                       "source/双人对战_hover.png",
                                       "source/双人对战_press.png",
                                       self)
        self.network_btn = TDPushButton("source/联机对战_normal.png","source/联机对战_hover.png","source/联机对战_press.png",self)
        self.single_btn.move(250,300)
        self.double_btn.move(250,400)
        self.network_btn.move(250,500)

        # 三个按钮绑定处理函数，处理函数中页面跳转
        self.single_btn.clicked.connect(self.single)
        self.double_btn.clicked.connect(self.double)
        self.network_btn.clicked.connect(self.network)

        self.game_window = None  # 游戏窗体

    def single(self):
        self.game_window = SinglePlayer()
        self.game_window.backSignal.connect(self.back)
        self.game_window.show()
        self.close()

    def double(self):
        self.game_window = DoublePlayer()
        self.game_window.backSignal.connect(self.back)
        self.game_window.show()
        self.close()

    def network(self):
        self.game_window = NetworkConfig(main_window=self)
        # self.game_window.backSignal.connect(self.back)
        self.game_window.show()
        self.close()

    def back(self):
        # 捕获到返回的信号
        # 把自己显示出来
        self.show()

if __name__ == "__main__":
    # 启动窗体应用
    app = QApplication(sys.argv)
    # 启动游戏窗体
    w = GameStart()
    w.show()
    sys.exit(app.exec_())


