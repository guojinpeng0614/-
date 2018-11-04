# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/8/30 9:55'

import json
import socket
import threading

from PyQt5.QtWidgets import QPushButton,QLabel,\
    QWidget,QLineEdit,QHBoxLayout,QVBoxLayout

from PyQt5.QtGui import QPixmap

from Base import Chess,is_win

from PyQt5 import QtGui

from PyQt5.QtCore import pyqtSignal

from Base import BasePlayer,TDPushButton


# 接收完整的数据帧
def recv_sockdata(the_socket):
    total_data = ""
    while True:
        data = the_socket.recv(1024).decode()
        if "END" in data:
            total_data += data[:data.index("END")]
            break
        total_data += data
    return total_data


# 网络设置窗口
class NetworkConfig(QWidget):
    def __init__(self,main_window = None,parent=None):
        super().__init__(parent)
        # 用一个变量保存主界面窗体
        self.main_window = main_window
        # 第一行：昵称：
        self.name_label = QLabel("昵称",self)
        self.name_edit  = QLineEdit(self)
        self.name_edit.setText("玩家1")
        self.h1 = QHBoxLayout()
        self.h1.addWidget(self.name_label,3)
        self.h1.addWidget(self.name_edit,7)
        # 第二行：昵称：
        self.ip_label = QLabel("主机IP",self)
        self.ip_edit  = QLineEdit(self)
        self.ip_edit.setText("127.0.0.1")
        self.h2 = QHBoxLayout()
        self.h2.addWidget(self.ip_label,3)
        self.h2.addWidget(self.ip_edit,7)
        # 第三行 两个按钮
        self.con_btn = QPushButton("连接主机",self)
        self.ser_btn = QPushButton("我是主机",self)
        self.con_btn.clicked.connect(self.client_mode)
        self.ser_btn.clicked.connect(self.server_mode)
        self.h3 = QHBoxLayout()
        self.h3.addWidget(self.con_btn)
        self.h3.addWidget(self.ser_btn)

        self.v = QVBoxLayout()
        self.v.addLayout(self.h1)
        self.v.addLayout(self.h2)
        self.v.addLayout(self.h3)
        self.setLayout(self.v)
        self.game_window = None

    def client_mode(self):
        '''
        启动客户端模式的程序
        '''
        self.game_window = NetworkClient(name=self.name_edit.text(),ip=self.ip_edit.text())
        self.game_window.show()
        self.game_window.backSignal.connect(self.main_window.back)
        self.close()

    def server_mode(self):
        '''
        启动服务器模式的程序
        '''
        self.game_window = NetworkServer(name=self.name_edit.text())
        self.game_window.show()
        self.game_window.backSignal.connect(self.main_window.back)
        self.close()


class NetworkPlayer(BasePlayer):
    dataSignal = pyqtSignal(dict)

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.tcp_socket = None
        # 这里是棋盘
        self.chessboard = [[None for i in range(0, 19)] for j in range(0, 19)]
        # 生成一个历史数组，记录下棋的信息
        self.history = []

        self.dataSignal.connect(self.deal_data)

    def setup_ui(self):
        super().setup_ui()
        self.state_label = QLabel("游戏状态",self)
        self.state_text = QLabel("等待连接",self)
        self.state_label.move(630,200)
        self.state_text.move(680,204)

        self.cuicu_btn = TDPushButton("source/催促按钮_normal.png","source/催促按钮_hover.png","source/催促按钮_press.png",self)
        self.cuicu_btn.show()
        self.cuicu_btn.move(640,450)

    def deal_data(self,data):
        print(data)
        if data["msg"] == "pos":
            pos = data['data']
            xx = pos[0]
            yy = pos[1]
            self.chess = Chess(color='b', parent=self)
            # 如果此处已经有棋子，点击失效
            if self.chessboard[xx][yy] is not None:
                return

            self.chessboard[xx][yy] = self.chess
            self.history.append((xx, yy))
            x = xx *30 + 50 - 15
            y = yy * 30 + 50 - 15

            self.chess.move(x, y)
            self.chess.show()


    def recv_data(self,sock):
        # 收到数据
        print("recv_data")
        while True:
            r_data =  recv_sockdata(sock)
            data = json.loads(r_data)
            self.dataSignal.emit(data)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        print("asd")
        # 如果游戏已经结束，点击失效
        if a0.x() < 40 or a0.x() > 600:
            return
        if a0.y() < 40 or a0.y() > 600:
            return
        # 通过标识，决定棋子的颜色
        self.chess = Chess('w', self)
        # 将棋子定位到准确的坐标点
        if (a0.x() - 50) % 30 <= 15:
            x = (a0.x() - 50) // 30 * 30 + 50
        else:
            x = ((a0.x() - 50) // 30 + 1) * 30 + 50

        if (a0.y() - 50) % 30 <= 15:
            y = (a0.y() - 50) // 30 * 30 + 50
        else:
            y = ((a0.y() - 50) // 30 + 1) * 30 + 50
        # 在棋盘数组中，保存棋子对象
        xx = (x - 50) // 30
        yy = (y - 50) // 30
        # 如果此处已经有棋子，点击失效
        if self.chessboard[xx][yy] is not None:
            return

        self.chessboard[xx][yy] = self.chess
        self.history.append((xx, yy))

        x = x - self.chess.width() / 2
        y = y - self.chess.height() / 2

        self.chess.move(x, y)
        self.chess.show()

        # 落子后， 发送棋子位置
        pos_data = {"msg":"pos","data":(xx,yy)}
        self.tcp_socket.sendall((json.dumps(pos_data)+" END").encode())

        # 翻转棋子颜色
        # self.is_black = not self.is_black

        color = is_win(self.chessboard)
        if color is False:
            return
        else:
            # QMessageBox.information(self,"消息","{}棋胜利".format(color))
            self.win_label = QLabel(self)
            if color == 'b':
                pic = QPixmap("source/黑棋胜利.png")
            else:
                pic = QPixmap("source/白棋胜利.png")
            self.win_label.setPixmap(pic)
            self.win_label.move(100, 100)
            self.win_label.show()
            self.is_over = True


class NetworkServer(NetworkPlayer):
    '''
    运行服务端游戏界面
    '''
    def __init__(self,name="玩家1",parent=None):
        super().__init__(parent)
        self.name = name

        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser_socket.bind(("0.0.0.0", 3003))
        self.ser_socket.listen(8)
        th = threading.Thread(target=self.start_listen)
        th.start()

    def start_listen(self):
        print("start listening ")
        while True:
            sock, addr = self.ser_socket.accept()
            self.tcp_socket = sock
            # 发送了自己的昵称
            self.tcp_socket.sendall(
                (
                    json.dumps(
                        {"msg": "name", "data": self.name}
                    ) + " END"
                ).encode()
            )
            self.recv_data(self.tcp_socket)


class NetworkClient(NetworkPlayer):
    '''
    运行客户端游戏界面
    '''
    def __init__(self,name="玩家1",ip="127.0.0.1",parent=None):
        super().__init__(parent)
        self.name = name
        self.tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr = (ip,3003)
        self.tcp_socket.connect(addr)
        self.tcp_socket.sendall((json.dumps({"msg":"name","data":self.name})+" END").encode())
        th = threading.Thread(target=self.recv_data,args=(self.tcp_socket,))
        # self.recv_data(self.tcp_socket)
        th.start()







