import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests
from time import sleep
from github import Github
import sys
import traceback
import matplotlib.pyplot as plt

try:
    # ścieżka do pliku main.py w bieżącym folderze
    path = os.path.join(os.getcwd(), "main.py")

    # usuń plik main.py, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # print("Usunięto plik main.py")
    # pobierz plik main.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/main.py"
    urllib.request.urlretrieve(url, path)
    # print("Zastąpiono plik main.py")

    # Aktualizacja pliku Aktualizator_aktualizatora

    # ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
    path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

    # usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # print("Usunięto plik Aktualizator_aktualizatora.py")
    # pobierz plik main.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Aktualizator_aktualizatora.py"
    urllib.request.urlretrieve(url, path)
    # print("Zastąpiono plik Aktualizator_aktualizatora.py")

    # Koniec dla: Aktualizacja pliku Aktualizator_aktualizatora

    # ścieżka do pliku version.txt w bieżącym folderze
    path = os.path.join(os.getcwd(), "version.txt")

    # zapisz zawartość pliku version.txt do zmiennej stara_version
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as f:
            stara_version = f.read()
    else:
        stara_version = "BRAK DANYCH"

    # usuń plik version.txt, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # print("Usunięto plik version.txt")

    # pobierz plik version.txt z repozytorium i utwórz go
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt"
    urllib.request.urlretrieve(url, path)
    # print("Zastąpiono plik version.txt")

    # odczytaj zawartość pliku version.txt do zmiennej nowa_version
    with open(path, "r", encoding='utf-8') as f:
        nowa_version = f.read()

    now = datetime.datetime.now()
    data_obliczenia = now.strftime("%d.%m.%Y %H:%M:%S")

    # Sprawdzenie, czy plik istnieje i ewentualne jego utworzenie
    if not os.path.isfile("Zapisy.txt"):
        open("Zapisy.txt", "w", encoding='utf-8').close()

    # Aktualizacja pliku Aktualizator_aktualizatora

    # ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
    path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

    # usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # print("Usunięto plik Aktualizator_aktualizatora.py")
    # pobierz plik main.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Aktualizator_aktualizatora.py"
    urllib.request.urlretrieve(url, path)
    # print("Zastąpiono plik Aktualizator_aktualizatora.py")

    # ścieżka do pliku lista_b.txt w bieżącym folderze
    path = os.path.join(os.getcwd(), "lista_b.txt")

    # usuń plik lista_b.txt, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # print("Usunięto plik lista_b.txt")
    # pobierz plik main.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/lista_b.txt"
    urllib.request.urlretrieve(url, path)
    # print("Zastąpiono plik lista_b.txt")

except Exception as e:
    # obsługa błędu i wyświetlenie dokładniejszych informacji o błędzie
    exc_type, exc_value, exc_traceback = sys.exc_info()
    # Odczytaj zawartość pliku Develop.txt w twoim programie
    path = os.path.join(os.getcwd(), "Develop.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            plik_od_dewelopera = f.read().strip()
    else:
        plik_od_dewelopera = "BRAK PLIKU D"
        messagebox.showerror(
            "Błąd", 'Poproś twórcę programu o informacje')

    if plik_od_dewelopera != "BRAK PLIKU D":
        informacje_do_zgloszenia = plik_od_dewelopera.split('\n')
        nazwa_uzytkownika = informacje_do_zgloszenia[0]
        token_do_wpisania = informacje_do_zgloszenia[1]

        # pobierz datę wygaśnięcia
        wygasa_dnia = int(informacje_do_zgloszenia[2])
        wygasa_miesiaca = int(informacje_do_zgloszenia[3])
        wygasa_roku = int(informacje_do_zgloszenia[4])

        # utwórz obiekt daty z daty wygaśnięcia
        wygasa_data = datetime.date(
            wygasa_roku, wygasa_miesiaca, wygasa_dnia)

        # pobierz dzisiejszą datę
        dzisiaj = datetime.date.today()
        # porównaj daty
        if dzisiaj > wygasa_data:
            messagebox.showerror(
                "Czas minął", "Zgłoś się do osoby odpowiadającej za program")
            exit()
        elif dzisiaj == wygasa_data:
            messagebox.showwarning(
                "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
    else:
        messagebox.showwarning(
            'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
        exit()

    # ustawienia konta
    username = f'{nazwa_uzytkownika}'
    password = f'{token_do_wpisania}'
    repository_name = 'Ksao0/Repozytorium-magnesy-t'
    issue_title = 'Automatyczne zgłoszenie błędu z WEW.py'
    a = traceback.format_exc()
    issue_body = f"Błąd funkcji WEW.py:\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

    # autentykacja
    g = Github(username, password)

    # pobierz repozytorium
    repo = g.get_repo(repository_name)

    # utwórz nowe zgłoszenie błędu
    repo.create_issue(title=issue_title, body=issue_body)

    messagebox.showinfo("Problem został zgłoszony",
                        "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
    exit()
