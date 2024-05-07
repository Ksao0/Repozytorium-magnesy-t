import os
import requests
import ctypes
import sys
from colorama import Fore, Style
import time
import threading

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
            print(Fore.MAGENTA +
                  f"Rozpoczynam aktualizację pliku {file_name}...")
            response = self.get_remote_file_content(url)
            if response is None:
                print(
                    Fore.RED + f"Nie udało się pobrać pliku {url}. Aktualizacja przerwana.")
                return

            with open(file_name, 'wb') as local_file:  # Otwarcie w trybie binarnym
                # Zapis zawartości binarnej
                local_file.write(response.content)
                print(Fore.LIGHTBLACK_EX + f"Pobrano {file_name}")

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
    time.sleep(3)

except Exception as e:
    print(f"Wystąpił błąd: {e}")
