import sys
from PyQt5.QtCore import QCoreApplication

app = QCoreApplication(sys.argv)

# Add the path to the Qt plugins directory that contains multimedia plugins
QCoreApplication.addLibraryPath("/usr/lib/x86_64-linux-gnu/qt5/plugins")