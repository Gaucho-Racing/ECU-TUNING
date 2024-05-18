import sys
import numpy as np
from PyQt5 import QtWidgets, uic, QtCore
import resources_rc  # Import the compiled resources
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QtWidgets.QMainWindow):
    
    # store presets of k, p, and b for each preset:
    presets = {
        "LINEAR": [0, 0, 0],
        "MAP_1": [0, 0, 0],
        "MAP_2": [0, 0, 0],
        "MAP_3": [0, 0, 0]
    }
    
    torque_data = np.zeros((20, 40))

    
    
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('interface.ui', self)
        self.setWindowTitle("GR24 PERFORMANCE TUNING")

        self.is_loading_preset = False  # Add a flag to indicate when loading a preset

        # Connect buttons to the function to change pages
        self.throttle_button.clicked.connect(lambda: self.changePage(0))  # THROTTLE RESPONSE
        self.launch_button.clicked.connect(lambda: self.changePage(1))  # LAUNCH CONTROL
        self.regen_button.clicked.connect(lambda: self.changePage(2))  # REGEN PROFILE
        self.energy_button.clicked.connect(lambda: self.changePage(3))    # ENERGY CONSUMPTION
        self.race_button.clicked.connect(lambda: self.changePage(4))  # RACE MODE PRESETS
        self.flash_button.clicked.connect(self.updateSDCard) # update firmware to SD
        
        
        # presets 1 - 4 
        self.updateTorqueSettings = self.createTQSettingsSelect()
        self.linear.layout().addWidget(self.updateTorqueSettings)

        # Create the 2D fuel table chart
        self.fuel_table_fig, self.fuel_table_ax = self.createFuelTable()
        self.canvas_fuel_table = FigureCanvas(self.fuel_table_fig)
        self.rpm.layout().addWidget(self.canvas_fuel_table)  # Add to layout before the 3D graph
        
        

        self.rpm_fig, self.rpm_ax = self.createTorqueProfile()
        self.canvas_rpm = FigureCanvas(self.rpm_fig)
        self.rpm.layout().addWidget(self.canvas_rpm)
        
        self.slider_multiplier, self.slide_k = self.createSlider("Multiplier [k]", 0, 50)
        self.settings.layout().addWidget(self.slider_multiplier)
        self.slide_k.valueChanged.connect(self.updateTorqueProfile)
        self.slide_k.valueChanged.connect(self.savePreset)

       
        self.slider_steepness, self.slide_p = self.createSlider("Steepness [p]", 0, 50)
        self.settings.layout().addWidget(self.slider_steepness)
        self.slide_p.valueChanged.connect(self.updateTorqueProfile)
        self.slide_p.valueChanged.connect(self.savePreset)

        self.slider_offset, self.slide_b = self.createSlider("Offset [b]", 0, 10)
        self.settings.layout().addWidget(self.slider_offset)
        self.slide_b.valueChanged.connect(self.updateTorqueProfile)
        self.slide_b.valueChanged.connect(self.savePreset)
        
        

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
            background: #9fff5e;  
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
        
    
    def createTQSettingsSelect(self):
        # Create a horizontal layout
        layout = QtWidgets.QHBoxLayout()

        # Create the combo box for selecting presets
        self.presetComboBox = QtWidgets.QComboBox()
        # Add some placeholder presets (these could be loaded from a file)
        self.presetComboBox.addItems(["LINEAR", "MAP_1", "MAP_2", "MAP_3"])
        
        # Connect the combo box's current index change signal to loadPreset
        self.presetComboBox.currentIndexChanged.connect(self.loadPreset)
        
        # # Create the save button
        # saveButton = QtWidgets.QPushButton("Save")
        
        # # Connect the save button to its respective slot
        # saveButton.clicked.connect(self.savePreset)
        
        # Add the combo box and save button to the layout
        layout.addWidget(self.presetComboBox)
        # layout.addWidget(saveButton)
        
        # Create a widget to set the layout on
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        
        return widget


    def updateTQSettingsSelect(self):
        currentPreset = self.presetComboBox.currentText()
        self.slide_k.setValue(self.presets[currentPreset][0])
        self.slide_p.setValue(self.presets[currentPreset][1])
        self.slide_b.setValue(self.presets[currentPreset][2])
        
        
    def loadPreset(self):
        self.is_loading_preset = True
        currentPreset = self.presetComboBox.currentText()
        print(f"Loading {currentPreset}")
        self.updateTQSettingsSelect()  # Update the presets list after loading
        self.is_loading_preset = False


    def savePreset(self):
        if(self.is_loading_preset): 
            return
        print("Saving current settings as a new preset")
        currentPreset = self.presetComboBox.currentText()
        self.presets[currentPreset] = [self.slide_k.value(), self.slide_p.value(), self.slide_b.value()]
    
    def createFuelTable(self):
        fig = Figure(facecolor='black')
        ax = fig.add_subplot(111, facecolor='black')

        cax = ax.matshow(self.torque_data, cmap='hot')
        fig.colorbar(cax)

        ax.set_title("LOAD [AMPERES]", color='white')
        ax.set_xlabel("MOTOR RPM", color='white')
        ax.set_ylabel("REQ TORQUE", color='white')


        return fig, ax
    
    def createTorqueProfile(self):
        fig = Figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#000000')  # Dark mode background color
        fig.patch.set_facecolor('#000000') # Dark mode figure color
        
        # Set fixed limits for the axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 5500)
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
        y = np.linspace(0, 5500, 100)
        x, y = np.meshgrid(x, y)
        b = self.slide_b.value()/10.0
        p = self.slide_p.value()/10.0
        k = self.slide_k.value()/10.0
        
        z = np.clip((x - (1-x)*(x + b)*((y/5500.0)**p)*k )*100, 0, 100)

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
        
        
        for i in range(20):
            for j in range(40):
                rpm = 5500 * j / 40
                throttle = 1 * i / 20
                self.torque_data[i][j] = np.clip((throttle - (1-throttle)*(throttle + b)*((rpm/5500.0)**p)*k )*100, 0, 100)
        
        
        self.fuel_table_ax.clear()
        self.fuel_table_ax.set_title("LOAD [AMPERES]", color='white')
        self.fuel_table_ax.set_xlabel("RPM", color='white')
        self.fuel_table_ax.set_ylabel("REQ TORQUE", color='white')
        self.fuel_table_ax.matshow(self.torque_data, cmap='hot', origin='upper')
        self.canvas_fuel_table.draw()
        
        



    def updateSDCard(self):
        # TODO: NOTE THAT THE VALUES MUST BE SCALED DOWN BY 10 ex: 0 - 50 -> 0 - 5.0
        print(self.presets)
        K_L = self.presets["LINEAR"][0]   
        P_L = self.presets["LINEAR"][1] 
        B_L = self.presets["LINEAR"][2]
        K_M1 = self.presets["MAP_1"][0]
        P_M1 = self.presets["MAP_1"][1]
        B_M1 = self.presets["MAP_1"][2]
        K_M2 = self.presets["MAP_2"][0]
        P_M2 = self.presets["MAP_2"][1]
        B_M2 = self.presets["MAP_2"][2]
        K_M3 = self.presets["MAP_3"][0]
        P_M3 = self.presets["MAP_3"][1]
        B_M3 = self.presets["MAP_3"][2]
        
        # write to the SD card
        # 1. open the file
        '''
        K1 P1 B1
        K2 P2 B2
        K3 P3 B3
        K4 P4 B4
        CMAX1 
        CMAX2
        CMAX3
        CMAX4
        REGEN1
        REGEN2
        REGEN3
        REGEN4
        TCPARAMS1 TCPARAMS2 TCPARAMS3
        '''
        torque_profile = f"{K_L/10.0} {P_L/10.0} {B_L/10.0}\n{K_M1/10.0} {P_M1/10.0} {B_M1/10.0}\n{K_M2/10.0} {P_M2/10.0} {B_M2/10.0}\n{K_M3/10.0} {P_M3/10.0} {B_M3/10.0}\n"            
        print(torque_profile)
        
        # 2. write the values
        # 3. close the file
        print("done")
        
        
        # in regen, make sure that the rear wheels lock after the front
        
    
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    # print the presets
  
    

