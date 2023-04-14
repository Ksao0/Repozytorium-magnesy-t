import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess


def aktul():
    # Ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
    path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

    # Usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # Pobierz plik Aktualizator_aktualizatora.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Aktualizator_aktualizatora.py"
    urllib.request.urlretrieve(url, path)

    print('Aktualizowanie...')
    Aktualizacja = ["python", "Aktualizator_aktualizatora.py"]
    subprocess.run(Aktualizacja)
    print('Zakończono aktualizację! ')

    # ścieżka do pliku version.txt w bieżącym folderze
    path = os.path.join(os.getcwd(), "version.txt")

    # zapisz zawartość pliku version.txt do zmiennej stara_version
    if os.path.exists(path):
        with open(path, "r", encoding='utf-8') as f:
            stara_version = f.read()
    else:
        stara_version = ""

    # usuń plik version.txt, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # print("Usunięto plik version.txt")

    # pobierz plik version.txt z repozytorium i utwórz go
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/version.txt"
    urllib.request.urlretrieve(url, path)
    # print("Zastąpiono plik version.txt")

    # odczytaj zawartość pliku version.txt do zmiennej nowa_version
    with open(path, "r", encoding='utf-8') as f:
        nowa_version = f.read()

    now = datetime.datetime.now()
    data_obliczenia = now.strftime("%d.%m.%Y %H:%M")

    with open("Zapisy.txt", "a", encoding='utf-8') as plik:
        plik.write(
            f"\n          Zaktualizowano program do nowej wersji! Uruchom ponownie, aby wprowadzić zmiany! Data: {data_obliczenia}\n")
        plik.write(f"           Stara wersja: {stara_version}\n")
        plik.write(f"           Nowa wersja: {nowa_version}\n\n")

    print(f"Stara wersja: {stara_version}\n")
    print(f"Nowa wersja: {nowa_version}\n\n")
    print('Uruchom ponownie program, aby wprowadzić zmiany')


def oblicz_zyski():

    # Ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
    path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

    # Usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # Pobierz plik Aktualizator_aktualizatora.py z repozytorium
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Aktualizator_aktualizatora.py"
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

    data_obliczenia = now.strftime("%d.%m.%Y %H:%M")

    # Liczenie kosztów
    magnesy_w_pakiecie = liczba_pakietow * 224
    cena_za_pakiet = cena_za_magnes * 224
    razem = cena_za_pakiet * liczba_pakietow

    tektura = 12 * liczba_pakietow
    nadruk = 35 * liczba_pakietow
    foliamg = 18 * liczba_pakietow
    woreczkipp = 11 * liczba_pakietow

    nowy_koszt = 123 * liczba_pakietow

    koszty = tektura + nadruk + foliamg + woreczkipp + nowy_koszt
    bilans = razem - koszty

    wyniki = f"Data: {data_obliczenia}\nKoszty: {koszty:.2f} zł\nZysk sprzedaży: {bilans:.2f} zł\nLiczba pakietów: {liczba_pakietow} szt.\nLiczba magnesów: {magnesy_w_pakiecie} szt.\nCena za 1 magnes: {cena_za_magnes:.2f} zł\nJeden pakiet to: {cena_za_pakiet:.2f} zł\nCena za wszystkie pakiety: {razem:.2f} zł\n\n"
    label_wyniki.configure(text=wyniki)

    # Zapis wyników do pliku, jeśli zmienna zapis_do_pliku jest ustawiona na True
    if zapis_do_pliku.get():
        with open("Zapisy.txt", "a", encoding='utf-8') as plik:
            plik.write(wyniki)
        if not os.path.isfile("Zapisy.txt"):
            open("Zapisy.txt", "w", encoding='utf-8').close()
            plik.write(wyniki)


# Tworzenie głównego okna
root = tk.Tk()
root.title("Kalkulator zysków")
root.geometry("400x300")

zapis_do_pliku = tk.BooleanVar()
zapis_do_pliku.set(True)


def otworz_okno():
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
    frame_przyciski, text="Historia", command=otworz_okno)
button_historia.pack(side=tk.LEFT)

# Przycisk aktul
button_aktul = tk.Button(
    frame_przyciski, text="Aktualizacja (terminal)", command=aktul)
button_aktul.pack(side=tk.LEFT)

# Dodanie pola tekstowego na wyniki
label_wyniki = tk.Label(root, text="")
label_wyniki.pack()

root.mainloop()
