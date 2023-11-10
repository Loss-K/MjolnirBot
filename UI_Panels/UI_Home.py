import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
import UI_Settings

class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("aworthyhammer Bot")
        #self.setWindowIcon(QIcon("icon.png"))
        self.setFixedWidth(325)
        self.setFixedHeight(250)

        self.create_details()


    def create_details(self):

        #C/D Button

        self.connect_button = QPushButton("Connect", self)
        self.connect_button.setGeometry(50, 25, 100, 100)
        self.connect_button.clicked.connect(self.connect_buttonClick)

        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.setGeometry(175, 75, 100, 50)
        self.disconnect_button.setDisabled(True)
        self.disconnect_button.clicked.connect(self.disconnect_buttonClick)

        # End Stream Announcement

        self.endStreamMessage_button = QPushButton("End Stream\nMessage(s)", self)
        self.endStreamMessage_button.setGeometry(175, 25, 100, 50)
        self.endStreamMessage_button.clicked.connect(self.sendclosing_buttonClick)

        self.es_Prop_button = QPushButton("Settings", self)
        self.es_Prop_button.setGeometry(115, 150, 100, 50)
        self.es_Prop_button.clicked.connect(self.settings_buttonClick)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.setGeometry(115, 200, 100, 50)
        self.quit_button.clicked.connect(self.quitapp_buttonClick)

    def connect_buttonClick(self):
        print("connected")
        # import Mjolnir

    def sendclosing_buttonClick(self):
        print("closing messages")

    def disconnect_buttonClick(self):
        print("disconnected")
        # Mjolnir.Mjolnirbot().endstream()

    def settings_buttonClick(self):
        print("settings")
        self.window_test = UI_Settings.Setting_window()
        self.window_test.show()
        self.es_Prop_button.setDisabled(True)

    def quitapp_buttonClick(self):
        print("quit selected")
        sys.exit(self)

def main():
    bot_app = QApplication([])
    window = Home()
    window.show()
    sys.exit(bot_app.exec())


if __name__ == '__main__':
    main()
