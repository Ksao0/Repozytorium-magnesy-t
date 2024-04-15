import os
import requests
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar
import ctypes
import sys
import threading
from colorama import Fore, Style

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

try:
    class Automa(QThread):
        aktualizacja_zakonczona = pyqtSignal(int)

        def __init__(self, urls, folder_path):
            super().__init__()
            self.urls = urls
            self.folder_path = folder_path

        def run(self):
            total_size = sum(self.get_file_size(url) for url in self.urls)
            total_downloaded = 0
            for i, url in enumerate(self.urls):
                file_name = os.path.join(self.folder_path, url.split('/')[-1])
                response = requests.get(url, stream=True)
                total_size_in_bytes = self.get_file_size(url)
                block_size = 1024  # 1 KB
                with open(file_name, 'wb') as file:
                    for data in response.iter_content(block_size):
                        file.write(data)
                        total_downloaded += len(data)
                        percent = total_downloaded * 100 / total_size
                        self.aktualizacja_zakonczona.emit(int(percent))

        def get_file_size(self, url):
            response = requests.head(url)
            return int(response.headers.get('content-length', 0))

    def read_urls_from_file(file_path):
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        return urls

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.progress_bar = QProgressBar(self)
            self.progress_bar.setGeometry(30, 40, 200, 25)
            self.progress_bar.setMaximum(100)
            self.progress_bar.setMinimum(0)
            self.setWindowTitle("Aktualizacja plików")
            self.setFixedSize(400, 100)
            # Ustawienie stylu dla paska postępu
            self.progress_bar.setStyleSheet(
                "QProgressBar { border: 2px solid #231225; border-radius: 5px; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 #250623, stop: 0.5 #351c34, stop: 1 #1b0c1a); }"
                "QProgressBar::chunk { background-color: #3e1642; width: 10px; }"
            )
            # Ustawienie stylu dla głównego okna
            self.setStyleSheet(
                "QWidget { background-color: #1B0C1A; color: #F2F2F2; selection-color: #40535b; selection-background-color: #441d32; }"
                "QStatusBar { background-color: #333333; color: #FFFFFF; }"
            )
            self.show()

    # Szukanie folderu na pulpicie zawierającego wymagane pliki
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    for root, dirs, files in os.walk(desktop_path):
        if "main2.py" in files and "version.txt" in files and "rei" in dirs:
            folder_path = root
            break
    else:
        print("Nie znaleziono wymaganych plików/folderów na pulpicie.")
        sys.exit(1)

    # Kontynuowanie działania programu, jeśli znaleziono odpowiedni folder
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # Ścieżka do pliku lista.txt w repozytorium
    lista_txt_url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/lista.txt"
    lista_txt_content = requests.get(lista_txt_url).text
    urls = [line.strip()
            for line in lista_txt_content.split('\n') if line.strip()]

    automa = Automa(urls, folder_path)
    automa.aktualizacja_zakonczona.connect(main_window.progress_bar.setValue)
    automa.aktualizacja_zakonczona.connect(lambda value: app.quit())  # Zamyka aplikację po pobraniu
    automa.start()

    sys.exit(app.exec_())

except Exception as e:
    print(f"Wystąpił błąd: {e}")
