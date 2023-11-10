import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
import ast

# from Mjolnir import Mjolnirbot

class Setting_window(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("aworthyhammer Settings")
        #self.setWindowIcon(QIcon("icon.png"))
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        self.discord_settings()
        self.pom_settings()
        self.twitch_settings()

        # self.standard_settings()
        self.all_the_tabs()

    def all_the_tabs(self):
        # self.tabs = QTabWidget()
        self.twitchTab = QWidget()
        self.discordTab = QWidget()
        self.pomodoro_Tab = QWidget()
       # self.chatMod_Tab = QWidget()
        self.resize(500, 500)

        self.addTab(self.twitchTab, "Twitch")
        self.addTab(self.discordTab, "Discord")
        self.addTab(self.pomodoro_Tab, "Pomodoro")
        #self.addTab(self.chatMod_Tab, "ChatMod")

        self.savebutton = QPushButton("Save", self)
        self.savebutton.setGeometry(125, 450, 100, 50)

        self.exitbutton = QPushButton("Exit", self)
        self.exitbutton.setGeometry(250, 450, 100, 50)
        self.exitbutton.clicked.connect(self.exit_settings)

        self.twitchTab.layout = QVBoxLayout(self)
        self.discordTab.layout = QVBoxLayout(self)
        self.pomodoro_Tab.layout = QVBoxLayout(self)
#
        self.dircheck = self.__dir__()

        twitchlist = []
        discordlist = []
        pomolist =[]
        chatmodlist = []
        for i in self.dircheck:
            if 'settings' in i:
                pass
            else:
                if "twitch" in i:
                    twitchlist.append(i)
                if "discord" in i:
                    discordlist.append(i)
                if "pom" in i or '_break' in i:
                    pomolist.append(i)

        for widget_name in twitchlist:
            widget = self.__getattribute__(widget_name.split(".")[-1])
            if isinstance(widget, QWidget) and 'Tab' not in widget_name:
                self.twitchTab.layout.addWidget(widget)
                print(f'added widget: {widget_name}')

        for widget_name in discordlist:
            widget = self.__getattribute__(widget_name.split(".")[-1])
            if isinstance(widget, QWidget) and 'Tab' not in widget_name:
                self.discordTab.layout.addWidget(widget)
                print(f'added widget: {widget_name}')

        for widget_name in pomolist:
            print(widget_name)
            widget = self.__getattribute__(widget_name.split(".")[-1])
            if isinstance(widget, QWidget) and 'Tab' not in widget_name:
                self.pomodoro_Tab.layout.addWidget(widget)
                print(f'added widget: {widget_name}')

        self.twitchTab.setLayout(self.twitchTab.layout)
        self.twitchTab.layout.addStretch(2)
        self.twitchTab.layout.setSpacing(20)

        self.discordTab.setLayout(self.discordTab.layout)
        self.discordTab.layout.addStretch(2)
        self.discordTab.layout.setSpacing(20)

        self.pomodoro_Tab.setLayout(self.pomodoro_Tab.layout)
        self.pomodoro_Tab.layout.addStretch(2)
        self.pomodoro_Tab.layout.setSpacing(20)

        self.show()


    def twitch_settings(self):

        self.twitch_un_label = QLabel()
        self.twitch_un_label.setText('Twitch Username')
        self.twitch_username = QLineEdit()

        self.twitch_API_label = QLabel()
        self.twitch_API_label.setText('API KEY')
        self.twitch_API = QLineEdit()

        self.twitch_Twitch_PermLabel = QLabel()
        self.twitch_Twitch_PermLabel.setText('Twitch Permission')
        self.twitch_permission = QLineEdit()
        
    def discord_settings(self):

        self.discord_un_label = QLabel()
        self.discord_un_label.setText('Discord Channel')
        self.discord_username = QLineEdit()


        self.discord_API_label = QLabel()
        self.discord_API_label.setText('Discord API KEY')
        self.discord_API = QLineEdit()


        self.discord_discord_PermLabel = QLabel()
        self.discord_discord_PermLabel.setText('Discord Permission')
        self.discord_permission = QLineEdit()

    def pom_settings(self):

        self.short_pom_Label = QLabel()
        self.short_pom_Label.setText('Short Pomodoro')
        self.short_pom = QLineEdit(self)
        self.short_pom.setPlaceholderText("default 25")

        self.long_pom_Label = QLabel()
        self.long_pom_Label.setText('Long Pomodoro')
        self.long_pom = QLineEdit(self)
        self.long_pom.setPlaceholderText("default 60")

        self.short_break_Label = QLabel()
        self.short_break_Label.setText('Short Break')
        self.short_break = QLineEdit(self)
        self.short_break.setPlaceholderText("default 10")

        self.long_break_Label = QLabel()
        self.long_break_Label.setText('Long Break')
        self.long_break = QLineEdit(self)
        self.long_break.setPlaceholderText("default 25")

    # def chat_settings(self):
    #
    #     self.username = QLineEdit(self)

    #
    #     self.username = QLineEdit(self)

    #
    #     self.username = QLineEdit(self)

    #

    #
    def exit_settings(self):

        self.btn_options = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Discard
        self.e_window = QDialogButtonBox(self.btn_options)
        self.e_window.accepted.connect(self.e_window.accepted)
        self.e_window.rejected.connect(self.e_window.rejected)

        self.e_window.setWindowTitle("Exiting -> Do you want to save?")
        self.message = QLabel("Do you want to save your changes?")
        self.e_window.layout().addWidget(self.message)

        if  QDialogButtonBox.StandardButtonS:
            print("Saved")



        self.e_window.show()

        # Todo - Fix actions after inital window - Fix formatting on window.

def main():
    bot_app = QApplication([])
    window = Setting_window()
    window.show()
    sys.exit(bot_app.exec())


if __name__ == '__main__':
    main()
