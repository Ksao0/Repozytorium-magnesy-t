from PyQt5.QtWidgets import QMessageBox, QPushButton, QFileDialog
from PyQt5 import QtWidgets
import win32com.client
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QTabWidget, QApplication, QScrollArea
from github import Github
import requests
import time
import subprocess
import urllib.request
import urllib
import datetime
import messagebox
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDoubleSpinBox, QLabel, QSpinBox, QTextEdit, QProgressBar
import os
import sys
import threading
import shutil

from win10toast import ToastNotifier

from packaging import version

# Minimalizowanie cmd
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Zmień na właściwy adres URL pliku .ico
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca.py"

response = requests.get(url)
if response.status_code == 200:
    icon_data = response.content
    filename = os.path.basename(url)

    with open(filename, 'wb') as icon_file:
        icon_file.write(icon_data)
else:
    print("Nie udało się pobrać pliku.")


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
            msg.setWindowTitle("Skrót utworzony")
            msg.setText("Skrót na pulpicie został utworzony!")
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
    print('Dziennik działań:')

    def Inne1p():
        try:  # Tego pliku nie ma w repozytorium
            subprocess.run(['python', 'Inne.py'])
        except:
            pass

    # Tworzenie nowego wątku, który wywołuje funkcję open_file()
    thread = threading.Thread(target=Inne1p)

    # Uruchamianie wątku
    thread.start()

    # Tworzenie nowego wątku, który wywołuje funkcję open_file()
    thread = threading.Thread(target=sprawdzanie_nowych_aktualizacji)

    # Uruchamianie wątku
    thread.start()

    # Tworzenie nowego wątku, który wywołuje funkcję open_file()
    thread = threading.Thread(target=download_icon)

    # Uruchamianie wątku
    thread.start()


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
            nazwa_aplikacji = "Magnesy"
            title = f"{nazwa_aplikacji} - {tytul_powiadomienia}"
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


def sprawdzanie_nowych_aktualizacji():
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
            version_local = "BRAK DANYCH"

        version_local_lines = version_local.split('\n')

        najnowsza_wersja_online = version_online_lines[0]
        local_aktualna_wersja = version_local_lines[0]

        if version.parse(local_aktualna_wersja) < version.parse(najnowsza_wersja_online):
            print("Dostępna jest aktualizacja:")
            print(f"  {local_aktualna_wersja} --> {najnowsza_wersja_online}")
            toaster = Powiadomienia()
            toaster.powiadomienie_jednorazowe(
                tytul_powiadomienia="Nowa wersja", tresc_powiadomienia=f"Dostępna jest aktualizacja:\n   {local_aktualna_wersja} --> {najnowsza_wersja_online}\nMożesz ją zainstalować ", duration=3)

        if version.parse(version_online_lines[0]) > version.parse(version_local_lines[1]):
            messagebox.showerror("Aktualizacje nie są takie straszne ;)",
                                 f"Ta wersja jet już przestarzała, warto robić aktualizacje co jakiś czas\nP.S. Zrób to teraz\n\t{local_aktualna_wersja} --> {najnowsza_wersja_online}")

    except Exception as e:
        print(e)
        pass


