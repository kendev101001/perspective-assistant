
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider

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
