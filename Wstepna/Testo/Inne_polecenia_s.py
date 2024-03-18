from PyQt5.QtWidgets import QMessageBox, QPushButton, QFileDialog
from PyQt5 import QtWidgets
import win32com.client
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from github import Github
import requests
import time
import subprocess
import urllib.request
import urllib
import datetime
import messagebox
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDoubleSpinBox, QLabel, QSpinBox, QTextEdit, QProgressBar
import os
import sys
import threading
import shutil

from win10toast import ToastNotifier

from packaging import version

# Minimalizowanie cmd
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)



class Komunikacja_okno(QWidget):
    def __init__(self):
        super().__init__()

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        # Tworzymy układ siatkowy dla okna rozszerzeń
        układ = QGridLayout()

        text_edit_historia = QTextEdit(self)
        układ.addWidget(text_edit_historia, 1, 0, 6, 3)

        text_edit_historia.setPlainText("Tu będzie się pojawiać twoja historia rozmowy:")

        # Ustawiamy układ dla okna rozszerzeń
        self.setLayout(układ)

        # Ustawiamy tytuł i rozmiar okna rozszerzeń
        self.setWindowTitle('Lista rozszerzeń')
        self.setGeometry(1300, 300, 400, 320)

if __name__ == '__main__':

    # Inicjalizujemy aplikację
    app = QApplication(sys.argv)

    # Uruchamiamy pętlę główną
    sys.exit(app.exec_())