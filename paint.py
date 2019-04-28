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
    step = 4
    ip = '127.0.0.1'
    port = 9001
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mask = np.zeros((self.row, self.col))
        self.isErase = False

    def initUI(self):
        self.bd_w, self.bd_h = self.step*self.col, self.step*self.row
        self.bd = QPixmap(QSize(self.bd_w, self.bd_h))
        self.bd.fill(Qt.white)

        self.qp = QPainter()

        lbBarcode = QLabel('BarCode:', self)
        lbBarcode.setGeometry(self.bd_w + 20, 20, 80, 25)

        self.txtBarcode = QLineEdit(self)
        self.txtBarcode.setGeometry(self.bd_w + 70 + 20, 20, 100, 25)

        self.cbErase = QCheckBox('Erase', self)
        self.cbErase.setGeometry(self.bd_w + 20, 55 + 20, 70, 25)
        self.cbErase.stateChanged.connect(self.setErase)

        self.btnClear = QPushButton('Clear', self)
        self.btnClear.setGeometry(self.bd_w + 20 + 70, 55 + 20, 50, 25)
        self.btnClear.clicked.connect(self.clear)

        self.btnScan = QPushButton('Scan', self)
        self.btnScan.setGeometry(self.bd_w + 20, 55 + 55 + 20, 50, 25)
        self.btnScan.clicked.connect(self.scan)

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

    def maskToStr(self):
        return ' '.join(map(str, map(int, self.mask.flatten())))

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

    def mouseMoveEvent (self,e):
        if self.isDraw:
            self.fillRect(e.x(), e.y())

    def drawGrid(self):
        pen = QPen(Qt.gray, 1, Qt.SolidLine)
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
        if self.isErase:
            if self.mask[r][c] == 1:
                self.mask[r][c] = 0
                self.qp.begin(self.bd)
                self.qp.setBrush(QColor(255, 255, 255))
                self.qp.drawRect(c * self.step, r * self.step, self.step, self.step)
                self.qp.end()
                self.update()
        else:
            if self.mask[r][c] == 0:
                self.mask[r][c] = 1
                self.qp.begin(self.bd)
                self.qp.setBrush(QColor(128, 128, 128))
                self.qp.drawRect(c * self.step, r * self.step, self.step, self.step)
                self.qp.end()
                self.update()
    
    def setErase(self, state):
        if state == Qt.Checked:
            self.isErase = True
        else:
            self.isErase = False

    def clear(self):
        self.mask = np.zeros((self.row, self.col))
        self.qp.begin(self.bd)
        self.bd.fill(Qt.white)
        self.qp.end()
        self.update()


    def scan(self):
        #self.printMask()
        #print(f'{self.maskToStr()}')
        data = {"authcode":"2",
                "GlassInfo": [
                    { 
                        "Index": 0, 
                        "ObjLens": 20, 
                        "eSCANType": "CV", 
                        "Barcode": f"{self.txtBarcode.text()}", 
                        "RangeInfo": [{ 
                            "Index": 0, 
                            "RngType": "NM", 
                            "RngX": 0, 
                            "RngY": 0, 
                            "RngW": 0, 
                            "RngH": 0, 
                            "FocusScanType": 2, 
                            "GridXCnt": 1, 
                            "GridYCnt": 1, 
                            "Reserve": 0 
                            }],
                        "Mask":{"Row": 75, "Col": 25, "Data": f"{self.maskToStr()}"}
                        }
                    ]}
        try:
            resp = requests.post(f'http://{self.ip}:{self.port}/scan', data=json.dumps(data))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = Demo()
    sys.exit(app.exec_())
