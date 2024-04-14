import os
import requests
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
import ctypes
import sys

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


class Automa(QThread):
    aktualizacja_zakonczona = pyqtSignal(int)

    def __init__(self, urls):
        super().__init__()
        self.urls = urls

    def run(self):
        total_files = len(self.urls)
        for i, url in enumerate(self.urls):
            file_name = url.split('/')[-1]
            response = requests.get(url, stream=True)
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            progress_bar = 0
            with open(file_name, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    progress_bar += len(data)
                    percent = progress_bar * 100 / total_size_in_bytes
                    self.aktualizacja_zakonczona.emit(int(i + percent / total_files))


def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


# Użycie:
app = QCoreApplication(sys.argv)

# Ścieżka do pliku lista.txt w repozytorium
lista_txt_url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/lista.txt"
lista_txt_content = requests.get(lista_txt_url).text
urls = [line.strip() for line in lista_txt_content.split('\n') if line.strip()]

automa = Automa(urls)
automa.aktualizacja_zakonczona.connect(lambda value: app.quit())
automa.start()

sys.exit(app.exec_())
