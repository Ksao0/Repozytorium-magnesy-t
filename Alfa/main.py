import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests
from time import sleep

print('Nie zamykaj tego okna!')
print('Wykonywanie czynności początkowych...')


def aktul():
    os.system('cls')
    # Ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
    path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

    # Usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # Pobierz plik Aktualizator_aktualizatora.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Aktualizator_aktualizatora.py"
    urllib.request.urlretrieve(url, path)

    print('Aktualizowanie...')
    Aktualizacja = ["python", "Aktualizator_aktualizatora.py"]
    subprocess.run(Aktualizacja)
    print('Zakończono! ')
    print('Uruchom program ponownie, aby wprowadzić ewentualne zmiany')


def wykasuj_zapisy():
    # Ścieżka do pliku Zapisy.txt w bieżącym folderze
    path = os.path.join(os.getcwd(), "Zapisy.txt")

    # Usuń plik Zapisy.txt, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
        with open('Zapisy.txt', mode='w', encoding='utf-8') as file:
            file.write('')


def rozwiaz_problemy():
    os.system('cls')
    print('Wszystkie dane (ceny, poprzednie obliczenia, informacje o wersji, niektóre pliki aktualizacyjne, oraz sam program) zostaną usunięte. Tej operacji nie można cofnąć\nAby zainstalowaać program ponownie: Uruchom plik Aktualizator_aktualizatora.py')
    input("Naciśnij klawisz Enter, aby potwierdzić operację...")
    print('Aby anulować wpisz cokolwiek innego:')
    usuwanie_danych_potwierdzenie = str(
        input('Napisz "USUN01" (pamiętaj o dużych literach i braku polskich znaków), aby potwierdzić: '))
    if usuwanie_danych_potwierdzenie == "USUN01":
        print('Wszystkie dane zostały usunięte')
        # Ścieżka do pliku w bieżącym folderze
        path = os.path.join(os.getcwd(), "Ceny.txt")

        # Usuń plik jeśli istnieje
        if os.path.exists(path):
            os.remove(path)

            # Ścieżka do pliku w bieżącym folderze
        path = os.path.join(os.getcwd(), "version.txt")

        # Usuń plik jeśli istnieje
        if os.path.exists(path):
            os.remove(path)

            # Ścieżka do pliku w bieżącym folderze
        path = os.path.join(os.getcwd(), "Aktualizacja.py")

        # Usuń plik jeśli istnieje
        if os.path.exists(path):
            os.remove(path)

            # Ścieżka do pliku w bieżącym folderze
        path = os.path.join(os.getcwd(), "main.py")

        # Usuń plik jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
            sleep(3)
            exit()
        
    else:
        print('Anulowano')


