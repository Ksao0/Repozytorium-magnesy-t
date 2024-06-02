import os
import requests
import sys
from colorama import Fore, Style
import time
import threading
import random
import subprocess
import ctypes
from PyQt5.QtWidgets import QWidget
from win10toast import ToastNotifier
from packaging import version

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


class Powiadomienia(QWidget):
    # Przekierowanie błędów do "czarnej dziury"
    sys.stderr = open('nul', 'w')

    def __init__(self):
        self.toaster = self.MyToastNotifier()

    def powiadomienie_jednorazowe(self, tytul_powiadomienia, tresc_powiadomienia, duration):
        self.toaster.show_toast(
            msg=tresc_powiadomienia, duration=duration, tytul_powiadomienia=tytul_powiadomienia)

    class MyToastNotifier(ToastNotifier):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.wyswietlone_powiadomienie = False

        def show_toast(self, msg, icon_path=None, duration=5, threaded=True, tytul_powiadomienia=""):
            icon_path = "rei/icon.ico"
            nazwa_aplikacji = ""  # Nazwa aplikacji nie będzie już wyświetlana
            if nazwa_aplikacji != "":
                title = f"{nazwa_aplikacji} - {tytul_powiadomienia}"
            else:
                title = f"{tytul_powiadomienia}"
            try:
                if not self.wyswietlone_powiadomienie:
                    if not threaded:
                        return super().show_toast(title, msg, icon_path, duration, threaded)
                    else:
                        threading.Thread(target=self._show_toast, args=(
                            title, msg, icon_path, duration)).start()
                        self.wyswietlone_powiadomienie = True
                        return 1  # lub inna wartość int
            except Exception as e:
                # Przechwytywanie błędów, ale nie wyświetlanie ich
                pass
        #ctypes.windll.user32.ShowWindow(
        #    ctypes.windll.kernel32.GetConsoleWindow(), 1)


def version_sprawdzanie():
    try:
        # Szukanie folderu na pulpicie zawierającego plik main2.py
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        for root, dirs, files in os.walk(desktop_path):
            if "main2.py" in files and "rei" in dirs:
                folder_path = root
                break
        else:
            print("Nie znaleziono wymaganych plików/folderów na pulpicie.")
            return

        # Pobierz zawartość pliku version.txt z repozytorium na GitHub
        try:
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version.txt'
            response = requests.get(url)
            response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
            version_online = response.content.decode('utf-8').strip()
        except requests.exceptions.RequestException as e:
            toaster = Powiadomienia()
            toaster.powiadomienie_jednorazowe(
                tytul_powiadomienia="Internet?", tresc_powiadomienia=f"Chyba nie masz dostępu do internetu, do zobaczenia!", duration=3)
            return

        version_online_lines = version_online.split('\n')
        # Odczytaj zawartość pliku version.txt w twoim programie
        path = os.path.join(folder_path, "version.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                version_local = f.read().strip()
        else:
            version_local = "1.0.0"

        version_local_lines = version_local.split('\n')

        najnowsza_wersja_online = version_online_lines[0]
        local_aktualna_wersja = version_local_lines[0]

        if version.parse(local_aktualna_wersja) < version.parse(najnowsza_wersja_online) or version.parse(version_online_lines[0]) > version.parse(version_local_lines[1]):
            toaster = Powiadomienia()
            toaster.powiadomienie_jednorazowe(
                tytul_powiadomienia="Nowa wersja!", tresc_powiadomienia=f"Pobieranie aktualizacji:\n   {local_aktualna_wersja} --> {najnowsza_wersja_online}\nZaczynamy instalowanie!", duration=3)
            #ctypes.windll.user32.ShowWindow(
            #    ctypes.windll.kernel32.GetConsoleWindow(), 1)
            zainstaluj_biblioteki()
    except Exception as e:
        print(e)
        time.sleep(3)


def zainstaluj_biblioteki():
    try:
        toaster = Powiadomienia()
        toaster.powiadomienie_jednorazowe(
            tytul_powiadomienia="Biblioteki?", tresc_powiadomienia=f"Ze względu na to, że możesz nie mieć wszystkich bibliotek wymaganych do działania programu proces aktualizacji potrwa trochę dłużej", duration=3)
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 1)
    except:
        print(Fore.LIGHTGREEN_EX + 'Ze względu na to, że możesz nie mieć wszystkich bibliotek wymaganych do działania programu proces aktualizacji potrwa trochę dłużej\n')

    def get_installed_packages():
        try:
            installed_packages = subprocess.check_output(
                ['pip', 'freeze']).decode().split('\n')
            installed_packages = [pkg.split('==')[0]
                                  for pkg in installed_packages if pkg]
            return installed_packages
        except subprocess.CalledProcessError:
            print("Nie udało się uzyskać listy zainstalowanych pakietów.")
            return []

    try:
        libraries_to_install = requests.get(
            'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/bib.txt').text.strip().split()

        installed_packages = get_installed_packages()

        def install_library(lib):
            if lib not in installed_packages:
                print(Fore.LIGHTBLACK_EX +
                      f"Instalowanie biblioteki: {lib}, czekaj...")
                subprocess.run(["pip", "install", lib],
                               capture_output=True, text=True)
                print(Fore.BLUE + "Biblioteka", lib,
                      "została pomyślnie zainstalowana.")
            else:
                print(Fore.CYAN +
                      f"Biblioteka {lib} jest już zainstalowana.")

        # Tworzenie wątków dla instalacji bibliotek
        threads = []
        for lib in libraries_to_install:
            thread = threading.Thread(
                target=install_library, args=(lib,))
            thread.start()
            threads.append(thread)

        # Oczekiwanie na zakończenie wszystkich wątków
        for thread in threads:
            thread.join()

        print(Fore.LIGHTGREEN_EX + '\nAktualność plików:')

    except Exception as e:
        print(Fore.RED + "Wystąpił błąd:", e)


