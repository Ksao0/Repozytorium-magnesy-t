import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from packaging import version
import ctypes
import colorama
from colorama import Fore, Style
import urllib.request
import subprocess

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Maksymalna szerokość okna
MAX_WIDTH = 550  # Możesz dostosować wartość do swoich preferencji

# Inicjalizacja Colorama
colorama.init()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Wczytujemy obraz
        image_path = "tropic.png"
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

        # Dodajemy napis
        text_label = QLabel("Instalator", self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet(
            "color: white; font-size: 16px; background-color: rgba(0, 0, 0, 0.5);")
        text_label.setGeometry(10, 10, width - 17, 30)

        # Dodajemy napis
        text_label_N = QLabel("Co nowego?", self)
        text_label_N.setStyleSheet(
            "color: white; font-size: 28px; text-align: center;")
        text_label_N.setGeometry(213, 75, 650, 45)

        # Dodajemy napis
        text_label_N2 = QLabel("""Proszę czekać""", self)
        text_label_N2.setStyleSheet(
            "color: white; font-size: 11.5px; text-align: center;")
        text_label_N2.setGeometry(130, 130, 320, 215)

        # Dodajemy przyciski
        button1 = QPushButton("Aktualizuj", self)
        button1.setGeometry(10, height - 40, 100, 30)

        button2 = QPushButton("Zainstaluj biblioteki", self)
        button2.setGeometry(120, height - 40, 125, 30)

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
                version_local = "1.0.0" if not os.path.exists(path) else open(
                    path, "r", encoding="utf-8").read().strip()

                najnowsza_wersja_online = version_online.split('\n')[0]
                local_aktualna_wersja = version_local.split('\n')[0]

                if version.parse(local_aktualna_wersja) < version.parse(najnowsza_wersja_online):
                    text_label.setText(
                        f'{local_aktualna_wersja} --> {najnowsza_wersja_online}')
                else:
                    text_label.setText(f'Masz najnowszą wersję')

                text_label_N2.setText("\n".join(version_opis.split('\n')[1:]))

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

                # Instaluj biblioteki, które nie są jeszcze zainstalowane
                for lib in libraries_to_install:
                    if lib not in installed_packages:
                        print(Fore.YELLOW + "Instalowanie biblioteki:", lib)
                        subprocess.run(["pip", "install", lib],
                                       capture_output=True, text=True)
                        print(Fore.GREEN + "Biblioteka", lib,
                              "została pomyślnie zainstalowana.")
                    else:
                        print(Fore.CYAN +
                              f"Biblioteka {lib} jest już zainstalowana.")

                print(Fore.GREEN +
                      "Wszystkie biblioteki zostały pomyślnie zainstalowane.")
            except Exception as e:
                print(Fore.RED + "Wystąpił błąd:", e)

        # Funkcja do uzyskania listy zainstalowanych pakietów
        def get_installed_packages():
            # Uzyskanie listy zainstalowanych pakietów za pomocą polecenia pip freeze
            try:
                installed_packages = subprocess.check_output(
                    ['pip', 'freeze']).decode().split('\n')
                # Usunięcie pustych elementów i zwrócenie listy pakietów
                return [pkg.split('==')[0] for pkg in installed_packages if pkg]
            except subprocess.CalledProcessError:
                # Obsługa błędu w przypadku niepowodzenia wykonania polecenia
                print("Nie udało się uzyskać listy zainstalowanych pakietów.")
                return []

        def aktualizacja():
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

                    for url in self.urls:
                        file_name = os.path.join(
                            self.folder_path, url.split('/')[-1])

                        if not os.path.exists(file_name):
                            print(
                                Fore.MAGENTA + f"Plik {file_name} nie istnieje na komputerze. Traktuję jako nieaktualny.")
                            self.download_file(url, file_name)
                        else:
                            if not self.compare_files(url, file_name):
                                print(Fore.LIGHTYELLOW_EX +
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
                sys.exit(1)

            # Ścieżka do pliku lista.txt w repozytorium
            lista_txt_url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/lista.txt"
            lista_txt_content = requests.get(lista_txt_url).text
            urls = [line.strip()
                    for line in lista_txt_content.split('\n') if line.strip()]

            automa = Automa(urls, folder_path)
            automa.run()

        # Przypisanie akcji do przycisków
        button1.clicked.connect(aktualizacja)
        button2.clicked.connect(zainstaluj_biblioteki)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.setStyleSheet(open('styl_instalator.css').read())
    sys.exit(app.exec_())
