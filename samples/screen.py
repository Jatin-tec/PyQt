import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QSplitter, QMainWindow, QHBoxLayout, QGridLayout, QComboBox

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout

class VideoGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        gridLayout = QGridLayout()

        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            database="your_database",
            user="your_user",
            password="your_password",
            host="your_host",
            port="your_port"
        )

        # Create a cursor object to execute queries
        cursor = conn.cursor()

        # Fetch data from the device table
        cursor.execute("SELECT * FROM device")
        devices = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Create video widgets and add them to the grid layout
        for i, device in enumerate(devices):
            name, rtsp_link, hls_link = device[1], device[2], device[3]
            nameLabel = QLabel(f"Name: {name}")
            rtspLabel = QLabel(f"RTSP Link: {rtsp_link}")
            hlsLabel = QLabel(f"HLS Link: {hls_link}")

            gridLayout.addWidget(nameLabel, i, 0)
            gridLayout.addWidget(rtspLabel, i, 1)
            gridLayout.addWidget(hlsLabel, i, 2)

        self.setLayout(gridLayout)

class NotificationBar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.notificationLayout = QVBoxLayout()
        self.setLayout(self.notificationLayout)

        # Fetch and display existing notifications from the activity table
        conn = psycopg2.connect(
            database="chokidar",
            user="admin",
            password="1234",
            host="localhost",
            port="5432"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activity")
        activities = cursor.fetchall()
        for activity in activities:
            self.addActivityNotification(activity[1])

        cursor.close()
        conn.close()

        # Connect to NATS for real-time updates
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connectToNats())

    async def connectToNats(self):
        nc = NATS()

        async def error_cb(e):
            print(f"Error: {e}")

        async def on_connect():
            print("Connected to NATS")

        async def on_disconnect():
            print("Disconnected from NATS")

        try:
            await nc.connect(
                servers=["nats://localhost:4222"],
                error_cb=error_cb,
                connect_cb=on_connect,
                disconnect_cb=on_disconnect,
            )
            await nc.subscribe("activities", cb=self.handleNatsMessage)

        except ErrConnectionClosed as e:
            print(f"Connection failed: {e}")

    async def handleNatsMessage(self, msg):
        activity = msg.data.decode()
        self.addActivityNotification(activity)

    def addActivityNotification(self, activity):
        label = QLabel(f"Activity: {activity}")
        self.notificationLayout.addWidget(label)

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.database_label = QLabel("Database Settings")
        layout.addWidget(self.database_label)

        self.database_name_input = QLineEdit()
        self.database_name_input.setPlaceholderText("Database Name")
        layout.addWidget(self.database_name_input)

        self.database_user_input = QLineEdit()
        self.database_user_input.setPlaceholderText("Database User")
        layout.addWidget(self.database_user_input)

        self.database_password_input = QLineEdit()
        self.database_password_input.setPlaceholderText("Database Password")
        self.database_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.database_password_input)

        self.database_host_input = QLineEdit()
        self.database_host_input.setPlaceholderText("Database Host")
        layout.addWidget(self.database_host_input)

        self.database_port_input = QLineEdit()
        self.database_port_input.setPlaceholderText("Database Port")
        layout.addWidget(self.database_port_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.saveSettings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def saveSettings(self):
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            database=self.database_name_input.text(),
            user=self.database_user_input.text(),
            password=self.database_password_input.text(),
            host=self.database_host_input.text(),
            port=self.database_port_input.text()
        )

        # Create a cursor object to execute queries
        cursor = conn.cursor()

        # Create device table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS device
                           (id SERIAL PRIMARY KEY, name text, rtsp_link text, hls_link text)''')

        # Create activity table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS activity
                           (id SERIAL PRIMARY KEY, description text)''')

        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()

class SetupWizard(QWidget):
    def __init__(self):
        super().__init__()

        self.step = 1
        self.user_info = {}
        self.devices = []

        self.setupUI()

    def setupUI(self):
        layout = QVBoxLayout()

        if self.step == 1:
            self.name_input = QLineEdit()
            self.company_input = QLineEdit()
            self.camera_input = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow("Name:", self.name_input)
            form_layout.addRow("Company:", self.company_input)
            form_layout.addRow("Total Number of Cameras:", self.camera_input)

            next_button = QPushButton("Next")
            next_button.clicked.connect(self.nextStep)

            layout.addLayout(form_layout)
            layout.addWidget(next_button)
        
        elif self.step == 2:
            if not self.devices:
                self.manualInput()
            else:
                for device in self.devices:
                    ip_label = QLabel(device["ip"])
                    username_input = QLineEdit()
                    password_input = QLineEdit()

                    form_layout = QFormLayout()
                    form_layout.addRow("Username:", username_input)
                    form_layout.addRow("Password:", password_input)

                    layout.addWidget(ip_label)
                    layout.addLayout(form_layout)

                next_button = QPushButton("Next")
                next_button.clicked.connect(self.nextStep)

                layout.addWidget(next_button)

        elif self.step == 3:
            # Display a summary of the information entered
            user_summary = QLabel(f"Name: {self.user_info['name']}\nCompany: {self.user_info['company']}\nTotal Cameras: {self.user_info['cameras']}")
            layout.addWidget(user_summary)

            for device in self.devices:
                device_summary = QLabel(f"IP: {device['ip']}\nUsername: {device['username']}\nPassword: {device['password']}")
                layout.addWidget(device_summary)

            confirm_button = QPushButton("Confirm")
            confirm_button.clicked.connect(self.saveToDatabase)

            layout.addWidget(confirm_button)

        self.setLayout(layout)

    def manualInput(self):
        num_devices = int(self.camera_input.text())

        for i in range(num_devices):
            ip_input = QLineEdit()
            port_input = QLineEdit()
            username_input = QLineEdit()
            password_input = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow(f"Device {i + 1} IP:", ip_input)
            form_layout.addRow(f"Device {i + 1} Port:", port_input)
            form_layout.addRow(f"Device {i + 1} Username:", username_input)
            form_layout.addRow(f"Device {i + 1} Password:", password_input)

            self.devices.append({
                "ip": ip_input.text(),
                "port": port_input.text(),
                "username": username_input.text(),
                "password": password_input.text()
            })

            layout = QVBoxLayout()
            layout.addLayout(form_layout)
            self.setLayout(layout)

    def nextStep(self):
        if self.step == 1:
            self.user_info = {
                "name": self.name_input.text(),
                "company": self.company_input.text(),
                "cameras": int(self.camera_input.text())
            }
            self.step += 1
            self.setupUI()
        elif self.step == 2:
            if not self.devices:
                self.manualInput()
            else:
                self.step += 1
                self.setupUI()
        elif self.step == 3:
            self.step += 1
            self.setupUI()

    def saveToDatabase(self):
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            database="your_database",
            user="your_user",
            password="your_password",
            host="your_host",
            port="your_port"
        )

        # Create a cursor object to execute queries
        cursor = conn.cursor()

        # Insert user info
        cursor.execute('INSERT INTO users VALUES (?, ?, ?)',
                       (self.user_info['name'], self.user_info['company'], self.user_info['cameras']))

        # Insert device info
        for device in self.devices:
            cursor.execute('INSERT INTO devices VALUES (?, ?, ?, ?)',
                           (device['ip'], device['port'], device['username'], device['password']))

        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()

def main():
    app = QApplication(sys.argv)
    wizard = SetupWizard()
    wizard.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()