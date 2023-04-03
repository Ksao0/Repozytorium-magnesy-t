import os
import urllib.request
import datetime
# ścieżka do pliku main.py w bieżącym folderze
path = os.path.join(os.getcwd(), "main.py")

# usuń plik main.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
print("Usunięto plik main.py")
# pobierz plik main.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/main.py"
urllib.request.urlretrieve(url, path)
print("Zastąpiono plik main.py")

# ścieżka do pliku version.txt w bieżącym folderze
path = os.path.join(os.getcwd(), "version.txt")

# zapisz zawartość pliku version.txt do zmiennej stara_version
if os.path.exists(path):
    with open(path, "r") as f:
        stara_version = f.read()
else:
    stara_version = ""

# usuń plik version.txt, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
print("Usunięto plik version.txt")

# pobierz plik version.txt z repozytorium i utwórz go
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/version.txt"
urllib.request.urlretrieve(url, path)
print("Zastąpiono plik version.txt")

# odczytaj zawartość pliku version.txt do zmiennej nowa_version
with open(path, "r") as f:
    nowa_version = f.read()

now = datetime.datetime.now()
data_obliczenia = now.strftime("%d.%m.%Y %H:%M")

with open("Zapisy.txt", "a") as plik:
    plik.write(
        f"          Zaktualizowano program do nowej wersji! data: {data_obliczenia}\n")
    plik.write(f"           Stara wersja: {stara_version}\n")
    plik.write(f"           Nowa wersja: {nowa_version}\n\n")

print(f"Stara wersja: {stara_version}\n")
print(f"Nowa wersja: {nowa_version}\n\n")

# NOWA FUNKCJA

# nazwa pliku do utworzenia
nazwa_pliku = 'Uruchamianie.py'

# usuń plik o nazwie 'Uruchamianie.py', jeśli taki istnieje
if os.path.exists(nazwa_pliku):
    os.remove(nazwa_pliku)
    print(f'Usunięto plik {nazwa_pliku}.')

# otwórz plik w trybie zapisu
with open(nazwa_pliku, 'w') as plik:
    # zapisz dane do pliku
    plik.write('import os\n')
    plik.write('import tkinter as tk\n')
    plik.write('from tkinter import messagebox\n')
    plik.write('from tkinter import scrolledtext\n')
    plik.write('# Włączanie aktualizacji obu poziomów, a następnie programu
# wyświetl komunikat o zakończeniu zapisu
print(f'Plik {nazwa_pliku} został utworzony i zapisany.')

# KONIEC NOWEJ FUNKCJI

input("Naciśnij klawisz Enter, aby zakończyć program...")
