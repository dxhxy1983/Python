'''
让程序定时关闭

QTimer,singleShot
'''


import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


if __name__=='__main__':
    app=QApplication(sys.argv)
    label=QLabel('<font color=red size=140> <b>Hello World,窗口在5秒后自动关闭!</b> </font>')
    label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    label.show()
    QTimer.singleShot(1000,app.quit)


    sys.exit(app.exec_())
