
import sys
from PyQt6.QtWidgets import QApplication
from . import pyCLAMP

# Create the application
app = QApplication(sys.argv)
# app.setStyle('Fusion')

# Create the UI widget
ui = pyCLAMP.newPyClampWindow()

# Show UI widget and run application
ui.show()
ui.updateUI()

# Run the application
status = app.exec()
sys.exit(status)