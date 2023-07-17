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
from colorama import init, Fore, Style

global klamstwo
klamstwo = False


def klamstwo_fun():
    # Pobierz zawartość pliku prefvers.txt z repozytorium na GitHub
    url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/prefvers.txt'
    response = requests.get(url)
    response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
    prefvers = response.content.decode('utf-8').strip()
    prefvers_lines = prefvers.split('\n')

    # Odczytaj zawartość pliku version.txt w twoim programie
    path = os.path.join(os.getcwd(), "version.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            version_local = f.read().strip()
    else:
        version_local = "BRAK DANYCH"

    version_local_first_line = version_local.split('\n')[0]

    # Porównaj każdą linijkę w prefvers z pierwszą linijką version_local
    if version_local_first_line in prefvers_lines:
        global klamstwo
        klamstwo = True
        return
    if klamstwo == True:
        messagebox.showerror(
            'Brak dostępu', "Ta opcja jest nadrzędnie zablokowana. Spróbuj ponownie za kilka godzin lub dni")
        exit()


klamstwo_fun()

# Inicjalizacja modułu colorama (do kolorowego tekstu)
# Fore.RED
# Style.BRIGHT
# Style.RESET_ALL
init()

try:
    # Ścieżka do pliku Aktualizacja.py w bieżącym folderze
    path = os.path.join(os.getcwd(), "Aktualizacja.py")

    # Usuń plik Aktualizacja.py, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    print(Fore.YELLOW + "Rozpoczynanie aktualizacji II poziomu")
    # Pobierz plik Aktualizacja.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Aktualizacja.py"
    urllib.request.urlretrieve(url, path)
    print(Fore.GREEN + "Zakończono aktualizację II poziomu\n")
    print(Fore.YELLOW + 'Rozpoczynanie aktualizacji I poziomu')

    Aktualizacja = ["python", "Aktualizacja.py"]
    subprocess.run(Aktualizacja)

    input(Fore.CYAN + "Naciśnij klawisz Enter, aby zakończyć...")
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
    issue_title = 'Automatyczne zgłoszenie błędu z Aktualizator_aktualizatora.py'
    a = traceback.format_exc()
    issue_body = f"Błąd funkcji Aktualizator_aktualizatora.py:\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

    # autentykacja
    g = Github(username, password)

    # pobierz repozytorium
    repo = g.get_repo(repository_name)

    # utwórz nowe zgłoszenie błędu
    repo.create_issue(title=issue_title, body=issue_body)

    messagebox.showinfo("Problem został zgłoszony",
                        "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
    exit()
