import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from packaging import version
import ctypes
import colorama
from colorama import Fore, Style
import urllib.request
import subprocess
import threading
import time
import random
import psutil


# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Maksymalna szerokość okna
MAX_WIDTH = 550

# Inicjalizacja Colorama
colorama.init()

global teraz
global teraz_bib
teraz = 0
teraz_bib = 0
global zdjecie
zdjecie = 0
global zakonczono_pliki
zakonczono_pliki = False
global zakonczon_biblioteki
zakonczon_biblioteki = False
global tryb_stary
tryb_stary = "no"
max_ilosc_zatrzymanych_watkow = 2
ilosc_zatrzymanych_watkow = 0
tryb = "Automatyczny"


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
# Klasa do obsługi operacji na pliku DATA.txt. Dzięki tej klasie można łatwo podmieniać linijki w pliku DATA.txt, który przechowuje liczbę linii z pliku bib.txt z repozytorium GitHub.


def info_DATA_biblioteki():
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
                  "Format pliku DATA.txt nie jest prawidłowy, jeśli ten błąd będzie się powtarzał - usuń DATA.txt z plików programu" + Style.RESET_ALL)

            liczba_z_data = -1

        if liczba_z_data < liczba_linii_z_url:
            nazwa_pliku = "DATA.txt"
            operacje = OperacjeNaPliku(nazwa_pliku)
            numer_linii = 0  # Numer linii do zmiany
            nowa_zawartosc = f"{liczba_linii_z_url}"
            operacje.podmien_linijke(numer_linii, nowa_zawartosc)

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
# Funkcja info_DATA_biblioteki() sprawdza, czy plik DATA.txt istnieje i czy liczba linii w pliku bib.txt z repozytorium GitHub jest taka sama jak w DATA.txt. Jeśli nie, to podmienia pierwszą linię w DATA.txt na aktualną liczbę linii z bib.txt. Jeśli DATA.txt nie istnieje, to tworzy go i zapisuje liczbę linii z bib.txt.


def obraz():
    # URL do pliku PNG w repozytorium GitHub
    url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Instala.png'

    # Nazwa pliku do zapisania
    filename = 'Instala.png'

    try:
        # Pobranie pliku
        urllib.request.urlretrieve(url, filename)
    except Exception as e:
        print(f"Nie udało się pobrać pliku, instalator może nie mieć szaty graficznej")


path = os.path.join(os.getcwd(), "Instala.png")
if not os.path.exists(path):
    obraz()
else:
    szansa = random.randint(0, 100)

    if szansa < 35:
        obraz()