class OknoRozszerzen(QWidget):
    def __init__(self):
        super().__init__()

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        # Przykładowe użycie
        toaster = Powiadomienia()
        toaster.powiadomienie_jednorazowe(
            tytul_powiadomienia="Rozszerzenia", tresc_powiadomienia="Niektóre rozszerzenia mogą otwierać się dłużej\nAby zarządzać rozszerzeniem, przejdź do plików programu i dodaj, lub usuń jego folder", duration=3)

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
                                        # Sprawdzamy, czy skrypt nie jest już uruchomiony
                                        if sciezka_skryptu not in self.uruchomione_rozszerzenia:
                                            # Dodajemy skrypt do listy uruchomionych
                                            self.uruchomione_rozszerzenia.append(
                                                sciezka_skryptu)
                                            # Uruchamiamy skrypt w osobnym wątku
                                            threading.Thread(target=lambda: os.system(
                                                f"python {sciezka_skryptu}")).start()

                                    except Exception as e:
                                        # Komunikat o błędzie
                                        messagebox.showerror(
                                            'Błąd rozszerzenia', 'To rozszerzenie jest uszkodzone')

                                return _uruchom_skrypt

                            przycisk.clicked.connect(uruchom_skrypt(
                                os.path.join(sciezka_folderu, f"{nazwa_skryptu}.py")))
                            układ.addWidget(przycisk)

        # Ustawiamy układ dla okna rozszerzeń
        self.setLayout(układ)

        # Ustawiamy tytuł i rozmiar okna rozszerzeń
        self.setWindowTitle('Lista rozszerzeń')
        self.setGeometry(1300, 300, 400, 320)


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

        # Tutaj zdefiniuj przycisk "Aktualizuj"
        self.przycisk_aktualizuj = QPushButton('Aktualizuj')
        self.przycisk_anuluj = QPushButton('Anuluj')  # Nieużywane

        self.urls = [
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/main2.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version.txt",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_domyslny.css"
            # Dodaj tutaj inne URL-e do plików, jeśli są
        ]

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        układ = QGridLayout()

        etykieta_info = QLabel(
            'Na razie nie można sprawdzać dostępności aktualizacji')
        układ.addWidget(etykieta_info, 0, 0, 1, 2)

        self.pasek_postępu = QProgressBar()
        układ.addWidget(self.pasek_postępu, 1, 0, 1, 2)

        self.przycisk_aktualizuj = QPushButton('Aktualizuj')
        przycisk_anuluj = QPushButton('Anuluj')

        self.przycisk_aktualizuj.clicked.connect(self.rozpocznij_aktualizacje)
        przycisk_anuluj.clicked.connect(self.anuluj_aktualizacje)

        self.przycisk_anuluj.setEnabled(False)
        self.przycisk_anuluj.setStyleSheet(
            'background-color: lightgray; color: gray;')

        układ.addWidget(self.przycisk_aktualizuj, 2, 0)
        układ.addWidget(przycisk_anuluj, 2, 1)

        self.setLayout(układ)
        self.setWindowTitle('Okno Aktualizatora')
        self.setGeometry(200, 200, 400, 150)

        self.pasek_postępu.setValue(0)
        self.watek_aktualizacji = AktualizacjaWatek(self.urls)
        self.watek_aktualizacji.aktualizacja_zakonczona.connect(
            self.zakoncz_aktualizacje)

    def rozpocznij_aktualizacje(self):
        self.pasek_postępu.setValue(0)

        # Wyłącz przycisk i zmień jego wygląd
        self.przycisk_aktualizuj.setEnabled(False)
        self.przycisk_aktualizuj.setText('Aktualizacja w toku...')
        self.przycisk_aktualizuj.setStyleSheet(
            'background-color: lightgray; color: gray;')

        # Wyłącz przycisk i zmień jego wygląd
        self.przycisk_anuluj.setEnabled(True)
        self.przycisk_anuluj.setStyleSheet(
            'background-color: gray; color: lightgray;')

        self.watek_aktualizacji.start()

    def zakoncz_aktualizacje(self, value):
        self.pasek_postępu.setValue(value)
        if value == 100:
            # Tutaj dodano uruchomienie programu z nowego pliku main.py po zakończeniu aktualizacji
            # subprocess.run(["python", "Aktualizator.py"])
            # Uruchomienie programu z nowego pliku main2.py po zakończeniu aktualizacji
            os.execl(sys.executable, sys.executable, "main2.py")
            QCoreApplication.quit()  # Zamknij bieżący program po zakończeniu aktualizacji

    def anuluj_aktualizacje(self):
        print('Aktualizacja anulowana.')
        self.watek_aktualizacji.terminate()
        self.close()


