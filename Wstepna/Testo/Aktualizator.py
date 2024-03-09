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

        button_opinie = QPushButton('Aktualizuj', self)
        układ.addWidget(button_opinie, 0, 3, 1, 1)

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

        wyniki = f"Data: {data_obliczenia}\n\nLiczba pakietów: {liczba_pakietow} szt.\nLiczba magnesów: {magnesy_w_pakiecie} szt.\nCena za 1 magnes: {cena_za_magnes:.2f}zł\nJeden pakiet to: {cena_za_pakiet:.2f} zł\nKoszty: {koszty:.2f} zł\nZysk sprzedaży: {bilans:.2f} zł\nCena za wszystkie pakiety: {razem:.2f} zł\n\n"
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
