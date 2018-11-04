# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/8/30 9:41'

from PyQt5.QtWidgets import QWidget,QPushButton,QLabel
from PyQt5.QtGui import QPalette,QBrush,QPixmap,QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui,QtCore
# 这个文件存放相关的基础数据


class TDPushButton(QLabel):
    clicked = pyqtSignal()
    def __init__(self,str1,str2,str3,parent):
        super().__init__(parent)

        # 设置窗体图标
        self.setWindowIcon(QIcon("source/icon.ico"))
        # 设置窗体的标题
        self.setWindowTitle("五子棋-PA1801")

        # 加载三态图片
        self.pic_normal = QPixmap(str1)
        self.pic_hover  = QPixmap(str2)
        self.pic_press  = QPixmap(str3)
        # 重设大小，显示正常状态下的图片
        self.resize(self.pic_normal.size())
        self.setPixmap(self.pic_normal)

    # 鼠标已进入，就会执行此事件
    def enterEvent(self, a0: QtCore.QEvent):
        self.setPixmap(self.pic_hover)

    # 鼠标一离开，将图片换回来
    def leaveEvent(self, a0: QtCore.QEvent):
        self.setPixmap(self.pic_normal)

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.setPixmap(self.pic_press)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        self.clicked.emit()
        self.setPixmap(self.pic_hover)


# 封装一个棋子类
class Chess(QLabel):
    def __init__(self,color='w',parent=None):
        super().__init__(parent)
        self.color = color
        if color == "w":
            pic = QPixmap("source/白子.png")
        elif color == 'b':
            pic = QPixmap("source/黑子.png")
        self.resize(pic.size())
        self.setPixmap(pic)