# Klasa MainWindow dziedziczy po QMainWindow i tworzy główne okno aplikacji


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        global zdjecie
        # Ścieżka do obrazu
        image_path = "Instala.png"

        # Sprawdzenie, czy plik istnieje
        if os.path.exists(image_path):
            try:
                # Wczytujemy obraz
                pixmap = QPixmap(image_path)

                # Obliczamy proporcjonalne wymiary obrazu
                width, height = pixmap.width(), pixmap.height()
                if width > MAX_WIDTH:
                    ratio = MAX_WIDTH / width
                    width = MAX_WIDTH
                    height = int(height * ratio)

                # Skalujemy obraz
                pixmap = pixmap.scaled(width, height)

                # Tworzymy etykietę i ustawiamy tło na obraz
                label = QLabel(self)
                label.setPixmap(pixmap)
                self.setWindowTitle('Instalator')
                label.resize(width, height)

                # Ustawiamy rozmiar okna na nowe wymiary obrazu
                self.resize(width, height)

                # Zablokowanie możliwości zmiany rozmiaru okna
                self.setFixedSize(width, height)
                app.setStyleSheet("""
    QPushButton {
        background-color: rgba(13, 59, 49, 0.795); /* Kolor tła przycisków z 50% przezroczystością */
        color: rgb(128, 199, 182); /* Kolor tekstu przycisków */
        border: 1px solid rgba(5, 63, 50, 0.788); /* Grubość i kolor obramowania przycisków */
        border-radius: 5px; /* Zaokrąglenie narożników przycisków */
        padding: 5px 10px; /* Wewnętrzny odstęp przycisków */
        text-align: center;
        alignment: center
    }
    """)
            except Exception as e:
                print("Wystąpił błąd podczas wczytywania lub skalowania obrazu:", str(e))
        else:
            label = QLabel(self)
            self.setWindowTitle('Instalator')

            width = 550
            height = 452

            zdjecie = 1
            # Ustawiamy rozmiar okna na nowe wymiary obrazu
            self.resize(width, height)
            app.setStyleSheet("""
QWidget {
    background-color: rgba(9, 39, 32, 0.795); /* Kolor tła głównego okna */
    color: rgba(9, 39, 32, 0.795); /* Kolor tekstu */
    selection-color: rgba(9, 39, 32, 0.795); /* Ustawienie koloru zaznaczonego tekstu */
    selection-background-color: rgba(9, 39, 32, 0.795); /* Ustawienie koloru tła zaznaczonego tekstu */
}

QPushButton {
    background-color: rgba(13, 59, 49, 0.795); /* Kolor tła przycisków z 50% przezroczystością */
    color: rgb(128, 199, 182); /* Kolor tekstu przycisków */
    border: 1px solid rgba(5, 63, 50, 0.788); /* Grubość i kolor obramowania przycisków */
    border-radius: 5px; /* Zaokrąglenie narożników przycisków */
    padding: 5px 10px; /* Wewnętrzny odstęp przycisków */
    text-align: center;
    alignment: center
}
""")

        # Dodajemy napis
        text_label = QLabel("Instalator", self)

        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Wcześniej było, ale jest błąd (też działa, ale pylance tak twierdzi): text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet(
            "color: white; font-size: 16px; background-color: rgba(1, 22, 17, 0.665);")
        text_label.setGeometry(10, 10, width - 17, 30)

        # Dodajemy napis
        text_label_N = QLabel("Co nowego?", self)
        text_label_N.setStyleSheet(
            "color: white; font-size: 28px; text-align: center;")
        text_label_N.setGeometry(213, 75, 650, 45)

        # Dodajemy napis
        text_label_N2 = QLabel("""Proszę czekać""", self)
        if zdjecie == 1:
            text_label_N2.setStyleSheet(
                "color: white; font-size: 11.5px; text-align: center;")
        else:
            text_label_N2.setStyleSheet(
                "color: white; font-size: 11.5px; text-align: center;")
        text_label_N2.setGeometry(130, 130, 340, 215)

        # Dodajemy przyciski
        button_aktualizuj = QPushButton("Aktualizuj", self)
        button_aktualizuj.setGeometry(10, height - 40, 100, 30)

        button_tylko_biblioteki = QPushButton("Zainstaluj biblioteki", self)
        button_tylko_biblioteki.setGeometry(120, height - 40, 115, 30)

        # Lista rozwijana do wyboru trybu
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(245, height - 40, 145, 30)
        self.combo_box.addItems(
            ["Automatyczny", "Rdzenie (max)", "Procesory logiczne (max)", "1", "2"])

        # Obsługa wyboru trybu
        self.combo_box.currentIndexChanged.connect(self.wybierz_tryb)

        def aktualizacja1():
            global teraz
            global teraz_bib
            if teraz == 0 and teraz_bib == 0:
                teraz = 1
                print(Fore.LIGHTYELLOW_EX +
                      '\nRozpoczynam aktualizację:' + Style.RESET_ALL)

                global zakonczono_pliki, zakonczon_biblioteki
                zakonczono_pliki = False
                zakonczon_biblioteki = False

                # Tworzenie nowego wątku, który wywołuje funkcję open_file()
                thread = threading.Thread(
                    target=aktualizacja, name="Aktualizowanie")
                # Uruchamianie wątku
                thread.start()

                # Tworzenie nowego wątku, który wywołuje funkcję open_file()
                thread = threading.Thread(
                    target=zainstaluj_biblioteki1, name="Koordynowanie pobierania bibliotek")
                # Uruchamianie wątku
                thread.start()

                while True:
                    if zakonczono_pliki == True and zakonczon_biblioteki == True:
                        break

                ctypes.windll.user32.ShowWindow(
                    ctypes.windll.kernel32.GetConsoleWindow(), 1)

                print(Fore.GREEN +
                      '\nAktualizacja zakończona, możesz zamknąć instalator.\nWyłącz wszystkie otwarte okna programu do magnesów')

            else:
                print(Fore.MAGENTA + "Ten wątek jest już aktywny. (aktualizacja)")

        def zainstaluj_biblioteki1():
            global teraz_bib
            if teraz_bib == 0:
                teraz_bib = 1
                # Tworzenie nowego wątku, który wywołuje funkcję open_file()
                thread = threading.Thread(
                    target=zainstaluj_biblioteki, name="Pobieranie bibliotek")

                # Uruchamianie wątku
                thread.start()
            else:
                print(Fore.MAGENTA + "Ten wątek jest już aktywny. (biblioteki)")

        # Funkcja do sprawdzania wersji

        def wersja():
            try:
                # Pobierz zawartość pliku version.txt z repozytorium na GitHub
                version_online = requests.get(
                    'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version.txt').text.strip()

                version_opis = requests.get(
                    'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version_o.txt').text.strip()

                # Odczytaj zawartość pliku version.txt w twoim programie
                path = os.path.join(os.getcwd(), "version.txt")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        version_local = f.read().strip()
                else:
                    version_local = "1.0.0"

                najnowsza_wersja_online = version_online.split('\n')[0]
                local_aktualna_wersja = version_local.split('\n')[0]

                if local_aktualna_wersja != "1.0.0":
                    if version.parse(local_aktualna_wersja) < version.parse(najnowsza_wersja_online):
                        text_label.setText(
                            f'{local_aktualna_wersja} --> {najnowsza_wersja_online}')
                        text_label_N2.setText(
                            "\n".join(version_opis.split('\n')[1:]))
                    else:
                        text_label.setText(f'Masz najnowszą wersję')
                        text_label_N2.setText(
                            "\n".join(version_opis.split('\n')[1:]))
                else:
                    text_label.setText(f'Jeszcze nie masz naszego programu')
                    text_label_N.setText("Niezainstalowano")
                    text_label_N2.setText(
                        """
Zainstaluj biblioteki, a następnie utwórz pusty folder, w którym będą:
    - folder rei,
    - plik main2.py (pamiętaj o odpowiednim rozszerzeniu pliku).
Następnie przeprowadź aktualizację.

Folder z plikami nie musi znajdować się bozpośrednio na pulpicie,
może być w innych folderach.
Wszystkie pliki muszą się znajdować w jednym folderze.

Jeśli nie spełnisz tego wymagania - nie pobierzesz plików z kodem,
pobrane zostaną tylko biblioteki.
                            """)

            except Exception as e:
                print("Wystąpił błąd:", e)

        wersja()

        def zainstaluj_biblioteki():
            # Przywracanie widoczności okna terminala
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 1)

            try:
                # Pobierz listę bibliotek z repozytorium
                libraries_to_install = requests.get(
                    'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/bib.txt').text.strip().split()

                # Sprawdź zainstalowane biblioteki
                installed_packages = get_installed_packages()

                # Funkcja instalująca pojedynczą bibliotekę
                def install_library(lib):
                    with sema:  # Ograniczenie ilości wątków do wartości na początku pliku
                        if lib not in installed_packages:
                            print(Fore.LIGHTBLACK_EX +
                                  f"Instalowanie biblioteki: {lib}, czekaj...")

                            # Monitorowanie użycia CPU podczas instalacji
                            while True:
                                # Pobierz aktualne zużycie CPU
                                cpu_percent = psutil.cpu_percent(interval=1)
                                global max_ilosc_zatrzymanych_watkow
                                global ilosc_zatrzymanych_watkow
                                if cpu_percent > 95.0 and ilosc_zatrzymanych_watkow <= max_ilosc_zatrzymanych_watkow:
                                    ilosc_zatrzymanych_watkow = ilosc_zatrzymanych_watkow + 1
                                    czas_zatrzymania_watku = random.randint(
                                        0, 5)
                                    czas_zatrzymania_watku = czas_zatrzymania_watku + \
                                        int(cpu_percent/10)
                                    print(
                                        Fore.RED + f"Wysokie zużycie CPU: {cpu_percent}%. Wątek {threading.current_thread().name} zatrzymuje się na chwilę ({czas_zatrzymania_watku} s).")
                                    time.sleep(czas_zatrzymania_watku)
                                    print(
                                        Fore.MAGENTA + f"CPU: {cpu_percent}%. Wątek {threading.current_thread().name} wznowiony.")
                                    ilosc_zatrzymanych_watkow = ilosc_zatrzymanych_watkow - 1
                                else:
                                    break

                            subprocess.run(["pip", "install", lib],
                                           capture_output=True, text=True)
                            print(Fore.BLUE + "Biblioteka", lib,
                                  "została pomyślnie zainstalowana.")
                        else:
                            print(Fore.CYAN +
                                  f"Biblioteka {lib} jest już zainstalowana.")

                # Tworzenie wątków dla instalacji bibliotek
                threads = []
                for lib in libraries_to_install:
                    thread = threading.Thread(
                        target=install_library, args=(lib,), name=f"Pobieranie {lib}")
                    thread.start()
                    threads.append(thread)

                # Oczekiwanie na zakończenie wszystkich wątków
                for thread in threads:
                    thread.join()

                print(Fore.GREEN +
                      "Wszystkie biblioteki zostały pomyślnie zainstalowane.")
                info_DATA_biblioteki()
            except Exception as e:
                print(Fore.RED + "Wystąpił błąd:", e)

            global teraz_bib
            teraz_bib = 0
            time.sleep(1)
            global zakonczon_biblioteki
            zakonczon_biblioteki = True

        # Funkcja do uzyskania listy zainstalowanych pakietów
        def get_installed_packages():
            try:
                installed_packages = subprocess.check_output(
                    ['pip', 'freeze']).decode().split('\n')
                installed_packages = [pkg.split('==')[0]
                                      for pkg in installed_packages if pkg]
                return installed_packages
            except subprocess.CalledProcessError:
                print("Nie udało się uzyskać listy zainstalowanych pakietów.")
                return []

        def aktualizacja():
            global teraz
            # Przywracanie widoczności okna terminala
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 1)

            class Automa:
                def __init__(self, urls, folder_path):
                    self.urls = urls
                    self.folder_path = folder_path

                def run(self):
                    if not os.path.exists(self.folder_path):
                        print(
                            Fore.RED + "Folder zawierający wymagane pliki nie istnieje.")
                        sys.exit(1)

                    # Tworzenie wątków
                    threads = []
                    for url in self.urls:
                        file_name = os.path.join(
                            self.folder_path, url.split('/')[-1])

                        # Tworzenie i uruchamianie wątku dla każdego pliku
                        thread = threading.Thread(
                            target=self.process_file, args=(url, file_name), name="Pobieranie plików z kodem")
                        thread.start()
                        threads.append(thread)

                    # Oczekiwanie na zakończenie wszystkich wątków
                    for thread in threads:
                        thread.join()

                def process_file(self, url, file_name):
                    with sema2:
                        if not os.path.exists(file_name):
                            print(
                                Fore.MAGENTA + f"Plik {file_name} nie istnieje na komputerze. Traktuję jako nieaktualny.")
                            self.download_file(url, file_name)
                        else:
                            if not self.compare_files(url, file_name):
                                print(Fore.LIGHTBLACK_EX +
                                      f"Plik {file_name} jest nieaktualny.")
                                self.download_file(url, file_name)
                            else:
                                print(Fore.CYAN +
                                      f"Plik {file_name} jest aktualny.")

                def compare_files(self, url, local_file_path):
                    response = self.get_remote_file_content(url)
                    if response is None:
                        print(
                            Fore.RED + f"Nie udało się pobrać zawartości pliku {url}.")
                        return False

                    with open(local_file_path, 'rb') as local_file:  # Otwarcie w trybie binarnym
                        local_content = local_file.read().decode(
                            'utf-8', errors='ignore')  # Dekodowanie

                    return local_content == response.text

                def download_file(self, url, file_name):
                    print(Fore.MAGENTA +
                          f"Rozpoczynam aktualizację pliku {file_name}...")
                    # Monitorowanie użycia CPU podczas instalacji
                    while True:
                        # Pobierz aktualne zużycie CPU
                        cpu_percent = psutil.cpu_percent(interval=1)
                        if cpu_percent > 85.0:
                            czas_zatrzymania_watku = random.randint(
                                0, 5)
                            czas_zatrzymania_watku = czas_zatrzymania_watku + \
                                int(cpu_percent/10)
                            print(
                                Fore.RED + f"Wysokie zużycie CPU: {cpu_percent}%. Wątek {threading.current_thread().name} zatrzymuje się na chwilę ({czas_zatrzymania_watku} s).")
                            time.sleep(czas_zatrzymania_watku)
                            print(
                                Fore.MAGENTA + f"CPU: {cpu_percent}%. Wątek {threading.current_thread().name} wznowiony.")
                        else:
                            break
                    response = self.get_remote_file_content(url)
                    if response is None:
                        print(
                            Fore.RED + f"Nie udało się pobrać pliku {url}. Aktualizacja przerwana.")
                        return

                    with open(file_name, 'wb') as local_file:  # Otwarcie w trybie binarnym
                        # Zapis zawartości binarnej
                        local_file.write(response.content)
                        print(Fore.GREEN + f"Pobrano {file_name}")

                def get_remote_file_content(self, url):
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            return response
                        else:
                            print(
                                Fore.RED + f"Błąd podczas pobierania pliku {url}: {response.status_code}")
                            return None
                    except Exception as e:
                        print(
                            Fore.RED + f"Wystąpił błąd podczas pobierania pliku {url}: {e}")
                        return None

            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            for root, dirs, files in os.walk(desktop_path):
                if "main2.py" in files and "rei" in dirs:
                    folder_path = root
                    break
            else:
                print("Nie znaleziono wymaganych plików/folderów na pulpicie.")
                teraz = 0
                sys.exit(1)

            # Ścieżka do pliku lista.txt w repozytorium
            lista_txt_url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/lista.txt"
            lista_txt_content = requests.get(lista_txt_url).text
            urls = [line.strip()
                    for line in lista_txt_content.split('\n') if line.strip()]

            text_label.setText(
                f'Sprawdź terminal')

            automa = Automa(urls, folder_path)
            automa.run()
            teraz = 0
            time.sleep(2)
            global zakonczono_pliki
            zakonczono_pliki = True

        # Przypisanie akcji do przycisków
        button_aktualizuj.clicked.connect(
            lambda: threading.Thread(target=aktualizacja1, name="Koordynowanie aktualizacji").start())
        button_tylko_biblioteki.clicked.connect(lambda: threading.Thread(
            target=zainstaluj_biblioteki1, name="Koordynowanie pobierania bibliotek").start())

    def wybierz_tryb(self):
        global tryb
        wybrany_tryb = self.combo_box.currentText()
        tryb = wybrany_tryb
        print(Fore.LIGHTBLACK_EX + f"Wybrano tryb: {wybrany_tryb}")


