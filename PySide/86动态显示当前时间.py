
'''
动态显示当前时间

QTimer
QThread
多线程:用于同时完成多个任务

'''



from PySide2.QtWidgets import QGridLayout, QLabel, QWidget,QPushButton,QApplication,QListWidget,\
    QGridLayout,QLabel
from PySide2.QtCore import QDateTime, QThread, QTimer 
import sys


class ShowTime(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("动态显示当前时间")

        self.lable=QLabel("显示当前时间")
        self.startBtn=QPushButton("开始")
        self.endBtn = QPushButton("结束")
        layout=QGridLayout()
        layout.addWidget(self.lable)
        layout.addWidget(self.startBtn)
        layout.addWidget(self.endBtn)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
    
    def showTime(self):
        time= QDateTime.currentDateTime()
        timeDisplay= time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.lable.setText(timeDisplay)

    def startTimer(self):
        self.timer.start(1000)
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)
    
    def endTimer(self):
        self.timer.stop()
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)


       







if __name__=='__main__':
    app=QApplication(sys.argv)
    demo =ShowTime()
    demo.show()
    sys.exit(app.exec_())
