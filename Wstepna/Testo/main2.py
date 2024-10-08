from colorama import Fore, Style
from cryptography.fernet import Fernet
import ctypes
import datetime
from functools import lru_cache
from github import Github
import getpass
import zipfile
import gzip
import os
import requests
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox
import urllib
import urllib.request
import win32com.client
from win10toast import ToastNotifier
from packaging import version  # Upewnij się, że ten import jest prawidłowy
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication, QTimer, QThread, pyqtSignal, QRect, QDateTime
from PyQt5.QtGui import QPalette, QColor, QIcon, QPainter, QBrush
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QFileDialog,
    QDoubleSpinBox,
    QSpinBox,
    QTextEdit,
    QProgressBar,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QFrame
)
import random

os.system('cls')
global ustawienie_auto
global ustawienie_sprawdzanie_aktualizacji_w_tle
global zaawansowane_okno_zamkniete
zaawansowane_okno_zamkniete = False

global instalator_sesja
instalator_sesja = 0


class PaletaStylow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.kolory = []

    def set_kolory(self, kolory):
        self.kolory = kolory
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        x = 0
        y = 0
        rozmiar = 18
        padding = 5
        for kolor in self.kolory:
            painter.fillRect(QRect(x, y, rozmiar, rozmiar),
                             QBrush(QColor(kolor)))
            x += rozmiar + padding
            if x + rozmiar > self.width():
                x = 0
                y += rozmiar + padding


class OperacjeNaPliku:
    def __init__(self, nazwa_pliku):
        self.nazwa_pliku = nazwa_pliku

    def podmien_linijke(self, numer_linii, nowa_zawartosc):
        # Otwarcie pliku i odczytanie całej zawartości
        with open(self.nazwa_pliku, 'r', encoding='utf-8') as plik:
            linie = plik.readlines()

        # Sprawdzenie czy numer linii jest prawidłowy
        if numer_linii < 0 or numer_linii >= len(linie):
            print("Błąd: Numer linii jest nieprawidłowy.")
            return

        # Zmiana zawartości wybranej linii
        linie[numer_linii] = nowa_zawartosc + '\n'

        # Zapis zmodyfikowanej zawartości do pliku
        with open(self.nazwa_pliku, 'w', encoding='utf-8') as plik:
            for linia in linie:
                plik.write(linia)


if os.path.isfile("Ustawienia.txt"):
    try:
        with open("Ustawienia.txt", "r", encoding='utf-8') as plik:
            # Odczytanie zawartości i usunięcie białych znaków z końca
            ustawienia = plik.read().strip()
            ustawienia_linie = ustawienia.split('\n')
        if ustawienia_linie[0] == "Tak":
            ustawienie_sprawdzanie_aktualizacji_w_tle = True
        else:
            ustawienie_sprawdzanie_aktualizacji_w_tle = False

        if ustawienia_linie[1] == "Tak":
            ustawienie_auto = True
        else:
            ustawienie_auto = False
    except:
        # Otwarcie pliku w trybie zapisu (nadpisanie istniejącej zawartości)
        with open("Ustawienia.txt", "w", encoding='utf-8') as plik:
            plik.write("Tak\n")
            plik.write("Nie")
        ustawienie_sprawdzanie_aktualizacji_w_tle = True
        messagebox.showwarning(
            "Brak pliku ustawień", "Nie udało się znaleźć pliku z zapisanymi ustawieniami, więc wczytano domyślne wartości")
else:
    # Otwarcie pliku w trybie zapisu (nadpisanie istniejącej zawartości)
    with open("Ustawienia.txt", "w", encoding='utf-8') as plik:
        plik.write("Tak\n")
        plik.write("Nie")
    ustawienie_sprawdzanie_aktualizacji_w_tle = True
    messagebox.showwarning(
        "Brak pliku ustawień", "Nie udało się znaleźć pliku z zapisanymi ustawieniami, więc wczytano domyślne wartości")

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

try:
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca.py"

    response = requests.get(url)
    if response.status_code == 200:
        icon_data = response.content
        filename = os.path.basename(url)

        with open(filename, 'wb') as icon_file:
            icon_file.write(icon_data)
    else:
        print("Nie udało się pobrać pliku.")
except:
    print("Nie udało się pobrać pliku. Połącz się z internetem")

try:
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Klienci.py"

    response = requests.get(url)
    if response.status_code == 200:
        icon_data = response.content
        filename = os.path.basename(url)

        with open(filename, 'wb') as icon_file:
            icon_file.write(icon_data)
    else:
        print("Nie udało się pobrać pliku.")
except:
    print("Nie udało się pobrać pliku. Połącz się z internetem")


def wybierz_styl_z_pliku():
    def styl_awaryjny():
        toaster = Powiadomienia()
        toaster.powiadomienie_jednorazowe(
            tytul_powiadomienia=f"Ten styl too... {styl}?", tresc_powiadomienia=f'Ostatni ustawiony przez ciebie styl to „{styl}“. Taki styl nie istniwięc na razie ustawimy inny styl. Nie zmieniaj danych w plikach', duration=3)
        print('Zapisany styl nie istnieje')

        ustawianie_stylu("ametyst")

        # Otwarcie pliku w trybie zapisu (nadpisanie istniejącej zawartości)
        with open("Styl.txt", "w", encoding='utf-8') as plik:
            plik.write("ametyst")
        print(Fore.LIGHTCYAN_EX +
              ' Zapisano preferencje' + Style.RESET_ALL)
    try:
        # Funkcja do odczytywania zawartości pliku i wybierania stylu

        # Sprawdzenie, czy plik istnieje
        if os.path.isfile("Styl.txt"):
            # Otwarcie pliku do odczytu
            with open("Styl.txt", "r", encoding='utf-8') as plik:
                # Odczytanie zawartości i usunięcie białych znaków z końca
                styl = plik.read().strip()
                if os.path.isfile(f"styl_{styl}.css"):
                    ustawianie_stylu(styl)
                else:
                    try:
                        print('Nie znaleziono pliku arkusza stylu')
                        url = f"https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_{
                            styl}.css"

                        # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
                        nazwa_pliku = f"styl_{styl}.css"
                        response = requests.get(url)

                        if response.status_code == 200:
                            with open(nazwa_pliku, 'wb') as plik:
                                plik.write(response.content)
                            print(Fore.LIGHTBLACK_EX + f'Pobrano styl: {styl}')
                            app.setStyleSheet(open(f'styl_{styl}.css').read())
                            print(Fore.LIGHTBLACK_EX +
                                  f'Ustawiono styl na: {styl}')
                        else:
                            styl_awaryjny()
                    except:
                        styl_awaryjny()
        else:
            try:
                app.setStyleSheet(open('styl_ametyst.css').read())
                print('Nie znaleziono arkusza stylu\n Ustawiono styl na: ametyst')
            except:
                try:
                    try:
                        print('Nie znaleziono pliku arkusza stylu')
                        # Podaj URL pliku, który chcesz pobrać
                        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_ametyst.css"

                        # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
                        nazwa_pliku = "styl_ametyst.css"
                        response = requests.get(url)

                        if response.status_code == 200:
                            with open(nazwa_pliku, 'wb') as plik:
                                plik.write(response.content)
                            print('Pobrano styl: ametyst')
                            app.setStyleSheet(open('styl_ametyst.css').read())
                            print('Ustawiono styl na: ametyst')
                        else:
                            print("Wystąpił problem podczas pobierania pliku")
                    except:
                        app.setStyleSheet(open('styl_ametyst.css').read())
                except:

                    # Sprawdzenie połączenia internetowego
                    try:
                        requests.get("https://www.google.com", timeout=5)

                    except (requests.ConnectionError, requests.Timeout):
                        print("Brak połączenia z internetem.")
                        print(
                            'Nie posiadasz żadnego pliku ze stylem, połącz się z internetem.')
    except:
        print('Nie posiadasz żadnego pliku ze stylem, połącz się z internetem i ' +
              Fore.RED + 'wykonaj aktualizację programu' + Style.RESET_ALL)


