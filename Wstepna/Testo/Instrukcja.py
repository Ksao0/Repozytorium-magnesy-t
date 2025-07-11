import os
from PyQt5.QtGui import QColor

# Bufor do przechowywania historii terminala
log = []
# Do wykorzystania przy zadaniach
# from prompt_toolkit.shortcuts import button_dialog
#
# result = button_dialog(
#    title="Wybierz opcję",
#    text="Z czym masz problem?",
#    buttons=[
#        ("Edycja danych", "1"),
#        ("Historia zmian", "2"),
#        ("Aktualizacja programu", "3"),
#    ]
# ).run()
#
# print(f"Wybrano: {result}")


class KolorowyText:
    def __init__(self, text):
        self.text = text
        self.fg_color = None
        self.bg_color = None
        self.styles = []

    def kolor(self, nazwa):
        self.fg_color = QColor(nazwa)
        return self

    def tlo(self, nazwa):
        self.bg_color = QColor(nazwa)
        return self

    def pogrubiony(self):
        self.styles.append('1')
        return self

    def kursywa(self):
        self.styles.append('3')
        return self

    def podkreslony(self):
        self.styles.append('4')
        return self

    def przekreslony(self):
        self.styles.append('9')
        return self

    def build(self):
        sekwencje = list(self.styles)

        if self.fg_color and self.fg_color.isValid():
            r, g, b, _ = self.fg_color.getRgb()
            sekwencje.append(f"38;2;{r};{g};{b}")

        if self.bg_color and self.bg_color.isValid():
            r, g, b, _ = self.bg_color.getRgb()
            sekwencje.append(f"48;2;{r};{g};{b}")

        if sekwencje:
            prefix = f"\033[{';'.join(sekwencje)}m"
            suffix = "\033[0m"
            return f"{prefix}{self.text}{suffix}"
        else:
            return self.text

    def __str__(self):
        return self.build()


def auto_kolor(tekst, typ, newline=False):
    if typ == "pytanie":
        kol = KolorowyText(tekst).kolor("mediumseagreen").pogrubiony()
    elif typ == "opcje":
        kol = KolorowyText(tekst).kolor("lightseagreen")
    elif typ == "nawias":
        kol = KolorowyText(tekst).kolor("seagreen")
    elif typ == "odpowiedz":
        kol = KolorowyText(tekst).kolor("slateblue").pogrubiony().podkreslony()
    elif typ == "tresc":
        kol = KolorowyText(tekst).kolor("teal")
    elif typ == "tresc1":
        kol = KolorowyText(tekst).kolor("lightseagreen")
    else:
        kol = KolorowyText(tekst)

    gotowy = str(kol) + ('\n' if newline else '')
    log.append(gotowy)
    print(gotowy, end='')


def czysc_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def wczytaj_i_odswiez(prompt=">> ", typ="odpowiedz"):
    odpowiedz = input(prompt)
    czysc_terminal()
    for linia in log:
        print(linia, end='')  # nie dodaje dodatkowego newline
    auto_kolor(f"{prompt}{odpowiedz}\n", typ)
    return odpowiedz


def glowny_program():
    auto_kolor("Z czym masz problem? ", "pytanie")
    auto_kolor('(1-5 i enter jako zatwierdzenie)\n', 'nawias')
    auto_kolor("1 - Edycja danych i wprowadzanie ", "opcje")
    auto_kolor(
        "(Zmiana przewidywanych kosztów, wpisywanie pakietów i cen za magnes)\n", "nawias")
    auto_kolor("2 - Historia zmian\n", "opcje")
    auto_kolor("3 - Aktualizacja programu\n", "opcje")

    odpowiedz = wczytaj_i_odswiez()
    if odpowiedz == "1":
        auto_kolor(
            'Główne okno podzielone jest na trzy sekcje (od lewej: obliczenia, historia, ceny).\nW ', 'tresc')

        auto_kolor('sekcji pierwszej (obliczanie) ', 'tresc1')
        auto_kolor(
            '(od góry) widoczne są dwa pola do wpisywania - ', 'tresc')
        auto_kolor('Ilość pakietów', 'tresc1')
        auto_kolor(' i ', 'tresc')
        auto_kolor('Cena za magnes ', 'tresc1')
        auto_kolor('oraz trzy etykiety wypisujące obliczone wartości ', 'tresc')
        auto_kolor('(Zarobisz, Wydasz, Całkowita wartość pakietów)', 'tresc1')
        auto_kolor(
            ' i przypomnienie o opcji liczenia w trybie za magnes\n Etykiety pokazują wynki po naciśnięciu przycisku ', 'tresc')
        auto_kolor('Oblicz ', 'tresc1')
        auto_kolor('w tej sekcji.', 'tresc')

    k = input()


if __name__ == "__main__":
    glowny_program()
