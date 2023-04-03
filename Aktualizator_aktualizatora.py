import os
import urllib.request

# ścieżka do pliku Aktualizator.py w bieżącym folderze
path = os.path.join(os.getcwd(), "Aktualizator.py")

# usuń plik Aktualizator.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
print("Usunięto plik Aktualizator.py")
# pobierz plik Aktualizator.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Aktualizator.py"
urllib.request.urlretrieve(url, path)
print("Zastąpiono plik Aktualizator.py")
