# pobierz zawartość pliku version.txt z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/version.txt'
response = requests.get(url)
version_online = response.text.strip()

# odczytaj zawartość pliku version.txt w twoim programie
path = os.path.join(os.getcwd(), "version.txt")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        version_local = f.readline().strip()
else:
    version_local = "BRAK DANYCH"

# porównaj wersje
print(f'Aktualna wersja: {version_local}')
if version_local != "BRAK DANYCH":
    if version_online.strip() == version_local.strip():
        print('Masz najnowszą wersję programu.')
        wersja = version_local
    else:
        print('Dostępna jest nowa wersja programu.')
        wersja = "DOSTĘPNA AKTUALIZACJA"
else:
    print('Wykryto brak niektórych plików. Zaktualizuj program, aby program działał prawidłowo')
    wersja = "ZAKTUALIZUJ PROGRAM"