def edycja_kosztow():
    okno_zmiany = tk.Toplevel()
    okno_zmiany.title("Zmiana kosztów")
    okno_zmiany.geometry("370x300+800+290")
    okno_zmiany.grab_set()

    def edycja_kosztow_wczytaj():
        ceny_tektura = str(entry_cena_tektura.get())
        ceny_nadruk = str(entry_cena_nadruk.get())
        ceny_foliamg = str(entry_cena_foliamg.get())
        ceny_woreczkipp = str(entry_cena_woreczkipp.get())

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

    def edycja_kosztow_domyslna():
        ceny_tektura = str(entry_cena_tektura.get())
        ceny_nadruk = str(entry_cena_nadruk.get())
        ceny_foliamg = str(entry_cena_foliamg.get())
        ceny_woreczkipp = str(entry_cena_woreczkipp.get())

        path = os.path.join(os.getcwd(), "Ceny.txt")

        if os.path.exists(path):
            os.remove(path)

        with open("Ceny.txt", "a", encoding='utf-8') as plik:
            plik.write('13')
            plik.write('\n')
            plik.write('35')
            plik.write('\n')
            plik.write('18')
            plik.write('\n')
            plik.write('11')
        if not os.path.isfile("Ceny.txt"):
            open("Ceny.txt", "w", encoding='utf-8').close()
            plik.write('13')
            plik.write('\n')
            plik.write('35')
            plik.write('\n')
            plik.write('18')
            plik.write('\n')
            plik.write('11')

    # ścieżka do pliku Ceny.txt w bieżącym folderze
    path = os.path.join(os.getcwd(), "Ceny.txt")

    # zapisz zawartość pliku Ceny.txt do zmiennej teraz_ceny
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as f:
            teraz_ceny = f.read()
        if not os.path.isfile("Ceny.txt"):
            open("Ceny.txt", "w", encoding='utf-8').close()
            f.write('13')
            f.write('35')
            f.write('18')
            f.write('11')
    else:
        teraz_ceny = "13\n35\n18\n11"

    ceny_tektura = round(float(teraz_ceny.split('\n')[0]), 2)
    if ceny_tektura == '' or ceny_tektura == 201:
        ceny_tektura = 13
    ceny_nadruk = round(float(teraz_ceny.split('\n')[1]), 2)
    if ceny_nadruk == '' or ceny_nadruk == 201:
        ceny_nadruk = 35
    ceny_foliamg = round(float(teraz_ceny.split('\n')[2]), 2)
    if ceny_foliamg == '' or ceny_foliamg == 201:
        ceny_foliamg = 18
    ceny_woreczkipp = round(float(teraz_ceny.split('\n')[3]), 2)
    if ceny_woreczkipp == '' or ceny_woreczkipp == 201:
        ceny_woreczkipp = 11

    label_tektura = tk.Label(
        okno_zmiany, text=f"Aktualna cena za tekturę: {ceny_tektura}zł,    Domyślna: 13,00zł".rjust(50))
    label_tektura.pack()
    label_nadruk = tk.Label(
        okno_zmiany, text=f"Aktualna cena za nadruk: {ceny_nadruk}zł,    Domyślna: 35,00zł".rjust(50))
    label_nadruk.pack()
    label_foliamg = tk.Label(
        okno_zmiany, text=f"Aktualna cena za folię: {ceny_foliamg}zł,    Domyślna: 18,00zł".rjust(50))
    label_foliamg.pack()
    label_woreczkipp = tk.Label(
        okno_zmiany, text=f"Aktualna cena za woreczki: {ceny_woreczkipp}zł,    Domyślna: 11,00zł".rjust(50))
    label_woreczkipp.pack()

    label_cena_tektura = tk.Label(okno_zmiany, text="Zmiana ceny tektury:")
    label_cena_tektura.pack()
    entry_cena_tektura = tk.Entry(okno_zmiany)
    entry_cena_tektura.pack()

    label_cena_nadruk = tk.Label(okno_zmiany, text="Zmiana ceny nadruk:")
    label_cena_nadruk.pack()
    entry_cena_nadruk = tk.Entry(okno_zmiany)
    entry_cena_nadruk.pack()

    label_cena_foliamg = tk.Label(okno_zmiany, text="Zmiana ceny folia:")
    label_cena_foliamg.pack()
    entry_cena_foliamg = tk.Entry(okno_zmiany)
    entry_cena_foliamg.pack()

    label_cena_woreczkipp = tk.Label(okno_zmiany, text="Zmiana ceny woreczki:")
    label_cena_woreczkipp.pack()
    entry_cena_woreczkipp = tk.Entry(okno_zmiany)
    entry_cena_woreczkipp.pack()

    pustka = tk.Label(okno_zmiany)
    pustka.pack()

    edycja = tk.Frame(okno_zmiany)
    edycja.pack()

    button_zmien = tk.Button(
        edycja, text="Zapisz zmiany", command=edycja_kosztow_wczytaj)
    button_zmien.pack(side=tk.LEFT)

    button_zmien_domyslne = tk.Button(
        edycja, text="Wczytaj domyślne", command=edycja_kosztow_domyslna)
    button_zmien_domyslne.pack(side=tk.RIGHT)


