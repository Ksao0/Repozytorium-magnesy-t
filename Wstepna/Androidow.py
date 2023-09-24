# 1.0
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import requests
from PIL import Image
import urllib.request
from tqdm import tqdm
import subprocess
import sys
import datetime
from github import Github
import traceback
from colorama import init, Fore, Style

# Zmienna globalna do przechowywania informacji o pobraniu pliku APK
pobrany_apk = False

try:
    # Ścieżka do pliku w bieżącym folderze
    path = os.path.join(
        os.getcwd(), "app-debug.apk")

    # Usuń plik jeśli istnieje
    if os.path.exists(path):
        os.remove(path)

    def pobierz_apk():
        global pobrany_apk, save_as  # Deklarujemy zmienne globalne
        url = "https://github.com/Ksao0/Aplikacja_ma_telefon-Magnesy/raw/main/app-debug.apk"
        save_as = "app-debug.apk"

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192  # Rozmiar bloku pobierania

            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

            with open(save_as, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

            progress_bar.close()

            # Ustawiamy zmienną na True po pomyślnym pobraniu pliku APK
            pobrany_apk = True

            messagebox.showinfo("Pobieranie zakończone",
                                "Plik APK został pobrany.")

        except requests.exceptions.RequestException as e:
            messagebox.showerror(
                "Błąd pobierania", f"Wystąpił błąd podczas pobierania pliku: {str(e)}")

    def otworz_folder():
        # Sprawdzamy, czy plik APK został pobrany przed próbą otwarcia  folderu
        if pobrany_apk:
            folder = os.path.dirname(os.path.abspath(save_as))
            file_path = os.path.join(folder, "app-debug.apk")
            subprocess.Popen(f'explorer /select,"{file_path}"')
        else:
            messagebox.showwarning(
                "Brak pobranego pliku", "Plik APK nie został jeszcze pobrany w najnowszej wersji. Najpierw pobierz plik, a  następnie otwórz folder.")

    def zmien_zawartosc_pola_tekstowego():
        global instrukcja_button
        if instrukcja_button["text"] == "Instrukcja":
            instrukcja_button["text"] = "Powrót"
            zawartosc = "Wymagania: Wersja systemu Android 9 lub nowsza\n\n" \
                        '1. Naciśnij przycisk "Pobierz plik APK" i poczekaj, aż plik zostanie pobrany.\n' \
                        "2. Otwórz folder z pobranym plikiem APK (naciśnij przycisk).\n" \
                        "3. Podłącz telefon do komputera (pamiętaj o tym, aby włączyć transfer plików, w przeciwnym razie będziesz po prostu ładować telefon)\n" \
                        "4. Przenieś plik app-debug.apk na urządzenie z systemem Android, np. na kartę SD do katalogu Download\n" \
                        "   Możesz przenieść ten plik do dowolnego miejsca w pamięci, ważne, aby można go było potem znaleźć i otworzyć\n" \
                        "5. Uruchom plik app-debug.apk na telefonie i zainstaluj lub zaktualizuj aplikację\n" \
                        "Po wykonaniu tych czynności aplikacja na telefon zostanie zaktualizowana do najnowszej wersji!\n\n"
        else:
            instrukcja_button["text"] = "Instrukcja"
            zawartosc = "Opis najnowszej aktualizacji aplikacji na telefon\n"
            url = 'https://raw.githubusercontent.com/Ksao0/Aplikacja_ma_telefon-Magnesy/main/version2.txt'
            try:
                response = requests.get(url)
                response.raise_for_status()
                zawartosc += response.content.decode('utf-8').strip()
            except requests.exceptions.RequestException as e:
                zawartosc = f"Wystąpił błąd podczas pobierania zawartości pliku: {str(e)}"

        pole_tekstowe.config(state=tk.NORMAL)
        pole_tekstowe.delete("1.0", tk.END)
        pole_tekstowe.insert(tk.END, zawartosc)
        pole_tekstowe.config(state=tk.DISABLED)

    root = tk.Tk()
    root.title("Zarządzanie aplikacją na telefon (Eksperymentalne)")
    root.geometry("850x550+400+170")

    # Utworzenie folderu "rei", jeśli nie istnieje
    folder_path = "rei"
    os.makedirs(folder_path, exist_ok=True)

    # Pobranie ikony z repozytorium GitHub
    url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/ikona_magnesy.ico'
    file_path_ikonka = os.path.join(folder_path, 'ikona_magnesy.ico')
    urllib.request.urlretrieve(url, file_path_ikonka)

    # Przeskalowanie ikony na rozmiar 32x32
    img = Image.open(file_path_ikonka)
    img = img.resize((32, 32), Image.LANCZOS)
    resized_file_path = os.path.join(folder_path, 'resized_ikona_magnesy.ico')
    img.save(resized_file_path)

    # Ustawienie ikonki
    root.iconbitmap(resized_file_path)

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(side=tk.TOP, padx=10, pady=10)

    instrukcja_button = tk.Button(
        frame_buttons, text="Instrukcja", command=zmien_zawartosc_pola_tekstowego)
    instrukcja_button.pack(side=tk.LEFT, padx=5)

    button_pobierz_apk = tk.Button(
        frame_buttons, text="Pobierz plik APK", command=pobierz_apk)
    button_pobierz_apk.pack(side=tk.LEFT, padx=5)

    # Dodajemy przycisk do otwierania eksploratora plików
    button_otworz_folder = tk.Button(
        frame_buttons, text="Otwórz folder z APK", command=otworz_folder)
    button_otworz_folder.pack(side=tk.LEFT, padx=5)

    # Pobierz zawartość pliku version.txt z repozytorium na GitHub
    url = 'https://raw.githubusercontent.com/Ksao0/Aplikacja_ma_telefon-Magnesy/main/version2.txt'
    try:
        response = requests.get(url)
        response.raise_for_status()
        zawartosc = "Opis najnowszej aktualizacji aplikacji na telefon\n"
        zawartosc += response.content.decode('utf-8').strip()
    except requests.exceptions.RequestException as e:
        zawartosc = f"Wystąpił błąd podczas pobierania zawartości pliku: {str(e)}"

    pole_tekstowe = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    pole_tekstowe.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    pole_tekstowe.insert(tk.END, zawartosc)
    pole_tekstowe.config(state=tk.DISABLED)

    root.mainloop()
except Exception as e:
    # obsługa błędu i wyświetlenie dokładniejszych informacji o błędzie
    exc_type, exc_value, exc_traceback = sys.exc_info()
    # Odczytaj zawartość pliku Develop.txt w twoim programie
    path = os.path.join(os.getcwd(), "Develop.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            plik_od_dewelopera = f.read().strip()
    else:
        plik_od_dewelopera = "BRAK PLIKU D"
        messagebox.showerror(
            "Błąd", 'Poproś twórcę programu o informacje')

    if plik_od_dewelopera != "BRAK PLIKU D":
        informacje_do_zgloszenia = plik_od_dewelopera.split('\n')
        nazwa_uzytkownika = informacje_do_zgloszenia[0]
        token_do_wpisania = informacje_do_zgloszenia[1]

        # pobierz datę wygaśnięcia
        wygasa_dnia = int(informacje_do_zgloszenia[2])
        wygasa_miesiaca = int(informacje_do_zgloszenia[3])
        wygasa_roku = int(informacje_do_zgloszenia[4])

        # utwórz obiekt daty z daty wygaśnięcia
        wygasa_data = datetime.date(
            wygasa_roku, wygasa_miesiaca, wygasa_dnia)

        # pobierz dzisiejszą datę
        dzisiaj = datetime.date.today()
        # porównaj daty
        if dzisiaj > wygasa_data:
            messagebox.showerror(
                "Czas minął", "Zgłoś się do osoby odpowiadającej za program")
            exit()
        elif dzisiaj == wygasa_data:
            messagebox.showwarning(
                "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
    else:
        messagebox.showwarning(
            'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
        exit()

    # ustawienia konta
    username = f'{nazwa_uzytkownika}'
    password = f'{token_do_wpisania}'
    repository_name = 'Ksao0/Repozytorium-magnesy-t'
    issue_title = 'Automatyczne zgłoszenie błędu z Androidow.py'
    a = traceback.format_exc()
    issue_body = f"Błąd Androidow.py:\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

    # autentykacja
    g = Github(username, password)

    # pobierz repozytorium
    repo = g.get_repo(repository_name)

    # utwórz nowe zgłoszenie błędu
    repo.create_issue(title=issue_title, body=issue_body)

    messagebox.showinfo("Problem został zgłoszony",
                        "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
    exit()
