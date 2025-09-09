
import numpy as np
from PyQt6.QtGui import QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtWidgets import QLabel
from components.focal_point import FocalPoint

# Main view area for perspective grid view
class Canvas(QLabel):
    def __init__(self):
        # Inherit everything from QLabel
        super().__init__()

        # Define the canvas
        self.canvas = QPixmap(600, 300)
        self.canvas.setDevicePixelRatio(self.devicePixelRatio())        # Use DPI system, need to look into this
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
        # Set the background of the canvas to completely white
        self.canvas.fill(Qt.GlobalColor.white) 

        # Initialise a new painter object
        painter = QPainter(self.canvas)

        # Antialiasing settings
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)              # What exactly does this one do again??                                          
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.LosslessImageRendering, True)             # What exactly does this one do again??

        # Pen settings
        pen = QPen(Qt.GlobalColor.black, 1.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCosmetic(True) #??

        painter.setPen(pen)
        painter.setBrush(Qt.GlobalColor.black)          
        
        # Should move these into canvas initialisation?
        focal_point_radius = 5.0
        f_p_line_length = 100.0
        theta_vals = np.linspace(0, 2*np.pi, 9)[:-1]
        x = f_p_line_length * np.cos(theta_vals)
        y = f_p_line_length * np.sin(theta_vals)

        for point in self.focal_points:

            # Use floats
            center_x = float(point.position_x)
            center_y = float(point.position_y)
            point_position = QPointF(center_x, center_y)

            # Draw with floating point precision
            painter.drawEllipse(point_position, focal_point_radius, focal_point_radius)
            
            for x_i, y_i in zip(x, y):
                start_point = QPointF(point.position_x, point.position_y)
                end_point = QPointF(point.position_x + x_i, point.position_y + y_i)
                painter.drawLine(start_point, end_point)

        painter.end()
        self.setPixmap(self.canvas)