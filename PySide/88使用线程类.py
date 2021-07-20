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

sec= 0
class WorkThread(QThread):
    timer=pyqtSignal()
    
class Counter(QWidget):
    def __init__(self, parent=None):
        super(Counter,self).__init__(parent)
        self.setWindowTitle("使用线程类(QThread)编写计数器")
        self.resize(300,120)




if __name__=='__main__':
    app=QApplication(sys.argv)
    demo =Counter()
    demo.show()
    sys.exit(app.exec_())