def oblicz_zyski():

    # Ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
    path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

    # Usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # Pobierz plik Aktualizator_aktualizatora.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Aktualizator_aktualizatora.py"
    urllib.request.urlretrieve(url, path)

    # Sprawdzenie, czy plik istnieje i ewentualne jego utworzenie
    if not os.path.isfile("Zapisy.txt"):
        open("Zapisy.txt", "w", encoding='utf-8').close()

    liczba_pakietow = float(entry_pakietow.get())
    if not liczba_pakietow.is_integer():
        messagebox.showerror(
            "Błąd", "Liczba pakietów nie może mieć wartości dziesiętnej")
    if liczba_pakietow <= 0:
        messagebox.showerror("Błąd", "Liczba pakietów musi być dodatnia")
        return

    cena_za_magnes = float(entry_ceny.get().replace(",", "."))

    if cena_za_magnes <= 0:
        messagebox.showerror("Błąd", "Cena za magnes musi być dodatnia")
        return

    now = datetime.datetime.now()

    data_obliczenia = now.strftime("%d.%m.%Y %H:%M:%S")

    # Liczenie kosztów

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
    label_wyniki.configure(text=wyniki.rjust(200))

    # Zapis wyników do pliku, jeśli zmienna zapis_do_pliku jest ustawiona na True

    # ścieżka do pliku Zapisy.txt w bieżącym folderze
    path = os.path.join(os.getcwd(), "Zapisy.txt")

    # zapisz zawartość pliku Zapisy.txt do zmiennej stare_zapisy
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as f:
            stare_zapisy = f.read()
    else:
        stare_zapisy = ""

    # usuń plik Zapisy.txt, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # print("Usunięto plik Zapisy.txt")

    if zapis_do_pliku.get():
        with open("Zapisy.txt", "a", encoding='utf-8') as plik:
            plik.write(wyniki)
            plik.write(stare_zapisy)
        if not os.path.isfile("Zapisy.txt"):
            open("Zapisy.txt", "w", encoding='utf-8').close()
            plik.write(wyniki)
            plik.write(stare_zapisy)


# Tworzenie głównego okna

print('Sprawdzanie dostępności aktualizacji...')
# pobierz zawartość pliku version.txt z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/version.txt'
response = requests.get(url)

version_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku version.txt w twoim programie
path = os.path.join(os.getcwd(), "version.txt")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        version_local = f.read().strip()
else:
    version_local = "BRAK DANYCH"

# wyświetl tylko pierwszą linijkę wersji
version_local_first_line = version_local.split('\n')[0]
version_online_first_line = version_online.split('\n')[0]

