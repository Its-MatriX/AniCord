# -*- coding: utf-8 -*-

# В начале обязательно испортируем модули!
from os import name, _exit
from random import random
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv
from os.path import split, sep
import threading
import discontrol
import requests
import time
import random
from ctypes import WinDLL
from os.path import isfile, sep, expanduser

# Только Windows!
if name != 'nt':
    _exit(1)

WindowsUser32DLL = WinDLL('user32.dll')

userfolder = expanduser('~')

if not isfile(str(userfolder) + sep + 'anicord_accepted.txt'):
    text_warning = '''За использование этой программы ваш аккаунт могут забанить или требовать верификацию по номеру!
    
Автор программы не несёт ответственности!

Если вы нажмёте "Да" - вы принимаете вышесказанное, и больше не увидите данное сообщение.'''
    answer = WindowsUser32DLL.MessageBoxW(0, text_warning, 'Внимание!', 48 | 4)

    if answer == 6:
        open(str(userfolder) + sep + 'anicord_accepted.txt', 'w').write(
            'Этот файл был создан, когда вы приняли правила Anicord, чтобы программа понимала, что не нужно снова показывать предупреждение. Если вы удалите этот файл, предупреждение появится снова.'
        )
    else:
        _exit(0)


class PYQTHoverButton(QtWidgets.QPushButton):
    HoverSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PYQTHoverButton, self).__init__(parent)

    def enterEvent(self, event):
        self.HoverSignal.emit('enterEvent')

    def leaveEvent(self, event):
        self.HoverSignal.emit('leaveEvent')


class PYQTHoverLabel(QtWidgets.QLabel):
    HoverSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PYQTHoverLabel, self).__init__(parent)

    def enterEvent(self, event):
        self.HoverSignal.emit('enterEvent')

    def leaveEvent(self, event):
        self.HoverSignal.emit('leaveEvent')


class ApplicationState:
    AllowWindowMove = False
    DocsWindowIsOpened = False