# --- Funkcja pomocnicza do bezpiecznego pobierania liczby rdzeni ---
def safe_cpu_count(logical: bool) -> int:
    count = psutil.cpu_count(logical=logical)
    if count is None or count < 1:
        # Domyślnie minimalnie 1 rdzeń, bo inaczej nie ma sensu
        print(Fore.YELLOW +
              f"Uwaga: Nie wykryto liczby {'logiczych' if logical else 'fizycznych'} rdzeni. Ustawiam 1.")
        return 1
    return count


# --- Pobierz ilość rdzeni fizycznych i logicznych ---
physical_cores = safe_cpu_count(logical=False)
logical_cores = safe_cpu_count(logical=True)


# --- Wybór ilości wątków na podstawie rdzeni (max, ilość rdzeni) ---
MAX_THREADS_biblioteki = min(21, physical_cores)
MAX_THREADS_aktualizacja = min(9, physical_cores)

sema = threading.Semaphore(MAX_THREADS_biblioteki)
sema2 = threading.Semaphore(MAX_THREADS_aktualizacja)

minimalna_watkow = logical_cores

print(Fore.LIGHTBLACK_EX + f"Ilość rdzeni fizycznych: {physical_cores}")
print(Fore.LIGHTBLACK_EX + f"Ilość procesorów logicznych: {logical_cores}")


