import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests

print('Nie zamykaj tego okna!')


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
    print('Zakończono aktualizację! ')
    print('Uruchom program ponownie, aby wprowadzić zmiany')


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
    magnesy_w_pakiecie = liczba_pakietow * 224
    cena_za_pakiet = cena_za_magnes * 224
    razem = cena_za_pakiet * liczba_pakietow

    tektura = 13 * liczba_pakietow
    nadruk = 35 * liczba_pakietow
    foliamg = 18 * liczba_pakietow
    woreczkipp = 11 * liczba_pakietow

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
    okno_wyborowe.geometry("300x200+800+0")
    okno_wyborowe.grab_set()

    # Dodanie przycisku do nowego okna
    button = tk.Button(okno_wyborowe, text="Aktualizacja (terminal)",
                       command=aktul)
    button.pack()
    label_informacja = tk.Label(
        okno_wyborowe, text="Z czasem będzie tu dodawane więcej opcji")
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
button_aktul = tk.Button(
    frame_przyciski, text="Więcej opcji", command=otworz_okno_wybor)
button_aktul.pack(side=tk.LEFT)

# Dodanie pola tekstowego na wyniki
label_wyniki = tk.Label(root, text="", justify="left")
label_wyniki.pack()

root.mainloop()