version_sprawdzanie()

# Wygeneruj losową liczbę od 0 do 100
losowa_liczba = random.randint(0, 100)

# Sprawdź, czy wygenerowana liczba jest mniejsza niż 5 (czyli 5% szans)
if losowa_liczba < 2:
    zainstaluj_biblioteki()

try:
    print(f'{Fore.LIGHTBLACK_EX}Aktualizowanie magnesów\n\nAby wyłączyć tę opcję usuń ją z autostaru')

    class Automa:
        def __init__(self, urls, folder_path):
            self.urls = urls
            self.folder_path = folder_path

        def run(self):
            if not os.path.exists(self.folder_path):
                print(
                    Fore.RED + "Folder zawierający wymagane pliki nie istnieje.")
                sys.exit(1)

            # Tworzenie wątków
            threads = []
            for url in self.urls:
                file_name = os.path.join(
                    self.folder_path, url.split('/')[-1])

                # Tworzenie i uruchamianie wątku dla każdego pliku
                thread = threading.Thread(
                    target=self.process_file, args=(url, file_name))
                thread.start()
                threads.append(thread)

            # Oczekiwanie na zakończenie wszystkich wątków
            for thread in threads:
                thread.join()

        def process_file(self, url, file_name):
            if not os.path.exists(file_name):
                print(
                    Fore.MAGENTA + f"Plik {file_name} nie istnieje na komputerze. Traktuję jako nieaktualny.")
                self.download_file(url, file_name)
            else:
                if not self.compare_files(url, file_name):
                    print(Fore.CYAN +
                          f"Plik {file_name} jest nieaktualny.")
                    self.download_file(url, file_name)
                else:
                    print(Fore.LIGHTBLACK_EX +
                          f"Plik {file_name} jest aktualny.")

        def compare_files(self, url, local_file_path):
            response = self.get_remote_file_content(url)
            if response is None:
                print(
                    Fore.RED + f"Nie udało się pobrać zawartości pliku {url}.")
                return False

            with open(local_file_path, 'rb') as local_file:  # Otwarcie w trybie binarnym
                local_content = local_file.read().decode(
                    'utf-8', errors='ignore')  # Dekodowanie

            return local_content == response.text

        def download_file(self, url, file_name):
            print(Fore.LIGHTCYAN_EX +
                  f"Rozpoczynam aktualizację pliku {file_name}...")
            response = self.get_remote_file_content(url)
            if response is None:
                print(
                    Fore.RED + f"Nie udało się pobrać pliku {url}. Aktualizacja przerwana.")
                return

            with open(file_name, 'wb') as local_file:  # Otwarcie w trybie binarnym
                # Zapis zawartości binarnej
                local_file.write(response.content)
                print(Fore.LIGHTBLUE_EX + f"Pobrano {file_name}")

        def get_remote_file_content(self, url):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response
                else:
                    print(
                        Fore.RED + f"Błąd podczas pobierania pliku {url}: {response.status_code}")
                    return None
            except Exception as e:
                print(
                    Fore.RED + f"Wystąpił błąd podczas pobierania pliku {url}: {e}")
                return None

    # Szukanie folderu na pulpicie zawierającego plik main2.py
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    for root, dirs, files in os.walk(desktop_path):
        if "main2.py" in files and "rei" in dirs:
            folder_path = root
            break
    else:
        print("Nie znaleziono wymaganych plików/folderów na pulpicie.")
        sys.exit(1)

    # Sprawdzenie połączenia internetowego
    try:
        requests.get("https://www.google.com", timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        print("Brak połączenia z internetem.")
        sys.exit(2)

    # Ścieżka do pliku lista.txt w repozytorium
    lista_txt_url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/lista.txt"
    lista_txt_content = requests.get(lista_txt_url).text
    urls = [line.strip()
            for line in lista_txt_content.split('\n') if line.strip()]

    automa = Automa(urls, folder_path)
    automa.run()

except Exception as e:
    print(f"Wystąpił błąd: {e}")
