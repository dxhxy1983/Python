'''
使用线程类(QThread)编写计数器

QThread

def run(self):
    while True:
        self.sleep(1)
        if sec == 5:
            break;

QLCDNumber 

用到自定义信号

'''

import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

# from PyQt5.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *

sec= 0
class WorkThread(QThread):
    timer=Signal()  #每隔1秒发送一次信号
    end= Signal()   #计数完成后发送一次信号
    def run(self):
        while True:
            self.sleep(1) #休眠1秒
            if sec==5:
                self.end.emit()         #发送end信号
                break
            self.timer.emit()  #发送timer信号
class Counter(QWidget):
    def __init__(self, parent=None):
        super(Counter,self).__init__(parent)
        self.setWindowTitle("使用线程类(QThread)编写计数器")
        self.resize(300,120)

        layout =QVBoxLayout()
        self.lcdNumber=QLCDNumber()
        layout.addWidget(self.lcdNumber)
        button=QPushButton("开始计数")
        layout.addWidget(button)

        self.workThead=WorkThread()

        self.workThead.timer.connect(self.countTime)
        self.workThead.end.connect(self.end)
        button.clicked.connect(self.work)
        
        self.setLayout(layout)

    def countTime(self):
        global sec
        sec+=1
        self.lcdNumber.display(sec)

    def end(self):
        QMessageBox.information(self,"消息","计数结束",QMessageBox.Ok)

    def work(self):
        self.workThead.start()



if __name__=='__main__':
    app=QApplication(sys.argv)
    demo =Counter()
    demo.show()
    sys.exit(app.exec_())
