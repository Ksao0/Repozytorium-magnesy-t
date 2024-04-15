import os
import requests
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
import ctypes
import sys
from colorama import Fore, Style

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

try:
    print(f'{Fore.LIGHTBLACK_EX}Aktualizowanie magnesów\n\nAby wyłączyć tę opcję usuń ją z autostaru')

    class Automa(QThread):
        aktualizacja_zakonczona = pyqtSignal(int)

        def __init__(self, urls, folder_path, version_txt_path):
            super().__init__()
            self.urls = urls
            self.folder_path = folder_path
            self.version_txt_path = version_txt_path

        def run(self):
            local_version_content = self.read_local_version_txt()
            if local_version_content is None:
                print("Nie udało się odczytać pliku version.txt na komputerze.")
                QCoreApplication.quit()
                return

            remote_version_content = self.read_remote_version_txt()
            if remote_version_content is None:
                print("Nie udało się pobrać pliku version.txt z repozytorium.")
                QCoreApplication.quit()
                return

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
                    with open(file_name, 'wb') as file:
                        for data in response.iter_content(block_size):
                            file.write(data)
                            progress_bar += len(data)
                            percent = progress_bar * 100 / total_size_in_bytes
                            self.aktualizacja_zakonczona.emit(
                                int(i + percent / total_files))
            else:
                print(
                    "Plik version.txt na komputerze jest aktualny. Nie ma potrzeby aktualizacji.")
                QCoreApplication.quit()

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
        if "main2.py" in files and "version.txt" in files and "rei" in dirs:
            folder_path = root
            break
    else:
        print("Nie znaleziono wymaganych plików/folderów na pulpicie.")
        import messagebox
        messagebox.showerror(
            'Autostart - magnesy', "Niestety nie można znaleźć na pulpicie folderu z programem, jeśli go usunąłeś lub przeniosłeś gdzieś indziej - usuń Magnesy-update.bat z autostartu")
        sys.exit(1)

    version_txt_path = os.path.join(folder_path, "version.txt")

    # Sprawdzenie połączenia internetowego
    try:
        requests.get("https://www.google.com", timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        print("Brak połączenia z internetem.")
        sys.exit(1)

    # Użycie:
    app = QCoreApplication(sys.argv)

    # Ścieżka do pliku lista.txt w repozytorium
    lista_txt_url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/lista.txt"
    lista_txt_content = requests.get(lista_txt_url).text
    urls = [line.strip()
            for line in lista_txt_content.split('\n') if line.strip()]

    automa = Automa(urls, folder_path, version_txt_path)
    automa.aktualizacja_zakonczona.connect(lambda value: app.quit())
    automa.start()

    sys.exit(app.exec_())

except Exception as e:
    print(f"Wystąpił błąd: {e}")