class BasePlayer(QWidget):

    backSignal = pyqtSignal()

    def __init__(self,parent = None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(760,650)
        # 设置背景图
        palette = QPalette()
        palette.setBrush(self.backgroundRole(),
                QBrush(QPixmap("source/游戏界面.png")))
        self.setPalette(palette)
        # 添加按钮

        self.back_btn = TDPushButton("source/返回按钮_normal.png","source/返回按钮_hover.png","source/返回按钮_press.png",self)
        self.back_btn.clicked.connect(self.back)
        self.restart_btn = TDPushButton("source/开始按钮_normal.png","source/开始按钮_hover.png","source/开始按钮_press.png",self)
        self.lose_btn = TDPushButton("source/认输按钮_normal.png","source/认输按钮_hover.png","source/认输按钮_press.png",self)
        self.huiqi_btn = TDPushButton("source/悔棋按钮_normal.png","source/悔棋按钮_hover.png","source/悔棋按钮_press.png",self)

        self.back_btn.move(680,10)
        self.restart_btn.move(640,240)
        self.lose_btn.move(640,310)
        self.huiqi_btn.move(640,380)

    def back(self):
        # 关闭本窗体，告诉别人我要返回
        # 发射一个自定义的信号
        self.backSignal.emit()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        pass


def is_win(chessboard):
    '''
    判断棋盘上是否有玩家胜利
    :param chessboard: 19*19的二维数组
    :return: 没有返回False，有的话，返回胜利者的颜色
    '''
    for j in range(0,19): # 注意这里会出现数组越界的情况，我们在代码中直接pass掉
        for i in range(0,19):
            if chessboard[i][j] is not None:
                c = chessboard[i][j].color
                # 判断右、右下、下、左下四个方向是否构成五子连珠，如果构成了，就可以。
                # 右
                try:
                    if chessboard[i+1][j] is not None:
                        if chessboard[i+1][j].color == c:
                            if chessboard[i+2][j] is not None:
                                if chessboard[i+2][j].color == c:
                                    if chessboard[i+3][j] is not None:
                                        if chessboard[i+3][j].color == c:
                                            if chessboard[i+4][j] is not None:
                                                if chessboard[i+4][j].color == c:
                                                    return c
                except IndexError:
                    pass
                # 右下
                try:
                    if chessboard[i+1][j+1] is not None:
                        if chessboard[i+1][j+1].color == c:
                            if chessboard[i+2][j+2] is not None:
                                if chessboard[i+2][j+2].color == c:
                                    if chessboard[i+3][j+3] is not None:
                                        if chessboard[i+3][j+3].color == c:
                                            if chessboard[i+4][j+4] is not None:
                                                if chessboard[i+4][j+4].color == c:
                                                    return c
                except IndexError:
                    pass
                # 下
                try:
                    if chessboard[i][j+1] is not None:
                        if chessboard[i][j+1].color == c:
                            if chessboard[i][j+2] is not None:
                                if chessboard[i][j+2].color == c:
                                    if chessboard[i][j+3] is not None:
                                        if chessboard[i][j+3].color == c:
                                            if chessboard[i][j+4] is not None:
                                                if chessboard[i][j+4].color == c:
                                                    return c
                except IndexError:
                    pass
                # 左下
                try:
                    if chessboard[i-1][j+1] is not None:
                        if chessboard[i-1][j+1].color == c:
                            if chessboard[i-2][j+2] is not None:
                                if chessboard[i-2][j+2].color == c:
                                    if chessboard[i-3][j+3] is not None:
                                        if chessboard[i-3][j+3].color == c:
                                            if chessboard[i-4][j+4] is not None:
                                                if chessboard[i-4][j+4].color == c:
                                                    return c
                except IndexError:
                    pass

    # 所有的都不成立，返回False
    return False
    # for y in range(19):
    #     for x in range(19):
    #         if chessboard[x][y] is None: # 如果为空，继续执行
    #             continue
    #         color = chessboard[x][y].color
    #         # 不为空的逻辑
    #         # 右方向
    #         if chessboard[x+1][y] is not None:
    #             if chessboard[x+1][y].color == color:
    #                 if chessboard[x+2][y] is not None:
    #                     if chessboard[x+2][y].color == color:
    #                         if chessboard[x+3][y] is not None:
    #                             if chessboard[x+3][y].color == color:
    #                                 if chessboard[x+4][y] is not None:
    #                                     if chessboard[x+4][y].color == color:
    #                                         return chessboard[x][y].color
    #         # 下方向
    #         if chessboard[x][y+1] is not None:
    #             if chessboard[x][y+1].color == color:
    #                 if chessboard[x][y+2] is not None:
    #                     if chessboard[x][y+2].color == color:
    #                         if chessboard[x][y+3] is not None:
    #                             if chessboard[x][y+3].color == color:
    #                                 if chessboard[x][y+4] is not None:
    #                                     if chessboard[x][y+4].color == color:
    #                                         return chessboard[x][y].color
    #         # 右下方向
    #         if chessboard[x + 1][y + 1] is not None:
    #             if chessboard[x + 1][y + 1].color == color:
    #                 if chessboard[x + 2][y + 2] is not None:
    #                     if chessboard[x + 2][y + 2].color == color:
    #                         if chessboard[x + 3][y + 3] is not None:
    #                             if chessboard[x + 3][y + 3].color == color:
    #                                 if chessboard[x + 4][y + 4] is not None:
    #                                     if chessboard[x + 4][y + 4].color == color:
    #                                         return chessboard[x][y].color
    #         # 左下方向
    #         if chessboard[x - 1][y + 1] is not None:
    #             if chessboard[x - 1][y + 1].color == color:
    #                 if chessboard[x - 2][y + 2] is not None:
    #                     if chessboard[x - 2][y + 2].color == color:
    #                         if chessboard[x - 3][y + 3] is not None:
    #                             if chessboard[x - 3][y + 3].color == color:
    #                                 if chessboard[x - 4][y + 4] is not None:
    #                                     if chessboard[x - 4][y + 4].color == color:
    #                                         return chessboard[x][y].color
    #
    # return False # 没有五子连珠

