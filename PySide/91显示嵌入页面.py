from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import *

import sys
import os

class InnerHTML(QMainWindow):
    def __init__(self):
        super(InnerHTML,self).__init__()
        self.setWindowTitle("显示嵌入web页面")
        self.setGeometry(5,30,1355,730)
              
        self.browser=QWebEngineView()
        self.browser.setHtml('''
                    <html>

            <head>
            这里是文档的头部 ... ...
            ...
            </head>

            <body>
            这里是文档的主体 ... ...
            ...
            </body>

            </html>

          '''
        )
        self.setCentralWidget(self.browser)
       
        



    

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=InnerHTML()
    win.show()
    sys.exit(app.exec_())