class AutoStartManager:
    def __init__(self):
        pass

    def find_main2_folder(self):
        try:
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            for root, dirs, files in os.walk(desktop_path):
                if 'main2.py' in files and 'rei' in dirs:
                    # Jeśli do folderu rei to:
                    # return os.path.join(root, 'rei')
                    return os.path.join(root)
            return None
        except Exception as e:
            print(
                Fore.RED + f" - Wystąpił błąd (AutostartManager, find_main2_folder):\n{e}" + Style.RESET_ALL)

    def download_file(self, url, destination):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(destination, 'wb') as file:
                    file.write(response.content)
                return True
            else:
                print("Wystąpił problem podczas pobierania pliku.")
                return False
        except Exception as e:
            print(
                Fore.RED + f" - Wystąpił błąd (AutostartManager, download_file):\n{e}" + Style.RESET_ALL)

    def add_to_startup(self, file_path):
        uzytkownik = getpass.getuser()
        bat_path = fr'C:\Users\{
            uzytkownik}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        bat_file_path = os.path.join(bat_path, "Magnesy-update.bat")

        try:
            if not os.path.exists(bat_path):
                os.makedirs(bat_path)

            with open(bat_file_path, "w+") as bat_file:
                bat_file.write("@echo off\n")
                bat_file.write('start "" "{}"'.format(file_path))

                print("Plik Automa.py został dodany do autostartu.")
        except PermissionError as e:
            # Jeśli wystąpi błąd PermissionError, wyświetl okno dialogowe z prośbą o nadanie uprawnień administratora
            reply = QMessageBox.question(None, 'Uprawnienia administratora', "Program wymaga uprawnień administratora do dodania do autostartu. Czy chcesz uruchomić ponownie z uprawnieniami administratora?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Ponownie uruchom program z uprawnieniami administratora
                self.run_as_admin(sys.argv)
            else:
                print("Nie dodano programu do autostartu.\n" +
                      Fore.RED + f" - Wystąpił błąd:\n{e}" + Style.RESET_ALL)
        except Exception as e:
            print(
                Fore.RED + f" - Wystąpił błąd (AutostartManager, add_to_startup):\n{e}" + Style.RESET_ALL)

    def run_as_admin(self, argv=None):
        """
        Restarts the current program with admin rights.
        """
        if os.name != 'nt':
            return False  # Funkcja działa tylko na systemach Windows

        if ctypes.windll.shell32.IsUserAnAdmin():
            return True

        if argv is None:
            argv = sys.argv
        if hasattr(sys, '_MEIPASS'):
            # Support pyinstaller wrapped program.
            arguments = argv[1:]
        else:
            arguments = argv
        argument_line = ' '.join(arguments)
        executable = sys.executable
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", executable, argument_line, None, 1)
        sys.exit(0)

    def run(self):
        try:
            # Szukaj folderu zawierającego main2.py i folder rei
            main2_folder = self.find_main2_folder()
            print(f'{main2_folder}')
            if main2_folder:
                print(
                    "Znaleziono folder zawierający main2.py i folder rei:", main2_folder)

                # Ścieżka do pobrania pliku Automa.py
                automa_url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Automa.py"
                automa_destination = os.path.join(main2_folder, "Automa.py")

                # Pobierz plik Automa.py
                if self.download_file(automa_url, automa_destination):
                    print("Pobrano plik Automa.py.")

                    # Dodaj plik Automa.py do autostartu
                    self.add_to_startup(automa_destination)
                else:
                    print("Nie udało się pobrać pliku Automa.py.")
            else:
                print("Nie znaleziono folderu zawierającego main2.py i folder rei.")
        except Exception as e:
            print(
                Fore.RED + f" - Wystąpił błąd (AutostartManager, run):\n{e}" + Style.RESET_ALL)


def ustawianie_stylu(styl):
    try:
        szansa = random.randint(0, 100)
        if szansa < 20:
            # Podaj URL pliku, który chcesz pobrać
            url = f"https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_{
                styl}.css"

            # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
            nazwa_pliku = f"styl_{styl}.css"
            response = requests.get(url)

        app.setStyleSheet(open(f'styl_{styl}.css').read())
        print(f'Ustawiono styl na: {styl}')

    except:
        try:
            # Podaj URL pliku, który chcesz pobrać
            url = f"https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_{
                styl}.css"

            # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
            nazwa_pliku = f"styl_{styl}.css"
            response = requests.get(url)
        except:
            try:
                app.setStyleSheet(open('styl_ametyst.css').read())
                print('Nie znaleziono arkusza stylu\n Ustawiono styl na: ametyst')
            except:
                try:
                    print('Nie znaleziono pliku arkusza stylu')
                    # Podaj URL pliku, który chcesz pobrać
                    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_ametyst.css"

                    # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
                    nazwa_pliku = "styl_ametyst.css"
                    response = requests.get(url)

                    if response.status_code == 200:
                        with open(nazwa_pliku, 'wb') as plik:
                            plik.write(response.content)
                        print('Pobrano styl: ametyst')
                        app.setStyleSheet(open('styl_ametyst.css').read())
                        print('Ustawiono styl na: ametyst')
                    else:
                        print("Wystąpił problem podczas pobierania pliku")
                except:
                    print("Nie ustawiono stylu, połącz się z internetem")


