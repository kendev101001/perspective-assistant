import sys

from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QLabel, 
    QWidget, 
    QHBoxLayout,
    QSlider,
    QVBoxLayout
)
import numpy as np


# Main view area for perspective grid view
class Canvas(QLabel):
    def __init__(self):
        # Inherit everything from QLabel
        super().__init__()

        # Define the canvas
        self.canvas = QPixmap(600, 300)
        self.canvas.fill(Qt.GlobalColor.white)                        
        self.setPixmap(self.canvas)                                   
        self.setMouseTracking(True)                

        self.num_f_points = 1
        self.points_placed = 0
        self.mouse_x, self.mouse_y = 0, 0                          
        self.focal_points = []

    # Update the "global"(? at class level) mouse position
    # With current mouse position
    def mouseMoveEvent(self, ev):
        pos_x, pos_y = ev.pos().x(), ev.pos().y()
        self.mouse_x, self.mouse_y = pos_x, pos_y

    # Place a focal point
    def plotPoint(self):
        mouse_x, mouse_y = (self.mouse_x), int(self.mouse_y)
        focal_point = FocalPoint(len(self.focal_points))
        focal_point.setPosition(mouse_x, mouse_y)
        self.focal_points.append(focal_point)
        self.redrawCanvas()


    def draw_lines(self):
        pass

    # Register Mouse Clicks
    def mousePressEvent(self, ev):

        # When left button is clicked
        if ev.button() == Qt.MouseButton.LeftButton and self.points_placed < self.num_f_points:
            # print(f"Mouse Position: {self.mouse_x}, {self.mouse_y}")
            
            # Plot a point at that position
            self.plotPoint()
            self.points_placed += 1

    def removeExcessPoints(self):
        # While loop over if statement
        # Handles cases where slider moves to quickly/misses updates
        # More robust
        while len(self.focal_points) > self.num_f_points:
            self.focal_points.pop()
            self.points_placed = max(0, self.points_placed - 1)
        self.redrawCanvas()

    def redrawCanvas(self):
        self.canvas.fill(Qt.GlobalColor.white) 

        painter = QPainter(self.canvas)
        pen = QPen(Qt.GlobalColor.black, 1)

        painter.setPen(pen)
        painter.setBrush(Qt.GlobalColor.black)                                               
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)     
        
        # Should move these into canvas initialisation?
        focal_point_radius = 1
        f_p_line_length = 100
        theta_vals = np.linspace(0, 2*np.pi, 9)[:-1]
        x = f_p_line_length * np.cos(theta_vals)
        y = f_p_line_length * np.sin(theta_vals)

        for point in self.focal_points:
            painter.drawEllipse(point.position_x - focal_point_radius,
                                point.position_y - focal_point_radius,
                                2 * focal_point_radius,
                                2 * focal_point_radius)
            
            for x_i, y_i in zip(x, y):
                start_point = QPointF(point.position_x, point.position_y)
                end_point = QPointF(point.position_x + x_i, point.position_y + y_i)
                painter.drawLine(start_point, end_point)

        painter.end()
        self.setPixmap(self.canvas)


class FocalPoint():
    def __init__(self, focal_point_index):
        self.focal_point_index = focal_point_index
        self.position_x, self.position_y = 0, 0

    def setPosition(self, position_x, position_y):
        self.position_x, self.position_y = position_x, position_y


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
        self.canvas.removeExcessPoints()
        self.f_point_label.setText(f"Num F-Points: {value}")


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
