import os
import urllib.request

# ścieżka do pliku main.py w bieżącym folderze
path = os.path.join(os.getcwd(), "main.py")

# usuń plik main.py, jeśli istnieje
if os.path.exists(path):
    os.remove(path)
print("Usunięto plik main.py")

# pobierz plik main.py z repozytorium
url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/main.py"
urllib.request.urlretrieve(url, path)
print("Zastąpiono plik")
input("Naciśnij klawisz Enter, aby zakończyć program...")
