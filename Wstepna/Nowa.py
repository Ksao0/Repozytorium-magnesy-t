import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests
from time import sleep

informacje_wersji = tk.Tk()
informacje_wersji.title(f"Informacje o tej wersji")
informacje_wersji.geometry("700x500")

zapis_do_pliku = tk.BooleanVar()
zapis_do_pliku.set(True)

version_online = "BRAK DANYCH"

# Pobierz zawartość pliku version.txt z repozytorium na GitHub
try:
    url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt'
    response = requests.get(url)
    response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
    version_online = response.content.decode('utf-8').strip()
except:
    messagebox.showerror(
        "Błąd", f'Wystąpił błąd połączenia z internetem. Nie można pobrać informacji o najnowszej wersji.')

# Odczytaj zawartość pliku version.txt w twoim programie
path = os.path.join(os.getcwd(), "version.txt")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        version_local = f.read().strip()
else:
    version_local = "BRAK DANYCH"

version_online_lines = version_online.split('\n')
version_local_lines = version_local.split('\n')

label_informacja_wersji = tk.Label(
    informacje_wersji, text=f"Wersja na komputerze: {version_local_lines[0]}", justify="left")
label_informacja_wersji.pack()
label_informacja_wersji = tk.Label(
    informacje_wersji, text=f"Status: {version_local_lines[1]}", justify="left")
label_informacja_wersji.pack()
label_informacja_wersji = tk.Label(
    informacje_wersji, text=f"Numer poprawki: {version_local_lines[2]}", justify="left")
label_informacja_wersji.pack()
pustka = tk.Label()
pustka.pack()
pustka = tk.Label()
pustka.pack()
label_informacja_wersji = tk.Label(
    informacje_wersji, text=f"Najnowsza wersja: {version_online_lines[0]}", justify="left")
label_informacja_wersji.pack()
label_informacja_wersji = tk.Label(
    informacje_wersji, text=f"Status: {version_online_lines[1]}", justify="left")
label_informacja_wersji.pack()
label_informacja_wersji = tk.Label(
    informacje_wersji, text=f"Numer poprawki: {version_online_lines[2]}", justify="left")

# Dodanie kontenera typu Frame
frame_przyciski = tk.Frame(informacje_wersji)
frame_przyciski.pack()
informacje_wersji.mainloop()
