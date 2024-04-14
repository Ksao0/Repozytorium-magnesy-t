import os
import shutil
import requests
from PyQt5.QtWidgets import QProgressBar
import ctypes

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


class Automa:
    def __init__(self):
        self.urls = [
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/version.txt",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Klienci.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/main2.py"
            # Dodaj tutaj inne URL-e do plików, jeśli są
        ]
        self.pasek_postępu_automa = QProgressBar()

    def find_main2_folder(self):
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        for root, dirs, files in os.walk(desktop_path):
            if 'main2.py' in files and 'rei2' in dirs:
                return os.path.join(root, 'rei2')
        return None

    def download_files(self):
        main2_folder = self.find_main2_folder()
        if main2_folder:
            total_files = len(self.urls)
            self.pasek_postępu_automa.setMaximum(total_files)
            self.pasek_postępu_automa.setValue(0)
            for i, url in enumerate(self.urls):
                file_name = url.split('/')[-1]
                file_path = os.path.join(main2_folder, file_name)
                response = requests.get(url, stream=True)
                total_size_in_bytes = int(
                    response.headers.get('content-length', 0))
                block_size = 1024  # 1 KB
                progress_bar = 0
                with open(file_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        file.write(data)
                        progress_bar += len(data)
                        percent = progress_bar * 100 / total_size_in_bytes
                        self.pasek_postępu_automa.setValue(
                            int(i + percent / total_files))

        else:
            print("Folder 'main2.py' i 'rei2' nie został znaleziony na pulpicie.")
    print('Kończenie')


# Użycie:
automa = Automa()
automa.download_files()
