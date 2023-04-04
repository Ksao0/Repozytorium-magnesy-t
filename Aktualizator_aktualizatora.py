import os
import urllib.request
import subprocess

# ścieżka do pliku Aktualizator.py w bieżącym folderze
path = os.path.join(os.getcwd(), "Aktualizator.py")

# usuń plik Aktualizator.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
print("Rozpoczynanie aktualizacji II poziomu")
# pobierz plik Aktualizator.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Aktualizacja.py"
urllib.request.urlretrieve(url, path)
print("Zakończono aktualizację II poziomu")
print('Rozpoczynanie aktualizacji I poziomu')

Aktualizacja = ["python", "Aktualizacja.py"]
subprocess.run(Aktualizacja)

print("Zakończono aktualizację I poziomu")
input("Naciśnij klawisz Enter, aby zakończyć program...")