class OknoUstawien(QWidget):

    def __init__(self):
        super().__init__()

        # Dodaj atrybut do przechowywania referencji do OknoRozszerzen
        self.okno_rozszerzen = None

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        układ_glowny = QVBoxLayout(self)

        # Tworzymy obszar przewijania dla zakładek
        obszar_przewijania = QScrollArea(self)
        obszar_przewijania.setWidgetResizable(True)

        # Tworzymy widget zakładek
        zakladki = QTabWidget()

        # Tworzymy zakładki
        zakladka_glowna = QWidget()
        zakladka_inne = QWidget()
        zakladka_estetyka = QWidget()
        zakladka_tryb = QWidget()

        self.utworz_zakladke_glowna(zakladka_glowna)
        self.utworz_zakladke_inne(zakladka_inne)
        self.utworz_zakladke_estetyka(zakladka_estetyka)
        self.utworz_zakladke_tryb(zakladka_tryb)

        zakladki.addTab(zakladka_glowna, "Główna")
        zakladki.addTab(zakladka_inne, "Inne")
        zakladki.addTab(zakladka_estetyka, "Estetyka")
        zakladki.addTab(zakladka_tryb, "Licz w trybie za magnes")

        # Ustawiamy widget zakładek jako widżet obszaru przewijania
        obszar_przewijania.setWidget(zakladki)

        # Dodajemy obszar przewijania do układu głównego
        układ_glowny.addWidget(obszar_przewijania)

        self.setWindowTitle('Ustawienia')
        self.setGeometry(900, 300, 512, 365)

    # Pozostała część kodu

    def utworz_zakladke_glowna(self, zakladka):
        # Tworzymy układ siatkowy dla zakładki
        układ = QGridLayout(zakladka)

        etykieta_ustawien = QLabel(
            'Podaj ceny kosztów dla jednego pakietu', zakladka)
        układ.addWidget(etykieta_ustawien, 0, 0, 1, 2)

        etykieta_cena = QLabel('Cena tektury: ', zakladka)
        układ.addWidget(etykieta_cena, 1, 0, 1, 1)

        pole_cena_tektura = QDoubleSpinBox(zakladka)
        układ.addWidget(pole_cena_tektura, 1, 1, 1, 1)

        etykieta_cena = QLabel('Cena nadruku: ', zakladka)
        układ.addWidget(etykieta_cena, 2, 0, 1, 1)

        pole_cena_nadruk = QDoubleSpinBox(zakladka)
        układ.addWidget(pole_cena_nadruk, 2, 1, 1, 1)

        etykieta_cena = QLabel('Cena folii: ', zakladka)
        układ.addWidget(etykieta_cena, 3, 0, 1, 1)

        pole_cena_folia = QDoubleSpinBox(zakladka)
        układ.addWidget(pole_cena_folia, 3, 1, 1, 1)

        etykieta_cena = QLabel('Cena woreczków: ', zakladka)
        układ.addWidget(etykieta_cena, 4, 0, 1, 1)

        pole_cena_woreczki = QDoubleSpinBox(zakladka)
        układ.addWidget(pole_cena_woreczki, 4, 1, 1, 1)

        button_zapisz1 = QPushButton('Ustaw domyślne ceny', zakladka)
        button_zapisz1.clicked.connect(lambda: self.zmien_ceny(None, None, None, None, etykieta_cena_tektura,
                                                               etykieta_cena_nadruk, etykieta_cena_folia, etykieta_cena_woreczki))  # Połącz przycisk z funkcją
        układ.addWidget(button_zapisz1, 5, 0, 1, 1)

        button_zapisz2 = QPushButton('Zapisz zmiany', zakladka)
        button_zapisz2.clicked.connect(lambda: self.zmien_ceny(
            pole_cena_tektura, pole_cena_nadruk, pole_cena_folia, pole_cena_woreczki, etykieta_cena_tektura, etykieta_cena_nadruk, etykieta_cena_folia, etykieta_cena_woreczki))  # Połącz przycisk z funkcją
        układ.addWidget(button_zapisz2, 5, 1, 1, 1)

        etykieta_cena_tektura = QLabel('Używana cena tektury: ', zakladka)
        układ.addWidget(etykieta_cena_tektura, 6, 0, 1, 2)

        etykieta_cena_nadruk = QLabel('Używana cena nadruku: ', zakladka)
        układ.addWidget(etykieta_cena_nadruk, 7, 0, 1, 2)

        etykieta_cena_folia = QLabel('Używana cena folii: ', zakladka)
        układ.addWidget(etykieta_cena_folia, 8, 0, 1, 2)

        etykieta_cena_woreczki = QLabel('Używana cena woreczków: ', zakladka)
        układ.addWidget(etykieta_cena_woreczki, 9, 0, 1, 2)

        button_rozszerzenia = QPushButton('Rozszerzenia', zakladka)
        button_rozszerzenia.clicked.connect(
            self.pokaz_rozszerzenia)  # Połącz przycisk z funkcją
        układ.addWidget(button_rozszerzenia, 10, 1, 1, 1)

        # Tworzenie instancji klasy Ikonki
        self.ikonki_instance = Ikona()

        # Tworzenie przycisku
        button_rozszerzenia = QPushButton('Utwórz skrót na pulpicie', zakladka)
        button_rozszerzenia.clicked.connect(
            self.ikonki_instance.tworzenie_ikonki)  # Połącz przycisk z funkcją
        układ.addWidget(button_rozszerzenia, 10, 0, 1, 1)

        # Pobieranie kosztów z pliku
        path = os.path.join(os.getcwd(), "Ceny.txt")

        # zapisz zawartość pliku Ceny.txt do zmiennej teraz_ceny
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                teraz_ceny = f.read()
        else:
            teraz_ceny = "13\n35\n18\n11"

        if teraz_ceny.strip():
            ceny_tektura = round(float(teraz_ceny.split('\n')[0]), 2)
            ceny_nadruk = round(float(teraz_ceny.split('\n')[1]), 2)
            ceny_foliamg = round(float(teraz_ceny.split('\n')[2]), 2)
            ceny_woreczkipp = round(float(teraz_ceny.split('\n')[3]), 2)
        else:
            ceny_tektura = 0.0
            ceny_nadruk = 0.0
            ceny_foliamg = 0.0
            ceny_woreczkipp = 0.0

        etykieta_cena_tektura.setText(
            f'Używana cena tektury: {ceny_tektura} zł')
        etykieta_cena_nadruk.setText(f'Używana cena nadruku: {ceny_nadruk} zł')
        etykieta_cena_folia.setText(f'Używana cena folii: {ceny_foliamg} zł')
        etykieta_cena_woreczki.setText(
            f'Używana cena woreczków: {ceny_woreczkipp} zł')

        # Dodaj resztę elementów dla sekcji Głównej

    def utworz_zakladke_inne(self, zakladka):
        # Tworzymy układ siatkowy dla zakładki
        układ = QGridLayout(zakladka)
        etykieta_cena_tektura = QLabel(
            'Niedługo pojawią się tu nowe opcje\n\nBędą tu pewnie funkcje typu:\n - zgłaszania błędów/propozycji (podobne do tego, co było kiedyś)\n - automatyczna aktualizacja (po włączeniu komputera pliki byłyby podmieniane)\n - itp.', zakladka)
        układ.addWidget(etykieta_cena_tektura, 6, 0, 1, 2)
        # Dodaj elementy dla sekcji Inne

    def utworz_zakladke_estetyka(self, zakladka):
        # Tworzymy układ siatkowy dla zakładki
        układ = QGridLayout(zakladka)
        etykieta_cena_tektura = QLabel(
            'Chcesz zmienić wygląd programu?\nNiedługo dostaniesz taką możliwość!\n\n\nBędzie to najprawdopodobniej coś bardziej rozbudowanego niż to, co masz na telefonie\n - gotowe style\n - kreator motywów', zakladka)
        układ.addWidget(etykieta_cena_tektura, 6, 0, 1, 2)
        # Dodaj elementy dla sekcji Estetyka

    def utworz_zakladke_tryb(self, zakladka):
        # Tworzymy układ siatkowy dla zakładki
        układ = QGridLayout(zakladka)
        etykieta_cena_tektura = QLabel(
            'Wkrótce ;D', zakladka)
        układ.addWidget(etykieta_cena_tektura, 6, 0, 1, 2)
        # Dodaj elementy dla sekcji Estetyka

    def pokaz_rozszerzenia(self):
        # Tworzymy instancję klasy OknoRozszerzen
        if not self.okno_rozszerzen or not self.okno_rozszerzen.isVisible():
            self.okno_rozszerzen = OknoRozszerzen()
            self.okno_rozszerzen.show()
        else:
            self.okno_rozszerzen.raise_()

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