# --- Funkcja monitorująca zużycie CPU i zarządzająca wątkami ---
def monitor_cpu_usage():
    global minimalna_watkow
    global MAX_THREADS_biblioteki
    global tryb
    global sema
    global tryb_stary
    global max_ilosc_zatrzymanych_watkow

    tryb_stary = "no"
    MAX_THREADS_biblioteki_stary = None

    def ustaw_wartosci_wstepne():
        if tryb == "Procesory logiczne (max)":
            max_threads = logical_cores
            minimalna = logical_cores
        elif tryb == "Rdzenie (max)":
            max_threads = physical_cores
            minimalna = physical_cores
        elif tryb == "1":
            max_threads = 1
            minimalna = 1
        elif tryb == "2":
            max_threads = 2
            minimalna = 2
        else:  # Automatyczny tryb
            max_threads = physical_cores
            minimalna = 2

        max_zatrzymane = max(0, (max_threads // 2) - 1)
        return max_threads, minimalna, max_zatrzymane

    MAX_THREADS_biblioteki, minimalna_watkow, max_ilosc_zatrzymanych_watkow = ustaw_wartosci_wstepne()
    sema = threading.Semaphore(MAX_THREADS_biblioteki)

    print(
        f"Maksymalna ilość wątków w trybie '{tryb}': {MAX_THREADS_biblioteki}")
    print(
        f"Maksymalna ilość zatrzymanych wątków jednocześnie: {max_ilosc_zatrzymanych_watkow}")

    param_lock = threading.Lock()

    while True:
        if tryb_stary != tryb:
            with param_lock:
                MAX_THREADS_biblioteki, minimalna_watkow, max_ilosc_zatrzymanych_watkow = ustaw_wartosci_wstepne()
                sema = threading.Semaphore(MAX_THREADS_biblioteki)
            print(
                f"[Zmiana trybu] Maksymalna ilość wątków: {MAX_THREADS_biblioteki}")
            print(
                f"[Zmiana trybu] Maksymalna ilość zatrzymanych wątków: {max_ilosc_zatrzymanych_watkow}")

        cpu_percent = psutil.cpu_percent(interval=1)
        disk_percent = psutil.disk_usage('/').percent  # monitorowanie dysku

        # Dynamiczna adaptacja tylko dla trybu automatycznego
        if tryb not in ["Procesory logiczne (max)", "Rdzenie (max)", "1", "2"]:
            if minimalna_watkow > 1:
                max_limit = physical_cores + (logical_cores // 2)
                if cpu_percent < 50.0 and disk_percent < 80.0:
                    if MAX_THREADS_biblioteki < max_limit:
                        MAX_THREADS_biblioteki += 1
                        max_ilosc_zatrzymanych_watkow = max(
                            0, (MAX_THREADS_biblioteki // 2) - 1)
                        sema = threading.Semaphore(MAX_THREADS_biblioteki)
                        print(
                            Fore.GREEN + f"CPU < 50% i dysk < 80%, zwiększam wątki do {MAX_THREADS_biblioteki}")
                elif cpu_percent > 85.0 or disk_percent > 95.0:
                    if MAX_THREADS_biblioteki > minimalna_watkow:
                        MAX_THREADS_biblioteki -= 1
                        max_ilosc_zatrzymanych_watkow = max(
                            0, (MAX_THREADS_biblioteki // 2) - 1)
                        sema = threading.Semaphore(MAX_THREADS_biblioteki)
                        print(
                            Fore.RED + f"CPU > 85% lub dysk > 95%, zmniejszam wątki do {MAX_THREADS_biblioteki}")

        if MAX_THREADS_biblioteki_stary != MAX_THREADS_biblioteki:
            print(Fore.LIGHTCYAN_EX +
                  f"Aktualna maksymalna ilość wątków: {MAX_THREADS_biblioteki}; zużycie CPU: {cpu_percent}%; zużycie dysku: {disk_percent}%")
            print(Fore.LIGHTBLACK_EX +
                  f"Maksymalna ilość zatrzymanych wątków: {max_ilosc_zatrzymanych_watkow}")

        tryb_stary = tryb
        MAX_THREADS_biblioteki_stary = MAX_THREADS_biblioteki
        time.sleep(1)


# --- Uruchomienie wątku monitorującego CPU ---
thread_CPU = threading.Thread(
    target=monitor_cpu_usage, name="monitor_cpu", daemon=True)
thread_CPU.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
