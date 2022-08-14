# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv
from os import _exit
from os.path import split, sep
import threading
import discontrol
import requests
import time


class PYQTHoverButton(QtWidgets.QPushButton):
    HoverSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PYQTHoverButton, self).__init__(parent)

    def enterEvent(self, event):
        self.HoverSignal.emit('enterEvent')

    def leaveEvent(self, event):
        self.HoverSignal.emit('leaveEvent')


class Ui_ApplicationWindow(QtWidgets.QMainWindow):
    MainButtonChangeSignal = QtCore.pyqtSignal(dict)
    TokenInputHintChangeSignal = QtCore.pyqtSignal(dict)
    StatusesInputChangeSignal = QtCore.pyqtSignal(dict)
    IsWorking = False
    IsCkecking = False
    IsPinned = False
    MainButtonHover = False
    IsPaschal = False
    RandomColors = [
        'rgb(71, 82, 196)', 'rgb(59, 165, 93)', 'rgb(237, 66, 69)',
        'rgb(250, 168, 26)', 'rgb(178, 80, 167)'
    ]

    def InitWindow(self, Window):
        Window.setObjectName("Window")
        Window.resize(326, 355)
        Window.setMinimumSize(QtCore.QSize(325, 355))
        Window.setMaximumSize(QtCore.QSize(1000, 355))
        Window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        folder = split(__file__)[0] + sep
        self.setWindowIcon(QtGui.QIcon(folder + 'icon.png'))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.CentralWidget = QtWidgets.QWidget(Window)
        self.CentralWidget.setObjectName("CentralWidget")
        self.MainBackground = QtWidgets.QLabel(self.CentralWidget)
        self.MainBackground.setGeometry(QtCore.QRect(0, 10, 326, 301))
        self.MainBackground.setStyleSheet(
            "background-color: rgb(54, 57, 63);\n"
            "border-radius: 10")
        self.MainBackground.setObjectName("MainBackground")
        self.TokenInput = QtWidgets.QLineEdit(self.CentralWidget)
        self.TokenInput.setGeometry(QtCore.QRect(20, 75, 281, 31))
        self.TokenInput.setStyleSheet("border-radius: 3;\n"
                                      "color: rgb(8, 138, 90);\n"
                                      "background-color: rgb(32, 34, 37);\n"
                                      "padding-left: 5;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 87 8pt \"Segoe UI Black\";")
        self.TokenInput.setPlaceholderText("")
        self.TokenInput.setObjectName("TokenInput")
        self.AuthInputHint = QtWidgets.QLabel(self.CentralWidget)
        self.AuthInputHint.setGeometry(QtCore.QRect(20, 50, 306, 21))
        self.AuthInputHint.setStyleSheet("color: rgb(175, 177, 181);\n"
                                         "font: 87 8pt \"Segoe UI Black\";")
        self.AuthInputHint.setAlignment(QtCore.Qt.AlignLeading
                                        | QtCore.Qt.AlignLeft
                                        | QtCore.Qt.AlignVCenter)
        self.AuthInputHint.setObjectName("AuthInputHint")
        self.StatusInputHint = QtWidgets.QLabel(self.CentralWidget)
        self.StatusInputHint.setGeometry(QtCore.QRect(20, 120, 306, 21))
        self.StatusInputHint.setStyleSheet("color: rgb(175, 177, 181);\n"
                                           "font: 87 8pt \"Segoe UI Black\";")
        self.StatusInputHint.setAlignment(QtCore.Qt.AlignLeading
                                          | QtCore.Qt.AlignLeft
                                          | QtCore.Qt.AlignVCenter)
        self.StatusInputHint.setObjectName("StatusInputHint")
        self.Statuses = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.Statuses.setGeometry(QtCore.QRect(20, 145, 281, 101))
        self.Statuses.setStyleSheet("border-radius: 3;\n"
                                    "background-color: rgb(32, 34, 37);\n"
                                    "padding-left: 3;\n"
                                    "padding-bottom: 3;\n"
                                    "padding-right: 3;\n"
                                    "padding-top: 3;\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "font: 87 8pt \"Segoe UI Black\";")
        self.Statuses.setCenterOnScroll(False)
        self.VerticalScrollBar = QtWidgets.QScrollBar()
        self.VerticalScrollBar.setStyleSheet("""
 QScrollBar:vertical {
	border: none;
    background: rgb(46, 51, 56);
    width: 15px;
    margin: 10px 0 10px 0;
	border-radius: 0px;
}
QScrollBar::handle:vertical {	
	background-color: rgb(32, 34, 37);
	min-height: 30px;
	border-radius: 3px;
}
QScrollBar::sub-line:vertical {
	border: none;
	background-color: rgb(54, 57, 63);
	height: 10px;
	border-top-left-radius: 7px;
	border-top-right-radius: 7px;
	subcontrol-position: top;
	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:hover {	
	background-color: rgb(50, 53, 59);
}
QScrollBar::sub-line:vertical:pressed {	
	background-color: rgb(37, 41, 45);
}
QScrollBar::add-line:vertical {
	border: none;
	background-color: rgb(54, 57, 63);
	height: 10px;
	border-bottom-left-radius: 7px;
	border-bottom-right-radius: 7px;
	subcontrol-position: bottom;
	subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:hover {	
	background-color: rgb(50, 53, 59);
}
QScrollBar::add-line:vertical:pressed {	
	background-color: rgb(37, 41, 45);
}
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
	background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	background: none;
}
        """)
        self.Statuses.setVerticalScrollBar(self.VerticalScrollBar)
        self.Statuses.setBackgroundVisible(False)
        self.Statuses.setPlaceholderText("")
        self.Statuses.setObjectName("Statuses")
        self.DelayHint = QtWidgets.QLabel(self.CentralWidget)
        self.DelayHint.setGeometry(QtCore.QRect(20, 260, 71, 16))
        self.DelayHint.setStyleSheet("color: rgb(175, 177, 181);\n"
                                     "font: 87 8pt \"Segoe UI Black\";")
        self.DelayHint.setAlignment(QtCore.Qt.AlignLeading
                                    | QtCore.Qt.AlignLeft
                                    | QtCore.Qt.AlignVCenter)
        self.DelayHint.setObjectName("DelayHint")
        self.DelayInput = QtWidgets.QDoubleSpinBox(self.CentralWidget)
        self.DelayInput.setGeometry(QtCore.QRect(90, 258, 26, 21))
        self.DelayInput.setStyleSheet("border-radius: 3;\n"
                                      "background-color: rgb(32, 34, 37);\n"
                                      "padding-left: 2;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 87 8pt \"Segoe UI Black\";")
        self.DelayInput.setWrapping(False)
        self.DelayInput.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.DelayInput.setAccelerated(False)
        self.DelayInput.setDecimals(1)
        self.DelayInput.setMinimum(0.1)
        self.DelayInput.setMaximum(9.9)
        self.DelayInput.setSingleStep(0.1)
        self.DelayInput.setObjectName("DelayInput")
        self.DelayHintSecText = QtWidgets.QLabel(self.CentralWidget)
        self.DelayHintSecText.setGeometry(QtCore.QRect(120, 260, 26, 16))
        self.DelayHintSecText.setStyleSheet("color: rgb(175, 177, 181);\n"
                                            "font: 87 8pt \"Segoe UI Black\";")
        self.DelayHintSecText.setAlignment(QtCore.Qt.AlignLeading
                                           | QtCore.Qt.AlignLeft
                                           | QtCore.Qt.AlignVCenter)
        self.DelayHintSecText.setObjectName("DelayHintSecText")
        self.ButtonsBackground = QtWidgets.QLabel(self.CentralWidget)
        self.ButtonsBackground.setGeometry(QtCore.QRect(0, 295, 326, 61))
        self.ButtonsBackground.setStyleSheet(
            "background-color: rgb(47, 49, 54);\n"
            "border-radius: 10")
        self.ButtonsBackground.setText("")
        self.ButtonsBackground.setObjectName("ButtonsBackground")
        self.WorkerButton = PYQTHoverButton(self.CentralWidget)
        self.WorkerButton.setGeometry(QtCore.QRect(210, 310, 96, 31))
        self.WorkerButton.setCursor(QtGui.QCursor(
            QtCore.Qt.PointingHandCursor))
        self.WorkerButton.setStyleSheet(
            "background-color: rgb(88, 101, 242);\n"
            "border-radius: 3;\n"
            "color: rgb(255, 255, 255);\n"
            "font: 87 8pt \"Segoe UI Black\";")
        self.WorkerButton.setObjectName("WorkerButton")
        self.QuitButton = PYQTHoverButton(self.CentralWidget)
        self.QuitButton.setGeometry(QtCore.QRect(135, 310, 71, 31))
        self.QuitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.QuitButton.setStyleSheet("background-color: rgb(47, 49, 54);\n"
                                      "border-radius: 3;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 87 8pt \"Segoe UI Black\";")
        self.QuitButton.setObjectName("QuitButton")
        self.PanelBackground = QtWidgets.QLabel(self.CentralWidget)
        self.PanelBackground.setGeometry(QtCore.QRect(0, 0, 326, 36))
        self.PanelBackground.setStyleSheet(
            "background-color: rgb(47, 49, 54);\n"
            "border-radius: 10")
        self.PanelBackground.setObjectName("PanelBackground")
        self.ActionClose = PYQTHoverButton(self.CentralWidget)
        self.ActionClose.setGeometry(QtCore.QRect(290, 5, 31, 26))
        self.ActionClose.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ActionClose.setStyleSheet("background-color: rgb(233, 65, 68);\n"
                                       "border-radius: 5;\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "font: 87 8pt \"Segoe UI Black\";")
        self.ActionClose.setObjectName("ActionClose")
        self.ActionHide = PYQTHoverButton(self.CentralWidget)
        self.ActionHide.setGeometry(QtCore.QRect(220, 5, 31, 26))
        self.ActionHide.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ActionHide.setStyleSheet("background-color: rgb(47, 49, 54);\n"
                                      "border-radius: 5;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 87 12pt \"Segoe UI Black\";")
        self.ActionHide.setObjectName("ActionHide")
        self.ActionLock = PYQTHoverButton(self.CentralWidget)
        self.ActionLock.setGeometry(QtCore.QRect(255, 5, 31, 26))
        self.ActionLock.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ActionLock.setStyleSheet("background-color: rgb(47, 49, 54);\n"
                                      "border-radius: 5;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 87 8pt \"Segoe UI Black\";")
        self.ActionLock.setObjectName("ActionLock")
        self.WindowTitle = QtWidgets.QLabel(self.CentralWidget)
        self.WindowTitle.setGeometry(QtCore.QRect(10, 7, 120, 21))
        self.WindowTitle.setStyleSheet("color: rgb(175, 177, 181);\n"
                                       "font: 87 10pt \"Segoe UI Black\";")
        self.StatusInputHint.setStyleSheet("color: rgb(175, 177, 181);\n"
                                           "font: 87 8pt \"Segoe UI Black\";")
        self.WindowTitle.setAlignment(QtCore.Qt.AlignLeading
                                      | QtCore.Qt.AlignLeft
                                      | QtCore.Qt.AlignVCenter)
        self.WindowTitle.setObjectName("WindowTitle")
        self.WindowTitle.setText('AniCord - 1.3 Beta')

        Window.setCentralWidget(self.CentralWidget)

        Window.setWindowTitle("AniCord")
        self.AuthInputHint.setText("ТОКЕН УЧЁТНОЙ ЗАПИСИ")
        self.StatusInputHint.setText("СТАТУСЫ (ПО ОДНОМУ НА СТРОКУ)")
        self.DelayHint.setText("ЗАДЕРЖКА")
        self.DelayHintSecText.setText("СЕК")
        self.WorkerButton.setText("Пуск")
        self.QuitButton.setText("Закрыть")
        self.ActionLock.setIcon(QtGui.QIcon(folder + 'pin.png'))
        self.ActionClose.setIcon(QtGui.QIcon(folder + 'close.png'))
        self.ActionHide.setIcon(QtGui.QIcon(folder + 'hide.png'))

        QtCore.QMetaObject.connectSlotsByName(Window)

        self.ActionClose.clicked.connect(self.WindowClose)
        self.QuitButton.clicked.connect(self.WindowClose)
        self.ActionHide.clicked.connect(self.WindowHide)
        self.ActionLock.clicked.connect(self.PinWindow)

        self.ActionClose.HoverSignal.connect(self.CloseButtonHover)
        self.ActionHide.HoverSignal.connect(self.HideButtonHover)
        self.WorkerButton.HoverSignal.connect(self.MainButtonHover)
        self.ActionLock.HoverSignal.connect(self.LockButtonHover)

        self.MainButtonChangeSignal.connect(self.MainButtonChangeEvent)
        self.TokenInputHintChangeSignal.connect(self.TokenInputChangeEvent)
        self.StatusesInputChangeSignal.connect(self.StatusesInputChangeEvent)

        self.WorkerButton.clicked.connect(self.Work)

    def Work(self):
        threading.Thread(target=self._work).start()

    def _work(self):
        self.MainButtonHover = False
        self.TokenInputHintChangeSignal.emit({
            'text':
            'ТОКЕН УЧЁТНОЙ ЗАПИСИ',
            'style':
            "color: rgb(175, 177, 181);\n"
            "font: 87 8pt \"Segoe UI Black\";"
        })
        self.StatusesInputChangeSignal.emit({
            'text':
            'СТАТУСЫ (ПО ОДНОМУ НА СТРОКУ)',
            'style':
            "color: rgb(175, 177, 181);\n"
            "font: 87 8pt \"Segoe UI Black\";"
        })

        if self.IsWorking:
            self.MainButtonChangeSignal.emit({
                'text':
                'Пуск',
                'style':
                "background-color: rgb(88, 101, 242);\n"
                "border-radius: 3;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \"Segoe UI Black\";"
            })

            self.IsWorking = False

            return

        self.IsCkecking = True

        try:
            statuses = self.Statuses.toPlainText()
            if statuses == '':
                raise NameError
            if '\n' not in statuses:
                raise NameError
        except:
            self.IsCkecking = False
            self.MainButtonChangeSignal.emit({
                'text':
                'Пуск',
                'style':
                "background-color: rgb(88, 101, 242);\n"
                "border-radius: 3;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \"Segoe UI Black\";"
            })
            self.StatusesInputChangeSignal.emit({
                'text':
                'СТАТУСЫ - НЕВЕРЕН',
                'style':
                "color: rgb(243, 134, 136);\n"
                "font: 87 8pt \"Segoe UI Black\";"
            })
            return

        self.MainButtonChangeSignal.emit({
            'text':
            'Проверка',
            'style':
            "background-color: rgb(64, 68, 75);\n"
            "border-radius: 3;\n"
            "color: rgb(255, 255, 255);\n"
            "font: 87 8pt \"Segoe UI Black\";"
        })

        try:
            response = requests.get(
                'https://discord.com/api/v9/users/@me/library',
                headers={'Authorization': self.TokenInput.text()})
            if response.status_code == 401:
                raise NameError
        except:
            self.IsCkecking = False
            self.MainButtonChangeSignal.emit({
                'text':
                'Пуск',
                'style':
                "background-color: rgb(88, 101, 242);\n"
                "border-radius: 3;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \"Segoe UI Black\";"
            })
            self.TokenInputHintChangeSignal.emit({
                'text':
                'ТОКЕН УЧЁТНОЙ ЗАПИСИ - НЕВЕРЕН',
                'style':
                "color: rgb(243, 134, 136);\n"
                "font: 87 8pt \"Segoe UI Black\";"
            })
            return

        client = discontrol.Client(self.TokenInput.text(), False)

        self.IsCkecking = False
        self.IsWorking = True

        self.MainButtonChangeSignal.emit({
            'text':
            'Работает',
            'style':
            "background-color: rgb(59, 165, 93);\n"
            "border-radius: 3;\n"
            "color: rgb(255, 255, 255);\n"
            "font: 87 8pt \"Segoe UI Black\";"
        })

        lines = self.Statuses.toPlainText().split('\n')
        delay = self.DelayInput.value()

        while self.IsWorking:
            for line in lines:
                if not self.IsWorking:
                    return
                client.set_status_text(line)
                time.sleep(delay)

    def PinWindow(self):
        self.IsPinned = not self.IsPinned

        if not self.IsPinned:
            self.ActionLock.setStyleSheet(
                "background-color: rgb(47, 49, 54);\n"
                "border-radius: 5;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \"Segoe UI Black\";")
        else:
            self.ActionLock.setStyleSheet(
                "background-color: rgb(59, 165, 93);\n"
                "border-radius: 5;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \"Segoe UI Black\";")

        if self.IsPinned:
            self.setWindowFlags(self.windowFlags()
                                | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags()
                                & ~QtCore.Qt.WindowStaysOnTopHint)
            self.show()

    def TokenInputChangeEvent(self, data):
        self.AuthInputHint.setText(data['text'])
        self.AuthInputHint.setStyleSheet(data['style'])

    def StatusesInputChangeEvent(self, data):
        self.StatusInputHint.setText(data['text'])
        self.StatusInputHint.setStyleSheet(data['style'])

    def MainButtonChangeEvent(self, data):
        self.WorkerButton.setText(data['text'])
        self.WorkerButton.setStyleSheet(data['style'])

    def WindowClose(self):
        _exit(0)

    def WindowHide(self):
        self.showMinimized()

    def LockButtonHover(self, event):
        if not self.IsPinned:
            if event == 'enterEvent':
                self.ActionLock.setStyleSheet(
                    "background-color: rgb(63, 65, 72);\n"
                    "border-radius: 5;\n"
                    "color: rgb(255, 255, 255);\n"
                    "font: 87 12pt \"Segoe UI Black\";")
            else:
                self.ActionLock.setStyleSheet(
                    "background-color: rgb(47, 49, 54);\n"
                    "border-radius: 5;\n"
                    "color: rgb(255, 255, 255);\n"
                    "font: 87 8pt \"Segoe UI Black\";")
        else:
            if event == 'enterEvent':
                self.ActionLock.setStyleSheet(
                    "background-color: rgb(52, 146, 82);\n"
                    "border-radius: 5;\n"
                    "color: rgb(255, 255, 255);\n"
                    "font: 87 12pt \"Segoe UI Black\";")
            else:
                self.ActionLock.setStyleSheet(
                    "background-color: rgb(59, 165, 93);\n"
                    "border-radius: 5;\n"
                    "color: rgb(255, 255, 255);\n"
                    "font: 87 8pt \"Segoe UI Black\";")

    def CloseButtonHover(self, event):
        if event == 'enterEvent':
            self.ActionClose.setStyleSheet(
                "background-color: rgb(186, 52, 54);\n"
                "border-radius: 5;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \"Segoe UI Black\";")
        else:
            self.ActionClose.setStyleSheet(
                "background-color: rgb(233, 65, 68);\n"
                "border-radius: 5;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \"Segoe UI Black\";")

    def HideButtonHover(self, event):
        if event == 'enterEvent':
            self.ActionHide.setStyleSheet(
                "background-color: rgb(63, 65, 72);\n"
                "border-radius: 5;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 12pt \"Segoe UI Black\";")
        else:
            self.ActionHide.setStyleSheet(
                "background-color: rgb(47, 49, 54);\n"
                "border-radius: 5;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 12pt \"Segoe UI Black\";")

    def MainButtonHoverFX(self):
        self.MainButtonChangeEvent({
            'text':
            'Пуск',
            'style':
            "background-color: rgb(81, 93, 224);\n"
            "border-radius: 3;\n"
            "color: rgb(255, 255, 255);\n"
            "font: 87 8pt \"Segoe UI Black\";"
        })

        time.sleep(3)

        if self.IsPaschal:
            return

        self.IsPaschal = True

        while self.MainButtonHover:
            for color in self.RandomColors:
                if not self.MainButtonHover:
                    break
                self.MainButtonChangeEvent({
                    'text':
                    'ПУСК!',
                    'style':
                    f"background-color: {color};\n"
                    "border-radius: 3;\n"
                    f"color: rgb(255, 255, 255);\n"
                    "font: 87 10pt \"Segoe UI Black\";"
                })

                time.sleep(.2)

        self.IsPaschal = False

        self.WorkerButton.setStyleSheet(
            "background-color: rgb(88, 101, 242);\n"
            "border-radius: 3;\n"
            "color: rgb(255, 255, 255);\n"
            "font: 87 8pt \"Segoe UI Black\";")
        self.WorkerButton.setText('Пуск')

    def MainButtonHover(self, event):
        if not self.IsWorking and not self.IsCkecking:
            if event == 'enterEvent':
                self.MainButtonHover = True
                threading.Thread(target=self.MainButtonHoverFX).start()
            else:
                self.MainButtonHover = False
                self.WorkerButton.setStyleSheet(
                    "background-color: rgb(88, 101, 242);\n"
                    "border-radius: 3;\n"
                    "color: rgb(255, 255, 255);\n"
                    "font: 87 8pt \"Segoe UI Black\";")

        elif self.IsWorking and not self.IsCkecking:
            if event == 'enterEvent':
                self.MainButtonHover = True
                self.WorkerButton.setStyleSheet(
                    "background-color: rgb(52, 146, 82);\n"
                    "border-radius: 3;\n"
                    "color: rgb(255, 255, 255);\n"
                    "font: 87 8pt \"Segoe UI Black\";")
            else:
                self.MainButtonHover = False
                self.WorkerButton.setStyleSheet(
                    "background-color: rgb(59, 165, 93);\n"
                    "border-radius: 3;\n"
                    "color: rgb(255, 255, 255);\n"
                    "font: 87 8pt \"Segoe UI Black\";")


class ApplicationWindow(Ui_ApplicationWindow):

    def __init__(self):
        super().__init__()
        self.InitWindow(self)

    def closeEvent(self, *args):
        _exit(0)

    def mousePressEvent(self, event):
        try:
            if event.button() == QtCore.Qt.LeftButton:
                self.old_pos = event.pos()
        except:
            pass

    def mouseReleaseEvent(self, event):
        try:
            if event.button() == QtCore.Qt.LeftButton:
                self.old_pos = None
        except:
            pass

    def mouseMoveEvent(self, event):
        try:
            if not self.old_pos:
                return
            delta = event.pos() - self.old_pos
            self.move(self.pos() + delta)
        except:
            pass


if __name__ == "__main__":
    Application = QtWidgets.QApplication(argv)
    Window = ApplicationWindow()
    Window.show()
    _exit(Application.exec_())