# porównaj wersje
print(f'\nWersja na komputerze: {version_local_first_line}')
print(f'Wersja w repozytorium: {version_online_first_line}')
print(f'\nOpis najnowszej wersji (repozytorium): {version_online}')
if version_local != "BRAK DANYCH":
    if version_online.strip() == version_local.strip():
        print('Masz najnowszą wersję programu.')
        path = os.path.join(os.getcwd(), "version.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                version_local = f.readline().strip()
        wersja = version_local
    else:
        if version_local_first_line == version_online_first_line:
            print('Masz najnowszą wersję programu.')
            wersja = version_local
            # ścieżka do pliku version.txt w bieżącym folderze
            path = os.path.join(os.getcwd(), "version.txt")

            # usuń plik version.txt, jeśli istnieje
            if os.path.exists(path):
                os.remove(path)
            # print("Usunięto plik version.txt")

            # pobierz plik version.txt z repozytorium i utwórz go
            url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/version.txt"
            urllib.request.urlretrieve(url, path)
        else:
            print('Dostępna jest nowa wersja programu.')
            wersja = "DOSTĘPNA AKTUALIZACJA"
else:
    print('Wykryto brak niektórych plików. Zaktualizuj program, aby program działał prawidłowo')
    wersja = "ZAKTUALIZUJ PROGRAM"


root = tk.Tk()
root.title(f"Kalkulator zysków ver. {wersja}")
root.geometry("410x350")

zapis_do_pliku = tk.BooleanVar()
zapis_do_pliku.set(True)


def otworz_okno_wybor():
    okno_wyborowe = tk.Toplevel()
    okno_wyborowe.title("Okno wyborowe")
    okno_wyborowe.geometry("370x290+800+0")
    okno_wyborowe.grab_set()

    # Dodanie przycisku do nowego okna
    button = tk.Button(okno_wyborowe, text="Aktualizacja (terminal)",
                       command=aktul)
    button.pack()
    label_informacja = tk.Label(
        okno_wyborowe, text="Do wyboru są dwie stale aktualizowane wersje:\nAlfa i Beta")
    label_informacja.pack()
    button_wykasuj_zapisy = tk.Button(okno_wyborowe, text="Wykasuj informacje o zapisach",
                                      command=wykasuj_zapisy)
    button_wykasuj_zapisy.pack()
    label_informacja = tk.Label(
        okno_wyborowe, text="Zostaną usunięte informacje o poprzednich oblczeniach.\nTej operacji nie można cofnąć.")
    label_informacja.pack()

    button_zmiana_danych = tk.Button(
        okno_wyborowe, text="Edytuj dane", command=edycja_kosztow)
    button_zmiana_danych.pack()

    label_informacja = tk.Label(
        okno_wyborowe, text="Zmień przyjęte przez program parametry.\nJeśli wystąpią problemy z funkcją: Stwórz plik Ceny.txt\nz zawartością czterech dowolnych cyfr\n Każda w nowej linii")
    label_informacja.pack()

    button_rozwiaz_problemy = tk.Button(
        okno_wyborowe, text="Rozwiąż problemy (terminal)", command=rozwiaz_problemy)
    button_rozwiaz_problemy.pack()
    label_informacja = tk.Label(
        okno_wyborowe, text="Program zostanie zresetowany.\nWszystkie dane zostaną usunięte")
    label_informacja.pack()


def otworz_okno_zapisy():
    with open("Zapisy.txt", "r", encoding='utf-8') as plik:
        zawartosc = plik.read()

    # Tworzenie nowego okna
    okno = tk.Toplevel()
    okno.title("Historia")
    okno.geometry("800x900")

    # Dodanie elementu ScrolledText
    pole_tekstowe = scrolledtext.ScrolledText(okno, wrap=tk.WORD)
    pole_tekstowe.pack(expand=True, fill=tk.BOTH)

    # Wstawienie zawartości pliku do elementu ScrolledText
    pole_tekstowe.insert(tk.END, zawartosc)


# Dodanie etykiet i pól tekstowych
label_pakietow = tk.Label(root, text="Liczba pakietów:")
label_pakietow.pack()
entry_pakietow = tk.Entry(root)
entry_pakietow.pack()

label_ceny = tk.Label(root, text="Cena za magnes:")
label_ceny.pack()
entry_ceny = tk.Entry(root)
entry_ceny.pack()


pustka = tk.Label()
pustka.pack()


# Dodanie kontenera typu Frame
frame_przyciski = tk.Frame(root)
frame_przyciski.pack()

# Dodanie przycisków do kontenera
button_oblicz = tk.Button(frame_przyciski, text="Oblicz", command=oblicz_zyski)
button_oblicz.pack(side=tk.LEFT)

checkbox_zapis = tk.Checkbutton(
    root, text="Zapisz wyniki do pliku", variable=zapis_do_pliku)
checkbox_zapis.pack()

# Przycisk otwierajacy drugie okno o nazwie historia
button_historia = tk.Button(
    frame_przyciski, text="Historia", command=otworz_okno_zapisy)
button_historia.pack(side=tk.LEFT)

# Przycisk więcej opcji
button_wiecej = tk.Button(
    frame_przyciski, text="Więcej opcji", command=otworz_okno_wybor)
button_wiecej.pack(side=tk.LEFT)

# Dodanie pola tekstowego na wyniki
label_wyniki = tk.Label(root, text="", justify="left")
label_wyniki.pack()

root.mainloop()
