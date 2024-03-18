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
import tkinter.messagebox
import messagebox
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QDoubleSpinBox, QLabel, QSpinBox, QTextEdit, QProgressBar
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


def download_icon():
    try:
        # Zmień na właściwy adres URL pliku .ico
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/icon.ico"
        save_folder = "rei"  # Nazwa folderu, gdzie chcesz zapisać plik .ico

        # Utworzenie folderu "rei", jeśli nie istnieje
        folder_path = "rei"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        response = requests.get(url)
        if response.status_code == 200:
            icon_data = response.content
            filename = os.path.basename(url)
            save_path = os.path.join(save_folder, filename)

            with open(save_path, 'wb') as icon_file:
                icon_file.write(icon_data)
        else:
            return

    except Exception as e:
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
        download_icon()
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