class Ikona:
    def tworzenie_ikonki(self):
        def find_folders_with_main2_and_rei(desktop_path):
            # Lista przechowująca ścieżki do folderów, w których znaleziono plik main2.py i folder rei
            folders_found = []

            # Przeszukaj wszystkie foldery na pulpicie
            for root, dirs, files in os.walk(desktop_path):
                if "main2.py" in files and "rei" in dirs:
                    # Znaleziono folder zawierający zarówno plik main2.py, jak i folder rei
                    folders_found.append(root)

            return folders_found

        def create_shortcut(target, shortcut_name, icon_path=None):
            # Pobierz ścieżkę do pulpitu
            desktop_path = os.path.join(os.path.join(
                os.environ['USERPROFILE']), 'Desktop')

            # Sprawdź, czy istnieje skrót o tej samej ścieżce docelowej na pulpicie i usuń go, jeśli istnieje
            existing_shortcut = os.path.join(
                desktop_path, f'{shortcut_name}.lnk')
            if os.path.exists(existing_shortcut):
                os.remove(existing_shortcut)

            # Utwórz obiekt skrótu
            shell = win32com.client.Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(
                os.path.join(desktop_path, f'{shortcut_name}.lnk'))

            # Ustaw właściwości skrótu
            shortcut.Targetpath = target
            if icon_path:
                shortcut.IconLocation = icon_path

            # Ustaw miejsce rozpoczęcia
            shortcut.WorkingDirectory = os.path.dirname(target)
            # Zapisz skrót
            shortcut.save()

            # Wyświetl powiadomienie o utworzeniu skrótu
            msg = QMessageBox()
            msg.setWindowTitle("Skrót utworzony!")
            msg.setText(
                "Skrót na pulpicie został utworzony!\nBędze w pierwwszym wolnym miejscu na pulpicie, lub w miejscu już istniejącego skrótu do tego programu.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()

        def select_folder_and_create_shortcut():
            # Pobierz ścieżkę do pulpitu
            desktop_path = os.path.join(os.path.join(
                os.environ['USERPROFILE']), 'Desktop')

            # Znajdź foldery zawierające zarówno plik main2.py, jak i folder rei
            folders_found = find_folders_with_main2_and_rei(desktop_path)

            if not folders_found:
                msg = QMessageBox()
                msg.setWindowTitle("Nie znaleziono folderów")
                msg.setText(
                    "Nie znaleziono plików programu na pulpicie, nie można utworzyć skrótu")
                msg.exec_()
                return

            if len(folders_found) == 1:
                selected_folder_path = folders_found[0]
            else:
                # Jeśli znaleziono więcej niż jeden folder, poproś użytkownika o wybór
                selected_folder_path, ok_pressed = QFileDialog.getExistingDirectory(
                    None, "Wybierz folder", desktop_path)
                if not ok_pressed:
                    return

            # Utwórz ścieżkę do pliku ikony
            icon_path = os.path.join(selected_folder_path, "rei", "icon.ico")

            # Utwórz skrót na pulpicie do pliku main2.py w wybranym folderze
            create_shortcut(os.path.join(selected_folder_path,
                            "main2.py"), "Magnesy", icon_path)

        select_folder_and_create_shortcut()


def Inne():
    print(Fore.LIGHTBLACK_EX + 'Dziennik działań:')

    try:
        def Inne1p():
            path = os.path.join(os.getcwd(), "Inne.py")
            if os.path.exists(path):
                try:  # Tego pliku nie ma w repozytorium
                    subprocess.run(['python', 'Inne.py'])
                except:
                    pass

        thread = threading.Thread(target=sprawdzanie_nowych_aktualizacji)
        thread.start()
        time.sleep(1)

        thread = threading.Thread(target=download_icon)
        thread.start()
        time.sleep(1)

        thread = threading.Thread(target=Inne1p)
        thread.start()
    except:
        print("Brak dostępu do internetu")


def download_icon():
    try:
        # Zmień na właściwy adres URL pliku .ico
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/icon.ico"
        save_folder = "rei"  # Nazwa folderu, gdzie chcesz zapisać plik .ico

        # Utworzenie folderu "rei", jeśli nie istnieje
        folder_path = "rei"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        response = requests.get(url)
        if response.status_code == 200:
            icon_data = response.content
            filename = os.path.basename(url)
            save_path = os.path.join(save_folder, filename)

            with open(save_path, 'wb') as icon_file:
                icon_file.write(icon_data)
        else:
            return

    except Exception as e:
        return


class Powiadomienia(QWidget):
    # Przekierowanie błędów do "czarnej dziury"
    sys.stderr = open('nul', 'w')

    def __init__(self):
        self.toaster = self.MyToastNotifier()

    def powiadomienie_jednorazowe(self, tytul_powiadomienia, tresc_powiadomienia, duration):
        self.toaster.show_toast(
            msg=tresc_powiadomienia, duration=duration, tytul_powiadomienia=tytul_powiadomienia)

    class MyToastNotifier(ToastNotifier):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.wyswietlone_powiadomienie = False

        def show_toast(self, msg, icon_path=None, duration=5, threaded=True, tytul_powiadomienia=""):
            icon_path = "rei/icon.ico"
            nazwa_aplikacji = ""  # Nazwa aplikacji nie będzie już wyświetlana
            if nazwa_aplikacji != "":
                title = f"{nazwa_aplikacji} - {tytul_powiadomienia}"
            else:
                title = f"{tytul_powiadomienia}"
            try:
                if not self.wyswietlone_powiadomienie:
                    if not threaded:
                        return super().show_toast(title, msg, icon_path, duration, threaded)
                    else:
                        threading.Thread(target=self._show_toast, args=(
                            title, msg, icon_path, duration)).start()
                        self.wyswietlone_powiadomienie = True
                        return 1  # lub inna wartość int
            except Exception as e:
                # Przechwytywanie błędów, ale nie wyświetlanie ich
                pass


def sprawdz_biblioteki():
    nazwa_pliku = "DATA.txt"
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/bib.txt"

    # Pobierz zawartość pliku z URL i policz linie
    response = requests.get(url)
    if response.status_code != 200:
        print("Błąd: Nie można pobrać pliku z URL.")
        return

    linie_z_url = response.text.splitlines()
    liczba_linii_z_url = len(linie_z_url)

    # Sprawdź, czy plik DATA.txt istnieje
    if os.path.exists(nazwa_pliku):
        with open(nazwa_pliku, 'r', encoding='utf-8') as plik:
            pierwsza_linia = plik.readline().strip()

        try:
            liczba_z_data = int(pierwsza_linia)
        except ValueError:
            print(Fore.YELLOW + "Błąd:\n" + Fore.RED +
                  "Format pliku DATA.txt nie jest prawidłowy, jeśli ten błąd będzie się powtarzał - usuń DATA.txt z plików programu i wykonaj aktualizcję" + Style.RESET_ALL)
            liczba_z_data = -1

        if liczba_z_data == liczba_linii_z_url:
            print("Ilość bibliotek jest zgodna")
        elif liczba_z_data < liczba_linii_z_url:
            print(Fore.YELLOW +
                  "Liczba znanych bibliotek w pliku jest mniejsza niż wymagana - " + Fore.CYAN + "zaktualizuj program" + Style.RESET_ALL)
            toaster = Powiadomienia()
            toaster.powiadomienie_jednorazowe(
                tytul_powiadomienia="Biblioteki", tresc_powiadomienia=f"Wykonaj aktualizację, a problem zniknie", duration=3)
            messagebox.showerror(
                "Zagrożenie", "Wykonaj aktualizację, aby program działał prawidłowo, okno instalatora zostanie za chwilę otwarte.\nNie otwieraj instalatora przez program przed wykonaniem tej aktualizacji!")

            subprocess.run(['python', 'Instalator.py'])

        elif liczba_z_data > liczba_linii_z_url:
            # Któraś biblioteka nie jest już wymagana
            nazwa_pliku = "DATA.txt"
            operacje = OperacjeNaPliku(nazwa_pliku)
            numer_linii = 0  # Numer linii do zmiany
            nowa_zawartosc = f"{pierwsza_linia}"
            operacje.podmien_linijke(numer_linii, nowa_zawartosc)
    else:
        # Zapisz liczbę linijek do nowego pliku DATA.txt
        with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
            plik.write(str(liczba_linii_z_url) + '\n')
        print(f"Plik {nazwa_pliku} nie istniał. Zapisano dane {
              liczba_linii_z_url} do nowego pliku.")


def sprawdzanie_nowych_aktualizacji():
    global ustawienie_sprawdzanie_aktualizacji_w_tle
    while True:
        try:
            # Pobierz zawartość pliku version.txt z repozytorium na GitHub
            try:
                url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version.txt'
                response = requests.get(url)
                response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
                version_online = response.content.decode('utf-8').strip()
            except requests.exceptions.RequestException as e:
                messagebox.showerror(
                    "Błąd", f'Wystąpił błąd połączenia z internetem. Spróbuj ponownie później')
                return
            version_online_lines = version_online.split('\n')
            # Odczytaj zawartość pliku version.txt w twoim programie
            path = os.path.join(os.getcwd(), "version.txt")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    version_local = f.read().strip()
            else:
                version_local = "1.0.0"

            version_local_lines = version_local.split('\n')

            najnowsza_wersja_online = version_online_lines[0]
            local_aktualna_wersja = version_local_lines[0]
            if version.parse(local_aktualna_wersja) == version.parse(najnowsza_wersja_online):
                # Jeśli się okarz, że zapomniałem dodać jakąś bibliotekę podczas wydawania nowej wersji
                sprawdz_biblioteki()
            if version.parse(local_aktualna_wersja) < version.parse(najnowsza_wersja_online):
                print("Dostępna jest aktualizacja:")
                print(f"  {local_aktualna_wersja} --> {najnowsza_wersja_online}")
                toaster = Powiadomienia()
                toaster.powiadomienie_jednorazowe(
                    tytul_powiadomienia="Nowa wersja", tresc_powiadomienia=f"Dostępna jest aktualizacja:\n   {local_aktualna_wersja} --> {najnowsza_wersja_online}\nMożesz ją zainstalować", duration=3)

            if version.parse(version_online_lines[0]) > version.parse(version_local_lines[1]):
                messagebox.showerror("Aktualizacje nie są takie straszne ;)",
                                     f"Ta wersja jest już przestarzała, warto robić aktualizacje co jakiś czas\nP.S. Zrób to teraz\n\t{local_aktualna_wersja} --> {najnowsza_wersja_online}")
        except Exception as e:
            print(e)
            pass

        n = 0
        while n != 60:
            time.sleep(2)
            if ustawienie_sprawdzanie_aktualizacji_w_tle == False:
                break
            n = n + 1
        if ustawienie_sprawdzanie_aktualizacji_w_tle == False:
            break


class OknoRozszerzen(QWidget):
    def __init__(self):
        super().__init__()

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        toaster = Powiadomienia()
        toaster.powiadomienie_jednorazowe(
            tytul_powiadomienia="Rozszerzenia? Hmm...", tresc_powiadomienia="Niektóre rozszerzenia mogą otwierać się dłużej\nAby zarządzać rozszerzeniem, przejdź do plików programu i dodaj, lub usuń jego folder", duration=3)

        # Tworzymy układ siatkowy dla okna rozszerzeń
        układ = QGridLayout()

        # Przechodzimy przez foldery w "Rozszerzenia"
        sciezka_rozszerzen = "Rozszerzenia"

        if not os.path.exists(sciezka_rozszerzen) or not os.listdir(sciezka_rozszerzen):
            brak_rozszerzen_label = QLabel('Brak dostępnych rozszerzeń.')
            układ.addWidget(brak_rozszerzen_label, 0, 0, 1, 2)
        else:
            # Dodaję listę do śledzenia uruchomionych skryptów
            self.uruchomione_rozszerzenia = []

            for folder_rozszerzenia in os.listdir(sciezka_rozszerzen):
                sciezka_folderu = os.path.join(
                    sciezka_rozszerzen, folder_rozszerzenia)

                if os.path.isdir(sciezka_folderu):
                    sciezka_info = os.path.join(sciezka_folderu, "info.txt")

                    if os.path.exists(sciezka_info):
                        with open(sciezka_info, 'r', encoding='utf-8') as plik_info:
                            nazwa_rozszerzenia = plik_info.readline().strip()
                            nazwa_skryptu = plik_info.readline().strip()

                            przycisk = QPushButton(nazwa_rozszerzenia, self)

                            def uruchom_skrypt(sciezka_skryptu):
                                def _uruchom_skrypt():
                                    try:
                                        # Sprawdzamy, czy plik skryptu istnieje
                                        if os.path.exists(sciezka_skryptu):
                                            # Sprawdzamy, czy skrypt nie jest już uruchomiony
                                            if sciezka_skryptu not in self.uruchomione_rozszerzenia:
                                                # Dodajemy skrypt do listy uruchomionych
                                                self.uruchomione_rozszerzenia.append(
                                                    sciezka_skryptu)
                                                # Uruchamiamy skrypt przy użyciu wątków
                                                thread = threading.Thread(
                                                    target=self.uruchom_skrypt_w_watkach, args=(sciezka_skryptu,))
                                                thread.start()
                                        else:
                                            # Jeśli plik nie istnieje, wyświetlamy odpowiedni komunikat
                                            self.show_error_message(
                                                f'Niestety to rozszerzenie jest uszkodzone, nie można znaleźć pliku:\n {sciezka_skryptu}')
                                    except Exception as e:
                                        # Obsługa innych błędów
                                        self.show_error_message(
                                            'Wystąpił nieznany błąd podczas uruchamiania rozszerzenia')

                                return _uruchom_skrypt

                            przycisk.clicked.connect(uruchom_skrypt(
                                os.path.join(sciezka_folderu, f"{nazwa_skryptu}.py")))
                            układ.addWidget(przycisk)

        # Ustawiamy układ dla okna rozszerzeń
        self.setLayout(układ)

        # Ustawiamy tytuł i rozmiar okna rozszerzeń
        self.setWindowTitle('Lista rozszerzeń')
        self.setGeometry(1300, 300, 400, 320)

    def uruchom_skrypt_w_watkach(self, sciezka_skryptu):
        os.system('python ' + sciezka_skryptu)

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Błąd rozszerzenia")
        msg.setInformativeText(message)
        msg.setWindowTitle("Błąd")
        msg.exec_()


class AktualizacjaWatek(QThread):
    aktualizacja_zakonczona = pyqtSignal(int)

    def __init__(self, urls):
        super().__init__()
        self.urls = urls

    def run(self):
        total_size = sum(self.get_file_size(url) for url in self.urls)
        current_size = 0

        for url in self.urls:
            path = os.path.join(os.getcwd(), os.path.basename(url))

            if os.path.exists(path):
                os.remove(path)

            # Sprawdź, czy URL prowadzi do pliku czy do folderu
            if url.endswith('/'):  # Jeśli kończy się na '/', to jest to folder
                folder_name = os.path.basename(url[:-1])
                folder_path = os.path.join(os.getcwd(), folder_name)
                self.download_folder(url, folder_path)
            else:
                urllib.request.urlretrieve(url, path)
                current_size += self.get_file_size(url)

            progress_percentage = int((current_size / total_size) * 100)
            self.aktualizacja_zakonczona.emit(progress_percentage)

        # Emitowanie sygnału z wartością 100, gdy wszystkie pliki są pobrane
        self.aktualizacja_zakonczona.emit(100)

    def get_file_size(self, url):
        with urllib.request.urlopen(url) as response:
            return int(response.getheader('Content-Length', 0))

    def download_folder(self, url, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        folder_contents = urllib.request.urlopen(
            url).read().decode('utf-8').splitlines()

        for content in folder_contents:
            content_url = url + content
            content_path = os.path.join(folder_path, content)

            # Jeśli kończy się na '/', to jest to kolejny folder
            if content.endswith('/'):
                self.download_folder(content_url, content_path)
            else:
                urllib.request.urlretrieve(content_url, content_path)


class OknoAktualizacji(QWidget):
    def __init__(self):
        super().__init__()

        self.przycisk_instalator = QPushButton('Anuluj')  # Nieużywane

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        układ = QGridLayout()

        etykieta_info = QLabel(
            'Nigdy nie przerywaj aktualizacji! Zostaniesz poinformowany o jej zakończeniu.\nPamiętaj o dostępie do internetu!\nAktualizacji nie można cofnąć.')
        układ.addWidget(etykieta_info, 0, 0, 1, 2)

        self.pasek_postępu = QProgressBar()
        układ.addWidget(self.pasek_postępu, 1, 0, 1, 2)

        # Użyj przycisku self.przycisk_instalator
        self.przycisk_instalator = QPushButton('Instalator')
        self.przycisk_instalator.clicked.connect(self.okno_instalator)

        # Ustaw arkusz stylu dla przycisku self.przycisk_instalator
        self.przycisk_instalator.setStyleSheet("""
        QPushButton {
            background-color: rgba(13, 59, 49, 0.795); /* Kolor tła przycisków z 50% przezroczystością */
            color: rgb(128, 199, 182); /* Kolor tekstu przycisków */
            border: 1px solid rgba(5, 63, 50, 0.788); /* Grubość i kolor obramowania przycisków */
            border-radius: 5px; /* Zaokrąglenie narożników przycisków */
            padding: 5px 10px; /* Wewnętrzny odstęp przycisków */
            text-align: center;
        }
        """)

        # Dodaj przycisk self.przycisk_instalator do interfejsu
        układ.addWidget(self.przycisk_instalator, 2, 0, 1, 2)

        self.setLayout(układ)
        self.setWindowTitle('Wprowadzenie do aktualizacji')
        self.setGeometry(200, 200, 400, 150)

    def okno_instalator(self):
        global instalator_sesja
        if instalator_sesja == 0:
            instalator_sesja = 1

            def otworz():
                try:
                    # ścieżka do pliku Instalator.py w bieżącym folderze
                    path = os.path.join(os.getcwd(), "Instalator.py")

                    # usuń plik Instalator.py, jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                    # print("Usunięto plik Instalator.py")

                    # pobierz plik main.py z repozytorium
                    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Instalator.py"
                    urllib.request.urlretrieve(url, path)
                    # print("Zastąpiono plik Instalator.py")
                    print('Pobrano instalator')

                    subprocess.run(['python', 'Instalator.py'])
                except Exception as e:
                    print(
                        Fore.RED + f" - Wystąpił błąd podczas instalacji:\n {e}" + Style.RESET_ALL)
                    try:
                        print('Ponowna próba pobrania instalatora...')
                        # ścieżka do pliku Instalator.py w bieżącym folderze
                        path = os.path.join(os.getcwd(), "Instalator.py")

                        # usuń plik Instalator.py, jeśli istnieje
                        if os.path.exists(path):
                            os.remove(path)
                        # print("Usunięto plik Instalator.py")

                        # pobierz plik main.py z repozytorium
                        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Instalator.py"
                        urllib.request.urlretrieve(url, path)
                        # print("Zastąpiono plik Instalator.py")
                    except Exception as e:
                        print(
                            Fore.RED + f" - Wystąpił błąd podczas instalacji:\n {e}" + Style.RESET_ALL)
                        print(Fore.MAGENTA +
                              "Połącz się z internetem" + Style.RESET_ALL)
                        messagebox.showinfo(
                            'Aktualizacja', 'Aby przejść do instalatora musisz go najpierw posiadać. Spróbuj ponownie za chwilę\nPołącz się z internetem')
                        global instalator_sesja
                        instalator_sesja = 1

            # Tworzenie nowego wątku, który wywołuje funkcję open_file()
            thread = threading.Thread(target=otworz)

            # Uruchamianie wątku
            thread.start()
        else:
            messagebox.showwarning(
                'Zabezpieczenia', 'Instalator może być otwarty tylko raz na uruchomienie programu. Jeśli okno jeszcze się nie wyświetliło - poczekaj, nadal się ładuje, może to potrwać kilka sekund i zależy to od twojego internetu.')


class OknoUstawien(QWidget):

    def __init__(self):
        super().__init__()

        # Dodaj atrybut do przechowywania referencji do OknoRozszerzen
        self.okno_rozszerzen = None

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        układ_glowny = QVBoxLayout(self)

        # Tworzymy widget zakładek
        zakladki = QTabWidget()

        # Tworzymy zakładki i obszary przewijania
        zakladka_inne = QWidget()
        zakladka_estetyka = QWidget()
        zakladka_tryb = QWidget()
        zakladka_notatnik = QWidget()

        scroll_inne = QScrollArea()
        scroll_estetyka = QScrollArea()
        scroll_tryb = QScrollArea()
        scroll_notatnik = QScrollArea()

        # Ustawiamy widgety przewijania dla każdej zakładki
        scroll_inne.setWidget(zakladka_inne)
        scroll_inne.setWidgetResizable(True)
        scroll_estetyka.setWidget(zakladka_estetyka)
        scroll_estetyka.setWidgetResizable(True)
        scroll_tryb.setWidget(zakladka_tryb)
        scroll_tryb.setWidgetResizable(True)
        scroll_notatnik.setWidget(zakladka_notatnik)
        scroll_notatnik.setWidgetResizable(True)

        # Dodajemy zakładki do zakładek
        zakladki.addTab(scroll_inne, "Inne")
        zakladki.addTab(scroll_estetyka, "Estetyka")
        zakladki.addTab(scroll_tryb, "Licz w trybie za magnes")
        zakladki.addTab(scroll_notatnik, "Notatnik")

        # Dodajemy zakładki do głównego układu
        układ_glowny.addWidget(zakladki)

        self.setWindowTitle('Ustawienia')
        self.setGeometry(900, 300, 512, 365)

        # Inicjalizujemy zawartość zakładek
        self.utworz_zakladke_inne(zakladka_inne)
        self.utworz_zakladke_estetyka(zakladka_estetyka)
        self.utworz_zakladke_tryb(zakladka_tryb)
        self.utworz_zakladke_notatnik(zakladka_notatnik)

    # Pozostała część kodu

    def utworz_zakladke_glowna(self, zakladka):
        # Tworzymy układ siatkowy dla zakładki
        układ = QGridLayout(zakladka)

        etykieta_ustawien = QLabel(
            'Podaj ceny kosztów dla jednego pakietu', zakladka)
        układ.addWidget(etykieta_ustawien, 0, 0, 1, 2)

        # Dodaj resztę elementów dla sekcji Głównej

    def utworz_zakladke_inne(self, zakladka):
        # Tworzymy układ siatkowy dla zakładki
        układ = QGridLayout(zakladka)

        etykieta_cena_tektura = QLabel(
            '''
Sprawdzanie aktualizacji w tle:
Aktualizacje będą stale sprawdzane podczas działania programu
 - ZOSTANIESZ POINFORMOWWANY O ICH DOSTĘPNOŚCI,
    aktualizacja nie będzie przeprowadzona automatycznie
Po zamknięciu programu ten wątek zostanie zamknięty.

Aktualizacja po uruchomieniu:
Po włączeniu komputera program MOŻE BYĆ jednorazowo aktualizowany
 - NIE ZOSTANIESZ POINFORMOWANY PRZED ROZPOCZĘCIEM AKTUALIZACJI
Ta opcja nie wpłynie na działanie komputera,
Wszystkie wątki programu zostaną zamknięte po aktualizacji.
''', zakladka)
        układ.addWidget(etykieta_cena_tektura, 6, 0, 1, 2)

        self.button_polacz = QPushButton("Połącz z serwerem", zakladka)
        self.button_polacz.clicked.connect(self.otworz_odbiorca)
        układ.addWidget(self.button_polacz, 3, 0, 1, 1)

        self.button_automa = QPushButton(
            "Aktualizacja po uruchomieniu", zakladka)
        self.button_automa.clicked.connect(self.automa)
        układ.addWidget(self.button_automa, 4, 0, 1, 1)

        if ustawienie_sprawdzanie_aktualizacji_w_tle == True:
            self.toggle_button = QPushButton(
                'Sprawdzanie aktualiacji w tle: włączone', zakladka)
            self.toggle_button.setCheckable(True)
            # Ustawienie wartości domyślnej na True
            self.toggle_button.setChecked(True)
        else:
            self.toggle_button = QPushButton(
                'Sprawdzanie aktualiacji w tle: wyłączone', zakladka)
            self.toggle_button.setCheckable(True)
            # Ustawienie wartości domyślnej na False
            self.toggle_button.setChecked(False)

        # Stylowanie przycisku
        self.toggle_button.setStyleSheet("""
            QPushButton {
                text-align: left;
            }
        """)

        # Dodanie przełącznika do układu siatkowego
        układ.addWidget(self.toggle_button, 2, 0, 1, 1)

        self.toggle_button.clicked.connect(self.onToggleSwitch)

        self.button_skrot = QPushButton(
            "Dodaj skrót na pulpicie", zakladka)
        self.button_skrot.clicked.connect(self.tworzenie_skrotu)
        układ.addWidget(self.button_skrot, 5, 0, 1, 1)

    def tworzenie_skrotu(self):
        # Utwórz instancję klasy i wywołaj metodę
        ikona = Ikona()
        ikona.tworzenie_ikonki()

    def automa(self):
        if messagebox.askokcancel("Autostart", 'Ta opcja doda aktualizator do autostartu, możesz to cofnąć w każdej chwili\nW niektórych przypadkach możesz zobaczyć okno terminalu na killka sekund\nJeśli program się zamknie - coś poszło nie tak'):
            global ustawienie_auto
            # Utwórz instancję klasy AutoStartManager i uruchom
            auto_start_manager = AutoStartManager()
            auto_start_manager.run()

            nazwa_pliku = "Ustawienia.txt"
            operacje = OperacjeNaPliku(nazwa_pliku)
            numer_linii = 1  # Numer linii do zmiany
            nowa_zawartosc = "Tak"
            operacje.podmien_linijke(numer_linii, nowa_zawartosc)
            ustawienie_auto = True

            toaster = Powiadomienia()
            toaster.powiadomienie_jednorazowe(
                tytul_powiadomienia=f"Ustawiono!", tresc_powiadomienia=f'Zaktualizowowaliśmy lub ustawiliśmy to ustawienie dla użytkownika {getpass.getuser()}!\nInstrukcje dotyczące usuwania tego ustawienia są w dzienniku działań', duration=3)

            # Ścieżka do katalogu Startup
            sciezka_do_kasowania = rf'{Fore.LIGHTYELLOW_EX}C:\Users\{Fore.CYAN}TWOJA_NAZWA_UŻYTKOWNIKA{
                Fore.LIGHTYELLOW_EX}\AppData\Roaming\Microsoft\Windows\Start     Menu\Programs\Startup{Style.RESET_ALL}'

            # Kolorowe instrukcje
            print(f"{Fore.LIGHTBLACK_EX}Aby wyłączyć - usuń plik {Fore.LIGHTYELLOW_EX}startup.py{Style.RESET_ALL}{Fore.LIGHTBLACK_EX} z tej ścieżki:\n{sciezka_do_kasowania}{Fore.LIGHTBLACK_EX}\nPamiętaj o uzupełnieniu nazwy użytkownika ({
                  Fore.BLUE}{getpass.getuser()}{Style.RESET_ALL}{Fore.LIGHTBLACK_EX})\nEwentualnie usuń {Fore.LIGHTYELLOW_EX} startup.py{Style.RESET_ALL}{Fore.LIGHTBLACK_EX} z autostartu w menedżerze zadań\n")
        else:
            messagebox.showinfo('Autostart', "Anulowano")

    def otworz_odbiorca(self):
        messagebox.showwarning("Bezpieczeństwo i zdalny dostęp",
                               "Jeśli nie masz pewności, z kim zostaniesz połączony - nie włączaj tej funkcji.\nObejmuje zdalną zmianę kodu.")
        toaster = Powiadomienia()
        toaster.powiadomienie_jednorazowe(
            tytul_powiadomienia="Zabezpieczenia", tresc_powiadomienia='Jeśli "serwer" będzie używać innego szyfrowania niż twoje - zdalny dostęp i wymiana wiadomości nie będą działać', duration=3)

        if not messagebox.askokcancel("Bezpieczeństwo i zdalny dostęp", "Czy chcesz kontynuować?"):
            return

        def w_nowym_watku():
            try:
                self.button_polacz.setText('Próba wykonania')
                self.button_polacz.setEnabled(False)
                if os.path.isfile("Odbiorca.py"):
                    subprocess.run(['python', 'Odbiorca.py'])
                else:
                    toaster = Powiadomienia()
                    toaster.powiadomienie_jednorazowe(
                        tytul_powiadomienia=f"Coś jest nie tak", tresc_powiadomienia=f'Na wszelki wypadek zaktualizuj program do najnowszej wersji i spróbuj ponownie', duration=3)
            except:
                toaster = Powiadomienia()
                toaster.powiadomienie_jednorazowe(
                    tytul_powiadomienia="Błąd", tresc_powiadomienia="Coś poszło nie tak", duration=3)

        thread = threading.Thread(target=w_nowym_watku)

        # Uruchamianie wątku
        thread.start()

    def onToggleSwitch(self):
        global ustawienie_sprawdzanie_aktualizacji_w_tle
        global zaawansowane_okno_zamkniete
        if self.toggle_button.isChecked():
            if zaawansowane_okno_zamkniete != True:
                # Sprawdzenie, czy plik istnieje i ewentualne jego utworzenie
                if not os.path.isfile("Ustawienia.txt"):
                    open("Ustawienia.txt", "w", encoding='utf-8').close()

                nazwa_pliku = "Ustawienia.txt"
                operacje = OperacjeNaPliku(nazwa_pliku)
                numer_linii = 0  # Numer linii do zmiany
                nowa_zawartosc = "Tak"
                operacje.podmien_linijke(numer_linii, nowa_zawartosc)
                self.toggle_button.setText(
                    'Sprawdzanie aktualiacji w tle: włączone')
                ustawienie_sprawdzanie_aktualizacji_w_tle = True

                # Tworzenie nowego wątku, który wywołuje funkcję open_file()
                thread = threading.Thread(
                    target=sprawdzanie_nowych_aktualizacji)

                # Uruchamianie wątku
                thread.start()
            else:
                toaster = Powiadomienia()
                toaster.powiadomienie_jednorazowe(
                    tytul_powiadomienia=f"Uruchom program ponownie, aby wprowadzić zmiany", tresc_powiadomienia=f'Zmiana zacznie działać po ponownym uruchomieniu programu', duration=3)

                # Sprawdzenie, czy plik istnieje i ewentualne jego utworzenie
                if not os.path.isfile("Ustawienia.txt"):
                    open("Ustawienia.txt", "w", encoding='utf-8').close()

                nazwa_pliku = "Ustawienia.txt"
                operacje = OperacjeNaPliku(nazwa_pliku)
                numer_linii = 0  # Numer linii do zmiany
                nowa_zawartosc = "Tak"
                operacje.podmien_linijke(numer_linii, nowa_zawartosc)
                self.toggle_button.setText(
                    'Sprawdzanie aktualiacji w tle: włączone')

        else:
            nazwa_pliku = "Ustawienia.txt"
            operacje = OperacjeNaPliku(nazwa_pliku)
            numer_linii = 0  # Numer linii do zmiany
            nowa_zawartosc = "Nie"
            operacje.podmien_linijke(numer_linii, nowa_zawartosc)
            self.toggle_button.setText(
                'Sprawdzanie aktualiacji w tle: wyłączone')
            ustawienie_sprawdzanie_aktualizacji_w_tle = False

    def utworz_zakladke_estetyka(self, zakladka):
        # Tworzymy układ siatkowy dla zakładki
        układ = QGridLayout(zakladka)

        # Przyciski i podglądy stylów
        style_buttons = [
            ("Szarość", "szarość"),
            ("Ametyst", "ametyst"),
            ("Zieleń", "p_zielony")
        ]

        row = 2
        for text, style_name in style_buttons:
            # Utwórz przycisk do ustawiania stylu
            button = QPushButton(text, zakladka)
            button.clicked.connect(
                lambda _, s=style_name: self.ustawianie_styli(s))

            # Utwórz widget do podglądu stylu
            preview_widget = PaletaStylow(zakladka)
            self.aktualizuj_podglad_stylu(button, preview_widget, style_name)

            # Dodaj przycisk i widget do układu
            układ.addWidget(button, row, 0)
            układ.addWidget(preview_widget, row, 1, 1, 2)

            row += 1

    def aktualizuj_podglad_stylu(self, button, preview_widget, style_name):
        try:
            # Wczytaj styl z pliku lub pobierz z internetu
            path = f"styl_{style_name}.css"
            if not os.path.isfile(path):
                url = f"https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/{
                    path}"
                response = requests.get(url)
                if response.status_code == 200:
                    with open(path, 'wb') as plik:
                        plik.write(response.content)
                else:
                    preview_widget.set_kolory(["#FFFFFF"])
                    return

            with open(path, 'r', encoding='utf-8') as file:
                style = file.read()

            # Wyszukaj kolory w stylu
            kolory = self.wyszukaj_kolory(style)
            kolory = self.sortuj_kolory(kolory)
            preview_widget.set_kolory(kolory)

            # Zastosuj styl do buttona
            button.setStyleSheet(style)

        except Exception as e:
            print(f"Błąd podczas ładowania stylu: {e}")
            preview_widget.set_kolory(["#FFFFFF"])

    def wyszukaj_kolory(self, style):
        # Przykładowa implementacja wyszukiwania kolorów w stylu
        import re
        kolory = re.findall(r'#\w{6}', style)
        return list(set(kolory))  # Usunięcie duplikatów

    def sortuj_kolory(self, kolory):
        # Sortuj kolory według jasności
        def jasnosc(kolor):
            kolor_rgb = QColor(kolor)
            return kolor_rgb.lightness()

        return sorted(kolory, key=jasnosc)

    def ustawianie_styli(self, styl):
        try:
            with open("Styl.txt", "r", encoding='utf-8') as plik:
                styl_teraz = plik.read().strip()
        except:
            styl_teraz = "Brak stylu"

        if styl_teraz == styl:
            return

        try:
            path = f"styl_{styl}.css"
            if not os.path.isfile(path):
                url = f"https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/{
                    path}"
                response = requests.get(url)
                if response.status_code == 200:
                    with open(path, 'wb') as plik:
                        plik.write(response.content)
                else:
                    print("Wystąpił problem podczas pobierania pliku")
                    return

            app.setStyleSheet(open(path, 'r', encoding='utf-8').read())
            with open("Styl.txt", "w", encoding='utf-8') as plik:
                plik.write(styl)
            print('Zapisano preferencje')
        except Exception as e:
            print(f"Błąd podczas ustawiania stylu: {e}")

    def utworz_zakladke_tryb(self, zakladka):
        # Tworzymy układ siatkowy dla zakładki
        układ = QGridLayout(zakladka)

        etykieta_ilosc_magnesow = QLabel("Ilość magnesów: ", zakladka)
        układ.addWidget(etykieta_ilosc_magnesow, 0, 0, 1, 1)

        pole_ilosc_magnesow = QSpinBox(zakladka)
        pole_ilosc_magnesow.setMaximum(10000000)
        układ.addWidget(pole_ilosc_magnesow, 0, 1, 1, 2)

        etykieta_cena_za_magnes = QLabel("Cena za magnes: ", zakladka)
        układ.addWidget(etykieta_cena_za_magnes, 1, 0, 1, 1)

        pole_cena_za_magnes = QDoubleSpinBox(zakladka)
        układ.addWidget(pole_cena_za_magnes, 1, 1, 1, 2)

        oblicz_za_magnes = QPushButton("Oblicz", zakladka)
        oblicz_za_magnes.clicked.connect(lambda: self.oblicz(
            pole_ilosc_magnesow, pole_cena_za_magnes, zarobisz_za_magnes, wydasz_za_magnes, c_war_za_magnes_za_magnes))
        układ.addWidget(oblicz_za_magnes, 2, 0, 1, 3)

        zarobisz_za_magnes = QLabel("Zarobisz: ")
        układ.addWidget(zarobisz_za_magnes, 3, 0, 1, 2)

        wydasz_za_magnes = QLabel("Wydasz: ")
        układ.addWidget(wydasz_za_magnes, 4, 0, 1, 2)

        c_war_za_magnes_za_magnes = QLabel("Całkowita wartość: ")
        układ.addWidget(c_war_za_magnes_za_magnes, 5, 0, 1, 2)

    def oblicz(self, pole_ilosc_magnesow, pole_cena_za_magnes, zarobisz_za_magnes, wydasz_za_magnes, c_war_za_magnes_za_magnes):
        liczba_magnesow = pole_ilosc_magnesow.value()
        cena_za_magnes_2 = pole_cena_za_magnes.value()

        now = datetime.datetime.now()

        data_obliczenia = now.strftime("%d.%m.%Y %H:%M:%S")

        # # Pobieranie kosztów z pliku
        path = os.path.join(os.getcwd(), "Ceny.txt")

        # zapisz zawartość pliku Ceny.txt do zmiennej teraz_ceny
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                teraz_ceny = f.read()
        else:
            if messagebox.askokcancel("Brak pliku cen", "Nie można było znaleźć pliku cen kosztów. Czy chcesz kontynuuować♀ z domyslnymi cenami?\nTektura: 13 zł\nNadruk: 35 zł\nFolia magnetyczna: 18 zł\nWoreczki pp: 11 zł"):
                teraz_ceny = "13\n35\n18\n11"
            else:
                messagebox.showinfo("Ustaw ceny"
                                    "Ustaw nowe ceny w odpowiednim oknie i spróbuj ponownie.")
                return

        ceny_tektura = round(float(teraz_ceny.split('\n')[0]), 2)
        ceny_nadruk = round(float(teraz_ceny.split('\n')[1]), 2)
        ceny_foliamg = round(float(teraz_ceny.split('\n')[2]), 2)
        ceny_woreczkipp = round(float(teraz_ceny.split('\n')[3]), 2)

        @lru_cache(maxsize=None)
        def obliczenia(ceny_tektura, ceny_nadruk, ceny_foliamg, ceny_woreczkipp, liczba_magnesow, cena_za_magnes_2):
            ceny_tektura = ceny_tektura / 224
            ceny_nadruk = ceny_nadruk / 224
            ceny_foliamg = ceny_foliamg / 224
            ceny_woreczkipp = ceny_woreczkipp / 224

            tektura = ceny_tektura * liczba_magnesow
            nadruk = ceny_nadruk * liczba_magnesow
            foliamg = ceny_foliamg * liczba_magnesow
            woreczkipp = ceny_woreczkipp * liczba_magnesow

            koszty = tektura + nadruk + foliamg + woreczkipp

            razem = cena_za_magnes_2 * liczba_magnesow
            bilans = razem - koszty
            return bilans, koszty, razem

        bilans, koszty, razem = obliczenia(
            ceny_tektura, ceny_nadruk, ceny_foliamg, ceny_woreczkipp, liczba_magnesow, cena_za_magnes_2)

        zarobisz_za_magnes.setText(f'Zarobisz: {bilans:.2f} zł')
        wydasz_za_magnes.setText(f'Wydasz: {koszty:.2f} zł')

        c_war_za_magnes_za_magnes.setText(
            f'Całkowita wartość pakietów: {razem:.2f} zł')

    def pokaz_rozszerzenia(self):
        # Tworzymy instancję klasy OknoRozszerzen
        if not self.okno_rozszerzen or not self.okno_rozszerzen.isVisible():
            self.okno_rozszerzen = OknoRozszerzen()
            self.okno_rozszerzen.show()
        else:
            self.okno_rozszerzen.raise_()

    def utworz_zakladke_notatnik(self, zakladka):
        układ = QVBoxLayout(zakladka)

        self.notatnik = QTextEdit(zakladka)
        self.notatnik.setPlaceholderText(
            "Wpisz swoje notatki tutaj i zapisz przyciskiem poniżej...\n"
            "Notatka jest zapisywana automatycznie co 3 sekundy\n"
            "Notatka jest trwała i ma nieograniczoną długość."
        )

        # Ścieżka do pliku ZIP
        self.zip_plik = "notatki.zip"
        self.notatnik_plik = "notatki.txt"

        # Wczytaj istniejące notatki, jeśli plik ZIP istnieje
        if os.path.exists(self.zip_plik):
            with zipfile.ZipFile(self.zip_plik, 'r') as z:
                if self.notatnik_plik in z.namelist():
                    with z.open(self.notatnik_plik) as plik:
                        self.notatnik.setPlainText(plik.read().decode('utf-8'))

        # Dodajemy notatnik do układu
        układ.addWidget(self.notatnik)

        # Tworzymy przycisk zapisu
        self.przycisk_zapisz = QPushButton("Zapisz notatki", zakladka)
        self.przycisk_zapisz.clicked.connect(self.zapisz_notatki)
        układ.addWidget(self.przycisk_zapisz)

        # Etykieta do wyświetlania statusu zapisu
        self.etykieta_statusu = QLabel("Wczytano notatkę", zakladka)
        układ.addWidget(self.etykieta_statusu)
        self.etykieta_statusu.setStyleSheet("color: gray;")

        # Inicjalizacja czasu ostatniej zmiany
        self.czas_ostatniej_zmiany = QDateTime.currentDateTime()

        # Timer do sprawdzania zmiany co 3 sekundy
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.sprawdz_i_zapisz)
        self.timer.start(3000)  # 3000 ms = 3 sekundy

        # Połączenie sygnału zmiany tekstu z aktualizacją czasu ostatniej zmiany
        self.notatnik.textChanged.connect(self.aktualizuj_czas_zmiany)

    def aktualizuj_czas_zmiany(self):
        self.czas_ostatniej_zmiany = QDateTime.currentDateTime()
        self.etykieta_statusu.setText("Niezapisane zmiany")
        self.etykieta_statusu.setStyleSheet("color: orange;")

    def sprawdz_i_zapisz(self):
        # Sprawdzenie, czy minęło 3 sekundy od ostatniej zmiany
        if self.czas_ostatniej_zmiany.secsTo(QDateTime.currentDateTime()) >= 3:
            self.zapisz_notatki()

    def zapisz_notatki(self):
        try:
            self.etykieta_statusu.setText("Zapisywanie...")
            self.etykieta_statusu.setStyleSheet("color: blue;")
            self.repaint()  # Aktualizacja etykiety przed rozpoczęciem zapisu

            with zipfile.ZipFile(self.zip_plik, 'w') as z:
                with z.open(self.notatnik_plik, 'w') as plik:
                    plik.write(self.notatnik.toPlainText().encode('utf-8'))

            # Po zakończeniu zapisu
            self.etykieta_statusu.setText(
                "Notatki zostały zapisane pomyślnie.")
            self.etykieta_statusu.setStyleSheet("color: green;")
        except Exception as e:
            self.etykieta_statusu.setText(
                f"Nie udało się zapisać notatek: {e}")
            self.etykieta_statusu.setStyleSheet("color: red;")


