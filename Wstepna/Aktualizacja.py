import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests
import time
from time import sleep
from github import Github
import sys
import traceback
import matplotlib.pyplot as plt
from colorama import init, Fore, Style
from tqdm import tqdm


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
        messagebox.showerror(
            'Odmowa dostępu', "Ta opcja jest nadrzędnie zablokowana. Spróbuj ponownie za kilka godzin lub dni")
        exit()


klamstwo_fun()

# Inicjalizacja modułu colorama (do kolorowego tekstu)
# Fore.RED
# Style.BRIGHT
# Style.RESET_ALL
init()


def blokada_dostepu():
    messagebox.showerror(
        'Blokada dostępu', 'Ta wersja ma blokadę dostępu, została ona nałożona przez wydawcę programu. Nie można więc jej zainstalować. Pozostań w aktualnym nurcie')
    os.system('cls')
    print(Fore.YELLOW + "Rozpoczynanie aktualizacji II poziomu")
    print(Fore.GREEN + "Zakończono aktualizację II poziomu\n")
    print(Fore.YELLOW + 'Rozpoczynanie aktualizacji I poziomu')


od_nowa = 1
while od_nowa == 1:
    try:
        print(Fore.CYAN + 'Jaką wersję programu chcesz pobrać:\n1: Wersja stabilna\n2: Wersja Beta (zalecana)\n')

        wersja_programu = int(input(Fore.CYAN + "Podaj wersję programu: "))
        if wersja_programu == 1:
            os.system('cls')
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/version.txt'
            response = requests.get(url)
            response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
            wstepna_version_online = response.content.decode('utf-8').strip()
            wstepna_version_online_lines = wstepna_version_online.split('\n')
            if wstepna_version_online_lines[1] != "Status: yN":
                os.system('cls')
                try:
                    url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/lista_b.txt'
                    response = requests.get(url)
                    response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
                    lista_b_online = response.content.decode('utf-8').strip()
                except requests.exceptions.RequestException as e:
                    print(
                        "Błąd", f'Wystąpił błąd połączenia z internetem. Spróbuj ponownie później')
                    exit()

                # Odczytaj zawartość pliku lista_b.txt na komputerze
                path = os.path.join(os.getcwd(), "lista_b.txt")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        lista_b_local = f.read().strip()
                else:
                    lista_b_local = "BRAK PLIKU"

                lista_b_online_lines = lista_b_online.split('\n')
                lista_b_local_lines = lista_b_local.split('\n')

                niepobrane_biblioteki = set(
                    lista_b_online_lines) - set(lista_b_local_lines)

                if niepobrane_biblioteki:
                    print(
                        Fore.YELLOW + "\n\nWykryliśmy, że nie posiadasz bibliotek z tej listy, które są wymagane:")
                    print(Fore.LIGHTGREEN_EX +
                          "Aby to zrobić otwórz terminal cmd i wpisz:")
                    print("   pip install (nazwa biblioteki)")
                    print("Przykład:")
                    print("   pip install tkinter", Style.RESET_ALL)
                    print()
                    print(Fore.YELLOW + 'Lista wymaganych bibliotek:',
                          Style.RESET_ALL)

                    for biblioteka in lista_b_online_lines:
                        if biblioteka == "BRAK PLIKU":
                            continue
                        elif biblioteka in lista_b_local_lines:
                            print(Fore.LIGHTGREEN_EX + biblioteka)
                        else:
                            print(Fore.RED + biblioteka)

                    input(Fore.YELLOW + "Naciśnij klawisz Enter, aby zakończyć...")
                else:
                    print(Fore.GREEN + "Wszystkie biblioteki pobrane.")

                # Lista plików do pobrania
                files_to_download = [
                    {
                        "name": "main.py",
                        "display_name": "Plik główny",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/main.py"
                    },
                    {
                        "name": "lista_b.txt",
                        "display_name": "Biblioteki",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/lista_b.txt"
                    },
                    {
                        "name": "Aktualizator_aktualizatora.py",
                        "display_name": "Pliki aktualizacyjne (1/3)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/Aktualizator_aktualizatora.py"
                    },
                    {
                        "name": "version.txt",
                        "display_name": "Pliki aktualizacyjne (2/3)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/version.txt"
                    },
                    {
                        "name": "Aktualizator_aktualizatora.py",
                        "display_name": "Pliki aktualizacyjne (3/3)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/Aktualizator_aktualizatora.py"
                    },
                    {
                        "name": "main.py",
                        "display_name": "Kończenie (1/2)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/main.py"
                    },                    {
                        "name": "version.txt",
                        "display_name": "Kończenie (2/2)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Stara/version.txt"
                    }
                ]

                # Funkcja do śledzenia postępu pobierania
                def show_progress(chunk_size, total_size):
                    progress_bar.update(chunk_size)

                # Funkcja do formatowania czasu w sekundach do formatu MM:SS
                def format_time(seconds):
                    return time.strftime("%M:%S", time.gmtime(seconds))

                # Pobierz rozmiary plików
                file_sizes = [int(requests.head(file["url"]).headers.get(
                    "Content-Length", -1)) for file in files_to_download]

                # Inicjalizacja paska postępu
                total_size = sum(file_sizes)
                progress_bar = tqdm(total=total_size, unit="B",
                                    unit_scale=True, leave=False)

                try:
                    # Pobieranie plików
                    for file_info, file_size in zip(files_to_download, file_sizes):
                        progress_bar.set_description(
                            f"Aktualizowanie: {file_info['display_name']} | {file_size / (1024 ** 1):.1f} KiB")
                        response = requests.get(file_info["url"], stream=True)

                        with open(file_info["name"], 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                                show_progress(len(chunk), total_size)

                        speed = progress_bar.format_dict.get('rate', 0)
                        remaining_time = progress_bar.format_dict.get(
                            'remaining', 0)
                        if speed is not None and remaining_time is not None:
                            progress_bar.set_postfix(
                                speed=f"{speed:.0f} KiB/s", eta=format_time(remaining_time))
                        progress_bar.refresh()

                    print("\nPobieranie zakończone...")
                    sleep(1)
                except Exception as e:
                    print(Fore.RED + f"Wystąpił błąd" + Style.RESET_ALL)
                finally:
                    # Zakończenie paska postępu
                    progress_bar.close()

                print("\nAktualizowanie zakończone!")

                # KONIEC NOWYCH FUNKCJI
                od_nowa = 0
            else:
                blokada_dostepu()
        elif wersja_programu == 2:
            os.system('cls')
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt'
            response = requests.get(url)
            response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
            wstepna_version_online = response.content.decode('utf-8').strip()
            wstepna_version_online_lines = wstepna_version_online.split('\n')
            if wstepna_version_online_lines[1] != "Status: yN":
                os.system('cls')
                try:
                    url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/lista_b.txt'
                    response = requests.get(url)
                    response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
                    lista_b_online = response.content.decode('utf-8').strip()
                except requests.exceptions.RequestException as e:
                    print(
                        "Błąd", f'Wystąpił błąd połączenia z internetem. Spróbuj ponownie później')
                    exit()

                # Odczytaj zawartość pliku lista_b.txt na komputerze
                path = os.path.join(os.getcwd(), "lista_b.txt")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        lista_b_local = f.read().strip()
                else:
                    lista_b_local = "BRAK PLIKU"

                lista_b_online_lines = lista_b_online.split('\n')
                lista_b_local_lines = lista_b_local.split('\n')

                niepobrane_biblioteki = set(
                    lista_b_online_lines) - set(lista_b_local_lines)

                if niepobrane_biblioteki:
                    print(
                        Fore.YELLOW + "\n\nWykryliśmy, że nie posiadasz bibliotek z tej listy, które są wymagane:")
                    print(Fore.LIGHTGREEN_EX +
                          "Aby to zrobić otwórz terminal cmd i wpisz:")
                    print("   pip install (nazwa biblioteki)")
                    print("Przykład:")
                    print("   pip install tkinter", Style.RESET_ALL)
                    print()
                    print(Fore.YELLOW + 'Lista wymaganych bibliotek:',
                          Style.RESET_ALL)

                    for biblioteka in lista_b_online_lines:
                        if biblioteka == "BRAK PLIKU":
                            continue
                        elif biblioteka in lista_b_local_lines:
                            print(Fore.LIGHTGREEN_EX + biblioteka)
                        else:
                            print(Fore.RED + biblioteka)

                    input(Fore.YELLOW + "Naciśnij klawisz Enter, aby zakończyć...")
                else:
                    print(Fore.GREEN + "Wszystkie biblioteki pobrane.")

                # Lista plików do pobrania
                # Lista plików do pobrania
                files_to_download = [
                    {
                        "name": "main.py",
                        "display_name": "Plik główny",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/main.py"
                    },
                    {
                        "name": "lista_b.txt",
                        "display_name": "Biblioteki",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/lista_b.txt"
                    },
                    {
                        "name": "Aktualizator_aktualizatora.py",
                        "display_name": "Pliki aktualizacyjne (1/3)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Aktualizator_aktualizatora.py"
                    },
                    {
                        "name": "version.txt",
                        "display_name": "Pliki aktualizacyjne (2/3)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt"
                    },
                    {
                        "name": "Aktualizator_aktualizatora.py",
                        "display_name": "Pliki aktualizacyjne (3/3)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Aktualizator_aktualizatora.py"
                    },
                    {
                        "name": "main.py",
                        "display_name": "Kończenie (1/2)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/main.py"
                    },                    {
                        "name": "version.txt",
                        "display_name": "Kończenie (2/2)",
                        "url": "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt"
                    }
                ]
                # Funkcja do śledzenia postępu pobierania

                def show_progress(chunk_size, total_size):
                    progress_bar.update(chunk_size)

                # Funkcja do formatowania czasu w sekundach do formatu MM:SS
                def format_time(seconds):
                    return time.strftime("%M:%S", time.gmtime(seconds))

                # Pobierz rozmiary plików
                file_sizes = [int(requests.head(file["url"]).headers.get(
                    "Content-Length", -1)) for file in files_to_download]

                # Inicjalizacja paska postępu
                total_size = sum(file_sizes)
                progress_bar = tqdm(total=total_size, unit="B",
                                    unit_scale=True, leave=False)

                try:
                    # Pobieranie plików
                    for file_info, file_size in zip(files_to_download, file_sizes):
                        progress_bar.set_description(
                            f"Aktualizowanie: {file_info['display_name']} | {file_size / (1024 ** 1):.1f} KiB")
                        response = requests.get(file_info["url"], stream=True)

                        with open(file_info["name"], 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                                show_progress(len(chunk), total_size)

                        speed = progress_bar.format_dict.get('rate', 0)
                        remaining_time = progress_bar.format_dict.get(
                            'remaining', 0)
                        if speed is not None and remaining_time is not None:
                            progress_bar.set_postfix(
                                speed=f"{speed:.0f} KiB/s", eta=format_time(remaining_time))
                        progress_bar.refresh()

                    print("\nPobieranie zakończone...")
                    sleep(1)
                except Exception as e:
                    print(Fore.RED + f"Wystąpił błąd" + Style.RESET_ALL)
                finally:
                    # Zakończenie paska postępu
                    progress_bar.close()

                print("\nAktualizowanie zakończone!")

                # KONIEC NOWYCH FUNKCJI
                od_nowa = 0
            else:
                blokada_dostepu()
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
