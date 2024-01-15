import sys
import numpy as np
from PyQt5 import QtWidgets, uic, QtCore
import resources_rc  # Import the compiled resources
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('interface.ui', self)
        self.setWindowTitle("GR24 PERFORMANCE TUNING")

        # Connect buttons to the function to change pages
        self.throttle_button.clicked.connect(lambda: self.changePage(0))  # THROTTLE RESPONSE
        self.launch_button.clicked.connect(lambda: self.changePage(1))  # LAUNCH CONTROL
        self.regen_button.clicked.connect(lambda: self.changePage(2))  # REGEN PROFILE
        self.energy_button.clicked.connect(lambda: self.changePage(3))    # ENERGY CONSUMPTION
        self.race_button.clicked.connect(lambda: self.changePage(4))  # RACE MODE PRESETS

        self.linear_throttle_fig, self.linear_throttle_ax = self.createLinearThrottleMap()
        self.canvas_linear_throttle = FigureCanvas(self.linear_throttle_fig)
        self.linear.layout().addWidget(self.canvas_linear_throttle)
        self.slider_max_current, self.slide_current = self.createSlider("Max Current [Amps]", 0, 160)
        self.settings.layout().addWidget(self.slider_max_current)
        self.slide_current.valueChanged.connect(self.updateLinearThrottleMap)


        self.rpm_fig, self.rpm_ax = self.createTorqueProfile()
        self.canvas_rpm = FigureCanvas(self.rpm_fig)
        self.rpm.layout().addWidget(self.canvas_rpm)
        
        self.slider_multiplier, self.slide_k = self.createSlider("Multiplier [k]", 0, 50)
        self.settings.layout().addWidget(self.slider_multiplier)
        self.slide_k.valueChanged.connect(self.updateTorqueProfile)
        self.slider_steepness, self.slide_p = self.createSlider("Steepness [p]", 0, 50)
        self.settings.layout().addWidget(self.slider_steepness)
        self.slide_p.valueChanged.connect(self.updateTorqueProfile)
        self.slider_offset, self.slide_b = self.createSlider("Offset [b]", 0, 10)
        self.settings.layout().addWidget(self.slider_offset)
        self.slide_b.valueChanged.connect(self.updateTorqueProfile)
        
        

        self.show()
        
    def changePage(self, page_index):
        self.stackedWidget.setCurrentIndex(page_index)
    
    
    def createSlider(self, name, min, max):
        label = QtWidgets.QLabel(name)
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        # Customize slider appearance
        slider.setStyleSheet("""
        QSlider::groove:horizontal {
            border: 1px solid #ccc;
            background: black;
            height: 10px;
            border-radius: 5px;
        }
        QSlider::handle:horizontal {
            background: qradialgradient(
                cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                radius: 1.35, stop: 0 #fff, stop: 1 #777
            );
            width: 15px;
            margin-top: -2px;
            margin-bottom: -2px;
            border-radius: 7px;
        }
        QSlider::sub-page:horizontal {
            background: #ff0000;  
            border-radius: 5px;
        }
    """)

        slider.setMinimum(min)
        slider.setMaximum(max)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(slider)

        # Create a widget to hold the label and slider
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        return widget, slider
        
    
    def createLinearThrottleMap(self):
        fig = Figure(figsize=(6, 3))  # Adjust the figsize as needed
        ax = fig.add_subplot(111)
        ax.set_facecolor('#000000')
        fig.patch.set_facecolor('#000000')
        ax.tick_params(axis='x', colors='white', labelsize=8)  # Adjust labelsize as needed
        ax.tick_params(axis='y', colors='white', labelsize=8)  # Adjust labelsize as needed
        ax.set_xlim(0, 170)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Throttle Position", color='white', fontsize=8)  # Adjust fontsize as needed
        ax.xaxis.set_label_position('top')  # Move x-label to the top
        ax.set_xlabel("Current", color='red', fontsize=8, y=0.9)  # Adjust fontsize and y position as needed
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        return fig, ax


    def updateLinearThrottleMap(self):
        # Store the current axis limits
        xlim = self.linear_throttle_ax.get_xlim()
        ylim = self.linear_throttle_ax.get_ylim()
        
        x = np.linspace(0, 1)
        limit = self.slide_current.value()
        
        y = limit * x
        limit_line = np.ones(len(x)) * limit   
        
        # Update y based on the slider value, normalized to be between 0 and 1
        # Clear and update the plot
        self.linear_throttle_ax.clear()
        self.linear_throttle_ax.set_ylabel("Throttle Position", color='white', fontsize=8)  # Adjust fontsize as needed
        curr = "MAX CURRENT = " + str(limit) + "A"
        self.linear_throttle_ax.xaxis.set_label_position('top')  # Move x-label to the top
        if limit > 60:
            self.linear_throttle_ax.set_xlabel(curr, color='red', fontsize=8, y=0.9)  # Adjust fontsize and y position as needed
        else:
            self.linear_throttle_ax.set_xlabel(curr, color='white', fontsize=8, y=0.9)  # Adjust fontsize and y position as needed
        
        self.linear_throttle_ax.tick_params(axis='x', colors='white', labelsize=8)  # Adjust labelsize as needed
        self.linear_throttle_ax.tick_params(axis='y', colors='white', labelsize=8)  # Adjust labelsize as needed

        self.linear_throttle_ax.plot(y, x, color='white')
        self.linear_throttle_ax.plot(limit_line, x, color='red')
        # Reset the axis limits to their original values
        self.linear_throttle_ax.set_xlim(xlim)
        self.linear_throttle_ax.set_ylim(ylim)
        
        # Redraw the canvas
        self.canvas_linear_throttle.draw()  

    
    
    def createTorqueProfile(self):
        fig = Figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#000000')  # Dark mode background color
        fig.patch.set_facecolor('#000000') # Dark mode figure color
        
        # Set fixed limits for the axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 5000)
        ax.set_zlim(0, 100)
        
        # Add white axis labels
        ax.set_xlabel("THROTTLE", color='green')
        ax.set_ylabel("MOTOR RPM", color='cyan')
        ax.set_zlabel("% MAX CURRENT", color='red')
        
        # Change the color of the ticks to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.tick_params(axis='z', colors='white')

        # Set tick locations and labels
       
        return fig, ax
        
   
        
    def updateTorqueProfile(self):
        # Store the current axis limits
        xlim = self.rpm_ax.get_xlim()
        ylim = self.rpm_ax.get_ylim()
        zlim = self.rpm_ax.get_zlim()

        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 5000, 100)
        x, y = np.meshgrid(x, y)
        b = self.slide_b.value()/10.0
        p = self.slide_p.value()/10.0
        k = self.slide_k.value()/10.0
        
        z = np.clip((x - (1-x)*(x + b)*((y/5000.0)**p)*k )*100, 0, 100)

        # Clear and update the plot
        self.rpm_ax.clear()
        self.rpm_ax.plot_surface(x, y, z, cmap='viridis')
        

        # Reset the axis limits to their original values
        self.rpm_ax.set_xlim(xlim)
        self.rpm_ax.set_ylim(ylim)
        self.rpm_ax.set_zlim(zlim)
        self.rpm_ax.set_xlabel("THROTTLE", color='green')
        self.rpm_ax.set_ylabel("MOTOR RPM", color='cyan')
        self.rpm_ax.set_zlabel("% MAX CURRENT", color='red')

        # Redraw the canvas
        self.canvas_rpm.draw()

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

