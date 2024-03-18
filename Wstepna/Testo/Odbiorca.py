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


def Pia_inna(server_socket):
    try:  # Tego pliku nie ma w repozytorium
        subprocess.run(['python', 'Inne_plecenia_s.py'])
    except:
        pass
    return


def tworzenie_ikonki():
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
    return


def Pia_reset(server_socket):
    global pia_reset
    try:
        # Lista adresów URL plików do pobrania
        urls = [
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
        time.sleep(3)

        tworzenie_ikonki()  # Twoorzenie skrótu na pulpicie

        server_socket.close()  # Zamykanie gniazda przed restartem
        os.execl(sys.executable, sys.executable, "Odbiorca.py")
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


def receive_messages(server_socket):
    try:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break

            # Sprawdź czy otrzymana wiadomość jest poleceniem do wyświetlenia powiadomienia
            if odszyfrowywanie(data.decode()).startswith("Pia --pow"):
                sys.stderr = open('nul', 'w')
                # Parsowanie tytułu i treści powiadomienia
                command = odszyfrowywanie(data.decode()).strip()
                command_parts = command.split('("')
                if len(command_parts) == 2:
                    title, message = command_parts[1].split('", "')
                    # Usuń ewentualny znak ")" na końcu wiadomości
                    message = message.rstrip('")')
                    # Wyświetlanie powiadomienia
                    toaster.show_toast(f"Polecnia serwera: {title}", message)
                else:
                    print("Błędny format polecenia powiadomienia")
                break

            decrypted_data = odszyfrowywanie(data.decode())
            if decrypted_data.startswith("Pia --mes"):
                command = decrypted_data.strip()
                command_parts = command.split('("')
                if len(command_parts) == 2:
                    message_part = command_parts[1].rstrip('")')
                    parts = message_part.split('", "')
                    if len(parts) == 3:
                        notification_type, title, message = parts
                        show_notification(
                            title, message, notification_type, server_socket)
                    else:
                        print("Błędny format polecenia powiadomienia")
                else:
                    print("Błędny format polecenia powiadomienia")
                break

            elif odszyfrowywanie(data.decode()) == "Pia --reset":
                Pia_reset(server_socket)
                break
            elif odszyfrowywanie(data.decode()) == "Pia --inna":
                Pia_inna(server_socket)
                break
            elif odszyfrowywanie(data.decode()) == "Pia --exit":
                sys.exit()  # Wyjdź z programu
                break
            elif odszyfrowywanie(data.decode()) == "Pia --clear":
                os.system('cls')
                break
            else:
                print(Fore.LIGHTBLUE_EX +
                      'Otrzymana wiadomość od serwera:', odszyfrowywanie(data.decode()))
                print(Style.RESET_ALL)
    except Exception as e:
        print("Wystąpił błąd podczas odbierania danych. Aby rozpocząć szukanie połączenia spróbuj wysłać wiadomość, np: Rozłączyło nas")
    finally:
        server_socket.close()


def start_client():
    global pia_reset
    global ilosc_bledow  # Użyj globalnego słowa kluczowego przed użyciem zmiennej globalnej
    while True:
        if pia_reset == 0:
            try:
                with open("adres.txt", "r") as file:
                    server_ip = file.readline().strip()  # Pobranie adresu IP z pliku adres.txt
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                # Użycie pobranego adresu IP
                client_socket.connect((server_ip, 12345))
                print('Połączono z serwerem')
                receive_thread = threading.Thread(
                    target=receive_messages, args=(client_socket,))
                receive_thread.start()
                while True:
                    message = input()
                    if message.lower() == 'exit':
                        break
                    client_socket.sendall(szyfrowanie(message).encode())
                print("Połączenie zostało zerwane. Ponowne łączenie z serwerem...")
            except Exception as e:
                if ilosc_bledow < 7:  # Sprawdź warunek ilości błędów
                    if ilosc_bledow == 0:
                        print("Wystąpił błąd podczas uruchamiania klienta:", e)
                    ilosc_bledow += 1  # Zwiększ licznik błędów
                else:
                    print(
                        "Wystąpił zbyt wiele błędów. Zamykanie problematycznego procesu...")
                    time.sleep(2)
                    sys.exit()  # Wyjdź z programu
            finally:
                client_socket.close()
        if pia_reset == 1:
            try:
                with open("adres.txt", "r") as file:
                    server_ip = file.readline().strip()  # Pobranie adresu IP z pliku adres.txt
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                # Użycie pobranego adresu IP
                client_socket.connect((server_ip, 12345))
                print('Połączono z serwerem')
                receive_thread = threading.Thread(
                    target=receive_messages, args=(client_socket,))
                receive_thread.start()
                while True:
                    message = "Odzyskiwanie połączenia"
                    if message.lower() == 'exit':
                        break
                    client_socket.sendall(message.encode())
                print("Połączenie zostało zerwane. Ponowne łączenie z serwerem...")
            except Exception as e:
                if ilosc_bledow < 7:  # Sprawdź warunek ilości błędów
                    if ilosc_bledow == 0:
                        print("Wystąpił błąd podczas uruchamiania klienta:", e)
                    ilosc_bledow += 1  # Zwiększ licznik błędów
                else:
                    print(
                        "Wystąpiło zbyt wiele błędów. Zamykanie problematycznego procesu...")
                    time.sleep(2)
                    sys.exit()  # Wyjdź z programu
            finally:
                client_socket.close()


if __name__ == "__main__":
    start_client()
