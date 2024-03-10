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
import time
import requests
import threading

from github import Github


# while True:
#     def ta():
#         # Pobierz zawartość pliku version.txt z repozytorium na GitHub
#         try:
#             url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version.txt'
#             response = requests.get(url)
#             response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
#             version_online = response.content.decode('utf-8').strip()
#         except requests.exceptions.RequestException as e:
#             return
#
#         wstepna_version_online_lines = version_online.split('\n')
#         if wstepna_version_online_lines[1] == "Status: yN":
#             return
#
#         # Odczytaj zawartość pliku version.txt w twoim programie
#         path = os.path.join(os.getcwd(), "version.txt")
#         if os.path.exists(path):
#             with open(path, "r", encoding="utf-8") as f:
#                 version_local = f.read().strip()
#         else:
#             version_local = "BRAK DANYCH"
#
#         version_online_lines = version_online.split('\n')
#         version_local_lines = version_local.split('\n')
#
#         # Nowa wersja (bez nowych bibliotek)
#         if version_online_lines[0] != version_local_lines[0] and (version_online_lines[4] == version_local_lines[4]):
#             try:
#                 url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/main2.txt'
#                 response = requests.get(url)
#                 response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
#                 lista_b_online = response.content.decode('utf-8').strip()
#             except requests.exceptions.RequestException as e:
#                 messagebox.showerror(
#                     "Błąd", f'Wystąpił błąd połączenia z internetem. Spróbuj ponownie później')
#                 return

def otworz_main2():
    time.sleep(1)
    subprocess.run(["python", "main2.py"])
