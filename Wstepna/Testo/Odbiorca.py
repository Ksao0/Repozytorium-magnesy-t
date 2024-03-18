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
        server_socket.close()  # Zamykanie gniazda przed restartem
        os.execl(sys.executable, sys.executable, "Odbiorca.py")

    except Exception as e:
        print(Fore.RED + "Wystąpił błąd podczas wykonywania polecenia:", e)
        print(Style.RESET_ALL)
        # Wysłanie komunikatu do serwera w przypadku błędu
        server_socket.sendall(
            "Polecenie serwera nie mogło zostać wykonane [0]".encode())


# Funkcja do obsługi powiadomień
def show_notification(title, message, notification_type):
    # Wybierz rodzaj powiadomienia na podstawie przekazanego parametru
    if notification_type == "info":
        tkinter.messagebox.showinfo(title, message)
    elif notification_type == "warning":
        tkinter.messagebox.showwarning(title, message)
    elif notification_type == "error":
        tkinter.messagebox.showerror(title, message)
    # elif notification_type == "question":
    #    response = tkinter.messagebox.askquestion(title, message)
        # Tutaj możesz obsłużyć odpowiedź użytkownika na pytanie, jeśli jest to konieczne
    else:
        tkinter.messagebox.showinfo(title, message)


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
            elif odszyfrowywanie(data.decode()).startswith("Pia --mes"):
                sys.stderr = open('nul', 'w')
                # Parsowanie tytułu, treści powiadomienia i rodzaju powiadomienia
                command = odszyfrowywanie(data.decode()).strip()
                command_parts = command.split('|')
                if len(command_parts) == 3:
                    notification_type = command_parts[0]
                    title = command_parts[1]
                    message = command_parts[2]
                    # Wyświetlanie powiadomienia
                    show_notification(title, message, notification_type)
                else:
                    print("Błędny format polecenia powiadomienia")


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
