import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import requests
import shutil
from PIL import Image
import urllib.request


def pobierz_apk():
    url = "https://github.com/Ksao0/Aplikacja_ma_telefon-Magnesy/raw/main/app-debug.apk"
    save_as = "app-debug.apk"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_as, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        messagebox.showinfo("Pobieranie zakończone",
                            "Plik APK został pobrany.")

    except requests.exceptions.RequestException as e:
        messagebox.showerror(
            "Błąd pobierania", f"Wystąpił błąd podczas pobierania pliku: {str(e)}")


def zmien_zawartosc_pola_tekstowego():
    zawartosc = "To okno będzie rozwijane, aktualna oprawa graficzna oraz inne funkcje ulegną zmianie\n" \
    + "Wymagana jest wersja oprogramowania systemu android powyżej 9\n\n" \
    + "Oto krótka instrukcja sposobu instalowania i aktualizowania aplikacji do liczenia magnesów w wersji na telefon:\n" \
    + '1. Naciśnij przycisk "Pobierz plik APK", poczekaj, aż plik zostanie pobrany.\n' \
    + "2. Otwórz folder z plikami programu na komputerze.\n" \
    + "3. Przenieś plik app-debug.apk na urządzenie z systemem Android" \
    + "4. Uruchom plik app-debug.apk i zainstaluj aplikację"
    
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

button_pobierz_apk = tk.Button(
    root, text="Pobierz plik APK", command=pobierz_apk)
button_pobierz_apk.pack(side=tk.RIGHT)

button_instrukcja = tk.Button(
    root, text="Instrukcja", command=zmien_zawartosc_pola_tekstowego)
button_instrukcja.pack(side=tk.RIGHT)

# Pobierz zawartość pliku version.txt z repozytorium na GitHub
url = 'https://raw.githubusercontent.com/Ksao0/Aplikacja_ma_telefon-Magnesy/main/version.txt'
try:
    response = requests.get(url)
    response.raise_for_status()
    zawartosc = "Opis najnowszej aktualizacji aplikacji na telefon\n"
    zawartosc += response.content.decode('utf-8').strip()
except requests.exceptions.RequestException as e:
    zawartosc = f"Wystąpił błąd podczas pobierania zawartości pliku: {str(e)}"

pole_tekstowe = scrolledtext.ScrolledText(root, wrap=tk.WORD)
pole_tekstowe.pack(expand=True, fill=tk.BOTH)
pole_tekstowe.insert(tk.END, zawartosc)
pole_tekstowe.config(state=tk.DISABLED)

root.mainloop()
