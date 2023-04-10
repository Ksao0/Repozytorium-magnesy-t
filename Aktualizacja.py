import os
import urllib.request
import datetime
# ścieżka do pliku main.py w bieżącym folderze
path = os.path.join(os.getcwd(), "main.py")

# usuń plik main.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
# print("Usunięto plik main.py")
# pobierz plik main.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/main.py"
urllib.request.urlretrieve(url, path)
# print("Zastąpiono plik main.py")

# NOWE FUNKCJE

### Aktualizacja pliku Aktualizator_aktualizatora

# ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

# usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
# print("Usunięto plik Aktualizator_aktualizatora.py")
# pobierz plik main.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Aktualizator_aktualizatora.py"
urllib.request.urlretrieve(url, path)
# print("Zastąpiono plik Aktualizator_aktualizatora.py")

### Koniec dla: Aktualizacja pliku Aktualizator_aktualizatora

# KONIEC NOWYCH FUNKCJI

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
        f"\n          Zaktualizowano program do nowej wersji! data: {data_obliczenia}\n")
    plik.write(f"           Stara wersja: {stara_version}\n")
    plik.write(f"           Nowa wersja: {nowa_version}\n\n")

print(f"Stara wersja: {stara_version}\n")
print(f"Nowa wersja: {nowa_version}\n\n")

# NOWE FUNKCJE

### Kasowanie Uruchamianie.py

# nazwa pliku
nazwa_pliku = 'Uruchamianie.py'

# usuń plik o nazwie 'Uruchamianie.py', jeśli taki istnieje
if os.path.exists(nazwa_pliku):
    os.remove(nazwa_pliku)
    print(f'Usunięto plik {nazwa_pliku}.')

### Koniec dla: Kasowanie Uruchamianie.py

### Aktualizacja pliku Aktualizator_aktualizatora

# ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

# usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
# print("Usunięto plik Aktualizator_aktualizatora.py")
# pobierz plik main.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Aktualizator_aktualizatora.py"
urllib.request.urlretrieve(url, path)
# print("Zastąpiono plik Aktualizator_aktualizatora.py")
print('Zakończono altualizację I poziomu')
### Koniec dla: Aktualizacja pliku Aktualizator_aktualizatora

# KONIEC NOWYCH FUNKCJI

input("Naciśnij klawisz Enter, aby zakończyć program...")
