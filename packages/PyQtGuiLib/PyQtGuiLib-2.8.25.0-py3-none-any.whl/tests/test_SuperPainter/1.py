import sys
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Lines')

        self.show()


    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()


    def drawLines(self, qp):

        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        points = [QPoint(20, 40), QPoint(250, 40), QPoint(250, 80), QPoint(20, 80)]
        qp.drawLines(points)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
