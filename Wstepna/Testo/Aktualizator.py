import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDoubleSpinBox, QLabel, QSpinBox, QTextEdit, QProgressBar
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
import messagebox
import datetime
import urllib
import urllib.request
import subprocess
import time

from github import Github

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

            urllib.request.urlretrieve(url, path)

            current_size += self.get_file_size(url)
            progress_percentage = int((current_size / total_size) * 100)
            self.aktualizacja_zakonczona.emit(progress_percentage)

        # Emitowanie sygnału z wartością 100, gdy wszystkie pliki są pobrane
        self.aktualizacja_zakonczona.emit(100)

    def get_file_size(self, url):
        with urllib.request.urlopen(url) as response:
            return int(response.getheader('Content-Length', 0))

class OknoAktualizacji(QWidget):
    def __init__(self):
        super().__init__()

        self.urls = [
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Aktualizator.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/main.py"
            # Dodaj tutaj inne URL-e do plików, jeśli są
        ]

        self.inicjalizuj_ui()

    def inicjalizuj_ui(self):
        układ = QGridLayout()

        etykieta_info = QLabel('Dostępna jest nowa aktualizacja. Czy chcesz zaktualizować aplikację?')
        układ.addWidget(etykieta_info, 0, 0, 1, 2)

        self.pasek_postępu = QProgressBar()
        układ.addWidget(self.pasek_postępu, 1, 0, 1, 2)

        przycisk_tak = QPushButton('Tak')
        przycisk_anuluj = QPushButton('Anuluj')

        przycisk_tak.clicked.connect(self.rozpocznij_aktualizacje)
        przycisk_anuluj.clicked.connect(self.anuluj_aktualizacje)

        układ.addWidget(przycisk_tak, 2, 0)
        układ.addWidget(przycisk_anuluj, 2, 1)

        self.setLayout(układ)
        self.setWindowTitle('Okno Aktualizatora')
        self.setGeometry(200, 200, 400, 150)

        self.pasek_postępu.setValue(0)
        self.watek_aktualizacji = AktualizacjaWatek(self.urls)
        self.watek_aktualizacji.aktualizacja_zakonczona.connect(self.zakoncz_aktualizacje)

    def rozpocznij_aktualizacje(self):
        print('Rozpoczęcie aktualizacji...')
        self.pasek_postępu.setValue(0)
        self.watek_aktualizacji.start()

    def zakoncz_aktualizacje(self, value):
        self.pasek_postępu.setValue(value)
        if value == 100:
            print('Aktualizacja zakończona.')
            # Tutaj dodano uruchomienie programu z nowego pliku main.py po zakończeniu aktualizacji
            subprocess.run(["python", "Aktualizator.py"])
            self.close()
            # QCoreApplication.quit()  # Zamknij cały program po zakończeniu aktualizacji


    def anuluj_aktualizacje(self):
        print('Aktualizacja anulowana.')
        self.watek_aktualizacji.terminate()
        self.close()





class OknoUstawien(QWidget):

    def __init__(self):
        super().__init__()

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

        # Dodaj więcej elementów do okna ustawień, jeśli jest to konieczne

        # Ustawiamy układ dla okna ustawień
        self.setLayout(układ)

        # Ustawiamy tytuł i rozmiar okna ustawień
        self.setWindowTitle('Okno Ustawień')
        self.setGeometry(900, 300, 400, 300)

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
        self.setWindowTitle('Aktualizator ')
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



if __name__ == '__main__':
    # Inicjalizujemy aplikację
    app = QApplication(sys.argv)

    # Tworzymy instancję klasy ZaawansowaneOkno
    okno = ZaawansowaneOkno()

    # Wyświetlamy główne okno
    okno.show()

    # Uruchamiamy pętlę główną
    sys.exit(app.exec_())
