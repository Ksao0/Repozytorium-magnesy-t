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

# Inicjalizacja modułu colorama (do kolorowego tekstu)
# Fore.RED
# Style.BRIGHT
# Style.RESET_ALL
init()

try:
    path = os.path.join(os.getcwd(), "Ank.txt")

    # Usuń plik jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    print(Fore.CYAN + 'Jaką wersję programu chcesz pobrać:\n1: Wersja stabilna\n2: Wersja wstępna (zalecana)\n')

    wersja_programu = int(input(Fore.CYAN + "Podaj wersję programu: "))
    if wersja_programu == 1:
        os.system('cls')
        # ścieżka do pliku main.py w bieżącym folderze
        path = os.path.join(os.getcwd(), "main.py")

        # usuń plik main.py, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
        # print("Usunięto plik main.py")
        # pobierz plik main.py z repozytorium
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/main.py"
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
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/Aktualizator_aktualizatora.py"
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
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/version.txt"
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

        # ścieżka do pliku Zapisy.txt w bieżącym folderze
        path = os.path.join(os.getcwd(), "zapisy.txt")

        # zapisz zawartość pliku zapisy.txt do zmiennej stara_zapisy
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                stara_zapisy = f.read()
        else:
            stara_zapisy = ""

        # usuń plik zapisy.txt, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
        # print("Usunięto plik zapisy.txt")

        # Sprawdzenie, czy plik istnieje i ewentualne jego utworzenie
        if not os.path.isfile("Zapisy.txt"):
            open("Zapisy.txt", "w", encoding='utf-8').close()

        with open("Zapisy.txt", "a", encoding='utf-8') as plik:
            plik.write(
                f"\n          Zaktualizowano program do nowej wersji! data: {data_obliczenia}\n")
            plik.write(f"           Stara wersja: {stara_version}\n")
            plik.write(f"           Nowa wersja: {nowa_version}\n\n")
            plik.write(stara_zapisy)

        print(Fore.LIGHTMAGENTA_EX + f"Stara wersja: {stara_version}\n")
        print(Fore.CYAN + f"Nowa wersja: {nowa_version}\n\n")

        # NOWE FUNKCJE

        # Kasowanie Uruchamianie.py

        # nazwa pliku
        nazwa_pliku = 'Uruchamianie.py'

        # usuń plik o nazwie 'Uruchamianie.py', jeśli taki istnieje
        if os.path.exists(nazwa_pliku):
            os.remove(nazwa_pliku)
            print(f'Usunięto plik {nazwa_pliku}.')

        # Koniec dla: Kasowanie Uruchamianie.py

        # Aktualizacja pliku Aktualizator_aktualizatora

        # ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
        path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

        # usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
        # print("Usunięto plik Aktualizator_aktualizatora.py")
        # pobierz plik main.py z repozytorium
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/Aktualizator_aktualizatora.py"
        urllib.request.urlretrieve(url, path)
        # print("Zastąpiono plik Aktualizator_aktualizatora.py")
        print(Fore.GREEN + 'Zakończono aktualizację I poziomu')
        # Koniec dla: Aktualizacja pliku Aktualizator_aktualizatora

        # KONIEC NOWYCH FUNKCJI
    elif wersja_programu == 2:
        url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/lista_b.txt'
        response = requests.get(url)
        response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
        lista_b_online = response.content.decode('utf-8').strip()

        lista_b_online_lines = lista_b_online.split('\n')

        # Odczytaj zawartość pliku lista_b.txt na komputerze
        path = os.path.join(os.getcwd(), "lista_b.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                lista_b_local = f.read().strip()
        else:
            lista_b_local = "BRAK PLIKU"

        lista_b_local_lines = lista_b_local.split('\n')

        niepobrane_biblioteki = set(
            lista_b_online_lines) - set(lista_b_local_lines)

        if niepobrane_biblioteki:
            print(
                "\nZainstaluj biblioteki z tej listy, ich niepobranie grozi nieodwracalnym uszkodzeniem kodu.\nAby zainstalować: pip install NAZWA_BIBLIOTEKI:")
            for biblioteka in niepobrane_biblioteki:
                print(f"{biblioteka}")

        os.system('cls')
        print(Fore.YELLOW + 'Zainstaluj poniższe biblioteki komendą pip install NAZWA BIBLIOTEKI w terminalu cmd:' + Fore.CYAN +
              '\n - os\n - tkinter\n - messagebox\n - scrolledtext\n - time\n - datetime\n - urllib\n - request  (dwie biblioteki o podobnej nazwie)\n - requests (dwie biblioteki o podobnej nazwie)\n - subprocess\n')
        input(Fore.YELLOW + "Naciśnij klawisz Enter, aby potwierdzić, że masz zainstalowane powyższe biblioteki.\nNie odpowiadamy za błędy związane z ich nie pobraniem...")
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

        # ścieżka do pliku Zapisy.txt w bieżącym folderze
        path = os.path.join(os.getcwd(), "zapisy.txt")

        # zapisz zawartość pliku zapisy.txt do zmiennej stara_zapisy
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                stara_zapisy = f.read()
        else:
            stara_zapisy = ""

        # usuń plik zapisy.txt, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
        # print("Usunięto plik zapisy.txt")

        # Sprawdzenie, czy plik istnieje i ewentualne jego utworzenie
        if not os.path.isfile("Zapisy.txt"):
            open("Zapisy.txt", "w", encoding='utf-8').close()

        with open("Zapisy.txt", "a", encoding='utf-8') as plik:
            plik.write(
                f"\n          Zaktualizowano program do nowej wersji! data: {data_obliczenia}\n")
            plik.write(f"           Stara wersja: {stara_version}\n")
            plik.write(f"           Nowa wersja: {nowa_version}\n\n")
            plik.write(stara_zapisy)

        print(Fore.LIGHTMAGENTA_EX + f"Stara wersja: {stara_version}\n")
        print(Fore.CYAN + f"Nowa wersja: {nowa_version}\n\n")

        # NOWE FUNKCJE

        # Kasowanie Uruchamianie.py

        # nazwa pliku
        nazwa_pliku = 'Uruchamianie.py'

        # usuń plik o nazwie 'Uruchamianie.py', jeśli taki istnieje
        if os.path.exists(nazwa_pliku):
            os.remove(nazwa_pliku)
            print(f'Usunięto plik {nazwa_pliku}.')

        # Koniec dla: Kasowanie Uruchamianie.py

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
        print(Fore.GREEN + 'Zakończono aktualizację I poziomu')
        # Koniec dla: Aktualizacja pliku Aktualizator_aktualizatora

        # KONIEC NOWYCH FUNKCJI
    else:
        print(Fore.MAGENTA + 'Nie ma takiej opcji, anulowano')
        exit()
except Exception as e:
    messagebox.showerror('Nie można wykonać aktualizacji',
                         'Wystąpł błąd, który uniemożliwił wykonanie aktualizacji')
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
    issue_title = 'Automatyczne zgłoszenie błędu z Aktualizacja.py'
    a = traceback.format_exc()
    issue_body = f"Błąd funkcji Aktualizacja.py:\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

    # autentykacja
    g = Github(username, password)

    # pobierz repozytorium
    repo = g.get_repo(repository_name)

    # utwórz nowe zgłoszenie błędu
    repo.create_issue(title=issue_title, body=issue_body)

    messagebox.showinfo("Problem został zgłoszony",
                        "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
    exit()
