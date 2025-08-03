import sys

from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QLabel, 
    QWidget, 
    QHBoxLayout,
    QSlider,
    QVBoxLayout
)


# Main view area for perspective grid view
class Canvas(QLabel):
    def __init__(self):
        # Inherit everything from QLabel
        super().__init__()

        # Define the canvas
        canvas = QPixmap(600, 300)
        canvas.fill(Qt.GlobalColor.white)                           # Set canvas background colour to white
        self.setPixmap(canvas)                                      # Set the pixmap of the QLabel as the created Pixmap canvas
        self.setMouseTracking(True)                                 # Mouse position is always registerd whether clicking or not

        self.num_f_points = 1
        self.points_placed = 0
        self.mouse_x, self.mouse_y = 0, 0                           # Initialise mouse position

    # Update the "global"(? at class level) mouse position
    # With current mouse position
    def mouseMoveEvent(self, ev):
        pos_x, pos_y = ev.pos().x(), ev.pos().y()
        self.mouse_x, self.mouse_y = pos_x, pos_y

    # Place a focal point
    def plotPoint(self):
        canvas = self.pixmap()
        painter = QPainter(canvas)
        pen = painter.pen()
        pen.setWidth(5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)                    # Circular points
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)     # Antialiasing
        painter.setPen(pen)
        painter.drawPoint(int(self.mouse_x), int(self.mouse_y))
        painter.end()
        self.setPixmap(canvas)

    # Register Mouse Clicks
    def mousePressEvent(self, ev):

        # When left button is clicked
        if ev.button() == Qt.MouseButton.LeftButton and self.points_placed < self.num_f_points:
            print(f"Mouse Position: {self.mouse_x}, {self.mouse_y}")
            
            # Plot a point at that position
            self.plotPoint()
            self.points_placed += 1


class NumFPointControl(QWidget):
    def __init__(self, canvas, num_f_points):
        super().__init__()
        self.canvas = canvas
        self.num_f_points = num_f_points
        
        # Create window widget
        self.setLayout(QHBoxLayout())

        self.f_point_label = QLabel(f"Num F-Points: {self.num_f_points}")
        self.layout().addWidget(self.f_point_label)

        self.fp_slide = QSlider(Qt.Orientation.Horizontal)
        self.fp_slide.setMinimum(1)
        self.fp_slide.setMaximum(6)
        self.fp_slide.setValue(self.num_f_points)
        self.fp_slide.valueChanged.connect(self.updateNumFPoints)
        self.layout().addWidget(self.fp_slide)
    
    def updateNumFPoints(self, value):
        self.canvas.num_f_points = value
        self.f_point_label.setText(f"Num F-Points: {value}")
        print(f"Updated num_f_points to: {value}")


# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PA Pro")

        # Main widget, layout and canvas
        self.canvas = Canvas()
        window = QWidget()
        h_main_layout = QHBoxLayout()
        window.setLayout(h_main_layout)
        h_main_layout.addWidget(self.canvas)

        # Control panel
        controls = QWidget()
        v_controls_layout = QVBoxLayout()
        controls.setLayout(v_controls_layout)

        self.fp_control = NumFPointControl(self.canvas, self.canvas.num_f_points)
        
        v_controls_layout.addWidget(self.fp_control)
        v_controls_layout.addStretch()
        h_main_layout.addWidget(controls)

        self.setCentralWidget(window)
        self.adjustSize()
        self.setFixedSize(self.size())


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
