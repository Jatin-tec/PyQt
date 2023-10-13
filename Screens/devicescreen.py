from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class DevicesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel("Devices"))
        
        self.setLayout(self.main_layout)
