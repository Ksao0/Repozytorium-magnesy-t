import socket
import threading
from colorama import Fore, Style
import os
import sys
import requests
from colorama import init, Fore, Style
import time
init()

# Minimalizowanie cmd
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

ilosc_bledow = 0  # Inicjalizacja zmiennej ilosc_bledow

def Pia_reset(server_socket):
    try:
        # Lista adresów URL plików do pobrania
        urls = [
            "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Odbiorca.py",
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
                print(Fore.MAGENTA + "Polecenie serwera nie mogło zostać wykonane" + Style.RESET_ALL)
                server_socket.sendall("Polecenie serwera nie mogło zostać wykonane".encode())

    except Exception as e:
        print(Fore.RED + "Wystąpił błąd podczas wykonywania polecenia:", e)
        server_socket.sendall("Polecenie serwera nie mogło zostać wykonane [0]".encode())  # Wysłanie komunikatu do serwera w przypadku błędu



def receive_messages(server_socket):
    try:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break

            if data.decode() == "Pia --reset":
                Pia_reset(server_socket)
                break
            if data.decode() == "Pia --exit":
                sys.exit()  # Wyjdź z programu
            else:
                print(Fore.LIGHTBLUE_EX + 'Otrzymana wiadomość od serwera:', data.decode())
                print(Style.RESET_ALL)
    except Exception as e:
        print(Fore.YELLOW + "Wystąpił błąd podczas odbierania danych. Aby rozpocząć szukanie połączenia spróbuj wysłać dowolną wiadomość, np: Rozłączyło nas")
    finally:
        server_socket.close()


def start_client():
    global ilosc_bledow  # Użyj globalnego słowa kluczowego przed użyciem zmiennej globalnej
    while True:
        try:
            with open("adres.txt", "r") as file:
                server_ip = file.readline().strip()  # Pobranie adresu IP z pliku adres.txt
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Użycie pobranego adresu IP
            client_socket.connect((server_ip, 12345))
            print('Połączono z serwerem')
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.start()
            while True:
                message = input()
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
                print(Fore.YELLOWE +"Wystąpiło zbyt wiele błędów. Zamykanie problematycznego procesu...")
                time.sleep(2)
                sys.exit()  # Wyjdź z programu
        finally:
            client_socket.close()


if __name__ == "__main__":
    start_client()
