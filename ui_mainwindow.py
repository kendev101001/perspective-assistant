
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from components.num_f_point_controls import NumFPointControl
from components.canvas import Canvas

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