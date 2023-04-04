import os
import urllib.request
import subprocess

# ścieżka do pliku Aktualizacja.py w bieżącym folderze
path = os.path.join(os.getcwd(), "Aktualizacja.py")

# usuń plik Aktualizacja.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
print("Rozpoczynanie aktualizacji II poziomu")
# pobierz plik Aktualizacja.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Aktualizacja.py"
urllib.request.urlretrieve(url, path)
print("Zakończono aktualizację II poziomu")
print('Rozpoczynanie aktualizacji I poziomu')

Aktualizacja = ["python", "Aktualizacja.py"]
subprocess.run(Aktualizacja)
