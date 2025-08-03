import sys

from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        canvas = QPixmap(600, 300)
        canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(canvas)
        self.setMouseTracking(True)

        self.mouse_x, self.mouse_y = 0, 0

    def mouseMoveEvent(self, ev):
        pos_x, pos_y = ev.pos().x(), ev.pos().y()
        self.mouse_x, self.mouse_y = pos_x, pos_y
        

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            # print(f"Mouse Position: {self.mouse_x}, {self.mouse_y}")
            
            canvas = self.pixmap()
            painter = QPainter(canvas)
            pen = painter.pen()
            pen.setWidth(10)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(pen)
            painter.drawPoint(int(self.mouse_x), int(self.mouse_y))
            painter.end()
            self.setPixmap(canvas)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PA Pro")

        self.canvas = Canvas()

        self.setCentralWidget(self.canvas)
        self.adjustSize()
        self.setFixedSize(self.size())

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
