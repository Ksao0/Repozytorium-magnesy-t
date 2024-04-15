import os
import requests
import ctypes
import sys
from colorama import Fore, Style

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

try:
    print(f'{Fore.LIGHTBLACK_EX}Aktualizowanie magnesów\n\nAby wyłączyć tę opcję usuń ją z autostaru')

    class Automa:
        def __init__(self, urls, folder_path, version_txt_path):
            self.urls = urls
            self.folder_path = folder_path
            self.version_txt_path = version_txt_path

        def run(self):
            local_version_content = self.read_local_version_txt()
            if local_version_content is None:
                print("Nie udało się odczytać pliku version.txt na komputerze.")
                sys.exit(1)

            remote_version_content = self.read_remote_version_txt()
            if remote_version_content is None:
                print("Nie udało się pobrać pliku version.txt z repozytorium.")
                sys.exit(1)

            if local_version_content != remote_version_content:
                total_files = len(self.urls)
                for i, url in enumerate(self.urls):
                    file_name = os.path.join(
                        self.folder_path, url.split('/')[-1])
                    response = requests.get(url, stream=True)
                    total_size_in_bytes = int(
                        response.headers.get('content-length', 0))
                    block_size = 1024  # 1 KB
                    progress_bar = 0
                    previous_percent = 0  # Przechowuje poprzedni procent postępu
                    with open(file_name, 'wb') as file:
                        for data in response.iter_content(block_size):
                            file.write(data)
                            progress_bar += len(data)
                            percent = min(progress_bar * 100 / total_size_in_bytes, 100)  # Ograniczenie do maksymalnie 100%
                            if int(percent) != previous_percent:  # Wyświetl tylko, gdy postęp się zmienia
                                print(f"Pobrano {file_name}: {percent:.2f}%")
                                previous_percent = int(percent)  # Aktualizuj poprzedni procent
            else:
                print(
                    "Plik version.txt na komputerze jest aktualny. Nie ma potrzeby aktualizacji.")
                sys.exit(0)

        def read_local_version_txt(self):
            try:
                with open(self.version_txt_path, 'r') as file:
                    return file.read()
            except FileNotFoundError:
                return None

        def read_remote_version_txt(self):
            try:
                response = requests.get(
                    "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version.txt")
                return response.text
            except Exception as e:
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

    version_txt_path = os.path.join(folder_path, "version.txt")

    # Sprawdzenie połączenia internetowego
    try:
        requests.get("https://www.google.com", timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        print("Brak połączenia z internetem.")
        sys.exit(1)

    # Ścieżka do pliku lista.txt w repozytorium
    lista_txt_url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/lista.txt"
    lista_txt_content = requests.get(lista_txt_url).text
    urls = [line.strip()
            for line in lista_txt_content.split('\n') if line.strip()]

    automa = Automa(urls, folder_path, version_txt_path)
    automa.run()

except Exception as e:
    print(f"Wystąpił błąd: {e}")
