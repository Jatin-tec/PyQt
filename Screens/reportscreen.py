from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QRadioButton, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView
import uuid


class ReportsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(["", "Activity ID", "Type", "Activity", "Date", "Time", "Latitude", "Longitude", "Tags", "Device ID", "Media Gallery", ""])
        
         # Set columns to stretch and fill available space
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Resize first column to fit content
        header.setSectionResizeMode(11, QHeaderView.ResizeToContents)  # Resize last column to fit content
        for i in range(1, 11):
            header.setSectionResizeMode(i, QHeaderView.Stretch)  # Stretch other columns
        
        # Set table size policy to make it expand in both directions
        tableSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setSizePolicy(tableSizePolicy)

        layout.addWidget(self.table)

        # Adding sample data to the table (you can replace this with your actual data)
        for row in range(10):
            self.table.insertRow(row)
            radio_button = QRadioButton()
            self.table.setCellWidget(row, 0, radio_button)
            self.table.setItem(row, 1, QTableWidgetItem(str(uuid.uuid4())))
            self.table.setItem(row, 2, QTableWidgetItem("Type"))
            self.table.setItem(row, 3, QTableWidgetItem("Activity"))
            self.table.setItem(row, 4, QTableWidgetItem("DD/MM/YYYY"))
            self.table.setItem(row, 5, QTableWidgetItem("HH:MM"))
            self.table.setItem(row, 6, QTableWidgetItem("Latitude"))
            self.table.setItem(row, 7, QTableWidgetItem("Longitude"))
            self.table.setItem(row, 8, QTableWidgetItem("Tags"))
            self.table.setItem(row, 9, QTableWidgetItem("Device ID"))
            self.table.setItem(row, 10, QTableWidgetItem("Image Path"))

            download_button = QPushButton("Download")
            download_button.clicked.connect(lambda _, r=row: self.download_row(r))
            self.table.setCellWidget(row, 11, download_button)
                    
        self.setLayout(layout)

    def download_row(self, row):
        # Implement your download logic here, using row variable to identify the clicked row
        print(f"Downloading data from row {row}")
