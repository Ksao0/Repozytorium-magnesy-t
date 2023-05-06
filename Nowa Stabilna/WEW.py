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
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/main.py"
urllib.request.urlretrieve(url, path)
# print("Zastąpiono plik main.py")

# Aktualizacja pliku Aktualizator_aktualizatora

# ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

# usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
# print("Usunięto plik Aktualizator_aktualizatora.py")
# pobierz plik main.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Aktualizator_aktualizatora.py"
urllib.request.urlretrieve(url, path)
# print("Zastąpiono plik Aktualizator_aktualizatora.py")

# Koniec dla: Aktualizacja pliku Aktualizator_aktualizatora

# ścieżka do pliku version.txt w bieżącym folderze
path = os.path.join(os.getcwd(), "version.txt")

# zapisz zawartość pliku version.txt do zmiennej stara_version
if os.path.exists(path):
    with open(path, "r", encoding='utf-8') as f:
        stara_version = f.read()
else:
    stara_version = "BRAK DANYCH"

# usuń plik version.txt, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
# print("Usunięto plik version.txt")

# pobierz plik version.txt z repozytorium i utwórz go
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/version.txt"
urllib.request.urlretrieve(url, path)
# print("Zastąpiono plik version.txt")

# odczytaj zawartość pliku version.txt do zmiennej nowa_version
with open(path, "r", encoding='utf-8') as f:
    nowa_version = f.read()

now = datetime.datetime.now()
data_obliczenia = now.strftime("%d.%m.%Y %H:%M:%S")

# Sprawdzenie, czy plik istnieje i ewentualne jego utworzenie
if not os.path.isfile("Zapisy.txt"):
    open("Zapisy.txt", "w", encoding='utf-8').close()

# ścieżka do pliku Zapisy.txt w bieżącym folderze
path = os.path.join(os.getcwd(), "zapisy.txt")

# zapisz zawartość pliku zapisy.txt do zmiennej stara_zapisy
if os.path.exists(path):
    with open(path, "r", encoding='utf-8') as f:
        stara_zapisy = f.read()
else:
    stara_zapisy = ""

# usuń plik zapisy.txt, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
# print("Usunięto plik zapisy.txt")

# Aktualizacja pliku Aktualizator_aktualizatora

# ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

# usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
# print("Usunięto plik Aktualizator_aktualizatora.py")
# pobierz plik main.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Stabilna/Aktualizator_aktualizatora.py"
urllib.request.urlretrieve(url, path)
# print("Zastąpiono plik Aktualizator_aktualizatora.py")