class ZaawansowaneOkno(QWidget):
    def __init__(self):
        super().__init__()

        self.okno_ustawien = None
        self.okno_aktualizacji = None
        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        global text_edit_historia

        # Tworzymy układ siatkowy dla głównego okna
        układ = QGridLayout()

        # Tworzymy etykiety i przyciski
        etykieta_info = QLabel('Wpisz ilość pakietów i cenę za magnes', self)
        układ.addWidget(etykieta_info, 0, 0, 1, 2)

        button_ustawienia = QPushButton('Opcje', self)
        układ.addWidget(button_ustawienia, 0, 4, 1, 1)
        button_ustawienia.clicked.connect(self.pokaz_ustawienia)

        button_opinie = QPushButton('Aktualizuj', self)
        układ.addWidget(button_opinie, 0, 3, 1, 1)
        button_opinie.clicked.connect(self.pokaz_aktualizator)

        button_usun_zapisy = QPushButton('Usuń zapisy', self)
        układ.addWidget(button_usun_zapisy, 0, 5, 1, 1)
        button_usun_zapisy.clicked.connect(
            lambda: self.wykasuj_zapisy(text_edit_historia))

        etykieta_ilosc = QLabel('Ilość pakietów: ', self)
        układ.addWidget(etykieta_ilosc, 1, 0, 1, 1)

        pole_ilosc = QSpinBox(self)
        pole_ilosc.setMaximum(1001)
        układ.addWidget(pole_ilosc, 1, 1, 1, 1)

        etykieta_cena = QLabel('Cena za magnes: ', self)
        układ.addWidget(etykieta_cena, 2, 0, 1, 1)

        pole_cena = QDoubleSpinBox(self)
        pole_cena.setMaximum(1001)
        układ.addWidget(pole_cena, 2, 1, 1, 1)

        button_oblicz = QPushButton('Oblicz', self)
        układ.addWidget(button_oblicz, 3, 0, 1, 2)
        button_oblicz.clicked.connect(lambda: self.oblicz_i_zapisz(
            pole_ilosc, pole_cena, text_edit_historia, etykieta_zarobisz, etykieta_wydasz, etykieta_calkowita_wartosc_pakietow))

        etykieta_zarobisz = QLabel('Zarobisz: ', self)
        układ.addWidget(etykieta_zarobisz, 4, 0, 1, 2)

        etykieta_wydasz = QLabel('Wydasz: ', self)
        układ.addWidget(etykieta_wydasz, 5, 0, 1, 2)

        etykieta_calkowita_wartosc_pakietow = QLabel(
            'Całkowita wartość pakietów: ', self)
        układ.addWidget(etykieta_calkowita_wartosc_pakietow, 6, 0, 1, 2)

        etykieta_info_trybZ = QLabel(
            'Aby liczyć w trybie za magnes wejdź w opcje', self)
        układ.addWidget(etykieta_info_trybZ, 7, 0, 1, 2)

        button_klienci = QPushButton("Zarządzanie klientami", self)
        button_klienci.clicked.connect(self.klienci)
        układ.addWidget(button_klienci, 8, 0, 1, 2)

        text_edit_historia = QTextEdit(self)
        text_edit_historia.setReadOnly(True)
        układ.addWidget(text_edit_historia, 1, 2, 8, 2)

        text_edit_historia.setPlainText("Brak historii obliczeń")

        # Ładujemy dane z pliku do QTextEdit
        path = os.path.join(os.getcwd(), "Zapisy.txt.gz")
        if os.path.exists(path):
            with gzip.open(path, "rt", encoding="utf-8") as f:
                zawartosc = f.read().strip()
                if zawartosc == '':
                    text_edit_historia.setPlainText("Brak historii obliczeń")
                else:
                    text_edit_historia.setPlainText(zawartosc)

        # Tworzymy wewnętrzny kontener
        inner_container = QFrame()

        # Układ wewnątrz wewnętrznego kontenera
        inner_layout = QGridLayout()
        inner_container.setLayout(inner_layout)

        # Dodajemy widgety do wewnętrznego kontenera
        etykieta_ustawien = QLabel('Podaj ceny kosztów dla jednego pakietu')
        inner_layout.addWidget(etykieta_ustawien, 0, 0, 1, 2)

        # Odczytanie cen z pliku
        ceny = self.odczytaj_ceny_z_pliku('Ceny.txt')

        # Etykieta i pole dla ceny tektury
        etykieta_cena_tektura = QLabel('Cena tektury: ')
        inner_layout.addWidget(etykieta_cena_tektura, 1, 0, 1, 1)

        pole_cena_tektura = QDoubleSpinBox()
        pole_cena_tektura.setValue(ceny.get('tektura', 0.0))
        inner_layout.addWidget(pole_cena_tektura, 1, 1, 1, 1)

        # Etykieta i pole dla ceny nadruku
        etykieta_cena_nadruk = QLabel('Cena nadruku: ')
        inner_layout.addWidget(etykieta_cena_nadruk, 2, 0, 1, 1)

        pole_cena_nadruk = QDoubleSpinBox()
        pole_cena_nadruk.setValue(ceny.get('nadruk', 0.0))
        inner_layout.addWidget(pole_cena_nadruk, 2, 1, 1, 1)

        # Etykieta i pole dla ceny folii
        etykieta_cena_folia = QLabel('Cena folii: ')
        inner_layout.addWidget(etykieta_cena_folia, 3, 0, 1, 1)

        pole_cena_folia = QDoubleSpinBox()
        pole_cena_folia.setValue(ceny.get('folia', 0.0))
        inner_layout.addWidget(pole_cena_folia, 3, 1, 1, 1)

        # Etykieta i pole dla ceny woreczków
        etykieta_cena_woreczki = QLabel('Cena woreczków: ')
        inner_layout.addWidget(etykieta_cena_woreczki, 4, 0, 1, 1)

        pole_cena_woreczki = QDoubleSpinBox()
        pole_cena_woreczki.setValue(ceny.get('woreczki', 0.0))
        inner_layout.addWidget(pole_cena_woreczki, 4, 1, 1, 1)

        button_zapisz1 = QPushButton('Ustaw domyślne ceny (zapisane w kodzie)')
        button_zapisz1.clicked.connect(lambda: self.zmien_ceny(
            None, None, None, None, etykieta_cena_tektura, etykieta_cena_nadruk, etykieta_cena_folia, etykieta_cena_woreczki))
        inner_layout.addWidget(button_zapisz1, 5, 0, 1, 1)

        button_zapisz2 = QPushButton('Zapisz zmiany')
        button_zapisz2.clicked.connect(lambda: self.zmien_ceny(
            pole_cena_tektura, pole_cena_nadruk, pole_cena_folia, pole_cena_woreczki, etykieta_cena_tektura, etykieta_cena_nadruk, etykieta_cena_folia, etykieta_cena_woreczki))
        inner_layout.addWidget(button_zapisz2, 5, 1, 1, 1)

        etykieta_cena_tektura = QLabel('Używana cena tektury: ')
        inner_layout.addWidget(etykieta_cena_tektura, 6, 0, 1, 2)

        etykieta_cena_nadruk = QLabel('Używana cena nadruku: ')
        inner_layout.addWidget(etykieta_cena_nadruk, 7, 0, 1, 2)

        etykieta_cena_folia = QLabel('Używana cena folii: ')
        inner_layout.addWidget(etykieta_cena_folia, 8, 0, 1, 2)

        etykieta_cena_woreczki = QLabel('Używana cena woreczków: ')
        inner_layout.addWidget(etykieta_cena_woreczki, 9, 0, 1, 2)

        # Ustawianie cen od razu po włączeniu w etykietach
        ceny_tektura = pole_cena_tektura.value()
        ceny_nadruk = pole_cena_nadruk.value()
        ceny_foliamg = pole_cena_folia.value()
        ceny_woreczkipp = pole_cena_woreczki.value()

        etykieta_cena_tektura.setText(
            f'Używana cena tektury: {ceny_tektura}')
        etykieta_cena_nadruk.setText(
            f'Używana cena nadruku: {ceny_nadruk}')
        etykieta_cena_folia.setText(f'Używana cena folii: {ceny_foliamg}')
        etykieta_cena_woreczki.setText(
            f'Używana cena woreczków: {ceny_woreczkipp}')

        inner_container.setObjectName("inner_container")

        # Dodajemy wewnętrzny kontener do głównego układu
        układ.addWidget(inner_container, 1, 4, 6, 2)

        # Ustawiamy układ główny dla okna
        self.setLayout(układ)

        # Ustawiamy tytuł i rozmiar głównego okna
        self.setWindowTitle('Magnesy v2')
        self.setGeometry(220, 160, 1160, 630)

    def odczytaj_ceny_z_pliku(self, nazwa_pliku):
        # Sprawdzenie, czy plik istnieje
        if not os.path.isfile(nazwa_pliku):

            if messagebox.showwarning("Brak pliku cen", "Nie można było znaleźć pliku cen kosztów. Zostaną wczytane domyślne koszty za pakiet:\nTektura: 13 zł\nNadruk: 35 zł\nFolia magnetyczna: 18 zł\nWoreczki pp: 11 zł"):
                self.zmien_ceny(None, None, None, None, 13, 35, 18, 11)
            else:
                messagebox.showinfo(
                    "Informacja", "Poprzednie ostrzerzenie będzie wyświetlane do momentu ręcznego ustalenia cen\n(można ponownie ustawić ceny domyślne)")
                return {}

        ceny = {}
        try:
            with open(nazwa_pliku, 'r') as plik:
                linie = plik.readlines()
                ceny = {
                    'tektura': float(linie[0].strip()) if len(linie) > 1 else 0.0,
                    'nadruk': float(linie[1].strip()) if len(linie) > 0 else 0.0,
                    'folia': float(linie[2].strip()) if len(linie) > 2 else 0.0,
                    'woreczki': float(linie[3].strip()) if len(linie) > 3 else 0.0,
                }
        except (IOError, ValueError) as e:
            print(f'Błąd podczas odczytu pliku: {e}')

        return ceny

    def zmien_ceny(self, pole_cena_tektura, pole_cena_nadruk, pole_cena_folia, pole_cena_woreczki, etykieta_cena_tektura, etykieta_cena_nadruk, etykieta_cena_folia, etykieta_cena_woreczki):
        try:
            if pole_cena_tektura:
                ceny_tektura = pole_cena_tektura.value()
                ceny_nadruk = pole_cena_nadruk.value()
                ceny_foliamg = pole_cena_folia.value()
                ceny_woreczkipp = pole_cena_woreczki.value()
            else:
                ceny_tektura = '13'
                ceny_nadruk = '35'
                ceny_foliamg = '18'
                ceny_woreczkipp = '11'

            ceny_tektura = str(ceny_tektura)
            ceny_nadruk = str(ceny_nadruk)
            ceny_foliamg = str(ceny_foliamg)
            ceny_woreczkipp = str(ceny_woreczkipp)

            path = os.path.join(os.getcwd(), "Ceny.txt")

            if os.path.exists(path):
                os.remove(path)

            with open("Ceny.txt", "a", encoding='utf-8') as plik:
                plik.write(ceny_tektura)
                plik.write('\n')
                plik.write(ceny_nadruk)
                plik.write('\n')
                plik.write(ceny_foliamg)
                plik.write('\n')
                plik.write(ceny_woreczkipp)
            if not os.path.isfile("Ceny.txt"):
                open("Ceny.txt", "w", encoding='utf-8').close()
                plik.write(ceny_tektura)
                plik.write('\n')
                plik.write(ceny_nadruk)
                plik.write('\n')
                plik.write(ceny_foliamg)
                plik.write('\n')
                plik.write(ceny_woreczkipp)

            etykieta_cena_tektura.setText(
                f'Używana cena tektury: {ceny_tektura}')
            etykieta_cena_nadruk.setText(
                f'Używana cena nadruku: {ceny_nadruk}')
            etykieta_cena_folia.setText(f'Używana cena folii: {ceny_foliamg}')
            etykieta_cena_woreczki.setText(
                f'Używana cena woreczków: {ceny_woreczkipp}')
            # Zapisz wynik obliczeń do pliku Zapisy.txt

            path = os.path.join(os.getcwd(), "Zapisy.txt")

            if os.path.exists(path):
                os.remove(path)

            wszystkie_zmiany_cen = f" * ** *** ** * ZMIANA CEN KOSZTÓW * ** *** ** *\n" + \
                f"    Nowa cena tektury: {ceny_tektura} zł\n" + \
                f"    Nowa cena nadruku: {ceny_nadruk} zł\n" + \
                f"    Nowa cena folii: {ceny_foliamg} zł\n" + \
                f"    Nowa cena woreczków: {ceny_woreczkipp} zł\n\n"

            aktualna_zawartosc = text_edit_historia.toPlainText()
            text_edit_historia.setPlainText(
                wszystkie_zmiany_cen + aktualna_zawartosc)

            with open("Zapisy.txt", "a", encoding='utf-8') as plik:
                plik.write(wszystkie_zmiany_cen + aktualna_zawartosc)

        except Exception as e:
            print(e)
            return

    def closeEvent(self, event):
        global ustawienie_sprawdzanie_aktualizacji_w_tle
        global zaawansowane_okno_zamkniete
        ustawienie_sprawdzanie_aktualizacji_w_tle = False
        zaawansowane_okno_zamkniete = True
        event.accept()

    def klienci(self):
        try:
            subprocess.run(['python', 'Klienci.py'])
        except:
            pass

    def pokaz_ustawienia(self):
        if not self.okno_ustawien or not self.okno_ustawien.isVisible():
            self.okno_ustawien = OknoUstawien()
            self.okno_ustawien.show()
        else:
            self.okno_ustawien.raise_()

    def pokaz_aktualizator(self):
        if not self.okno_aktualizacji or not self.okno_aktualizacji.isVisible():
            self.okno_aktualizacji = OknoAktualizacji()
            self.okno_aktualizacji.show()
        else:
            self.okno_aktualizacji.raise_()

    def wykasuj_zapisy(self, text_edit_historia):
        try:
            if messagebox.askyesno('Kasowanie historii', 'Czy na pewno chcesz usunąć poprzednie obliczenia?'):
                path = os.path.join(os.getcwd(), "Zapisy.txt.gz")
                if os.path.exists(path):
                    os.remove(path)
                    text_edit_historia.setPlainText(
                        'Historia została skasowana')
        except:
            messagebox.showinfo(
                'Brak pliku', "Nie masz jeszcze historii zapisów")

    def oblicz_i_zapisz(self, pole_ilosc, pole_cena, text_edit_historia, etykieta_zarobisz, etykieta_wydasz, etykieta_calkowita_wartosc_pakietow):
        liczba_pakietow = pole_ilosc.value()
        cena_za_magnes = pole_cena.value()

        now = datetime.datetime.now()
        data_obliczenia = now.strftime("%d.%m.%Y %H:%M:%S")

        path = os.path.join(os.getcwd(), "Ceny.txt")
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                teraz_ceny = f.read()
        else:
            teraz_ceny = "13\n35\n18\n11"

        ceny_tektura = round(float(teraz_ceny.split('\n')[0]), 2)
        ceny_nadruk = round(float(teraz_ceny.split('\n')[1]), 2)
        ceny_foliamg = round(float(teraz_ceny.split('\n')[2]), 2)
        ceny_woreczkipp = round(float(teraz_ceny.split('\n')[3]), 2)

        @lru_cache(maxsize=15)
        def obliczenia(ceny_tektura, ceny_nadruk, ceny_foliamg, ceny_woreczkipp, liczba_pakietow, cena_za_magnes):
            magnesy_w_pakiecie = liczba_pakietow * 224
            cena_za_pakiet = cena_za_magnes * 224
            razem = cena_za_pakiet * liczba_pakietow

            tektura = ceny_tektura * liczba_pakietow
            nadruk = ceny_nadruk * liczba_pakietow
            foliamg = ceny_foliamg * liczba_pakietow
            woreczkipp = ceny_woreczkipp * liczba_pakietow

            koszty = tektura + nadruk + foliamg + woreczkipp
            bilans = razem - koszty
            return magnesy_w_pakiecie, cena_za_pakiet, koszty, bilans, razem

        magnesy_w_pakiecie, cena_za_pakiet, koszty, bilans, razem = obliczenia(
            ceny_tektura, ceny_nadruk, ceny_foliamg, ceny_woreczkipp, liczba_pakietow, cena_za_magnes)

        wyniki = f"Data: {data_obliczenia}\n\nLiczba pakietów: {liczba_pakietow} szt.\nLiczba magnesów: {magnesy_w_pakiecie} szt.\nCena za 1 magnes: {
            cena_za_magnes:.2f} zł\nJeden pakiet to: {cena_za_pakiet:.2f} zł\nKoszty: {koszty:.2f} zł\nZysk sprzedaży: {bilans:.2f} zł\nCena za wszystkie pakiety: {razem:.2f} zł\n\n"
        aktualna_zawartosc = text_edit_historia.toPlainText()

        aktualna_zawartosc = aktualna_zawartosc.replace(
            "Brak historii obliczeń", "")
        aktualna_zawartosc = aktualna_zawartosc.replace(
            "Historia została skasowana", "")
        text_edit_historia.setPlainText(wyniki + aktualna_zawartosc)

        etykieta_zarobisz.setText(f'Zarobisz: {bilans:.2f} zł')
        etykieta_wydasz.setText(f'Wydasz: {koszty:.2f} zł')
        etykieta_calkowita_wartosc_pakietow.setText(
            f'Całkowita wartość pakietów: {razem:.2f} zł')

        # Zapisz wynik obliczeń do pliku Zapisy.txt.gz skompresowanego
        with gzip.open('Zapisy.txt.gz', mode='wt', encoding='utf-8') as file:
            file.write(wyniki + aktualna_zawartosc)


if __name__ == '__main__':

    # Inicjalizujemy aplikację
    app = QApplication(sys.argv)

    # Tworzymy instancję klasy ZaawansowaneOkno
    okno = ZaawansowaneOkno()

    # Wyświetlamy główne okno
    okno.show()

    wybierz_styl_z_pliku()

    # Tworzenie nowego wątku, który wywołuje funkcję open_file()
    thread = threading.Thread(target=Inne)

    # Uruchamianie wątku
    thread.start()

    # Uruchamiamy pętlę główną
    sys.exit(app.exec_())
