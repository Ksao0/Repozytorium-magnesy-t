import os
import urllib.request
import subprocess

# Ścieżka do pliku Aktualizacja.py w bieżącym folderze
path = os.path.join(os.getcwd(), "Aktualizacja.py")

# Usuń plik Aktualizacja.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
print("Rozpoczynanie aktualizacji II poziomu")
# Pobierz plik Aktualizacja.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Poprzednie/Stara/Aktualizacja.py"
urllib.request.urlretrieve(url, path)
print("Zakończono aktualizację II poziomu")
print('Rozpoczynanie aktualizacji I poziomu')

Aktualizacja = ["python", "Aktualizacja.py"]
subprocess.run(Aktualizacja)

input("Naciśnij klawisz Enter, aby zakończyć aktualizację...")
