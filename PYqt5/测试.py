# from sys import argv
# from PySide2.QtWidgets import QApplication
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtCore import QFile


# class States:
#     def __init__(self) -> None:
#         qfile_state=QFile("mugong.ui")
#         qfile_state.open(QFile.ReadOnly)
        

#         self.ui=QUiLoader().load(qfile_state)

#         # qfile_state.close()

# app = QApplication(argv)
# widget = States()
# # widget.resize(360, 360)
# # widget.setWindowTitle("hello, pyqt5")
# widget.show()
# sys.exit(app.exec())


# from PySide2.QtWidgets import QApplication, QMessageBox
# from PySide2.QtUiTools import QUiLoader

# class Stats:

#     def __init__(self):
#         # 从文件中加载UI定义

#         # 从 UI 定义中动态 创建一个相应的窗口对象
#         # 注意：里面的控件对象也成为窗口对象的属性了
#         # 比如 self.ui.button , self.ui.textEdit
#         self.ui = QUiLoader().load('mugong.ui')

#         # self.ui.button.clicked.connect(self.handleCalc)

#     def handleCalc(self):
#         pass

# app = QApplication([])
# stats = Stats()
# stats.ui.show()
# app.exec_()

from PySide2.QtWidgets import QApplication,QMainWindow
from mugong import Ui_ClickandComfort

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_ClickandComfort()
        # 初始化界面
        self.ui.setupUi(self)

      
        self.ui.pushButton_1.clicked.connect(self.btn1_clicked)


    def btn1_clicked(self):
        print("yes")

app = QApplication([])
mainw = MainWindow()
mainw.show()
app.exec_()







# import PyQt5.uic
# from PyQt5 import QtCore, QtGui
 
# MainWindowForm, MainWindowBase = PyQt5.uic.loadUiType('mugong.ui')
 
# class MainWindow(MainWindowBase, MainWindowForm):
#  def __init__(self, parent = None):
#   super(MainWindow, self).__init__(parent)
 
#   # setup the ui
#   self.setupUi(self)
 
# if ( __name__ == '__main__' ):
#  app = None
#  if ( not app ):
#   app = QtGui.QApplication([])
 
#  window = MainWindow()
#  window.show()
 
#  if ( app ):
#   app.exec_()









# -*- coding: utf-8 -*-
# Author：Jack LEE 
# FileName:UIloader
# CreatedDate: 2020/9/17

# import sys
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtWidgets import QApplication
# from PySide2.QtCore import QFile


# # 定义触发函数
# # def sayHello():
# #     window.textEdit.setText("hello world!")
# #     print("Button click!")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ui_file = QFile("ui/mugong.ui")
#     ui_file.open(QFile.ReadOnly)
#     loader = QUiLoader()
#     window = loader.load(ui_file)
#     ui_file.close()
#     # 在这里加入信号触发、空间位置控制等代码
#     window.pushButton.clicked.connect(sayHello)
#     # 添加结束
#     window.show()
#     sys.exit(app.exec_())