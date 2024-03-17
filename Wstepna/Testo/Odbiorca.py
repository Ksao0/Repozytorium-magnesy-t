import socket
import threading
from colorama import Fore, Style
import os
import sys
import requests

from colorama import init, Fore, Style

init()


def Pia_reset(server_socket):
    try:
        # Zmień na właściwy adres URL pliku .ico
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorcaa.py"

        response = requests.get(url)
        if response.status_code == 200:
            icon_data = response.content
            filename = os.path.basename(url)

            with open(filename, 'wb') as icon_file:
                icon_file.write(icon_data)
        else:
            print(
                Fore.MAGENTA + "Polecenie serwera nie mogło zostać wykonane" + Style.RESET_ALL)
            server_socket.sendall(
                "Polecenie serwera nie mogło zostać wykonane".encode())

    except:
        pass


def receive_messages(server_socket):
    try:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break

            if data.decode() == "Pia --reset":
                Pia_reset(server_socket)
            else:
                print(Fore.LIGHTBLUE_EX +
                      'Otrzymana wiadomość od serwera:', data.decode())
                print(Style.RESET_ALL)
    except Exception as e:
        print("Wystąpił błąd podczas odbierania danych. Aby rozpocząć szukanie połączenia spróbuj wysłać wiadomość, np: Rozłączyło nas")
    finally:
        server_socket.close()


def start_client():
    while True:
        try:
            with open("adres.txt", "r") as file:
                server_ip = file.readline().strip()  # Pobranie adresu IP z pliku adres.txt
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                client_socket.sendall(message.encode())
            print("Połączenie zostało zerwane. Ponowne łączenie z serwerem...")
        except Exception as e:
            print("Wystąpił błąd podczas uruchamiania klienta:", e)
        finally:
            client_socket.close()


if __name__ == "__main__":
    start_client()
