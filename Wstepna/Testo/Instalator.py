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

        import subprocess
        import pkg_resources

        def zainstaluj_biblioteki():
            # Przywracanie widoczności okna terminala
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
            try:
                # Pobierz listę bibliotek z repozytorium
                libraries_to_install = requests.get(
                    'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/bib.txt').text.strip().split()

                # Sprawdź zainstalowane biblioteki
                installed_packages = [
                    pkg.key for pkg in pkg_resources.working_set]

                # Instaluj biblioteki, które nie są jeszcze zainstalowane
                for lib in libraries_to_install:
                    if lib not in installed_packages:
                        print(Fore.YELLOW + "Instalowanie biblioteki:", lib)
                        subprocess.run(["pip", "install", lib],
                                    capture_output=True, text=True)
                        print(Fore.GREEN + "Biblioteka", lib, "została pomyślnie zainstalowana.")
                    else:
                        print(Fore.CYAN + f"Biblioteka {lib} jest już zainstalowana.")

                print(Style.RESET_ALL + Fore.GREEN + "Wszystkie biblioteki zostały pomyślnie zainstalowane." + Style.RESET_ALL)

            except Exception as e:
                print(Fore.RED + "Wystąpił błąd:", e)

        # Przypisanie akcji do przycisków
        button1.clicked.connect(wersja)
        button2.clicked.connect(zainstaluj_biblioteki)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.setStyleSheet(open('styl_instalator.css').read())
    sys.exit(app.exec_())