class Ui_Docs(QtWidgets.QMainWindow):

    IsVisitOurDiscordButtonHover = False
    IsVisitOurDiscordButtonPaschal = False
    OurDiscordButtonHoverChangeStylesValidThreadID = 0
    ChangeOurDiscordButtonStyleSignal = QtCore.pyqtSignal(dict)
    RandomColors = [
        'rgb(71, 82, 196)', 'rgb(59, 165, 93)', 'rgb(237, 66, 69)',
        'rgb(250, 168, 26)', 'rgb(178, 80, 167)'
    ]

    def InitWindow(self, Docs):
        folder = split(__file__)[0] + sep
        Docs.setObjectName("Docs")
        Docs.resize(370, 510)
        Docs.setMinimumSize(QtCore.QSize(370, 510))
        Docs.setMaximumSize(QtCore.QSize(370, 510))
        self.CentralWidget = QtWidgets.QWidget(Docs)
        self.CentralWidget.setObjectName("CentralWidget")
        self.Background = QtWidgets.QLabel(self.CentralWidget)
        self.Background.setGeometry(QtCore.QRect(0, 0, 371, 511))
        self.Background.setStyleSheet("background-color: rgb(54, 57, 63);")
        self.Background.setObjectName("Background")
        self.Title = QtWidgets.QLabel(self.CentralWidget)
        self.Title.setGeometry(QtCore.QRect(0, 5, 366, 41))
        self.Title.setStyleSheet("font: 87 18pt \"Segoe UI Black\";\n"
                                 "color: rgb(255, 255, 255);")
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.Line1 = QtWidgets.QLabel(self.CentralWidget)
        self.Line1.setGeometry(QtCore.QRect(20, 50, 326, 21))
        self.Line1.setStyleSheet("font: 87 14pt \"Segoe UI Black\";\n"
                                 "color: rgb(255, 255, 255);")
        self.Line1.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.Line1.setObjectName("Line1")
        self.Line2 = QtWidgets.QLabel(self.CentralWidget)
        self.Line2.setGeometry(QtCore.QRect(20, 75, 326, 56))
        self.Line2.setStyleSheet("font: 87 10pt \"Segoe UI Black\";\n"
                                 "color: rgb(235, 235, 235);")
        self.Line2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.Line2.setObjectName("Line2")
        self.Warning = QtWidgets.QLabel(self.CentralWidget)
        self.Warning.setGeometry(QtCore.QRect(20, 140, 326, 101))
        self.Warning.setStyleSheet("background-color: rgb(109, 78, 52);\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "font: 87 8pt \"Segoe UI Black\";\n"
                                   "border-radius: 10;\n"
                                   "border-style: solid;\n"
                                   "border-width: 2;\n"
                                   "border-color: rgb(255, 170, 0);\n"
                                   "padding-left: 5;\n"
                                   "padding-top: 5;")
        self.Warning.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                  | QtCore.Qt.AlignTop)
        self.Warning.setObjectName("Warning")
        self.Line3 = QtWidgets.QLabel(self.CentralWidget)
        self.Line3.setGeometry(QtCore.QRect(15, 265, 326, 21))
        self.Line3.setStyleSheet("font: 87 14pt \"Segoe UI Black\";\n"
                                 "color: rgb(255, 255, 255);")
        self.Line3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.Line3.setObjectName("Line3")
        self.Line4 = QtWidgets.QLabel(self.CentralWidget)
        self.Line4.setGeometry(QtCore.QRect(15, 280, 326, 91))
        self.Line4.setStyleSheet("font: 87 10pt \"Segoe UI Black\";\n"
                                 "color: rgb(235, 235, 235);")
        self.Line4.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.Line4.setObjectName("Line4")
        self.Line5 = QtWidgets.QLabel(self.CentralWidget)
        self.Line5.setGeometry(QtCore.QRect(15, 380, 326, 21))
        self.Line5.setStyleSheet("font: 87 14pt \"Segoe UI Black\";\n"
                                 "color: rgb(255, 255, 255);")
        self.Line5.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                | QtCore.Qt.AlignVCenter)
        self.Line5.setObjectName("Line5")
        self.GoToGithubPage = PYQTHoverButton(self.CentralWidget)
        self.GoToGithubPage.setGeometry(QtCore.QRect(15, 460, 161, 31))
        self.GoToGithubPage.setStyleSheet(
            "background-color: rgb(0, 0, 0);\n"
            "border-radius: 3;\n"
            "color: rgb(255, 255, 255);\n"
            "font: 87 8pt \\\"Segoe UI Black\\\";")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(folder + "github.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.GoToGithubPage.setIcon(icon)
        self.GoToGithubPage.setIconSize(QtCore.QSize(25, 25))
        self.GoToGithubPage.setObjectName("GoToGithubPage")
        self.VisitOurDiscord = PYQTHoverButton(self.CentralWidget)
        self.VisitOurDiscord.setGeometry(QtCore.QRect(15, 415, 336, 31))
        self.VisitOurDiscord.setStyleSheet(
            "background-color: rgb(88, 101, 242);\n"
            "border-radius: 3;\n"
            "color: rgb(255, 255, 255);\n"
            "font: 87 8pt \\\"Segoe UI Black\\\";")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(folder + "discord.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.VisitOurDiscord.setIcon(icon1)
        self.VisitOurDiscord.setIconSize(QtCore.QSize(25, 25))
        self.VisitOurDiscord.setObjectName("VisitOurDiscord")
        self.GuideToken = PYQTHoverButton(self.CentralWidget)
        self.GuideToken.setGeometry(QtCore.QRect(190, 460, 161, 31))
        self.GuideToken.setStyleSheet("background-color: rgb(59, 165, 93);\n"
                                      "border-radius: 3;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 87 8pt \\\"Segoe UI Black\\\";")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(folder + "help.png"))
        self.GuideToken.setIcon(icon2)
        self.GuideToken.setIconSize(QtCore.QSize(25, 25))
        self.GuideToken.setObjectName("GuideToken")
        Docs.setCentralWidget(self.CentralWidget)

        Docs.setWindowTitle("Anicord - О программе")
        self.Title.setText("Anicord")
        self.Line1.setText("Что это?")
        self.Line2.setText("Anicord - эта программа с открытым исходным\n"
                           "кодом, предназначенная для анимированного\n"
                           "статуса в Discord")
        self.Warning.setText(
            "И да, опять мы повторяем!\n\n"
            "За использование этой программы ваш аккаунт могут\n"
            "забанить или требовать верификацию по номеру!\n"
            "Автор программы не несёт ответственности!\n"
            "Всю ответственность вы перекладываете на себя.")
        self.Line3.setText("Я чайник! Как пользоваться?")
        self.Line4.setText("Сперва посмотрите на YouTube гайд\n"
                           "по получению токена аккаунта. Это просто!\n"
                           "Далее укажите статусы для анимации, укажите\n"
                           "задержку и нажмите \"Пуск\". Всё очень просто.")
        self.Line5.setText("Ссылки")
        self.GoToGithubPage.setText("Исходный код")
        self.VisitOurDiscord.setText("Наш Discord сервер!")
        self.GuideToken.setText("Гайд по токену (текст)")

        QtCore.QMetaObject.connectSlotsByName(Docs)

        self.ChangeOurDiscordButtonStyleSignal.connect(
            self.OurDiscordChangeStyleEvent)
        self.VisitOurDiscord.HoverSignal.connect(self.OurDiscordButtonHover)
        self.GoToGithubPage.HoverSignal.connect(self.GoToGithubPageHoverEvent)
        self.GuideToken.HoverSignal.connect(self.GuideTokenHoverEvent)

        self.VisitOurDiscord.clicked.connect(self.OpenOurDiscord)
        self.GoToGithubPage.clicked.connect(self.OpenSource)
        self.GuideToken.clicked.connect(self.OpenTokenGuide)

    def GuideTokenHoverEvent(self, event):
        if event == 'enterEvent':
            self.GuideToken.setStyleSheet(
                "background-color: rgb(52, 146, 82);\n"
                "border-radius: 3;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \\\"Segoe UI Black\\\";")
        else:
            self.GuideToken.setStyleSheet(
                "background-color: rgb(59, 165, 93);\n"
                "border-radius: 3;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \\\"Segoe UI Black\\\";")

    def GoToGithubPageHoverEvent(self, event):
        if event == 'enterEvent':
            self.GoToGithubPage.setStyleSheet(
                "background-color: rgb(35, 35, 35);\n"
                "border-radius: 3;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \\\"Segoe UI Black\\\";")
        else:
            self.GoToGithubPage.setStyleSheet(
                "background-color: rgb(0, 0, 0);\n"
                "border-radius: 3;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \\\"Segoe UI Black\\\";")

    def OpenTokenGuide(self):
        webbrowser.open(
            'https://github.com/Its-MatriX/AniCord/blob/main/gettoken.md')

    def OpenSource(self):
        webbrowser.open('https://github.com/Its-MatriX/AniCord')

    def OpenOurDiscord(self):
        link = requests.get('https://pastebin.com/raw/g4DVdy2Q').text
        webbrowser.open(link)

    def OurDiscordButtonHoverChangeStylesThread(self, ID):
        if self.IsVisitOurDiscordButtonPaschal:
            return

        while self.IsVisitOurDiscordButtonHover:
            for color in self.RandomColors:
                if ID != self.OurDiscordButtonHoverChangeStylesValidThreadID:
                    return
                self.ChangeOurDiscordButtonStyleSignal.emit({
                    'text':
                    'ПРИСОЕДИНЯЙТЕСЬ К НАШЕМУ СЕРВЕРУ!',
                    'style':
                    f"background-color: {color};\n"
                    "border-radius: 3;\n"
                    "color: rgb(255, 255, 255);\n"
                    "font: 87 8pt \\\"Segoe UI Black\\\";"
                })
                time.sleep(.2)
                if not self.IsVisitOurDiscordButtonHover:
                    return

    def OurDiscordButtonHover(self, event):
        if event == 'enterEvent':
            self.IsVisitOurDiscordButtonHover = True
            self.OurDiscordButtonHoverChangeStylesValidThreadID = random.randint(
                1, 100000000000000)
            threading.Thread(
                target=lambda: self.OurDiscordButtonHoverChangeStylesThread(
                    self.OurDiscordButtonHoverChangeStylesValidThreadID)
            ).start()
        else:
            self.IsVisitOurDiscordButtonHover = False
            self.ChangeOurDiscordButtonStyleSignal.emit({
                'text':
                'Наш Discord сервер!',
                'style':
                f"background-color: rgb(88, 101, 242);\n"
                "border-radius: 3;\n"
                "color: rgb(255, 255, 255);\n"
                "font: 87 8pt \\\"Segoe UI Black\\\";"
            })

        self.IsVisitOurDiscordButtonPaschal = False

    def OurDiscordChangeStyleEvent(self, data):
        self.VisitOurDiscord.setText(data['text'])
        self.VisitOurDiscord.setStyleSheet(data['style'])


class DocsWindow(Ui_Docs):

    def __init__(self):
        super().__init__()
        self.InitWindow(self)

    def closeEvent(self, event):
        ApplicationState.DocsWindowIsOpened = False


class Ui_ApplicationWindow(QtWidgets.QMainWindow):
    MainButtonChangeSignal = QtCore.pyqtSignal(dict)
    TokenInputHintChangeSignal = QtCore.pyqtSignal(dict)
    StatusesInputChangeSignal = QtCore.pyqtSignal(dict)
    WindowClsSignal = QtCore.pyqtSignal(str)
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
        self.Background = QtWidgets.QLabel(self.CentralWidget)
        self.Background.setGeometry(QtCore.QRect(0, 30, 326, 275))
        self.Background.setStyleSheet("background-color: rgb(47, 49, 54)")
        self.Background.setObjectName("Background")
        self.MainBackground = QtWidgets.QLabel(self.CentralWidget)
        self.MainBackground.setGeometry(QtCore.QRect(5, 36, 316, 259))
        self.MainBackground.setStyleSheet(
            "background-color: rgb(54, 57, 63);\n"
            "border-radius: 10;\n")
        self.MainBackground.setObjectName("MainBackground")
        self.TokenInput = QtWidgets.QLineEdit(self.CentralWidget)
        self.TokenInput.setGeometry(QtCore.QRect(20, 75, 281, 31))
        self.TokenInput.setStyleSheet("border-radius: 3;\n"
                                      "color: rgb(8, 138, 90);\n"
                                      "background-color: rgb(32, 34, 37);\n"
                                      "padding-left: 5;\n"
                                      "padding-right: 5;\n"
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
            "border-bottom-left-radius: 10;\n"
            "border-bottom-right-radius: 10;\n")
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
        self.AboutButton = PYQTHoverButton(self.CentralWidget)
        self.AboutButton.setGeometry(QtCore.QRect(105, 310, 101, 31))
        self.AboutButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AboutButton.setStyleSheet("background-color: rgb(47, 49, 54);\n"
                                       "border-radius: 3;\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "font: 87 8pt \"Segoe UI Black\";")
        self.AboutButton.setObjectName("AboutButton")
        self.PanelBackground = PYQTHoverLabel(self.CentralWidget)
        self.PanelBackground.setGeometry(QtCore.QRect(0, 0, 326, 36))
        self.PanelBackground.setStyleSheet(
            "background-color: rgb(47, 49, 54);\n"
            "border-top-left-radius: 10;\n"
            "border-top-right-radius: 10;\n")
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
        self.WindowTitle = PYQTHoverLabel(self.CentralWidget)
        self.WindowTitle.setGeometry(QtCore.QRect(10, 7, 120, 21))
        self.WindowTitle.setStyleSheet("color: rgb(175, 177, 181);\n"
                                       "font: 87 10pt \"Segoe UI Black\";")
        self.StatusInputHint.setStyleSheet("color: rgb(175, 177, 181);\n"
                                           "font: 87 8pt \"Segoe UI Black\";")
        self.WindowTitle.setAlignment(QtCore.Qt.AlignLeading
                                      | QtCore.Qt.AlignLeft
                                      | QtCore.Qt.AlignVCenter)
        self.WindowTitle.setObjectName("WindowTitle")
        self.WindowTitle.setText('Anicord - 1.4')

        Window.setCentralWidget(self.CentralWidget)

        Window.setWindowTitle("Anicord")
        self.AuthInputHint.setText("ТОКЕН УЧЁТНОЙ ЗАПИСИ")
        self.StatusInputHint.setText("СТАТУСЫ (ПО ОДНОМУ НА СТРОКУ)")
        self.DelayHint.setText("ЗАДЕРЖКА")
        self.DelayHintSecText.setText("СЕК")
        self.WorkerButton.setText("Пуск")
        self.AboutButton.setText("О программе")
        self.ActionLock.setIcon(QtGui.QIcon(folder + 'pin.png'))
        self.ActionClose.setIcon(QtGui.QIcon(folder + 'close.png'))
        self.ActionHide.setIcon(QtGui.QIcon(folder + 'hide.png'))

        QtCore.QMetaObject.connectSlotsByName(Window)

        self.ActionClose.clicked.connect(self.WindowClose)
        self.AboutButton.clicked.connect(self.About)
        self.ActionHide.clicked.connect(self.WindowHide)
        self.ActionLock.clicked.connect(self.PinWindow)

        self.ActionClose.HoverSignal.connect(self.CloseButtonHover)
        self.ActionHide.HoverSignal.connect(self.HideButtonHover)
        self.WorkerButton.HoverSignal.connect(self.MainButtonHover)
        self.ActionLock.HoverSignal.connect(self.LockButtonHover)
        self.PanelBackground.HoverSignal.connect(self.PanelBackgroundHover)
        self.WindowTitle.HoverSignal.connect(self.PanelBackgroundHover)

        self.MainButtonChangeSignal.connect(self.MainButtonChangeEvent)
        self.TokenInputHintChangeSignal.connect(self.TokenInputChangeEvent)
        self.StatusesInputChangeSignal.connect(self.StatusesInputChangeEvent)
        self.WindowClsSignal.connect(self.WindowClsEvent)

        self.WorkerButton.clicked.connect(self.Work)

    def WindowClsEvent(self, event):
        if event == 'hide':
            self.showMinimized()
        elif event == 'show':
            self.showNormal()

    def ListenDocsWindowClose(self):
        self.WindowClsSignal.emit('hide')
        time.sleep(.05)
        while ApplicationState.DocsWindowIsOpened:
            if self.isActiveWindow():
                self.WindowClsSignal.emit('hide')
            time.sleep(.05)

        self.WindowClsSignal.emit('show')

    def About(self):
        threading.Thread(target=self.ListenDocsWindowClose).start()
        ApplicationState.DocsWindowIsOpened = True
        global AboutWindow
        AboutWindow = DocsWindow()
        AboutWindow.show()

    def PanelBackgroundHover(self, event):
        if event == 'enterEvent':
            ApplicationState.AllowWindowMove = True
        else:
            ApplicationState.AllowWindowMove = False

    def Work(self):
        threading.Thread(target=self._work).start()

    def _work(self):
        self.MainButtonHover = False

        if self.TokenInput.text().lower() == 'украина':
            self.TokenInputHintChangeSignal.emit({
                'text':
                'ТОКЕН УЧЁТНОЙ ЗАПИСИ - ШИШ ХОХОЛ',
                'style':
                "color: rgb(59, 165, 93);\n"
                "font: 87 8pt \"Segoe UI Black\";"
            })
            return

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
                'СТАТУСЫ - НЕВЕРЕНЫ',
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

        token = self.TokenInput.text()

        if 'token:""' in token:
            token = token.replace('token:""', '').replace('""', '')

        try:
            print(token)
            response = requests.get(
                'https://discord.com/api/v9/users/@me/library',
                headers={'Authorization': token})
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

        client = discontrol.Client(token, False)

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

        if not self.IsWorking:
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
        if ApplicationState.AllowWindowMove:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = event.pos()
            except:
                pass

    def mouseReleaseEvent(self, event):
        if ApplicationState.AllowWindowMove:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = None
            except:
                pass

    def mouseMoveEvent(self, event):
        if ApplicationState.AllowWindowMove:
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