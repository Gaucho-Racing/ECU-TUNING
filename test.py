import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, 
                             QGridLayout, QPushButton, QComboBox, QLabel)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'ECU Tuning Application'
        self.width = 1000
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QGridLayout(main_widget)

        # Dropdown menu for presets
        self.presetComboBox = QComboBox(self)
        self.presetComboBox.addItem("Preset 1")
        self.presetComboBox.addItem("Preset 2")
        self.presetComboBox.addItem("Preset 3")
        layout.addWidget(self.presetComboBox, 0, 0, 1, 2)

        # Space for logo
        self.logoLabel = QLabel(self)
        self.logoLabel.setText("Your Logo Here")
        self.logoLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.logoLabel, 0, 2, 1, 2)

        # 2D plot setup with dark theme
        self.figure_2d, self.ax_2d = plt.subplots()
        self.figure_2d.patch.set_facecolor('black')
        self.ax_2d.set_facecolor('black')
        self.ax_2d.tick_params(axis='x', colors='white')
        self.ax_2d.tick_params(axis='y', colors='white')
        self.ax_2d.spines['bottom'].set_color('white')
        self.ax_2d.spines['top'].set_color('white')
        self.ax_2d.spines['right'].set_color('white')
        self.ax_2d.spines['left'].set_color('white')
        self.canvas_2d = FigureCanvas(self.figure_2d)
        layout.addWidget(self.canvas_2d, 1, 0, 1, 2)
        self.slider_2d = QSlider(Qt.Horizontal)
        self.slider_2d.valueChanged[int].connect(self.updateGraph2D)
        layout.addWidget(self.slider_2d, 2, 0, 1, 2)
        self.x_2d = np.linspace(0, 2 * np.pi, 100)
        self.y_2d = np.sin(self.x_2d)
        self.plot_2d, = self.ax_2d.plot(self.x_2d, self.y_2d, color='white')

        # 3D plot setup with dark theme
        self.figure_3d = plt.figure()
        self.ax_3d = self.figure_3d.add_subplot(111, projection='3d')
        self.canvas_3d = FigureCanvas(self.figure_3d)
        layout.addWidget(self.canvas_3d, 1, 2, 1, 2)
        self.slider_3d = QSlider(Qt.Horizontal)
        self.slider_3d.valueChanged[int].connect(self.updateGraph3D)
        layout.addWidget(self.slider_3d, 2, 2, 1, 2)
        self.X_3d, self.Y_3d = np.meshgrid(np.arange(-5, 5, 0.25), np.arange(-5, 5, 0.25))
        self.Z_3d = np.sin(np.sqrt(self.X_3d**2 + self.Y_3d**2))
        self.surf_3d = self.ax_3d.plot_surface(self.X_3d, self.Y_3d, self.Z_3d, cmap=cm.coolwarm)
        self.set3DDarkTheme()

        # Save Tune button
        self.saveButton = QPushButton('Save Tune', self)
        layout.addWidget(self.saveButton, 3, 3, 1, 1)
        self.saveButton.clicked.connect(self.saveTune)

    def set3DDarkTheme(self):
        self.ax_3d.set_facecolor('black')
        self.ax_3d.w_xaxis.pane.fill = False
        self.ax_3d.w_yaxis.pane.fill = False
        self.ax_3d.w_zaxis.pane.fill = False
        self.ax_3d.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax_3d.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax_3d.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        self.ax_3d.tick_params(colors='white', labelsize=8)

    def updateGraph2D(self, value):
        self.y_2d = np.sin(self.x_2d + value / 10)
        self.plot_2d.set_ydata(self.y_2d)
        self.ax_2d.relim()
        self.ax_2d.autoscale_view()
        self.canvas_2d.draw()

    def updateGraph3D(self, value):
        self.Z_3d = np.sin(np.sqrt(self.X_3d**2 + self.Y_3d**2) + value / 10)
        self.ax_3d.clear()
        self.surf_3d = self.ax_3d.plot_surface(self.X_3d, self.Y_3d, self.Z_3d, cmap=cm.coolwarm)
        self.set3DDarkTheme()  # Apply the dark theme settings after clearing the axes
        self.canvas_3d.draw()

    def saveTune(self):
        print("Save Tune logic goes here")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
