import socket
import threading
from colorama import Fore, Style

def receive_messages(server_socket):
    try:
        while True:
            data = server_socket.recv(1024)
            if not data:
                break
            print(Fore.YELLOW + 'Otrzymana wiadomość od serwera:', data.decode())
            print(Style.RESET_ALL)
    except Exception as e:
        print("Wystąpił błąd podczas odbierania danych:", e)
    finally:
        server_socket.close()

def start_client():
    try:
        with open("adres.txt", "r") as file:
            server_ip = file.readline().strip()  # Pobranie adresu IP z pliku adres.txt
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, 12345))  # Użycie pobranego adresu IP
        print('Połączono z serwerem')
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()
        while True:
            message = input()
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode())
    except Exception as e:
        print("Wystąpił błąd podczas uruchamiania klienta:", e)
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
