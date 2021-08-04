'''
PyQt5和JavaScript交互
什么叫交互:
PyQt5<--->Javascript

'''

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import *

import sys
import os

class PySideCallJS(QWidget):
    def __init__(self):
      super(PySideCallJS,self).__init__()
      self.initUI()
    def initUI(self):
      self.setWindowTitle("PyQt5调用Javascript")

      self.box=QVBoxLayout()
      self.browser=QWebEngineView()
      url=os.getcwd()+"\PySide\测试.html"
      self.browser.load(QUrl.fromLocalFile(url))
      self.box.addWidget(self.browser)   


      self.button=QPushButton("设置全名")
      self.button.clicked.connect(self.fullname)

      self.box.addWidget(self.button)

      self.setGeometry(5,30,1355,730)
      self.setLayout(self.box)


      

      # self.setCentralWidget(self.browser)
    def js_return(self,result):
      print(result)


      
    def fullname(self):
      self.value='hello world'
      self.browser.page().runJavaScript('fulln("'+self.value +'");')

       
  

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=PySideCallJS()
    win.show()
    sys.exit(app.exec_())
