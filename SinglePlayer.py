# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/8/30 9:53'

from Base import BasePlayer,Chess,is_win
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
import random


class SinglePlayer(BasePlayer):
    '''
    单人对战
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        # print("__init__")
        # 这里是棋盘
        self.chessboard = [[None for i in range(0, 19)] for j in range(0, 19)]
        # 生成一个历史数组，记录下棋的信息
        self.history = []
        self.is_black = True
        self.is_over = False
        self.restart_btn.clicked.connect(self.restart)
        self.lose_btn.clicked.connect(self.lose)
        self.huiqi_btn.clicked.connect(self.huiqi)
        self.win_label = None
        # print(self.chessboard)

    def huiqi(self):
        '''
        悔棋的逻辑
        '''
        if self.is_over:
            return
        if self.history:
            return
        # 去最后一个元组
        pos = self.history.pop()
        # 通过元组记录的坐标销毁棋子
        self.chessboard[pos[0]][pos[1]].close()
        self.chessboard[pos[0]][pos[1]] = None
        # 转置棋子颜色
        self.is_black = not self.is_black

    def lose(self):
        '''
        点击认输，执行此函数
        '''
        if self.is_over:
            return

        self.win_label = QLabel(self)
        if self.is_black:
            pic = QPixmap("source/白棋胜利.png")
        else:
            pic = QPixmap("source/黑棋胜利.png")
        self.win_label.setPixmap(pic)
        self.win_label.move(100, 100)
        self.win_label.show()
        self.is_over = True

    def restart(self):
        # 重新开始游戏
        self.is_over = False
        # 清空胜利图片
        if self.win_label is not None:
            self.win_label.close()
        # 清空棋盘
        for i in range(0, 19):
            for j in range(0, 19):
                if self.chessboard[j][i] is not None:
                    self.chessboard[j][i].close()
                    self.chessboard[j][i] = None

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        # 如果游戏已经结束，点击失效
        if self.is_over == True:
            return

        if a0.x() < 40 or a0.x() > 600:
            return
        if a0.y() < 40 or a0.y() > 600:
            return
        # 通过标识，决定棋子的颜色
        if self.is_black:
            self.chess = Chess(color='b', parent=self)
        else:
            self.chess = Chess('w', self)
        # 翻转棋子颜色
        self.is_black = not self.is_black
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

        color = is_win(self.chessboard)
        if color is False:
            pass
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

        # 判断完胜负，计算机落子
        self.auto_run()

    def auto_run(self):
        '''
        计算机执行落子函数
        '''
        # 分别保存黑子，白子分数的数组
        scores_c = [[0 for i in range(0,19)] for j in range(0,19)]
        scores_p = [[0 for i in range(0,19)] for j in range(0,19)]
        # 计算所有点的分数
        for j in range(0,19):
            for i in range(0,19):
                if self.chessboard[i][j] is not None:
                    continue  # 如果有棋子了，找下一个点
                # 假设下黑棋的分数
                self.chessboard[i][j] = Chess('b',self)
                scores_c[i][j] += self.score(i,j,'b')
                # 假设下白棋的分数
                self.chessboard[i][j] = Chess('w',self)
                scores_p[i][j] += self.score(i,j,'w')
                # 恢复棋盘为空
                self.chessboard[i][j] = None

        # 先将两个二维数组，转成一位数组便于运算
        r_scores_c = []
        r_scores_p = []
        for item in scores_c:
            r_scores_c += item
        for item in scores_p:
            r_scores_p += item

        # 最终分数，取两者中更大的一个，然后将取值合并成为一个数组
        result = [max(a,b) for a,b in zip(r_scores_c,r_scores_p)]
        # 取出最大值点的下标
        chess_index = result.index(max(result))
        # 通过下标计算出落子的位置
        xx = chess_index // 19
        yy = chess_index % 19

        # 落子
        if self.is_black:
            self.chess = Chess('b',self)
        else:
            self.chess = Chess('w',self)

        x = xx * 30 + 50 - 15
        y = yy * 30 + 50 - 15

        self.chess.move(x,y)
        self.chess.show()
        self.chessboard[xx][yy] = self.chess
        self.history.append((x,y))
        self.is_black = not self.is_black
        color = is_win(self.chessboard)
        if color is False:
            pass
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

    def score(self,x,y,color):
        '''
        计算，如果在x,y这个点下color颜色的棋子，会得到多少分
        '''
        blank_score = [0,0,0,0]
        chess_score = [0,0,0,0]

        # 右方向
        for i in range(x,x+5):
            if i >= 19 :
                break
            if self.chessboard[i][y] is not None:
                if self.chessboard[i][y].color == color:
                    # 如果是相同点，同色点分数加一
                    chess_score[0] += 1
                    # 朝同一个方向进行，每次遇到相同的颜色，都加一分
                else:
                    break
            else:
                blank_score[0] += 1
                break
        # 左方向
        for i in range(x-1,x-5,-1):
            if i <= 0:
                break
            if self.chessboard[i][y] is not None:
                if self.chessboard[i][y].color == color:
                    chess_score[0] += 1
                else:
                    break
            else:
                blank_score[0] += 1
                break
        # 下方向
        for j in range(y,y+5):
            if j >= 19 :
                break
            if self.chessboard[x][j] is not None:
                if self.chessboard[x][j].color == color:
                    chess_score[1] += 1
                else:
                    break
            else :
                blank_score[1] += 1
                break
        # 上方向
        for j in range(y-1,y-5,-1):
            if j <= 0:
                break
            if self.chessboard[x][j] is not None:
                if self.chessboard[x][j].color == color:
                    chess_score[1] += 1
                else:
                    break
            else:
                blank_score[1] += 1
                break
        # 右下方向
        j = y
        for i in range(x,x+5):
            if i >= 19 or j >= 19 :
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color:
                    chess_score[2] += 1
                else :
                    break
            else:
                blank_score[2] += 1
                break
            j+=1
        # 左上
        j = y-1
        for i in range(x-1,x-5,-1):
            if i <= 0 or j <= 0:
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color :
                    chess_score[2] += 1
                else:
                    break
            else:
                blank_score[2] += 1
                break
            j -= 1

        # 左下
        j = y
        for i in range(x,x-5,-1):
            if i <= 0 or j >= 19 :
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color:
                    chess_score[3] += 1
                else:
                    break
            else:
                blank_score[3] += 1
                break
            j+=1
        # 右上
        j = y - 1
        for i in range(x+1,x+5):
            if i >= 19 or j <= 0 :
                break
            if self.chessboard[i][j] is not None:
                if self.chessboard[i][j].color == color :
                    chess_score[3] += 1
                else :
                    break
            else :
                blank_score[3] += 1
                break
            j -= 1

        # 计算总分:
        for score in chess_score:
            if score > 4:  # 如果某个方向超过4，则此处落子五子连珠
                return 100
        for i in range(0,len(blank_score)):
            if blank_score[i] == 0:  # 说明在这个空白点的附近，没有同色棋子，也没有可继续落子的地方
                blank_score[i] -= 20
        # 四个方向的分数，将两个列表依次相加
        result = [a+b for a,b in zip(chess_score,blank_score)]

        return max(result)  # 返回四个方向其中的最高分值









