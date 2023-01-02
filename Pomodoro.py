import random
import sys
import time

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
import playsound


class TWindow(QWidget):
    def __init__(self):
        super().__init__()

        # self.flashflag = True

        self.setWindowTitle("Pomodoro Timer")
        #self.setWindowIcon(QIcon("icon.png"))
        self.setFixedWidth(500)
        self.setFixedHeight(200)

        # for a future update to not include the title
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        #self.setWindowOpacity(.5)

        self.setStyleSheet("background-color: #495252; background:transparent;")

        self.create_buttons()
        self.timer_details()

        #Sets up some stuff
        #This creates the minimize view bool. It starts unhidden, so false.
        self.hiding = False


    # Mouse Events

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.oldPosition)
        self.oldPosition = event.globalPosition().toPoint()

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.minimizeview()

    # Color updating (found online, may remove later)

    def chngeclr(self, color):

        cde = """
            ::chunk {{
                background: {0};
                border-radius: 2px;
            }}

        """.format(color)

        return cde

    #Build the pieces
    def create_buttons(self):

        # C/D Button
        self.playbutton = "AddOn_Functionality/Pomodoro/Play.png"
        self.pausebutton = "AddOn_Functionality/Pomodoro/Pause.ico"

        self.connect_button = QPushButton("Start Timer", self)
        self.connect_button.setGeometry(130, 100, 100, 40)
        self.connect_button.setStyleSheet("background-color: #191D1D;")
        # self.connect_button.clicked.connect(lambda: self.timer_start())
        self.connect_button.clicked.connect(lambda: self.timer_decide(timer_type='pom'))
        self.connect_button.setProperty("status", "Off")

        self.breakbutton = QPushButton("Start break", self)
        self.breakbutton.setGeometry(250, 100, 100, 40)
        self.breakbutton.setStyleSheet("background-color: #191D1D;")
        self.breakbutton.clicked.connect(lambda: self.timer_decide(timer_type='break'))
        self.breakbutton.setProperty("status", "Off")

        self.pom_dropdown = QComboBox(self)
        self.pom_dropdown.addItem("Short Pomodoro")
        self.pom_dropdown.addItem("Long Pomodoro")
        self.pom_dropdown.setStyleSheet("QComboBox" 
                                        "{"
                                        "background-color: #495252;"
                                        "}")
        self.pom_dropdown.setStyleSheet("QListView"
                                     "{"
                                     "background-color: #191D1D;"
                                     "}")
        self.pom_dropdown.setGeometry(175, 145, 150, 25)

        # For when minimal view is showing
        self.hiddenmessage = QLabel(self)
        self.hiddenmessage.hide()
        self.hiddenmessage.setGeometry(125, 100, 250, 50)
        self.hiddenmessage.setFont(QFont("Helvetica", 20))
        self.hiddenmessage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Below will later be updated to its own property window to save the settings.

        self.short_pom = QLineEdit(self)
        self.short_pom.setPlaceholderText("Short Pom")
        self.short_pom.setGeometry(50, 170, 75, 25)

        self.long_pom = QLineEdit(self)
        self.long_pom.setPlaceholderText("Long Pom")
        self.long_pom.setGeometry(130, 170, 75, 25)

        self.short_break = QLineEdit(self)
        self.short_break.setPlaceholderText("Short Break")
        self.short_break.setGeometry(250, 170, 75, 25)

        self.long_break = QLineEdit(self)
        self.long_break.setPlaceholderText("Long Break")
        self.long_break.setGeometry(325, 170, 75, 25)

        quit_button = QPushButton("Quit", self)
        quit_button.setGeometry(0, 0, 75, 30)
        quit_button.setStyleSheet("background-color: #191D1D;")
        quit_button.clicked.connect(lambda: sys.exit())


    def minimizeview(self):
        if self.hiding:
            self.short_pom.show()
            self.long_pom.show()
            self.short_break.show()
            self.long_break.show()
            self.connect_button.show()
            self.breakbutton.show()
            self.pom_dropdown.show()
            self.hiding = False
            self.hiddenmessage.hide()
        else:
            self.hiddenmessages = ['CRUSHING IT!', 'YOU BEAUTIFUL BEAST!', "AW YEAH!", "YOU'RE AMAZING!"]
            self.hiding = True
            self.short_pom.hide()
            self.long_pom.hide()
            self.short_break.hide()
            self.long_break.hide()
            self.connect_button.hide()
            self.breakbutton.hide()
            self.breakbutton.setVisible(False)
            self.breakbutton.setStyleSheet('background:transparent;')
            self.breakbutton.setStyleSheet('border: transparent;')
            self.pom_dropdown.hide()
            self.hiddenmessage.setText(self.hiddenmessages[random.randrange(0, len(self.hiddenmessages))])
            self.hiddenmessage.show()

    ### Timer Stuff

    def timer_decide(self, timer_type):

        match timer_type:
            case 'pom':
                self.currenttime_button = self.connect_button
                self.opposite_button = self.breakbutton
            case 'break':
                self.currenttime_button = self.breakbutton
                self.opposite_button = self.connect_button

        if self.currenttime_button.property("status") == "Off":
            self.currenttime_button.setProperty("status", "On")
            self.currenttime_button.setIcon(QIcon(self.playbutton))
            self.opposite_button.setDisabled(True)
            self.opposite_button.setIcon(QIcon())
            self.timer_start(stime=self.short_pom.text(), t_type=timer_type)

        elif self.currenttime_button.property("status") == "On":
            self.currenttime_button.setProperty("status", "Paused")
            self.opposite_button.setDisabled(False)
            self.opposite_button.setIcon(QIcon())
            self.currenttime_button.setIcon(QIcon(self.pausebutton))
            self.timer.stop()

        elif self.currenttime_button.property("status") == "Paused":
            self.currenttime_button.setProperty("status", "On")
            self.opposite_button.setDisabled(True)
            self.opposite_button.setIcon(QIcon())
            self.currenttime_button.setIcon(QIcon(self.playbutton))
            self.timer.start(1000)

    def timer_details(self):
        #Time Label
        self.pom_label = QLabel(self)
        self.pom_label.setText("00:00")
        self.pom_label.setFont(QFont("Arial", 40))
        self.pom_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pom_label.setGeometry(150, 50, 200, 50)

    def timer_start(self, stime, t_type):
        if t_type == 'pom':
            if stime == 0 or stime is None or stime == "":
                pom_min_label = 25
            else:
                pom_min_label = int(stime)
        if t_type == 'break':
            if stime == 0 or stime is None or stime == "":
                pom_min_label = 10
            else:
                pom_min_label = int(stime)

        self.pomtime = QtCore.QTime(00, pom_min_label, 00)
        # self.pomtime = QtCore.QTime(00, 00, 10)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.time())
        self.timer.start(1000)






    # def threesecondflash(self):
    #     if self.pom_label == "Victory":
    #         self.pom_label.setStyleSheet("color: white;")
    #     else:
    #         if self.flashflag:
    #             self.pom_label.setStyleSheet("color: blue;")
    #         else:
    #             self.pom_label.setStyleSheet("color: purple;")
    #         self.flashflag = not self.flashflag

    def time(self):
        self.pomtime = self.pomtime.addSecs(-1)

        if self.pomtime.minute() < 10:
            theminute = "0" + str(self.pomtime.minute())
        else:
            theminute = self.pomtime.minute()

        if self.pomtime.second() < 10:
            thesecond = "0" + str(self.pomtime.second())
        else:
            thesecond = self.pomtime.second()

        self.rem_time = f"{theminute}:{thesecond}"
        self.pom_label.setText(self.rem_time)
        # if self.pomtime.second() < 4 or self.pom_label.text == "Victory":
        #     self.threesecondflash()

        ### We need to confirm the break or pom type and play the appropiate sound

        if self.pomtime.minute() == 0 and self.pomtime.second() == 0:
            self.timer.stop()
            self.pom_label.setText("VICTORY")
            self.play_victory()

    def play_victory(self):
        playsound.playsound("AddOn_Functionality/Pomodoro/Victory.m4a", False)

    def play_breakend(self):
        pass


def main():
    bot_app = QApplication([])
    window = TWindow()
    window.show()
    sys.exit(bot_app.exec())


if __name__ == '__main__':
    main()
