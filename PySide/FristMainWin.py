import sys
from PySide2.QtWidgets import QApplication,QMainWindow

class FristMainWin(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("这是第一个窗口")
        self.resize(400,300)
        self.status=self.statusBar()
        self.status.showMessage("这是一个存在5秒的消息",5000)

if __name__=="__main__":
    app=QApplication(sys.argv)

    main=FristMainWin()
    main.show()
    sys.exit(app.exec_())