# -*- coding: utf-8 -*-
import wx
import os
import sys
import random


class Snake(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 668))
        self.initFrame()

    def initFrame(self):

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -1, -1])
        self.statusbar.SetStatusText(u"得分: 0", 0)
        self.statusbar.SetStatusText(u"难度: 简单", 1)
        self.statusbar.SetStatusText(u"", 2)
        self.board = Board(self)
        self.board.SetFocus()#获取焦点
        self.board.start()
        self.menuBar = wx.MenuBar()

        game = wx.Menu()
        game.Append(201, u"退出(&E)\tCtrl + Shift + Delete")
        game.Append(202, u"暂停(&S)\tCtrl + s")
        self.Bind(wx.EVT_MENU, self.Onset, id=201, id2=202)
        self.menuBar.Append(game, u"&游戏")

        speed = wx.Menu()
        speed.AppendRadioItem(204, u"简单")
        speed.AppendRadioItem(205, u"一般")
        speed.AppendRadioItem(206, u"困难")
        self.Bind(wx.EVT_MENU, self.OnSpeed, id=204, id2=206)
        self.menuBar.Append(speed, u"&难度")

        help = wx.Menu()
        help.Append(301, u"规则\tCtrl + 1")
        help.Append(302, u"关于\tCtrl + 2")

        self.menuBar.Append(help, u"帮助")
        self.Bind(wx.EVT_MENU, self.Onhelp, id=301)
        self.Bind(wx.EVT_MENU, self.Onhelp, id=302)
        self.SetMenuBar(self.menuBar)
        self.Centre()
        self.Show(True)

    def Onset(self, evt):
        id = evt.GetId()
        if id == 201:
            self.Close()
        if id == 202:
            self.board.pause()

    def OnSpeed(self, evt):
        id = evt.GetId()
        if id == 204:
            self.statusbar.SetStatusText(u"难度: 简单", 1)
            self.board.Speed = 1000
        if id == 205:
            self.statusbar.SetStatusText(u"难度: 一般", 1)
            self.board.Speed = 700
        if id == 206:
            self.statusbar.SetStatusText(u"难度: 困难", 1)
            self.board.Speed = 400
        self.board.Refresh()
        self.board.timer.Start(self.board.Speed)

    def Onhelp(self, evt):
         wx.MessageBox(u"第七次上机练习(WX)\n贪吃蛇\n\n学号:1016xxxx\n姓名:secrul",
                          u"About program", wx.OK | wx.ICON_INFORMATION, self)

