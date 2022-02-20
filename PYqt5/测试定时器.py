from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject,QRect
import sys

class myobject(QDialog):
    def timerEvent(self, Event):
        print(Event,"1")

class LoginDlg(QDialog):
    def setui(self):
        self.setWindowTitle("这是一个定时器")
        self.resize(300,200)
        self.btn=QPushButton(self)
        self.btn.setText("anniu")
        self.btn.setGeometry(QRect(180,10,100,50))

        self.btn.clicked.connect(self.pause)

        self.obj= myobject(self)
        self.obj.startTimer(3000)
    def pause(self):
        self.obj.killTimer(self.id)
        print("yitingzhi")
if __name__=="__main__":
    app=QApplication(sys.argv)
    ui=LoginDlg()
    ui.setui()
    ui.show()
    sys.exit(app.exec_())