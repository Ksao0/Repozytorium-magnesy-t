import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests

# pobierz zawartość pliku version.txt z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/version.txt'
response = requests.get(url)

version_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku version.txt w twoim programie
path = os.path.join(os.getcwd(), "version.txt")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        version_local = f.read().strip()
else:
    version_local = "BRAK DANYCH"

# wyświetl tylko pierwszą linijkę wersji
version_local_first_line = version_local.split('\n')[0]
version_online_first_line = version_online.split('\n')[0]

# porównaj wersje
print(f'\nWersja na komputerze: {version_local_first_line}')
print(f'Wersja w repozytorium: {version_online_first_line}')
if version_local_first_line == version_online_first_line:
  aktul_wersja = 0
else:
  aktul_wersja = 1


  # pobierz zawartość pliku main.py z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/main.py'
response = requests.get(url)

main_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku main.py w twoim programie
path = os.path.join(os.getcwd(), "main.py")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        main_local = f.read().strip()
else:
    main_local = "BRAK DANYCH"

# wyświetl tylko pierwszą linijkę wersji
main_local_first_line = version_local.split('\n')[0]
main_online_first_line = version_online.split('\n')[0]

# porównaj wersje
print(f'\nWersja na komputerze: {main_local_first_line}')
print(f'Wersja w repozytorium: {main_online_first_line}')
if main_local_first_line == main_online_first_line:
  aktul_main = 0
  print(
else:
  aktul_main = 1
  
