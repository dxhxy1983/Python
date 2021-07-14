##############
#滚动条控件（QScrollBar)
#  
# QScrollBar的作用
# 1.通过滚动条值的变化,控制其他控件的状态变化
# 2.通过滚动条值的变化,控制控件位置的变化
# ##############*)


import sys



# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ScrollBar(QWidget):

    def __init__(self) :
        super(ScrollBar,self).__init__()
        self.initUI()
    
    def initUI(self):
        hbox =QHBoxLayout()
        self.lable=QLabel('拖动滚动条去改变文字颜色')
        hbox.addWidget(self.lable)

        self.scrollbar1=QScrollBar() 
        self.scrollbar1.setMaximum(255)
        self.scrollbar1.sliderMoved.connect(self.sliderMoved)
        # self.scrollbar1.SliderMove.connect(self.sliderMoved)
        # self.scrollbar1.sconnect(self.sliderMoved)
        # self.scrollbar1.SliderValueChange.connect(self.sliderMoved)
        # self.scrollbar1.move.connect(self.sliderMoved)


        self.scrollbar2=QScrollBar()
        self.scrollbar2.setMaximum(255)
        self.scrollbar2.sliderMoved.connect(self.sliderMoved)

        self.scrollbar3=QScrollBar()
        self.scrollbar3.setMaximum(255)
        self.scrollbar3.sliderMoved.connect(self.sliderMoved)

        hbox.addWidget(self.scrollbar1)
        hbox.addWidget(self.scrollbar2)
        hbox.addWidget(self.scrollbar3)

        self.setGeometry(300,300,300,200)

        self.setLayout(hbox)
    
    
    def sliderMoved(self):
        print(self.scrollbar1.value(),self.scrollbar2.value(),self.scrollbar1.value())
        palette=QPalette()
        c=QColor(self.scrollbar1.value(),self.scrollbar2.value(),self.scrollbar1.value(),255)
        palette.setColor(QPalette.Foreground,c)
        self.lable.setPalette(palette)
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    demo =ScrollBar()
    demo.show()
    sys.exit(app.exec_())
