# import sys
# import matplotlib.pyplot as plt
# from PyQt5 import QtCore  # Import QtCore
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from PyQt5 import QtWidgets, uic
# import numpy as np
# import resources_rc

# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         uic.loadUi('interface.ui', self)

#         # Assuming you want to add the graph to the first page of the QStackedWidget
#         self.addGraphToPage(self.throttle_mapping, 0)

#         self.show()

#     def addGraphToPage(self, page, slider_id):
#         # Create a figure and add it to the canvas
#         fig = plt.figure()
#         self.canvas = FigureCanvas(fig)
#         page.layout().addWidget(self.canvas)

#         # Create the 3D plot
#         self.ax = fig.add_subplot(111, projection='3d')
#         self.ax.set_facecolor('#000000')  # Dark mode background color
#         fig.patch.set_facecolor('#000000') # Dark mode figure color

#         # Create a slider for adjusting the gradient
#         self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
#         self.slider.setMinimum(1)
#         self.slider.setMaximum(100)
#         self.slider.setValue(50)
#         self.slider.valueChanged.connect(self.updateGraph)
#         page.layout().addWidget(self.slider)

#         # Initial plot
#         self.updateGraph()

#     def updateGraph(self):
#         # Clear previous plot
#         self.ax.clear()

#         # Create a linear plane
#         x = np.linspace(-5, 5, 100)
#         y = np.linspace(-5, 5, 100)
#         x, y = np.meshgrid(x, y)
#         z = self.slider.value() / 50 * y  # Adjust the gradient based on the slider value

#         # Plot the surface
#         self.ax.plot_surface(x, y, z, cmap='viridis')

#         # Update the canvas
#         self.canvas.draw()

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec_())


import sys
from PyQt5 import QtWidgets, uic
import resources_rc  # Import the compiled resources

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('interface.ui', self)

        # Connect buttons to the function to change pages
        self.throttle_button.clicked.connect(lambda: self.changePage(0))  # THROTTLE RESPONSE
        self.launch_button.clicked.connect(lambda: self.changePage(1))  # LAUNCH CONTROL
        self.regen_button.clicked.connect(lambda: self.changePage(2))  # REGEN PROFILE
        self.energy_button.clicked.connect(lambda: self.changePage(3))    # ENERGY CONSUMPTION
        self.race_button.clicked.connect(lambda: self.changePage(4))  # RACE MODE PRESETS

        self.show()

    def changePage(self, page_index):
        self.stackedWidget.setCurrentIndex(page_index)
        
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
