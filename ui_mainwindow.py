
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from components.num_f_point_controls import NumFPointControl
from components.canvas import Canvas

# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set the title of the QMainWindow
        self.setWindowTitle("PA Pro")

        # Create a main widget
        central_widget = QWidget()

        # Create horizontal layout
        h_main_layout = QHBoxLayout()
        central_widget.setLayout(h_main_layout)

        # Create canvas widget
        self.canvas = Canvas()
        h_main_layout.addWidget(self.canvas)

        # Create control panel widget
        v_controls_layout = QVBoxLayout()                 # Vertical layout for control widget

        # Create a widget to control the number of focal points
        self.fp_control = NumFPointControl(self.canvas, self.canvas.num_f_points)
        v_controls_layout.addWidget(self.fp_control)
        v_controls_layout.addStretch()                           # What does this do again?
        h_main_layout.addLayout(v_controls_layout)               # Add controls widget to main horizontal layout

        self.setCentralWidget(central_widget)
        self.adjustSize()
        self.setFixedSize(self.size())