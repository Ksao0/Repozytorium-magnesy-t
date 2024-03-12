from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
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

from win10toast import ToastNotifier

# Minimalizowanie cmd
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


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
            icon_path = "rei2/ikona_magnesy2.ico"
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
    # Pobierz zawartość pliku version.txt z repozytorium na GitHub
    try:
        url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt'
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
    aktualna_wersja = version_online_lines[0]

    # aktualizacja_wymagana = int(version_online_lines[1])
    # aktualna_wersja_numer = int(aktualna_wersja)

    if aktualna_wersja != najnowsza_wersja_online:
        # Kiedyś zrobię osobne okno aktualizacji
        messagebox.askyesno(
            'Nowa wersja', 'Dostępna jest nowa wersja.\nCzy chcesz zaktualizować?')

    if not version_local_lines[1] == version_online_lines[0]:
        # Kiedyś zrobię osobne okno aktualizacji
        messagebox.askyesno(
            'Nowa wersja', 'Dostępna jest nowa wersja.\nCzy chcesz zaktualizować?')

    # if aktualizacja_wymagana < aktualna_wersja_numer:
    #     toaster = Powiadomienia()
    #     toaster.powiadomienie_jednorazowe(
    #         tytul_powiadomienia="Aktualizacja", tresc_powiadomienia="Program zostanie zaktualizowany", duration=3)


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
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Aktualizator.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/main2.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version.txt"
            # Dodaj tutaj inne URL-e do plików, jeśli są
        ]

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        układ = QGridLayout()

        etykieta_info = QLabel(
            'Na razie nie można sprawdzać dostępności aktualizacji\nUruchom ponownie po wykonaniu akcji')
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
            # Tutaj dodano uruchomienie programu z nowego pliku main.py po zakończeniu aktualizacji
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
        # Tworzymy układ siatkowy dla okna ustawień
        układ = QGridLayout()

        etykieta_ustawien = QLabel(
            'Podaj ceny kosztów dla jednego pakietu', self)
        układ.addWidget(etykieta_ustawien, 0, 0, 1, 2)

        etykieta_cena = QLabel('Cena tektury: ', self)
        układ.addWidget(etykieta_cena, 1, 0, 1, 1)

        pole_cena_tektura = QDoubleSpinBox(self)
        układ.addWidget(pole_cena_tektura, 1, 1, 1, 1)

        etykieta_cena = QLabel('Cena nadruku: ', self)
        układ.addWidget(etykieta_cena, 2, 0, 1, 1)

        pole_cena_nadruk = QDoubleSpinBox(self)
        układ.addWidget(pole_cena_nadruk, 2, 1, 1, 1)

        etykieta_cena = QLabel('Cena folii: ', self)
        układ.addWidget(etykieta_cena, 3, 0, 1, 1)

        pole_cena_folia = QDoubleSpinBox(self)
        układ.addWidget(pole_cena_folia, 3, 1, 1, 1)

        etykieta_cena = QLabel('Cena woreczków: ', self)
        układ.addWidget(etykieta_cena, 4, 0, 1, 1)

        pole_cena_woreczki = QDoubleSpinBox(self)
        układ.addWidget(pole_cena_woreczki, 4, 1, 1, 1)

        button_zapisz1 = QPushButton('Ustaw domyślne ceny', self)
        button_zapisz1.clicked.connect(lambda: self.zmien_ceny(None, None, None, None, etykieta_cena_tektura,
                                                               etykieta_cena_nadruk, etykieta_cena_folia, etykieta_cena_woreczki))  # Połącz przycisk z funkcją
        układ.addWidget(button_zapisz1, 5, 0, 1, 1)

        button_zapisz2 = QPushButton('Zapisz zmiany', self)
        button_zapisz2.clicked.connect(lambda: self.zmien_ceny(
            pole_cena_tektura, pole_cena_nadruk, pole_cena_folia, pole_cena_woreczki, etykieta_cena_tektura, etykieta_cena_nadruk, etykieta_cena_folia, etykieta_cena_woreczki))  # Połącz przycisk z funkcją
        układ.addWidget(button_zapisz2, 5, 1, 1, 1)

        etykieta_cena_tektura = QLabel('Używana cena tektury: ', self)
        układ.addWidget(etykieta_cena_tektura, 6, 0, 1, 2)

        etykieta_cena_nadruk = QLabel('Używana cena nadruku: ', self)
        układ.addWidget(etykieta_cena_nadruk, 7, 0, 1, 2)

        etykieta_cena_folia = QLabel('Używana cena folii: ', self)
        układ.addWidget(etykieta_cena_folia, 8, 0, 1, 2)

        etykieta_cena_woreczki = QLabel('Używana cena woreczków: ', self)
        układ.addWidget(etykieta_cena_woreczki, 9, 0, 1, 2)

        button_rozszerzenia = QPushButton('Rozszerzenia', self)
        button_rozszerzenia.clicked.connect(
            self.pokaz_rozszerzenia)  # Połącz przycisk z funkcją
        układ.addWidget(button_rozszerzenia, 10, 1, 1, 1)

        # Ustawiamy układ dla okna ustawień
        self.setLayout(układ)

        # Ustawiamy tytuł i rozmiar okna ustawień
        self.setWindowTitle('Ustawienia')
        self.setGeometry(900, 300, 400, 320)

        # # Pobieranie kosztów z pliku
        path = os.path.join(os.getcwd(), "Ceny.txt")

        # zapisz zawartość pliku Ceny.txt do zmiennej teraz_ceny
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                teraz_ceny = f.read()
        else:
            teraz_ceny = "13\n35\n18\n11"

        # Check if teraz_ceny is not empty before attempting to split and convert to float
        if teraz_ceny.strip():  # strip removes leading and trailing whitespaces
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
                plik.write(f"{aktualna_zawartosc}")

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
        układ.addWidget(text_edit_historia, 1, 3, 6, 3)

        text_edit_historia.setPlainText("Brak historii obliczeń")

        # Ładujemy dane z pliku do QTextEdit
        path = os.path.join(os.getcwd(), "Zapisy.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                zawartosc = f.read().strip()
                text_edit_historia.setPlainText(zawartosc)

        # Ustawiamy układ dla głównego okna
        self.setLayout(układ)

        # Ustawiamy tytuł i rozmiar głównego okna
        self.setWindowTitle('Magnesy v2')
        self.setGeometry(300, 300, 600, 400)

        # Arkusz stylów
        # Ewentualnie dodaj menu bar
        dark_stylesheet = """
        QWidget {
            background-color: #2E2E2E; /* Kolor tła głównego okna */
            color: #FFFFFF; /* Kolor tekstu */
            selection-color: #40535b; /* Ustawienie koloru zaznaczonego tekstu */
            selection-background-color: #EAEAEA; /* Ustawienie koloru tła zaznaczonego tekstu */
        }

        QStatusBar {
            background-color: #333333; /* Kolor tła paska statusu */
            color: #FFFFFF; /* Kolor tekstu paska statusu */
        }
        

        QPushButton {
            background-color: #404040; /* Kolor tła przycisków */
            color: #FFFFFF; /* Kolor tekstu przycisków */
            border: 1px solid #555555; /* Grubość i kolor obramowania przycisków */
            border-radius: 5px; /* Zaokrąglenie narożników przycisków */
            padding: 5px 10px; /* Wewnętrzny odstęp przycisków */
        }

        QTextEdit {
            background-color: #404040; /* Kolor tła przycisków */
            color: #FFFFFF; /* Kolor tekstu przycisków */
            border: 1px solid #555555; /* Grubość i kolor obramowania przycisków */
            border-radius: 5px; /* Zaokrąglenie narożników przycisków */
            padding: 5px 10px; /* Wewnętrzny odstęp przycisków */

            selection-color: #40535b; /* Ustawienie koloru zaznaczonego tekstu */
            selection-background-color: #EAEAEA; /* Ustawienie koloru tła zaznaczonego tekstu */

        }

        QScrollBar:vertical {
            background-color: #404040; /* Kolor tła pionowego paska przewijania */
            width: 10px; /* Szerokość pionowego paska przewijania */
        }

        QScrollBar::handle:vertical {
            background-color: #555555; /* Kolor "uchwytu" pionowego paska przewijania */
            border-radius: 5px; /* Zaokrąglenie narożników "uchwytu" */
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical,
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none; /* Wyłączenie tła dla różnych części pionowego paska przewijania */
        }

        QScrollBar:horizontal {
            background-color: #404040; /* Kolor tła poziomego paska przewijania */
            height: 10px; /* Wysokość poziomego paska przewijania */
        }

        QScrollBar::handle:horizontal {
            background-color: #555555; /* Kolor "uchwytu" poziomego paska przewijania */
            border-radius: 5px; /* Zaokrąglenie narożników "uchwytu" */
        }

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal,
        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {
            background: none; /* Wyłączenie tła dla różnych części poziomego paska przewijania */
        }

        

        QDoubleSpinBox {
            background-color: #404040; /* Kolor tła przycisków */
            color: #FFFFFF; /* Kolor tekstu przycisków */
            border: 1px solid #555555; /* Grubość i kolor obramowania przycisków */
            border-radius: 5px; /* Zaokrąglenie narożników przycisków */
            padding: 5px 10px; /* Wewnętrzny odstęp przycisków */
        }

        QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
            width: 0px; /* Ustaw szerokość przycisków na 0, aby je ukryć */
        }


        QSpinBox {
            background-color: #404040; /* Kolor tła przycisków */
            color: #FFFFFF; /* Kolor tekstu przycisków */
            border: 1px solid #555555; /* Grubość i kolor obramowania przycisków */
            border-radius: 5px; /* Zaokrąglenie narożników przycisków */
            padding: 5px 10px; /* Wewnętrzny odstęp przycisków */
        }

        QPushButton:hover {
            background-color: #505050; /* Kolor tła przycisków po najechaniu myszką */
        }

        QProgressBar {
            border: 2px solid #616161;
            border-radius: 5px;
            text-align: center;
            background: #424242;
        }

        QProgressBar::chunk {
            background-color: #757575;
            width: 10px;
        }

        """

        # Ustawienie arkusza stylów
        app.setStyleSheet(dark_stylesheet)

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
        with open('Zapisy.txt', mode='a', encoding='utf-8') as file:
            file.write(wyniki)


if __name__ == '__main__':

    # Inicjalizujemy aplikację
    app = QApplication(sys.argv)

    # Tworzymy instancję klasy ZaawansowaneOkno
    okno = ZaawansowaneOkno()

    # Wyświetlamy główne okno
    okno.show()

    # Uruchamiamy pętlę główną
    sys.exit(app.exec_())
