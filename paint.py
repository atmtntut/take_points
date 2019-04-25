import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import numpy as np
import json

class Demo(QWidget):
    width = 600
    height = 600
    row, col = 75, 25
    step = 10
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mask = np.zeros((self.row, self.col))

    def initUI(self):
        self.bd_w, self.bd_h = self.step*self.col, self.step*self.row
        self.bd = QPixmap(QSize(self.bd_w, self.bd_h))
        self.bd.fill(Qt.white)

        self.qp = QPainter()

        self.resize(self.bd_w + 200, self.bd_h)
        self.move(200, 200)
        self.setWindowTitle('paint')
        self.show()

    def printMask(self):
        for r in range(0, self.mask.shape[0]):
            print(f'{r}:', end=' ')
            for c in range(0, self.mask.shape[1]):
                print(f'{self.mask[r][c]}', end=' ')
            print('')

    def paintEvent(self, e):
        self.qp.begin(self)
        self.qp.drawPixmap(0, 0, self.bd)
        self.drawGrid()
        self.qp.end()

    def mousePressEvent (self, e):
        self.isDraw = True
        self.fillRect(e.x(), e.y())

    def mouseReleaseEvent (self,e):
        self.isDraw = False
        self.printMask()

    def mouseMoveEvent (self,e):
        if self.isDraw:
            self.fillRect(e.x(), e.y())

    def drawGrid(self):
        pen = QPen(Qt.blue, 1, Qt.SolidLine)
        self.qp.setPen(pen)
        for i in range(0, self.row+1):
            self.qp.drawLine(0, i*self.step, self.col*self.step, i*self.step)
        for j in range(0, self.col+1):
            self.qp.drawLine(j*self.step, 0, j*self.step, self.row*self.step)

    def fillRect(self, x, y):
        c = x // self.step
        r = y // self.step
        if c >= self.col or r >= self.row:
            return
        if self.mask[r][c] == 0:
            self.mask[r][c] = 1
            self.qp.begin(self.bd)
            self.qp.setBrush(QColor(128, 128, 128))
            self.qp.drawRect(c * self.step, r * self.step, self.step, self.step)
            self.qp.end()
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Demo()
    sys.exit(app.exec_())