class Board(wx.Panel):
    BoardWidth = 15
    BoardHeight = 15
    Speed = 1000
    ID_TIMER = 1
    direct = 1
    block = 2
    colors = ['BLACK', 'BLUE', 'RED', 'PINK', 'GREEN', 'ORANGE']

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        self.timer = wx.Timer(self, Board.ID_TIMER)
        self.isWaiting = False
        self.board = []
        self.sorce = 0
        self.clearBoard()
        # self.way = [0,0,0,0,0,0,0,0,0,0]
        self.way = [0,0,1,0,2,0,3,0,3,1]#蛇节点坐标
        self.board[0] = 2   #初始蛇的位置
        self.board[1] = 2
        self.board[2] = 2
        self.board[3] = 2
        self.board[18] = 2
        self.isStarted = False
        self.isPaused = False
        self.flag = 1

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=Board.ID_TIMER)
        self.clearBoard()

    def generateblock(self):#在空白处随机生成食物
        x = int(random.random()*Board.BoardWidth*Board.BoardWidth)
        while self.board[x] != 0:
            x = int(random.random() * Board.BoardWidth*Board.BoardHeight)
            for i in range(Board.BoardWidth*Board.BoardWidth):
                if self.board[i] == 0:
                    break
            if i == Board.BoardWidth*Board.BoardWidth - 1:
                wx.MessageBox("你太棒了\n满分",'congraturation')

        return x

    def blockAt(self, x, y):  #返回（x,y）点在board中的值
            return self.board[(y * Board.BoardWidth) + x]


    def squareWidth(self):  # 方块的宽度
        return self.GetClientSize().GetWidth() / Board.BoardWidth

    def squareHeight(self):  # 方块的高度,这里设置为和款一样
        return self.GetClientSize().GetWidth()/ Board.BoardWidth

    def start(self):  # 定时器开始运行

        if self.isPaused:  # 如果暂停，定时器结束
            return

        self.isStarted = True
        self.isWaiting = False
        self.sorce= 0
        self.clearBoard()
        self.newPos()
        self.timer.Start(self.Speed)

    def pause(self):  # 响应空格键，定时器
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        statusbar = self.GetParent().statusbar

        if self.isPaused:
            self.timer.Stop()
            statusbar.SetStatusText('paused', 2)
            statusbar.SetStatusText(u"得分:" + str(self.sorce), 0)
        else:
            self.timer.Start(self.Speed)
            statusbar.SetStatusText(u"得分:" + str(self.sorce), 0)
            statusbar.SetStatusText('', 2)
        self.Refresh()

    def clearBoard(self):  

        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(0)

    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardHeight):
                block = self.blockAt(j, i)
                if block != 0:
                    self.drawSquare(dc, j * self.squareWidth(),i * self.squareHeight(),self.board[j + i * self.BoardHeight])

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            self.pause()
            return
        if self.isPaused:
            return
        elif keycode == wx.WXK_LEFT or keycode == ord('A') or keycode == ord('a'):  # 左移
            self.direct = 3
        elif keycode == wx.WXK_RIGHT or keycode == ord('D') or keycode == ord('d'):  # 右移
            self.direct = 1
        elif keycode == wx.WXK_UP or keycode == ord('W') or keycode == ord('w'):  # 上
            self.direct = 0
        elif keycode == wx.WXK_DOWN or keycode == ord('S') or keycode == ord('s'):  # 下
            self.direct = 2
        elif keycode == ord('Q') or keycode == ord('q'):
            self.pause()
            if wx.MessageBox("确定退出吗？\n当前分数为："+str(self.sorce), "退出", wx.ICON_QUESTION | wx.YES_NO, self) == wx.YES:
                sys.exit()
            else:
                event.Skip()
        else:
            event.Skip()


    def OnTimer(self, event):
        if event.GetId() == Board.ID_TIMER:
            statusbar = self.GetParent().statusbar

            self.flag = self.flag+1
            if not self.tryMove():
                self.timer.Stop()
                self.isStarted = False
                statusbar.SetStatusText('Game over', 2)
        else:
            event.Skip()

    def newPos(self):
        tmp = self.generateblock()
        x = int(random.random()*6) + 3
        self.board[tmp] = x
        
        self.Refresh()

    def tryMove(self):
        print(self.way)
        statusbar = self.GetParent().statusbar
        if self.direct == 0:#向上
            if self.board[self.way[len(self.way) - 2]+Board.BoardWidth*(self.way[len(self.way) - 1]-1)] == 2:
                # 最新的节点的上面一个节点是蛇的身体，死掉了
                return False
            else:
                self.way.append(self.way[len(self.way) - 2])# 横坐标相同，扩展
                if self.way[len(self.way) - 2] == 0: #纵坐标，如果向上越界，返回最底部，否则向上移动一个
                    self.way.append(Board.BoardWidth - 1)
                else:
                    self.way.append(self.way[len(self.way) - 2] - 1)

        elif self.direct == 1:#右
                if self.board[self.way[len(self.way) - 2]+1+Board.BoardWidth*(self.way[len(self.way) - 1])] == 2:
                    return False
                else:
                    if self.way[len(self.way) - 2] == Board.BoardWidth - 1:
                        self.way.append(0)
                    else:
                        self.way.append(self.way[len(self.way) - 2]+1)
                    self.way.append(self.way[len(self.way) - 2])
        elif self.direct == 2:#向下
            if self.board[self.way[len(self.way) - 2] + Board.BoardWidth * (self.way[len(self.way) - 1] + 1)] == 2:
                return False
            else:
                self.way.append(self.way[len(self.way) - 2])
                if self.way[len(self.way) - 2] == Board.BoardWidth - 1:#向下越界，返回最上面，否则向下移动
                    self.way.append(0)
                else:
                    self.way.append(self.way[len(self.way) - 2] + 1)
        elif self.direct == 3:#左
                if self.board[self.way[len(self.way) - 2]-1+Board.BoardWidth*(self.way[len(self.way) - 1])] == 2:
                    return False
                else:
                    if self.way[len(self.way) - 2] == 0:
                        self.way.append(Board.BoardWidth - 1)
                    else:
                        self.way.append(self.way[len(self.way) - 2] - 1)
                    self.way.append(self.way[len(self.way) - 2])
        length = len(self.way)

        if self.board[self.way[length-2]+self.way[length- 1]*Board.BoardWidth] != 0:
            self.board[self.way[length - 2] + self.way[length - 1] * Board.BoardWidth] == 2
            self.newPos()
            self.sorce = self.sorce + 1
        else:
            self.board[self.way[length - 2] + self.way[length - 1] * Board.BoardWidth] = 2
            self.board[self.way[0] + self.way[1] * Board.BoardWidth] = 0
            del self.way[0]
            del self.way[0]
        statusbar.SetStatusText('得分：'+str(self.sorce), 0)
        
        self.Refresh()
        
        return True

    def drawSquare(self, dc, x, y,id):

        dc.SetPen(wx.TRANSPARENT_PEN)
        if id < 3:
            dc.SetBrush(wx.Brush('BLUE'))
            dc.DrawRectangle(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2)
        else:
            dc.SetBrush(wx.Brush(self.colors[id - 3]))
            dc.DrawRectangle(x + 1, y + 1, self.squareWidth() - 2,
                             self.squareHeight() - 2)

if '__name__==__main__':
    app = wx.App()
    Snake(None, title=u'贪吃蛇')
    app.MainLoop()


"""
可以让蛇变成多种颜色，吃下食物反映在尾巴上而不是头部
"""