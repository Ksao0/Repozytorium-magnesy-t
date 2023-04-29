import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests
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

# porównaj wersje
if version_local == version_online:
    aktul_wersja = 0
else:
    aktul_wersja = 1

# pobierz zawartość pliku Aktualizacja.py z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Aktualizacja.py'
response = requests.get(url)

Aktualizacja_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku Aktualizacja.py w twoim programie
path = os.path.join(os.getcwd(), "Aktualizacja.py")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        Aktualizacja_local = f.read().strip()
else:
    Aktualizacja_local = "BRAK DANYCH"

# porównaj wersje
if Aktualizacja_local == Aktualizacja_online:
    aktul_Aktualizacja = 0
else:
    aktul_Aktualizacja = 1

# pobierz zawartość pliku Aktualizator_aktualizatora.py z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Aktualizator_aktualizatora.py'
response = requests.get(url)

Aktualizator_aktualizatora_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku Aktualizator_aktualizatora.py w twoim programie
path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        Aktualizator_aktualizatora_local = f.read().strip()
else:
    Aktualizator_aktualizatora_local = "BRAK DANYCH"

# porównaj wersje
if Aktualizator_aktualizatora_local == Aktualizator_aktualizatora_online:
    aktul_Aktualizator_aktualizatora = 0
else:
    aktul_Aktualizator_aktualizatora = 1

# pobierz zawartość pliku Obecnosc.py z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Obecnosc.py'
response = requests.get(url)

Obecnosc_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku Obecnosc.py w twoim programie
path = os.path.join(os.getcwd(), "Obecnosc.py")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        Obecnosc_local = f.read().strip()
else:
    Obecnosc_local = "BRAK DANYCH"

# porównaj wersje
if Obecnosc_local == Obecnosc_online:
    aktul_Obecnosc = 0
else:
    aktul_Obecnosc = 1

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

# porównaj wersje
if main_local == main_online:
    aktul_main = 0
else:
    aktul_main = 1

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
  
