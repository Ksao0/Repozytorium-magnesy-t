import sys

import os
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDoubleSpinBox, QLabel, QSpinBox, QTextEdit, QProgressBar
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import messagebox
import datetime
import urllib
import urllib.request
import subprocess
import time                # ścieżka do pliku main.py w bieżącym folderze

path = os.path.join(os.getcwd(), "main.py")

# usuń plik main.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
# print("Usunięto plik main.py")
# pobierz plik main.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/main.py"
urllib.request.urlretrieve(url, path)
# print("Zastąpiono plik main.py")
