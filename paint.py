import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import requests
import json

class Demo(QWidget):
    width = 600
    height = 600
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(self.width, self.height)
        self.move(300, 300)
        self.setWindowTitle('paint')
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        self.drawGrid(qp, 50, 25)
        qp.end()

    def drawGrid(self, qp, row, col):
        step = max(self.width, self.height) // max(row, col)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(0, row+1):
            qp.drawLine(0, i*step, col*step, i*step)
        for j in range(0, col+1):
            qp.drawLine(j*step, 0, j*step, row*step)

    def drawRectangles(self, qp):
        #col = QColor(0, 0, 0)
        #col.setNamedColor('#d4d4d4')
        #qp.setPen(col)

        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QColor(255, 80, 0, 160))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QColor(25, 0, 90, 200))
        qp.drawRect(250, 15, 90, 60)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Demo()
    sys.exit(app.exec_())
