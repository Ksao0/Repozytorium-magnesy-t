import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests

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

# porównaj wersje
if version_local == version_online:
    aktul_wersja = 0
else:
    aktul_wersja = 1
    print(f'Plik version.txt jest nieaktualny lub uszkodzony.')


# pobierz zawartość pliku Aktualizacja.py z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Aktualizacja.py'
response = requests.get(url)

Aktualizacja_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku Aktualizacja.py w twoim programie
path = os.path.join(os.getcwd(), "Aktualizacja.py")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        Aktualizacja_local = f.read().strip()
else:
    Aktualizacja_local = "BRAK DANYCH"

# porównaj wersje
if Aktualizacja_local == Aktualizacja_online:
    aktul_Aktualizacja = 0
else:
    aktul_Aktualizacja = 1
    print(f'Plik Aktualizacja.py jest nieaktualny lub uszkodzony (aktualizacja możliwa).')

# pobierz zawartość pliku Aktualizator_aktualizatora.py z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Aktualizator_aktualizatora.py'
response = requests.get(url)

Aktualizator_aktualizatora_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku Aktualizator_aktualizatora.py w twoim programie
path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        Aktualizator_aktualizatora_local = f.read().strip()
else:
    Aktualizator_aktualizatora_local = "BRAK DANYCH"

# porównaj wersje
if Aktualizator_aktualizatora_local == Aktualizator_aktualizatora_online:
    aktul_Aktualizator_aktualizatora = 0
else:
    aktul_Aktualizator_aktualizatora = 1
    print(f'Plik Aktualizator_aktualizatora.py jest nieaktualny lub uszkodzony (aktualizacja niemożliwa).')

# pobierz zawartość pliku Obecnosc.py z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Obecnosc.py'
response = requests.get(url)

Obecnosc_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku Obecnosc.py w twoim programie
path = os.path.join(os.getcwd(), "Obecnosc.py")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        Obecnosc_local = f.read().strip()
else:
    Obecnosc_local = "BRAK DANYCH"

# porównaj wersje
if Obecnosc_local == Obecnosc_online:
    aktul_Obecnosc = 0
else:
    aktul_Obecnosc = 1
    print(f'Plik Obecnosc.py jest nieaktualny lub uszkodzony\n   Wykonuj czynności związane z naprawą dwa razy. Jeżeli błąd nadal będzie występował:\n      Wybierz opcję 2 przy pytaniu o automatyczną naprawę i zastosuj się do poleceń')

# pobierz zawartość pliku main.py z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/main.py'
response = requests.get(url)

main_online = response.content.decode('utf-8').strip()

# odczytaj zawartość pliku main.py w twoim programie
path = os.path.join(os.getcwd(), "main.py")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        main_local = f.read().strip()
else:
    main_local = "BRAK DANYCH"

# porównaj wersje
if main_local == main_online:
    aktul_main = 0
else:
    aktul_main = 1
    print(f'Plik main.py jest nieaktualny lub uszkodzony.')


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

    print('Naprawa...')
    Aktualizacja = ["python", "Aktualizator_aktualizatora.py"]
    subprocess.run(Aktualizacja)
    print('Zakończono!')
    print('Uruchom program ponownie, aby wprowadzić zmiany')


def naprawa():
    naprawa = int(input("Wybór: "))
    if naprawa == 1:
        if aktul_Obecnosc == 1:
            print(f'Plik Obecnosc.py jest nieaktualny lub uszkodzony\n   Wykonuj czynności związane z naprawą dwa razy. Jeżeli błąd nadal będzie występował:\n      Wybierz opcję 2 przy pytaniu o automatyczną naprawę i zastosuj się do poleceń')
        aktul()
    elif naprawa == 2:
        if aktul_Aktualizator_aktualizatora == 1 and aktul_Aktualizacja == 1 and aktul_Obecnosc == 1:
            print('Wykryto błąd krytyczny! Musisz wykonać te czynności:')
            print('Usuń plik Aktualizator_aktualizatora.py, utwórz plik o tej samej nazwie (Aktualizator_aktualizatora.py)\nNastępnie wklej do niego zawartość tego linku i uruchom ten plik:\nhttps://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Alfa/Aktualizator_aktualizatora.py')
        else:
            print(
                'Program może działać nieprawidłowo. Możesz wykonać te czynności (dostosowano do możliwości):')
            if aktul_Aktualizator_aktualizatora == 0 and aktul_main == 0:
                print(
                    '   Zaktualizować go do najnowszej wersji, jeżeli jeszcze tego nie zrobiono')
            print('   Ponownie sprawdzić zgodność plików i wybrać opcję naprawy')
    else:
        print('Nie ma takiej opcji')
        naprawa()

if  not aktul_Obecnosc = 0 or aktul_Aktualizacja = 0 or aktul_Aktualizator_aktualizatora = 0 or aktul_main = 0:
    print('Naprawić błąd? (żadne twoje dane nie zostaną usunęte)\n1: Tak\n2: Nie')
    naprawa()
else:
    print('Nie wykryto błędów')
    
    # ścieżka do pliku version.txt w bieżącym folderze
    path = os.path.join(os.getcwd(), "version.txt")
    
    # usuń plik version.txt, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)
    # print("Usunięto plik version.txt")
    
    # pobierz plik version.txt z repozytorium i utwórz go
    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/version.txt"
    urllib.request.urlretrieve(url, path)