class ZaawansowaneOkno(QWidget):
    def __init__(self):
        super().__init__()

        self.okno_ustawien = None  # Dodaj atrybut do przechowywania referencji do OknoUstawien
        # Dodaj atrybut do przechowywania referencji do OknoUstawien
        self.okno_aktualizacji = None
        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        global text_edit_historia
        # Tworzymy układ siatkowy dla głównego okna
        układ = QGridLayout()

        etykieta_info = QLabel('Wpisz ilość pakietów i cenę za magnes', self)
        układ.addWidget(etykieta_info, 0, 0, 1, 2)

        button_ustawienia = QPushButton('Ustawienia', self)
        układ.addWidget(button_ustawienia, 0, 4, 1, 1)
        button_ustawienia.clicked.connect(
            self.pokaz_ustawienia)  # Połącz przycisk z funkcją

        button_opinie = QPushButton('Aktualizuj', self)
        układ.addWidget(button_opinie, 0, 3, 1, 1)
        button_opinie.clicked.connect(
            self.pokaz_aktualizator)  # Poprawione podłączenie do funkcji

        button_usun_zapisy = QPushButton('Usuń zapisy', self)
        układ.addWidget(button_usun_zapisy, 0, 5, 1, 1)
        button_usun_zapisy.clicked.connect(
            lambda: self.wykasuj_zapisy(text_edit_historia))

        etykieta_ilosc = QLabel('Ilość pakietów: ', self)
        układ.addWidget(etykieta_ilosc, 1, 0, 1, 1)

        pole_ilosc = QSpinBox(self)
        układ.addWidget(pole_ilosc, 1, 1, 1, 1)

        etykieta_cena = QLabel('Cena za magnes: ', self)
        układ.addWidget(etykieta_cena, 2, 0, 1, 1)

        pole_cena = QDoubleSpinBox(self)
        układ.addWidget(pole_cena, 2, 1, 1, 1)

        button_oblicz = QPushButton('Oblicz', self)
        układ.addWidget(button_oblicz, 3, 0, 1, 2)
        button_oblicz.clicked.connect(lambda: self.oblicz_i_zapisz(
            pole_ilosc, pole_cena, text_edit_historia, etykieta_zarobisz, etykieta_wydasz, etykieta_calkowita_wartosc_pakietow))  # Połącz przycisk z funkcją

        etykieta_zarobisz = QLabel('Zarobisz: ', self)
        układ.addWidget(etykieta_zarobisz, 4, 0, 1, 2)

        etykieta_wydasz = QLabel('Wydasz: ', self)
        układ.addWidget(etykieta_wydasz, 5, 0, 1, 2)

        etykieta_calkowita_wartosc_pakietow = QLabel(
            'Całkowita wartość pakietów: ', self)
        układ.addWidget(etykieta_calkowita_wartosc_pakietow, 6, 0, 1, 2)

        text_edit_historia = QTextEdit(self)
        text_edit_historia.setReadOnly(True)
        układ.addWidget(text_edit_historia, 1, 3, 6, 3)

        text_edit_historia.setPlainText("Brak historii obliczeń")

        # Ładujemy dane z pliku do QTextEdit
        path = os.path.join(os.getcwd(), "Zapisy.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                zawartosc = f.read().strip()
                if zawartosc == '':
                    text_edit_historia.setPlainText("Brak historii obliczeń")
                else:
                    text_edit_historia.setPlainText(zawartosc)

        # Ustawiamy układ dla głównego okna
        self.setLayout(układ)

        # Ustawiamy tytuł i rozmiar głównego okna
        self.setWindowTitle('Magnesy v2')
        self.setGeometry(300, 300, 600, 400)

        # Arkusz stylów
        app.setStyleSheet(open('styl_domyslny.css').read())

    def pokaz_ustawienia(self):
        # Tworzymy instancję klasy OknoUstawien
        if not self.okno_ustawien or not self.okno_ustawien.isVisible():
            self.okno_ustawien = OknoUstawien()
            self.okno_ustawien.show()
        else:
            self.okno_ustawien.raise_()

    def pokaz_aktualizator(self):
        # Tworzymy instancję klasy OknoAktualizacji
        if not self.okno_aktualizacji or not self.okno_aktualizacji.isVisible():
            self.okno_aktualizacji = OknoAktualizacji()
            self.okno_aktualizacji.show()
        else:
            self.okno_aktualizacji.raise_()

    def wykasuj_zapisy(self, text_edit_historia):
        try:
            if messagebox.askyesno('Kasowanie historii', 'Czy na pewno chcesz usunąć poprzednie obliczenia?'):
                # Ścieżka do pliku Zapisy.txt w bieżącym folderze
                path = os.path.join(os.getcwd(), "Zapisy.txt")

                # Usuń plik Zapisy.txt, jeśli istnieje
                if os.path.exists(path):
                    os.remove(path)
                    with open('Zapisy.txt', mode='w', encoding='utf-8') as file:
                        file.write('')

                text_edit_historia.setPlainText('')
        except:
            messagebox.showinfo(
                'Brak pliku', "Nie masz jeszcze historii zapisów")

    def oblicz_i_zapisz(self, pole_ilosc, pole_cena, text_edit_historia, etykieta_zarobisz, etykieta_wydasz, etykieta_calkowita_wartosc_pakietow):
        liczba_pakietow = pole_ilosc.value()
        cena_za_magnes = pole_cena.value()

        now = datetime.datetime.now()

        data_obliczenia = now.strftime("%d.%m.%Y %H:%M:%S")

        # # Pobieranie kosztów z pliku
        path = os.path.join(os.getcwd(), "Ceny.txt")

        # zapisz zawartość pliku Ceny.txt do zmiennej teraz_ceny
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                teraz_ceny = f.read()
        else:
            teraz_ceny = "13\n35\n18\n11"

        ceny_tektura = round(float(teraz_ceny.split('\n')[0]), 2)
        ceny_nadruk = round(float(teraz_ceny.split('\n')[1]), 2)
        ceny_foliamg = round(float(teraz_ceny.split('\n')[2]), 2)
        ceny_woreczkipp = round(float(teraz_ceny.split('\n')[3]), 2)

        magnesy_w_pakiecie = liczba_pakietow * 224
        cena_za_pakiet = cena_za_magnes * 224
        razem = cena_za_pakiet * liczba_pakietow

        tektura = ceny_tektura * liczba_pakietow
        nadruk = ceny_nadruk * liczba_pakietow
        foliamg = ceny_foliamg * liczba_pakietow
        woreczkipp = ceny_woreczkipp * liczba_pakietow

        koszty = tektura + nadruk + foliamg + woreczkipp
        bilans = razem - koszty

        wyniki = f"Data: {data_obliczenia}\n\nLiczba pakietów: {liczba_pakietow} szt.\nLiczba magnesów: {magnesy_w_pakiecie} szt.\nCena za 1 magnes: {cena_za_magnes:.2f} zł\nJeden pakiet to: {cena_za_pakiet:.2f} zł\nKoszty: {koszty:.2f} zł\nZysk sprzedaży: {bilans:.2f} zł\nCena za wszystkie pakiety: {razem:.2f} zł\n\n"
        aktualna_zawartosc = text_edit_historia.toPlainText()
        text_edit_historia.setPlainText(wyniki + aktualna_zawartosc)

        etykieta_zarobisz.setText(f'Zarobisz: {bilans:.2f} zł')
        etykieta_wydasz.setText(f'Wydasz: {koszty:.2f} zł')

        etykieta_calkowita_wartosc_pakietow.setText(
            f'Całkowita wartość pakietów: {razem:.2f} zł')

        # Zapisz wynik obliczeń do pliku Zapisy.txt
        with open('Zapisy.txt', mode='w', encoding='utf-8') as file:
            file.write(wyniki + aktualna_zawartosc)


if __name__ == '__main__':

    # Inicjalizujemy aplikację
    app = QApplication(sys.argv)

    # Tworzymy instancję klasy ZaawansowaneOkno
    okno = ZaawansowaneOkno()

    # Wyświetlamy główne okno
    okno.show()

    # Tworzenie nowego wątku, który wywołuje funkcję open_file()
    thread = threading.Thread(target=Inne)

    # Uruchamianie wątku
    thread.start()

    # Uruchamiamy pętlę główną
    sys.exit(app.exec_())
