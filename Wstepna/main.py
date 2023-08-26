import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
import datetime
import urllib.request
import subprocess
import requests
from time import sleep
from github import Github
import sys
import traceback
import matplotlib.pyplot as plt
import random
import shutil
from PIL import Image
from colorama import init, Fore, Style

global okno_informacje_otwarte
global okno_edycja_kosztow_otwarte
global okno_problemu_otwarte
global okno_wyborowe_otwarte
global internet
global blokada_bledu
global blokada_klamstwa
global token_zaufania
global file_path_ikonka

token_zaufania = False
blokada_bledu = False
blokada_klamstwa = False
okno_informacje_otwarte = 0
okno_edycja_kosztow_otwarte = 0
okno_problemu_otwarte = 0
okno_wyborowe_otwarte = 0
internet = 1

dodatkowe_od_tworcy = "Chcę dodac możliwość stworzenia wykresu przedstawiającego dane o klientach, ale nie mam pomysłu jakie dane ma ten wykres\n" \
                      "przedstawiać i czy wykres ma uwzględniać wszystkie dane, czy jedynie ich część.\n" \
                      "Jeśli będzie wyświetlać zbyt wiele danych to stanie się nieczytelny przy więksej liczbie klientów\n" \
                      "Co sądzisz na ten temat?"

# Wywołanie funkcji startowej.
# Inicjalizacja modułu colorama (do kolorowego tekstu)
# Fore.RED
# Style.BRIGHT
# Style.RESET_ALL
init()


def download_icon():
    try:
        # Zmień na właściwy adres URL pliku .ico
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/ikona_magnesy2.ico"
        save_folder = "rei2"  # Nazwa folderu, gdzie chcesz zapisać plik .ico

        # Utworzenie folderu "rei", jeśli nie istnieje
        folder_path = "rei2"

        # Usunięcie folderu "rei" wraz z jego zawartością, jeśli istnieje
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

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


download_icon()


def zgloszenie_pobrania_nowej_wersji(version_online_first_line, version_local_lines, dodatkowe):
    try:
        # Odczytaj zawartość pliku Develop.txt w twoim programie
        path = os.path.join(os.getcwd(), "Develop.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                plik_od_dewelopera = f.read().strip()
        else:
            plik_od_dewelopera = "BRAK PLIKU D"
            messagebox.showerror(
                "Błąd", 'Zapytaj twórcę programu o informacje')

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
                return
        else:
            return

        if nazwa_uzytkownika != "Admin":
            # ustawienia konta
            username = f'{nazwa_uzytkownika}'
            password = f'{token_do_wpisania}'
            repository_name = 'Ksao0/Repozytorium-magnesy-t'
            issue_title = f'Użytkownik {nazwa_uzytkownika} zaktualizował program do wersji {version_online_first_line}'
            aktualna_data_czas = datetime.datetime.now()
            format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
            issue_body = f"Data: {format_data_czas} Zaktualizowano program do wersji {version_online_first_line}:\nPoprzednia wersja: {version_local_lines}\n\nWystąpił u: {nazwa_uzytkownika}  \n\n"
            if dodatkowe:
                issue_body += f"Sposób: {dodatkowe}"

            # autentykacja
            g = Github(username, password)

            # pobierz repozytorium
            repo = g.get_repo(repository_name)

            # utwórz nowe zgłoszenie błędu
            repo.create_issue(title=issue_title, body=issue_body)
            return
        else:
            return
    except:
        return


def token_zaufania_wygasl_f():
    messagebox.showerror(
        'Czas minął', 'Token zaufania wygasł. Ta funkcja jest niedostepna')


def restart_program():
    os.system('cls')
    print(Fore.YELLOW + "Ponowne uruchamianie...")

    try:
        path = os.path.join(os.getcwd(), "WEW.py")
        # pobierz plik WEW.py z repozytorium
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/WEW.py"
        urllib.request.urlretrieve(url, path)
        # print("Zastąpiono plik WEW.py")
    except:
        messagebox.showerror(
            "Błąd", "Wystąpił błąd, uruchom program ponownie ręcznie")
        exit(0)

    sleep(1)

    Aktualizacja = ["python", "WEW.py"]
    subprocess.run(Aktualizacja)

    sleep(1)
    os.system('cls')
    # Ponowne uruchomienie programu.
    python = sys.executable
    os.execl(python, python, *sys.argv)


print(Fore.RED + 'Nie zamykaj tego okna!')
print('Nigdy nie kasuj pliku WEW.py')
print(Fore.YELLOW + 'Wykonywanie czynności początkowych...', Style.RESET_ALL)


def ukrywanie_bledu():
    messagebox.showerror(
        'Odmowa dostępu', "Niestety ta opcja jest tymczasowo zablokowana, spróbuj ponownie za kilka godzin lub dni\nTo nie jest błąd")


def blad_poczatkowe():
    message = "Podczas uruchamiania programu nie było dostępu do internetu. Czynności początkowe nie zostały wykonane, więc ta opcja jest niedostępna. Czy chcesz wykonać czynnoci początkowe"
    response = messagebox.askokcancel("Błąd", message)
    if response == True:
        czynnosci_poczatkowe()
    else:
        return


def zglos_problem():
    global token_zaufania
    if token_zaufania == True:
        try:
            global file_path_ikonka
            if not internet == 0:
                messagebox.showinfo(
                    'Błąd sugestia i pytanie', "Opisz problem lub sugestię zwięźle i zrozumiale, abyśmy mogli jeszcze skuteczniej pracować nad ulepszaniem programu. Dziękujemy za Twój wkład!")
                global okno_edycja_kosztow_otwarte
                global okno_problemu_otwarte

                def otworz_okno():
                    global okno_problemu_otwarte
                    okno_problemu_otwarte = 1

                def zamknij_okno():
                    global okno_problemu_otwarte
                    okno_problemu_otwarte = 0
                    okno_problemu.destroy()

                if okno_problemu_otwarte == 0:
                    okno_problemu_otwarte = 1

                    def zglos_problem_wyslij():
                        # Odczytaj zawartość pliku Develop.txt w twoim programie
                        path = os.path.join(os.getcwd(), "Develop.txt")
                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                plik_od_dewelopera = f.read().strip()
                        else:
                            plik_od_dewelopera = "BRAK PLIKU D"
                            messagebox.showerror(
                                "Błąd", 'Zapytaj twórcę programu o informacje')

                        selected_category = combo_var.get()  # Pobierz wybraną kategorię z ComboBox-a

                        issue_title = entry_tutul_problemu.get()
                        issue_description = entry_opis_problemu.get(
                            "1.0", tk.END)

                        if not issue_title and issue_description and selected_category:
                            messagebox.showwarning(
                                "To zgłoszenie jest puste", "Nie podano tytułu zgłoszenia")
                            return

                        if not selected_category:
                            messagebox.showwarning(
                                "Brak kategorii", "Niewybrano kategorii zgłoszenia")
                            return

                        if not issue_title:
                            messagebox.showwarning(
                                "Brak tytułu", "Nie podano tytułu zgłoszenia")
                            return

                        if not issue_description.strip():
                            messagebox.showwarning(
                                "Brak treści", "Nie podano treści zgłoszenia")
                            return

                        if len(issue_description.strip()) < 70:
                            if selected_category == "Błąd":
                                if len(issue_description.strip()) < 100:
                                    messagebox.showwarning(
                                        "Opisz dokładniej", "Treść zgłoszenia musi mieć co najmniej 100 znaków (około 17 słów). Opisz wszystko jak najdokładniej, jeśli się do tego nie     zastosujesz - nie będziemy się domyślać i twoje zgłoszenie zostanie usunięte")
                                    return
                            elif selected_category == "Propozycja":
                                if len(issue_description.strip()) < 150:
                                    messagebox.showwarning(
                                        "Opisz dokładniej", "Jeśli chcesz zaproponować nową funkcję, musisz mieć na nią szczegółowy plan. Opisz ją dokładniej (treść propozycji musi mieć co    najmniej 150 znaków)")
                                    return
                            elif selected_category == "Interfejs programu":
                                if len(issue_description.strip()) < 70:
                                    messagebox.showwarning(
                                        "Opisz dokładniej", "Treść zgłoszenia musi mieć co najmniej 70 znaków (około 15 słów). Opisz wszystko jak najdokładniej, jeśli się do tego nie  zastosujesz - nie będziemy się domyślać i twoje zgłoszenie zostanie usunięte")
                                    return
                            else:
                                messagebox.showwarning(
                                    "Opisz dokładniej", "Treść zgłoszenia musi mieć co najmniej 70 znaków (to około 13 słów, zalecamy bardziej opisowe zgłoszenia). Opisz wszystko jak  najdokładniej, jeśli się do tego nie zastosujesz - nie będziemy się domyślać i twoje zgłoszenie zostanie usunięte")
                                return

                        if not plik_od_dewelopera == "BRAK PLIKU D":
                            informacje_do_zgloszenia = plik_od_dewelopera.split(
                                '\n')
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
                                    "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                                return
                            elif dzisiaj == wygasa_data:
                                messagebox.showwarning(
                                    "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                                return
                        else:
                            messagebox.showinfo(
                                "Informacja", 'Niestety nie masz dostępu do tej funkcji lub czas jej dostępności dla ciebie minął. Skontaktuj się z osobą odpowiedzialną za program.')
                            return

                        # ustawienia konta
                        username = f'{nazwa_uzytkownika}'
                        password = f'{token_do_wpisania}'
                        repository_name = 'Ksao0/Repozytorium-magnesy-t'
                        issue_title = f'{entry_tutul_problemu.get()}'
                        aktualna_data_czas = datetime.datetime.now()
                        format_data_czas = aktualna_data_czas.strftime(
                            "%d.%m.%Y %H:%M")
                        issue_body = f"Data: {format_data_czas}\nProponowana kategoria: {selected_category}\n" + entry_opis_problemu.get(
                            "1.0", tk.END) + " Wysłano przez: " + nazwa_uzytkownika

                        # autentykacja
                        g = Github(username, password)

                        # pobierz repozytorium
                        repo = g.get_repo(repository_name)

                        # utwórz nowe zgłoszenie błędu
                        repo.create_issue(title=issue_title, body=issue_body)

                        messagebox.showinfo("Twoje zgłoszenie zostało wysłane!",
                                            'Dziękujemy za twój wkład w rozwój programu! Postaramy się je rozpatrzyć jak najszybciej!')

                    if not okno_edycja_kosztow_otwarte == 0:
                        okno_problemu = tk.Toplevel()
                        okno_problemu.title(
                            "Zgłaszanie problemów lub propozycji")
                        okno_problemu.geometry("370x300+1170+510")
                        okno_problemu.iconbitmap(file_path_ikonka)
                    else:
                        okno_problemu = tk.Toplevel()
                        okno_problemu.title(
                            "Zgłaszanie problemów lub propozycji")
                        okno_problemu.geometry("370x300+800+510")
                        okno_problemu.iconbitmap(file_path_ikonka)

                    label_informacja = tk.Label(
                        okno_problemu, text="Pamiętaj o wybraniu kategorii")
                    label_informacja.pack()

                    # Zmienna do przechowywania wybranej opcji
                    combo_var = tk.StringVar()

                    combo_var.set("")

                    # Lista opcji w ComboBox-ie
                    lista_kategorii = ["Błąd", "Propozycja",
                                       "Problem z wydajnością", "Interfejs programu", "Pytanie", "Inne"]

                    # Tworzenie ComboBox-a
                    combo_box = ttk.Combobox(
                        okno_problemu, textvariable=combo_var, values=lista_kategorii, state="readonly")
                    combo_box.pack(pady=10)

                    label_informacja = tk.Label(
                        okno_problemu, text="Tytuł:")
                    label_informacja.pack()
                    entry_tutul_problemu = tk.Entry(okno_problemu)
                    entry_tutul_problemu.pack()

                    label_informacja = tk.Label(
                        okno_problemu, text="Opis:")
                    label_informacja.pack()
                    entry_opis_problemu = tk.Text(okno_problemu, height=9)
                    entry_opis_problemu.pack()

                    button_wyslij_problem = tk.Button(
                        okno_problemu, text="Wyślij", command=zglos_problem_wyslij)
                    button_wyslij_problem.pack()

                    okno_problemu.protocol("WM_DELETE_WINDOW", zamknij_okno)
                    okno_problemu.bind("<Map>", lambda event: otworz_okno)

                    okno_problemu.mainloop()
                else:
                    messagebox.showerror("Błąd", "To okno jest już otwarte!")
            else:
                blad_poczatkowe()
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
                    "Błąd", 'Zapytaj twórcę programu o informacje')

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
                        "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
            else:
                messagebox.showwarning(
                    'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                return

            # ustawienia konta
            username = f'{nazwa_uzytkownika}'
            password = f'{token_do_wpisania}'
            repository_name = 'Ksao0/Repozytorium-magnesy-t'
            issue_title = 'Automatyczne zgłoszenie błędu z zglos_problem()'
            a = traceback.format_exc()
            aktualna_data_czas = datetime.datetime.now()
            format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
            issue_body = f"Data: {format_data_czas} Błąd funkcji zglos_problem():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

            # autentykacja
            g = Github(username, password)

            # pobierz repozytorium
            repo = g.get_repo(repository_name)

            # utwórz nowe zgłoszenie błędu
            repo.create_issue(title=issue_title, body=issue_body)

            messagebox.showinfo("Problem został zgłoszony",
                                "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
            exit()
    else:
        token_zaufania_wygasl_f()


def czynnosci_poczatkowe():
    try:
        global internet
        # Aktualizacja pliku WEW

        # ścieżka do pliku WEW.py w bieżącym folderze
        path = os.path.join(os.getcwd(), "WEW.py")

        # usuń plik WEW.py, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
            # print("Usunięto plik WEW.py")
        try:
            # pobierz plik main.py z repozytorium
            url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/WEW.py"
            urllib.request.urlretrieve(url, path)
            # print("Zastąpiono plik WEW.py")
        except:
            print('Wykryto brak połączenia z internetem')
            messagebox.showerror(
                "Błąd", f'Wystąpił błąd połączenia z internetem. Sprawdź połączenie z internetem, a następnie naciśnij ok')
            internet = 0
            try:
                # pobierz plik main.py z repozytorium
                url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/WEW.py"
                urllib.request.urlretrieve(url, path)
                # print("Zastąpiono plik WEW.py")
            except:
                messagebox.showerror(
                    "Błąd", f'Ponownie wystąpił błąd połączenia z internetem. Nie można wykonać czynności początkowych. Niektóre opcje będą niedostępne, inne mogą wywoływać błędy, których nie można zgłosić')
                response = messagebox.askyesno(
                    "Aktualizacja", "Czy pomimo tego chcesz kontynuuować?")
                if response == True:
                    internet = 0
                else:
                    exit()

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
                "Błąd", 'Zapytaj twórcę programu o informacje')

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
                    "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
        else:
            messagebox.showwarning(
                'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
            return

        # ustawienia konta
        username = f'{nazwa_uzytkownika}'
        password = f'{token_do_wpisania}'
        repository_name = 'Ksao0/Repozytorium-magnesy-t'
        issue_title = 'Automatyczne zgłoszenie błędu z czynnosci_poczatkowe()'
        a = traceback.format_exc()
        aktualna_data_czas = datetime.datetime.now()
        format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
        issue_body = f"Data: {format_data_czas} Błąd funkcji czynnosci_poczatkowe():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


czynnosci_poczatkowe()


def taj():
    try:
        try:
            # Pobierz zawartość pliku prefvers.txt z repozytorium na GitHub
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/prefvers.txt'
            response = requests.get(url)
            response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
            prefvers = response.content.decode('utf-8').strip()
            prefvers_lines = prefvers.split('\n')

            # Odczytaj zawartość pliku version.txt w twoim programie
            path = os.path.join(os.getcwd(), "version.txt")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    version_local = f.read().strip()
            else:
                version_local = "BRAK DANYCH"

            version_local_first_line = version_local.split('\n')[0]

            # Porównaj każdą linijkę w prefvers z pierwszą linijką version_local
            if version_local_first_line in prefvers_lines:
                global blokada_klamstwa
                blokada_klamstwa = True
                return
        except:
            pass

        def informacja_o_wygasaniu_tokenu(pozostale_dni):
            try:
                # Odczytaj zawartość pliku Develop.txt w twoim programie
                path = os.path.join(os.getcwd(), "Develop.txt")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        plik_od_dewelopera = f.read().strip()
                else:
                    plik_od_dewelopera = "BRAK PLIKU D"
                    messagebox.showerror(
                        "Błąd", 'Zapytaj twórcę programu o informacje')

                informacje_do_zgloszenia = plik_od_dewelopera.split('\n')
                nazwa_uzytkownika = informacje_do_zgloszenia[0]
                token_do_wpisania = informacje_do_zgloszenia[1]

                # ustawienia konta
                username = f'{nazwa_uzytkownika}'
                password = f'{token_do_wpisania}'
                repository_name = 'Ksao0/Repozytorium-magnesy-t'
                issue_title = 'Automatyczne zgłoszenie: Token niedługo wygasa'
                a = traceback.format_exc()
                aktualna_data_czas = datetime.datetime.now()
                format_data_czas = aktualna_data_czas.strftime(
                    "%d.%m.%Y %H:%M")
                issue_body = f"Data: {format_data_czas} Token niedługo wygasa\nWystąpił u: {nazwa_uzytkownika}\n\nOpis: Trzeba sworzyć nowy token (pozostało: {pozostale_dni} dni)"

                # autentykacja
                g = Github(username, password)

                # pobierz repozytorium
                repo = g.get_repo(repository_name)

                # utwórz nowe zgłoszenie błędu
                repo.create_issue(title=issue_title, body=issue_body)

                return
            except:
                pass

        # Odczytaj zawartość pliku Develop.txt w twoim programie
        path = os.path.join(os.getcwd(), "Develop.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                plik_od_dewelopera = f.read().strip()

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

                global token_zaufania
                # porównaj daty
                if int((wygasa_data - dzisiaj).days) >= 0:
                    if (wygasa_data - dzisiaj).days >= 30:
                        print(
                            Fore.LIGHTGREEN_EX + f"Token zaufanego użytkownika wygasa za {(wygasa_data - dzisiaj).days} dni" + Style.RESET_ALL)
                        token_zaufania = True
                    elif (wygasa_data - dzisiaj).days >= 20:
                        print(
                            Fore.GREEN + f"Token zaufanego użytkownika wygasa za {(wygasa_data - dzisiaj).days} dni" + Style.RESET_ALL)
                        token_zaufania = True
                    elif (wygasa_data - dzisiaj).days >= 11:
                        print(
                            Fore.YELLOW + f"Token zaufanego użytkownika wygasa za {(wygasa_data - dzisiaj).days} dni" + Style.RESET_ALL)
                        token_zaufania = True
                    elif (wygasa_data - dzisiaj).days == 1:
                        print(
                            Fore.RED + f"Token zaufanego użytkownika wygasa jutro" + Style.RESET_ALL)
                        messagebox.showerror(
                            'Czas mija...', "Token zaufanego użytkownika wygasa jutro. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                        pozostale_dni = (wygasa_data - dzisiaj).days
                        informacja_o_wygasaniu_tokenu(pozostale_dni)
                        token_zaufania = True
                    else:  # 10, 9 [...] 2
                        print(
                            Fore.RED + f"Token zaufanego użytkownika wygasa za {(wygasa_data - dzisiaj).days} dni" + Style.RESET_ALL)
                        messagebox.showerror(
                            'Czas mija...', "Token zaufanego użytkownika niedługo wygasa. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                        token_zaufania = True
                        pozostale_dni = (wygasa_data - dzisiaj).days
                        informacja_o_wygasaniu_tokenu(pozostale_dni)
                else:
                    print(
                        Fore.RED + f"Token zaufanego użytkownika wygasł" + Style.RESET_ALL)
                    messagebox.showerror(
                        'Czas minął', "Token zaufanego użytkownika wygasł, jak najszybciej zgłoś się do osoby odpowiedzialnej za program.\nProgram może przestać działać prawidłowo")
                    try:
                        pozostale_dni = (wygasa_data - dzisiaj).days
                        informacja_o_wygasaniu_tokenu(pozostale_dni)
                    except:
                        pass

        # Pobierz zawartość pliku version.txt z repozytorium na GitHub
        try:
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt'
            response = requests.get(url)
            response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
            version_online = response.content.decode('utf-8').strip()
        except requests.exceptions.RequestException as e:
            messagebox.showerror(
                "Błąd", f'Wystąpił błąd połączenia z internetem. Spróbuj ponownie później')
            return

        wstepna_version_online_lines = version_online.split('\n')
        if wstepna_version_online_lines[1] == "Status: yN":
            os.system('cls')
            print(Fore.RED + "Niestety nie możemy pobrać najnowszej wersji programu, ponieważ wystąpił krytyczny błąd związany z kodem\n"
                  + "Opcje aktualizacji zostały wyłączone do odwołania, wiekszość informacji o najnowszej wersji może być nieprawidłowa")
            global blokada_bledu
            blokada_bledu = True

        try:
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/lista_b.txt'
            response = requests.get(url)
            response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
            lista_b_online = response.content.decode('utf-8').strip()
        except requests.exceptions.RequestException as e:
            messagebox.showerror(
                "Błąd", f'Wystąpił błąd połączenia z internetem. Spróbuj ponownie później')
            return

        # Odczytaj zawartość pliku lista_b.txt na komputerze
        path = os.path.join(os.getcwd(), "lista_b.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                lista_b_local = f.read().strip()
        else:
            lista_b_local = "BRAK PLIKU"

        # Odczytaj zawartość pliku version.txt w twoim programie
        path = os.path.join(os.getcwd(), "version.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                version_local = f.read().strip()
        else:
            version_local = "BRAK DANYCH"
        if version_local != "BRAK DANYCH":
            version_online_lines = version_online.split('\n')
            version_local_lines = version_local.split('\n')
            lista_b_online_lines = lista_b_online.split('\n')
            lista_b_local_lines = lista_b_local.split('\n')

            # Nowa wersja (bez nowych bibliotek)
            if version_online_lines[0] != version_local_lines[0] and (version_online_lines[4] == version_local_lines[4] and lista_b_online == lista_b_local) and blokada_bledu == False:
                # Jest dostępna nowa wersja programu, więc należy poinformować użytkownika o konieczności aktualizacji
                message = f"Dostępna jest nowa wersja programu: {version_online_lines[0]}. Czy chcesz ją teraz zainstalować?"
                response = messagebox.askyesno("Aktualizacja", message)
                if response == True:
                    # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    zgloszenie_pobrania_nowej_wersji(version_online_lines[0],
                                                     version_local_lines[0], "Aktualizacja za zgodą (1)")
                    if messagebox.showinfo("Aktualizacja", "Program zostanie uruchomiony ponownie"):
                        restart_program()
                else:
                    return
            # Nowe biblioteki
            if version_online_lines[4] != version_local_lines[4] or lista_b_online != lista_b_local:
                biblioteki_pobrane = False
                messagebox.showwarning(
                    "Wymagane biblioteki", "Po aktualizacji do działania programu wymagane są nowe biblioteki. Zainstaluj je jak najszybciej. Wszystkie dane zostaną wyświetlone w terminalu (czarne okno w tle)")

                print(Fore.CYAN + f'{version_online}')

                niepobrane_biblioteki = set(
                    lista_b_online_lines) - set(lista_b_local_lines)
                if niepobrane_biblioteki:
                    print(
                        Fore.YELLOW + "\n\nProgram wymaga większej ilości bibliotek, zainstaluj je:")
                    print(Fore.LIGHTGREEN_EX +
                          "Aby to zrobić otwórz terminal cmd i wpisz:")
                    print("   pip install (nazwa biblioteki)")
                    print("Przykład:")
                    print("   pip install tkinter", Style.RESET_ALL)
                    print()
                    print(Fore.YELLOW + 'Lista wymaganych bibliotek:',
                          Style.RESET_ALL)

                    for biblioteka in niepobrane_biblioteki:
                        print(Fore.RED + biblioteka)

                else:
                    if version_online_lines[4] == version_local_lines[4] or lista_b_online == lista_b_local:
                        if version_online_lines[4] != version_local_lines[4] and lista_b_online == lista_b_local:
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
                                    "Błąd", 'Zapytaj twórcę programu o informacje')

                            if plik_od_dewelopera != "BRAK PLIKU D":
                                informacje_do_zgloszenia = plik_od_dewelopera.split(
                                    '\n')
                                nazwa_uzytkownika = informacje_do_zgloszenia[0]
                                token_do_wpisania = informacje_do_zgloszenia[1]

                                # pobierz datę wygaśnięcia
                                wygasa_dnia = int(informacje_do_zgloszenia[2])
                                wygasa_miesiaca = int(
                                    informacje_do_zgloszenia[3])
                                wygasa_roku = int(informacje_do_zgloszenia[4])

                                # utwórz obiekt daty z daty wygaśnięcia
                                wygasa_data = datetime.date(
                                    wygasa_roku, wygasa_miesiaca, wygasa_dnia)

                                # pobierz dzisiejszą datę
                                dzisiaj = datetime.date.today()
                                # porównaj daty
                                if dzisiaj > wygasa_data:
                                    messagebox.showerror(
                                        "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                                    return
                                elif dzisiaj == wygasa_data:
                                    messagebox.showwarning(
                                        "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                            else:
                                messagebox.showwarning(
                                    'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                                return

                            # ustawienia konta
                            username = f'{nazwa_uzytkownika}'
                            password = f'{token_do_wpisania}'
                            repository_name = 'Ksao0/Repozytorium-magnesy-t'
                            issue_title = 'Automatyczne zgłoszenie błędu z taj()'
                            a = traceback.format_exc()
                            aktualna_data_czas = datetime.datetime.now()
                            format_data_czas = aktualna_data_czas.strftime(
                                "%d.%m.%Y %H:%M")
                            issue_body = f"Data: {format_data_czas} Błąd funkcji taj(): Nie dodano bibliotek do pobrania, jedynie informację o ich dodaniu\n\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: Niedopatrzenie\nWartość błędu:     --\nTraceback:\n\n"

                            # autentykacja
                            g = Github(username, password)

                            # pobierz repozytorium
                            repo = g.get_repo(repository_name)

                            # utwórz nowe zgłoszenie błędu
                            repo.create_issue(
                                title=issue_title, body=issue_body)

                            messagebox.showwarning("Problem został zgłoszony",
                                                   "Możliwe, że wystąpił błąd. Nie ma informacji o nowych bibliotekach, ale wykryto oznaczenie o nowych wymaganych. Jeśli wystąpią problemy - zgłoś błąd.")

                        if version_online_lines[4] == version_local_lines[4] and lista_b_online != lista_b_local:
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
                                    "Błąd", 'Zapytaj twórcę programu o informacje')

                            if plik_od_dewelopera != "BRAK PLIKU D":
                                informacje_do_zgloszenia = plik_od_dewelopera.split(
                                    '\n')
                                nazwa_uzytkownika = informacje_do_zgloszenia[0]
                                token_do_wpisania = informacje_do_zgloszenia[1]

                                # pobierz datę wygaśnięcia
                                wygasa_dnia = int(
                                    informacje_do_zgloszenia[2])
                                wygasa_miesiaca = int(
                                    informacje_do_zgloszenia[3])
                                wygasa_roku = int(
                                    informacje_do_zgloszenia[4])

                                # utwórz obiekt daty z daty wygaśnięcia
                                wygasa_data = datetime.date(
                                    wygasa_roku, wygasa_miesiaca, wygasa_dnia)

                                # pobierz dzisiejszą datę
                                dzisiaj = datetime.date.today()
                                # porównaj daty
                                if dzisiaj > wygasa_data:
                                    messagebox.showerror(
                                        "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                                    return
                                elif dzisiaj == wygasa_data:
                                    messagebox.showwarning(
                                        "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za programenia.                ")
                            else:
                                messagebox.showwarning(
                                    'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                                return

                            # ustawienia konta
                            username = f'{nazwa_uzytkownika}'
                            password = f'{token_do_wpisania}'
                            repository_name = 'Ksao0/Repozytorium-magnesy-t'
                            issue_title = 'Automatyczne zgłoszenie błędu z taj()'
                            a = traceback.format_exc()
                            aktualna_data_czas = datetime.datetime.now()
                            format_data_czas = aktualna_data_czas.strftime(
                                "%d.%m.%Y %H:%M")
                            issue_body = f"Data: {format_data_czas} Błąd funkcji taj(): Dodano nowe biblioteki, ale nie dodano informacji o nich\n\nWystąpił u: {nazwa_uzytkownika}   \n\nTyp błędu: Niedopatrzenie"

                            # autentykacja
                            g = Github(username, password)

                            # pobierz repozytorium
                            repo = g.get_repo(repository_name)

                            # utwórz nowe zgłoszenie błędu
                            repo.create_issue(
                                title=issue_title, body=issue_body)

                    else:
                        print(
                            "Brak różnic - wszystkie wymagane biblioteki zostały pobrane.")
                while biblioteki_pobrane == False:
                    input(
                        Fore.YELLOW + 'Zainstaluj biblioteki, a następnie naciśnij enter...' + Style.RESET_ALL)
                    if messagebox.askyesno('Tej operacji nie można cofnąć', 'Czy na pewno ręcznie pobrałeś wszystkie wymagane biblioteki?\nJeśli lista bibliotek się nie pojawiła - TAK'):
                        if messagebox.showinfo(
                                'Aktualizacja', "Program zostanie uruchomiony ponownie"):
                            biblioteki_pobrane = True
                            restart_program()
                    else:
                        messagebox.showwarning(
                            'Pobierz wszystkie biblioteki', "Instrukcja do pobrania bibliotek jest wyświelana w terminalu")
                        biblioteki_pobrane = False
                Aktualizacja = ["python", "WEW.py"]
                subprocess.run(Aktualizacja)
                zgloszenie_pobrania_nowej_wersji(
                    version_online_first_line, version_local_lines[0], "Aktualizacja z nowymi bibliotekami")
                exit()
            # Dostępna aktualizacja
            if (version_online_lines[0] == version_local_lines[0] and version_online_lines[1] == "Status: Poprawka wersji" and version_online_lines[2] != version_local_lines[2]) or (version_online_lines[0] == version_local_lines[0] and version_online_lines[1] == "Status: Nowa wersja" and version_online_lines[2] != version_local_lines[2]) and blokada_bledu == False:
                # Jest dostępna poprawka wersji, więc należy poinformować użytkownika o konieczności aktualizacji
                message = f"Dostępna jest nowa wersja programu.\n   {version_online_lines[2]}\nCzy chcesz ją teraz zainstalować?"
                response = messagebox.askyesno("Aktualizacja", message)
                if response == True:
                    # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    zgloszenie_pobrania_nowej_wersji(version_online_first_line,
                                                     version_local_lines[0], "Aktualizacja za zgodą (2)")
                    print('Zaktualizowano!')
                    message = "Program zostanie uruchomiony ponownie"
                    if messagebox.showinfo("Aktualizacja", message):
                        restart_program()
                else:
                    return
            # Prowadzone są intensywne zmiany
            if version_online_lines[1] == "Status: B7" or version_online_lines[1] == "Status: Poprawki B7" and blokada_bledu == False:
                response = messagebox.askokcancel(
                    "Aktualizacja", "Prowadzone są intensywne zmiany w programie lub wykryto poważny błąd. Przez pewien czas program będzie aktualizowany przed każdym użyciem.\nCzy chcesz kontynuuować?")
                if response == True:
                    # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    zgloszenie_pobrania_nowej_wersji(version_online_first_line + "B7",
                                                     version_local_lines[0], "Trwa B7")
                    print('Zaktualizowano!')
                    message = "Zmiany będą widoczne po następnym uruchomieniu"
                    messagebox.showinfo("Aktualizacja", message)
                else:
                    exit()
                    # Poprawki B7 nie zostały przyjęte:
            # Intensywne zmiany zakończone
            if (version_local_lines[1] == "Status: B7" or version_local_lines[1] == "Status: Poprawki B7") and version_online_lines[1] != "Status: B7" and blokada_bledu == False:
                Aktualizacja = ["python", "WEW.py"]
                subprocess.run(Aktualizacja)
                zgloszenie_pobrania_nowej_wersji(
                    version_online_first_line, version_local_lines[0], "Koniec B7 dla tego użytkownika")
                if messagebox.showinfo(
                        'Aktualizacja', "Program zostanie uruchomiony ponownie"):
                    restart_program()
        else:
            if blokada_bledu == False:
                if messagebox.showerror(
                        "Niezdefiniowany błąd", "Wystąpił błąd, program zostanie uruchomiony ponownie\nDo zobaczenia!"):
                    open("version.txt", "w", encoding='utf-8').close()

                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    zgloszenie_pobrania_nowej_wersji(
                        version_online_first_line, "Nieznana", "Brak pliku version.txt")
                    restart_program()
            else:
                messagebox.showerror(
                    "Błąd danych", "Wystąpił niezależny błąd danych spowodowany działaniem użytkownika. Ten błąd zostanie naprawiony po zaktualizowaniu programu")

        try:
            # Pobierz zawartość pliku nprefvers.txt z repozytorium na GitHub
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/nprefvers.txt'
            response = requests.get(url)
            response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
            nprefvers = response.content.decode('utf-8').strip()
            nprefvers_lines = nprefvers.split('\n')

            # Odczytaj zawartość pliku version.txt w twoim programie
            path = os.path.join(os.getcwd(), "version.txt")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    version_local = f.read().strip()
            else:
                version_local = "BRAK DANYCH"

            version_local_lines = version_local.split('\n')

            for line in nprefvers_lines:
                if line.strip() == version_local_lines[0].strip():
                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    zgloszenie_pobrania_nowej_wersji(version_online_first_line,
                                                     version_local_lines[0], None)
                    return

            # Porównaj każdą linijkę w nprefvers z pierwszą linijką version_local
            if version_local in nprefvers_lines:
                Aktualizacja = ["python", "WEW.py"]
                subprocess.run(Aktualizacja)
                zgloszenie_pobrania_nowej_wersji(
                    version_online_first_line, version_local_lines[0], None)
                return

        except:
            pass

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
                "Błąd", 'Zapytaj twórcę programu o informacje')

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
                    "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
        else:
            messagebox.showwarning(
                'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
            return

        # ustawienia konta
        username = f'{nazwa_uzytkownika}'
        password = f'{token_do_wpisania}'
        repository_name = 'Ksao0/Repozytorium-magnesy-t'
        issue_title = 'Automatyczne zgłoszenie błędu z taj()'
        a = traceback.format_exc()
        aktualna_data_czas = datetime.datetime.now()
        format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
        issue_body = f"Data: {format_data_czas} Błąd funkcji taj():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


if internet == 1:
    taj()


def aktul():
    global blokada_bledu
    if blokada_bledu == True:
        ukrywanie_bledu()
        return
    else:
        try:
            if not internet == 0:
                czynnosci_poczatkowe()
                if not internet == 0:
                    os.system('cls')
                    # Ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "Aktualizator_aktualizatora.py")

                    # Usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                    # Pobierz plik Aktualizator_aktualizatora.py z repozytorium
                    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Aktualizator_aktualizatora.py"
                    urllib.request.urlretrieve(url, path)

                    Aktualizacja = ["python", "Aktualizator_aktualizatora.py"]
                    subprocess.run(Aktualizacja)

                    # Odczytaj zawartość pliku version.txt w twoim programie
                    path = os.path.join(os.getcwd(), "version.txt")
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf-8") as f:
                            version_local = f.read().strip()
                    else:
                        version_local = "BRAK DANYCH"

                    version_local_lines = version_local.split('\n')

                    zgloszenie_pobrania_nowej_wersji(version_online_first_line,
                                                     version_local_lines[0], "Aktualizacja ręczna")
                    print(Fore.GREEN + 'Zakończono! ')
                    print(
                        Fore.YELLOW + 'Program zostanie uruchomiony ponownie.' + Style.RESET_ALL)
                    if messagebox.showinfo("Aktualizacja", "Program zostanie uruchomiony ponownie"):
                        sleep(1)
                        restart_program()
            else:
                blad_poczatkowe()
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
                    "Błąd", 'Zapytaj twórcę programu o informacje')

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
                        "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za program   ")
            else:
                messagebox.showwarning(
                    'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                return

            # ustawienia konta
            username = f'{nazwa_uzytkownika}'
            password = f'{token_do_wpisania}'
            repository_name = 'Ksao0/Repozytorium-magnesy-t'
            issue_title = 'Automatyczne zgłoszenie błędu z aktul()'
            a = traceback.format_exc()
            aktualna_data_czas = datetime.datetime.now()
            format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
            issue_body = f"Data: {format_data_czas} Błąd funkcji aktul():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

            # autentykacja
            g = Github(username, password)

            # pobierz repozytorium
            repo = g.get_repo(repository_name)

            # utwórz nowe zgłoszenie błędu
            repo.create_issue(title=issue_title, body=issue_body)

            messagebox.showinfo("Problem został zgłoszony",
                                "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
            exit()


def wykasuj_zapisy():
    try:
        # Ścieżka do pliku Zapisy.txt w bieżącym folderze
        path = os.path.join(os.getcwd(), "Zapisy.txt")

        # Usuń plik Zapisy.txt, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
            with open('Zapisy.txt', mode='w', encoding='utf-8') as file:
                file.write('')
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
                "Błąd", 'Zapytaj twórcę programu o informacje')

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
                    "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
        else:
            messagebox.showwarning(
                'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
            return

        # ustawienia konta
        username = f'{nazwa_uzytkownika}'
        password = f'{token_do_wpisania}'
        repository_name = 'Ksao0/Repozytorium-magnesy-t'
        issue_title = 'Automatyczne zgłoszenie błędu z wykasuj_zapisy()'
        a = traceback.format_exc()
        aktualna_data_czas = datetime.datetime.now()
        format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
        issue_body = f"Data: {format_data_czas} Błąd funkcji wykasuj_zapisy():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


def wykres():
    try:
        filename = "Zapisy.txt"
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()

        # Podziel dane na poszczególne obliczenia
        obliczenia = data.split("\n\n")

        # Sprawdź, czy jest wystarczająca ilość obliczeń do wygenerowania wykresu
        if len(obliczenia) < 8:
            print(Fore.YELLOW +
                  "Niewystarczająca ilość danych do wygenerowania wykresu" + Style.RESET_ALL)
            messagebox.showinfo(
                "Brak danych o wykresie", 'Niewystarczająca ilośc danych do wygenerowania wykresu. Wykonaj więcej obliczeń :D')
        else:
            # Utwórz listy przechowujące dane dla wykresu
            liczba_pakietow = []
            liczba_magnesow = []
            cena_magnesu = []
            cena_pakietu = []
            koszty = []
            zyski = []
            cena_za_w_pakiety = []

            # Przejdź przez każde obliczenie
            for obliczenie in obliczenia:
                # Podziel obliczenie na linie
                lines = obliczenie.strip().split("\n")
                # Pobierz potrzebne wartości z obliczenia
                for line in lines:
                    if "Liczba pakietów:" in line:
                        liczba_pakietow.append(
                            float(line.split(":")[1].strip().split(" ")[0]))
                    elif "Liczba magnesów:" in line:
                        liczba_magnesow.append(
                            float(line.split(":")[1].strip().split(" ")[0]))
                    elif "Cena za 1 magnes:" in line:
                        cena_magnesu.append(
                            float(line.split(":")[1].strip().split(" ")[0]))
                    elif "Jeden pakiet to:" in line:
                        cena_pakietu.append(
                            float(line.split(":")[1].strip().split(" ")[0]))
                    elif "Koszty:" in line:
                        koszty.append(
                            float(line.split(":")[1].strip().split(" ")[0]))
                    elif "Zysk sprzedaży:" in line:
                        zyski.append(
                            float(line.split(":")[1].strip().split(" ")[0]))
                    elif "Cena za wszystkie pakiety:" in line:
                        cena_za_w_pakiety.append(
                            float(line.split(":")[1].strip().split(" ")[0]))

            # Utwórz wykres
            fig, ax = plt.subplots()
            ax.plot(liczba_pakietow, label='Liczba pakietów')
            for i, j in zip(range(len(liczba_pakietow)), liczba_pakietow):
                ax.annotate(str(j), xy=(i, j), ha='center', va='bottom')
            ax.plot(liczba_magnesow, label='Liczba magnesów')
            for i, j in zip(range(len(liczba_magnesow)), liczba_magnesow):
                ax.annotate(str(j), xy=(i, j), ha='center', va='bottom')
            ax.plot(cena_magnesu, label='Cena za 1 magnes')
            for i, j in zip(range(len(cena_magnesu)), cena_magnesu):
                ax.annotate(str(j), xy=(i, j), ha='center', va='bottom')
            ax.plot(cena_pakietu, label='Jeden pakiet to zł')
            for i, j in zip(range(len(cena_pakietu)), cena_pakietu):
                ax.annotate(str(j), xy=(i, j), ha='center', va='bottom')
            ax.plot(koszty, label='Koszty')
            for i, j in zip(range(len(koszty)), koszty):
                ax.annotate(str(j), xy=(i, j), ha='center', va='bottom')
            ax.plot(zyski, label='Zysk sprzedaży')
            for i, j in zip(range(len(zyski)), zyski):
                ax.annotate(str(j), xy=(i, j), ha='center', va='bottom')
            ax.plot(cena_za_w_pakiety, label='Cena za wszystkie pakiety')
            for i, j in zip(range(len(cena_za_w_pakiety)), cena_za_w_pakiety):
                ax.annotate(str(j), xy=(i, j), ha='center', va='bottom')

            # Dodaj tytuł i etykiety osi
            ax.set_title(
                'Wyniki obliczeń sprzedaży magnesów (najnowsze wyniki są po lewej stronie, a starsze po prawej)')
            ax.set_xlabel('Numer obliczenia')
            ax.set_ylabel('Zł')

            # Dodaj legendę
            ax.legend()

            # Wyświetl wykres
            fig.set_size_inches(14, 8)
            plt.show()
    except Exception as e:
        if messagebox.askyesno(
           'Zgłaszanie błędu', "Czy chcesz zgłosić błąd, kóry przed chwilą wystąpił? Prawdopodobną jego przyczyną jest brak danych do wytworzenia wykresu"):
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
                    "Błąd", 'Zapytaj twórcę programu o informacje')

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
                        "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za program   ")
            else:
                messagebox.showwarning(
                    'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                return

            # ustawienia konta
            username = f'{nazwa_uzytkownika}'
            password = f'{token_do_wpisania}'
            repository_name = 'Ksao0/Repozytorium-magnesy-t'
            issue_title = 'Automatyczne zgłoszenie błędu z wykres()'
            a = traceback.format_exc()
            aktualna_data_czas = datetime.datetime.now()
            format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
            issue_body = f"Data: {format_data_czas} Błąd funkcji wykres():\nPrawdodpodobna przyczyna: Brak danych do wygenerowania wykresu\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu:    {exc_value}\nTraceback:\n\n{a}"

            # autentykacja
            g = Github(username, password)

            # pobierz repozytorium
            repo = g.get_repo(repository_name)

            # utwórz nowe zgłoszenie błędu
            repo.create_issue(title=issue_title, body=issue_body)

            messagebox.showinfo("Problem został zgłoszony",
                                "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
            exit()
        else:
            return


def rozwiaz_problemy():
    global blokada_bledu
    if blokada_bledu == True or blokada_klamstwa == True:
        ukrywanie_bledu()
        return
    else:
        try:
            if not internet == 0:
                message = "Przeczytaj uważnie wszystkie informacje w terminalu (czarne okno w tle). Upewnij się, że nie utracisz połączenia z internetem."
                messagebox.showwarning("Ostrzeżenie", message)

                os.system('cls')
                print(Fore.RED + 'Nie zamykaj tego okna!')
                print(Fore.YELLOW + 'Wszystkie dane (ceny, poprzednie obliczenia, informacje o wersji, niektóre pliki aktualizacyjne, oraz sam program)\nzostaną usunięte. Po usunięciu danych ' +
                      Style.BRIGHT + Fore.RED + 'tej operacji nie można cofnąć.' + Style.RESET_ALL + Fore.RED + '\nAby zainstalować program ponownie: Uruchom plik WEW.py')

                input(Fore.YELLOW + "Naciśnij klawisz Enter, aby kontynuuować...")
                print()
                print(Fore.YELLOW + 'Aby anulować wpisz cokolwiek innego:')
                usuwanie_danych_potwierdzenie = str(
                    input(Fore.RED + 'Napisz ' + Style.BRIGHT + '"USUN01"' + Style.RESET_ALL + Fore.RED + ' (pamiętaj o dużych literach i braku polskich znaków), aby potwierdzić: '))
                if usuwanie_danych_potwierdzenie == "USUN01":
                    print(
                        Fore.RED + '\nZaczekaj, aż to okno się zamknie, trwa kasowanie')
                    # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(os.getcwd(), "Ceny.txt")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(os.getcwd(), "version.txt")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(os.getcwd(), "Aktualizacja.py")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "Aktualizator_aktualizatora.py")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "Snake.py")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "ikona.ico")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                        sleep(3)

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "lista_b.txt")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                        sleep(2)

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "Zapisy.txt")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                        sleep(3)

                    folder_path = "rei"

                    # Usunięcie folderu "rei" wraz z jego zawartością, jeśli istnieje
                    if os.path.exists(folder_path):
                        shutil.rmtree(folder_path)

                    # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(os.getcwd(), "ikona_magnesy.ico")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                    # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(os.getcwd(), "Zapisy.txt")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                    # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "Androidow.py")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                        sleep(3)

                    # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(os.getcwd(), "main.py")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)

                    print(Fore.CYAN + 'Kasowanie zakończone')
                    exit()
                else:
                    print(Fore.GREEN +
                          '\nAnulowano wszystkie czynności. Możesz kontynuuować korzystanie z programu')
            else:
                blad_poczatkowe()
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
                    "Błąd", 'Zapytaj twórcę programu o informacje')

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
                        "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za program   ")
            else:
                messagebox.showwarning(
                    'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                return

            # ustawienia konta
            username = f'{nazwa_uzytkownika}'
            password = f'{token_do_wpisania}'
            repository_name = 'Ksao0/Repozytorium-magnesy-t'
            issue_title = 'Automatyczne zgłoszenie błędu z rozwiaz_problemy()'
            a = traceback.format_exc()
            aktualna_data_czas = datetime.datetime.now()
            format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
            issue_body = f"Data: {format_data_czas} Błąd funkcji rozwiaz_problemy():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}  "

            # autentykacja
            g = Github(username, password)

            # pobierz repozytorium
            repo = g.get_repo(repository_name)

            # utwórz nowe zgłoszenie błędu
            repo.create_issue(title=issue_title, body=issue_body)

            messagebox.showinfo("Problem został zgłoszony",
                                "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
            exit()


def ankieta():
    global token_zaufania
    global file_path_ikonka
    if token_zaufania == True:
        if blokada_bledu == 0:
            try:
                # Odczytaj zawartość pliku Ank.txt na komputerze
                path = os.path.join(os.getcwd(), "Ank.txt")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        ankieta_wykonana = f.read().strip()
                else:
                    ankieta_wykonana = "Nie"

                if ankieta_wykonana != "Tak":
                    if messagebox.askyesno(
                            "Jednorazowa ankieta", "Odpowiadając na te kilka pytań możesz wesprzeć rozwój naszego programu. Czy zgadzasz się na przeprowadzenie krótkiej ankiety?"):
                        okno_ankiety = tk.Toplevel()
                        okno_ankiety.title("Ankieta")
                        okno_ankiety.geometry("700x670")
                        okno_ankiety.iconbitmap(file_path_ikonka)

                        frame_pyt1 = tk.Frame(okno_ankiety)
                        frame_pyt1.pack()

                        label_informacja = tk.Label(
                            frame_pyt1, text='Jeżeli odpowiedź brzmi nie - Napisz \"Nie\"')
                        label_informacja.pack()

                        pustka = tk.Label()
                        pustka.pack()

                        label_pytanie = tk.Label(
                            frame_pyt1, text='Czy podczas korzystania z naszego programu musisz wykonywać jakieś dodatkowe obliczenia, jakie?')
                        label_pytanie.pack()

                        pole_tekstowe_pyt1 = tk.Text(
                            frame_pyt1, width=60, height=11)
                        pole_tekstowe_pyt1.pack()

                        # pyt1 = tk.IntVar()

                        # checkbox_pyt1_tak = tk.Radiobutton(
                        #    frame_pyt1, text="Tak", variable=pyt1, value=1)
                        # checkbox_pyt1_tak.pack()

                        # checkbox_pyt1_nie = tk.Radiobutton(
                        #    frame_pyt1, text="Nie", variable=pyt1, value=0)
                        # checkbox_pyt1_nie.pack()

                        frame_pyt2 = tk.Frame(okno_ankiety)
                        frame_pyt2.pack()

                        label_pytanie2 = tk.Label(
                            frame_pyt2, text='Czy nasz program zawiera funkcje, które twoim zdaniem są nieprzydatne? Wymień je')
                        label_pytanie2.pack()

                        pole_tekstowe_pyt2 = tk.Text(
                            frame_pyt2, width=60, height=11)
                        pole_tekstowe_pyt2.pack()

                        frame_pyt3 = tk.Frame(okno_ankiety)
                        frame_pyt3.pack()

                        label_pytanie3 = tk.Label(
                            frame_pyt3, text='Co chciałbyś dodać/usunąć/zmienić w aplikacji na telefon?')
                        label_pytanie3.pack()

                        pole_tekstowe_pyt3 = tk.Text(
                            frame_pyt3, width=60, height=11)
                        pole_tekstowe_pyt3.pack()

                        def wyslij():
                            try:
                                global odpowiedz_pytanie1
                                global odpowiedz_pytanie2
                                global odpowiedz_pytanie3

                                odpowiedz_pytanie1 = ""
                                odpowiedz_pytanie2 = ""
                                odpowiedz_pytanie3 = ""

                                odpowiedz_pytanie1 = pole_tekstowe_pyt1.get(
                                    "1.0", tk.END).strip()
                                odpowiedz_pytanie2 = pole_tekstowe_pyt2.get(
                                    "1.0", tk.END).strip()
                                odpowiedz_pytanie3 = pole_tekstowe_pyt3.get(
                                    "1.0", tk.END).strip()

                                udzielone_odpowiedzi = 0

                                if odpowiedz_pytanie1 != "":
                                    udzielone_odpowiedzi = udzielone_odpowiedzi + 1

                                if odpowiedz_pytanie2 != "":
                                    udzielone_odpowiedzi = udzielone_odpowiedzi + 1

                                if odpowiedz_pytanie3 != "":
                                    udzielone_odpowiedzi = udzielone_odpowiedzi + 1

                                liczba_nie = 0

                                if odpowiedz_pytanie1 == "Nie" or odpowiedz_pytanie1 == "NIE" or odpowiedz_pytanie1 == "nie" or odpowiedz_pytanie1 == "nIE":
                                    liczba_nie = liczba_nie + 1

                                if odpowiedz_pytanie2 == "Nie" or odpowiedz_pytanie2 == "NIE" or odpowiedz_pytanie2 == "nie" or odpowiedz_pytanie2 == "nIE":
                                    liczba_nie = liczba_nie + 1

                                if odpowiedz_pytanie3 == "Nie" or odpowiedz_pytanie3 == "NIE" or odpowiedz_pytanie3 == "nie" or odpowiedz_pytanie3 == "nIE":
                                    liczba_nie = liczba_nie + 1

                                if udzielone_odpowiedzi == 3 and liczba_nie == 0:
                                    messagebox.showinfo('Ankieta zostałą wysłana',
                                                        'Dziękujemy za udzielenie odpowiedzi!\nKod odpowiedzi: 3(a)')

                                elif udzielone_odpowiedzi == 3 and liczba_nie == 1:
                                    messagebox.showinfo('Ankieta zostałą wysłana',
                                                        'Dziękujemy za udzielenie odpowiedzi!\nKod odpowiedzi: 3(b)')

                                elif udzielone_odpowiedzi == 3 and liczba_nie == 2:
                                    messagebox.showinfo('Ankieta zostałą wysłana',
                                                        'Dziękujemy za udzielenie odpowiedzi!\nKod odpowiedzi: 3(c)')

                                elif udzielone_odpowiedzi == 2 and liczba_nie == 0:
                                    messagebox.showinfo('Ankieta zostałą wysłana',
                                                        'Dziękujemy za udzielenie odpowiedzi!\nKod odpowiedzi: 2(a)')

                                elif udzielone_odpowiedzi == 2 and liczba_nie == 1:
                                    messagebox.showinfo('Ankieta zostałą wysłana',
                                                        'Dziękujemy za udzielenie odpowiedzi!\nKod odpowiedzi: 2')

                                elif udzielone_odpowiedzi == 1 and liczba_nie != 1:
                                    messagebox.showinfo('Ankieta zostałą wysłana',
                                                        'Dziękujemy za udzielenie odpowiedzi!\nKod odpowiedzi: 1')

                                else:  # dla 0 i innych (nie itp.)
                                    messagebox.showinfo('Ta ankieta jest nieistotna',
                                                        'Możliwość wykonania następnej ankiety pojawi się po aktualizacji po aktualizacji\nKod odpowiedzi: (p) 0')
                                    path = os.path.join(os.getcwd(), "Ank.txt")
                                    # Usuń plik jeśli istnieje
                                    if os.path.exists(path):
                                        os.remove(path)

                                    with open("Ank.txt", "a", encoding='utf-8') as plik:
                                        plik.write('Tak')

                                    okno_ankiety.destroy()
                                    return

                                path = os.path.join(os.getcwd(), "Ank.txt")

                                # Usuń plik jeśli istnieje
                                if os.path.exists(path):
                                    os.remove(path)

                                with open("Ank.txt", "a", encoding='utf-8') as plik:
                                    plik.write('Tak')

                                # Odczytaj zawartość pliku Develop.txt w twoim programie
                                path = os.path.join(os.getcwd(), "Develop.txt")
                                if os.path.exists(path):
                                    with open(path, "r", encoding="utf-8") as f:
                                        plik_od_dewelopera = f.read().strip()
                                else:
                                    plik_od_dewelopera = "BRAK PLIKU D"
                                    messagebox.showerror(
                                        "Błąd", 'Zapytaj twórcę programu o informacje')

                                if plik_od_dewelopera != "BRAK PLIKU D":
                                    informacje_do_zgloszenia = plik_od_dewelopera.split(
                                        '\n')
                                    nazwa_uzytkownika = informacje_do_zgloszenia[0]
                                    token_do_wpisania = informacje_do_zgloszenia[1]

                                    # pobierz datę wygaśnięcia
                                    wygasa_dnia = int(
                                        informacje_do_zgloszenia[2])
                                    wygasa_miesiaca = int(
                                        informacje_do_zgloszenia[3])
                                    wygasa_roku = int(
                                        informacje_do_zgloszenia[4])

                                    # utwórz obiekt daty z daty wygaśnięcia
                                    wygasa_data = datetime.date(
                                        wygasa_roku, wygasa_miesiaca, wygasa_dnia)

                                    # pobierz dzisiejszą datę
                                    dzisiaj = datetime.date.today()
                                    # porównaj daty
                                    if dzisiaj > wygasa_data:
                                        messagebox.showerror(
                                            "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                                        return
                                    elif dzisiaj == wygasa_data:
                                        messagebox.showwarning(
                                            "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za programużenia.")
                                else:
                                    messagebox.showwarning(
                                        'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                                    return

                                # ustawienia konta
                                username = f'{nazwa_uzytkownika}'
                                password = f'{token_do_wpisania}'
                                repository_name = 'Ksao0/Repozytorium-magnesy-t'
                                issue_title = f'Ankieta od {nazwa_uzytkownika}'
                                aktualna_data_czas = datetime.datetime.now()
                                format_data_czas = aktualna_data_czas.strftime(
                                    "%d.%m.%Y %H:%M")
                                issue_body = f"Ankieta (data: {format_data_czas}):\nDodatkowe obliczenia: " + odpowiedz_pytanie1 + \
                                    "\nNiepotrzebne funkcje: " + odpowiedz_pytanie2 + \
                                    "\nAplikacja na telefon: " + odpowiedz_pytanie3

                                # autentykacja
                                g = Github(username, password)

                                # pobierz repozytorium
                                repo = g.get_repo(repository_name)

                                # utwórz nowe zgłoszenie błędu
                                repo.create_issue(
                                    title=issue_title, body=issue_body)
                                okno_ankiety.destroy()
                                return
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
                                        "Błąd", 'Zapytaj twórcę programu o informacje')

                                if plik_od_dewelopera != "BRAK PLIKU D":

                                    informacje_do_zgloszenia = plik_od_dewelopera.split(
                                        '\n')
                                    nazwa_uzytkownika = informacje_do_zgloszenia[0]
                                    token_do_wpisania = informacje_do_zgloszenia[1]

                                    # pobierz datę wygaśnięcia
                                    wygasa_dnia = int(
                                        informacje_do_zgloszenia[2])
                                    wygasa_miesiaca = int(
                                        informacje_do_zgloszenia[3])
                                    wygasa_roku = int(
                                        informacje_do_zgloszenia[4])

                                    # utwórz obiekt daty z daty wygaśnięcia
                                    wygasa_data = datetime.date(
                                        wygasa_roku, wygasa_miesiaca, wygasa_dnia)

                                    # pobierz dzisiejszą datę
                                    dzisiaj = datetime.date.today()
                                    # porównaj daty
                                    if dzisiaj > wygasa_data:
                                        messagebox.showerror(
                                            "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                                        return
                                    elif dzisiaj == wygasa_data:
                                        messagebox.showwarning(
                                            "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za programa.                      ")
                                else:
                                    messagebox.showwarning(
                                        'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                                    return

                                # ustawienia konta
                                username = f'{nazwa_uzytkownika}'
                                password = f'{token_do_wpisania}'
                                repository_name = 'Ksao0/Repozytorium-magnesy-t'
                                issue_title = 'Automatyczne zgłoszenie błędu z ankieta()'
                                a = traceback.format_exc()
                                aktualna_data_czas = datetime.datetime.now()
                                format_data_czas = aktualna_data_czas.strftime(
                                    "%d.%m.%Y %H:%M")
                                issue_body = f"Data: {format_data_czas} Błąd funkcji wyslij() w ankieta():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu:   {exc_value}   \nTraceback:\n\n{a}"

                                # autentykacja
                                g = Github(username, password)

                                # pobierz repozytorium
                                repo = g.get_repo(repository_name)

                                # utwórz nowe zgłoszenie błędu
                                repo.create_issue(
                                    title=issue_title, body=issue_body)

                                messagebox.showinfo("Problem został zgłoszony",
                                                    "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
                                exit()
                        button_wyslij = tk.Button(
                            okno_ankiety, text="Wyślij odpowiedzi", command=wyslij)
                        button_wyslij.pack()

                        okno_ankiety.mainloop()
                    else:
                        return
                else:
                    return
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
                        "Błąd", 'Zapytaj twórcę programu o informacje')

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
                            "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                        return
                    elif dzisiaj == wygasa_data:
                        messagebox.showwarning(
                            "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za program   ")
                else:
                    messagebox.showwarning(
                        'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                    return

                # ustawienia konta
                username = f'{nazwa_uzytkownika}'
                password = f'{token_do_wpisania}'
                repository_name = 'Ksao0/Repozytorium-magnesy-t'
                issue_title = 'Automatyczne zgłoszenie błędu z ankieta()'
                a = traceback.format_exc()
                aktualna_data_czas = datetime.datetime.now()
                format_data_czas = aktualna_data_czas.strftime(
                    "%d.%m.%Y %H:%M")
                issue_body = f"Data: {format_data_czas} Błąd funkcji ankieta():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

                # autentykacja
                g = Github(username, password)

                # pobierz repozytorium
                repo = g.get_repo(repository_name)

                # utwórz nowe zgłoszenie błędu
                repo.create_issue(title=issue_title, body=issue_body)

                messagebox.showinfo("Problem został zgłoszony",
                                    "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
                exit()

                # if random.choices([True, False], [0.2, 0.8])[0]:
                #     ankieta()
    else:
        pass


if internet == 1 and blokada_bledu == 0:
    if random.choices([True, False], [0.1, 0.9])[0]:
        ankieta()


def informacje_o_wersji_utworz_okno():
    if blokada_bledu == 0:
        try:
            global file_path_ikonka
            global dziennik_z_online
            if not internet == 0:
                def otworz_okno():
                    global okno_informacje_otwarte
                    okno_informacje_otwarte = 1

                def zamknij_okno():
                    global okno_informacje_otwarte
                    okno_informacje_otwarte = 0
                    informacje_wersji.destroy()

                if okno_informacje_otwarte == 0:
                    version_online = "BRAK DANYCH"
                    # Pobierz zawartość pliku version.txt z repozytorium na GitHub
                    try:
                        url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt'
                        response = requests.get(url)
                        response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
                        version_online = response.content.decode(
                            'utf-8').strip()
                    except:
                        messagebox.showerror(
                            "Błąd", f'Wystąpił błąd połączenia z internetem. Nie można pobrać informacji o najnowszej wersji.')

                    dziennik_z_online = "BRAK DANYCH"
                    # Pobierz zawartość pliku Dziennk_b.txt z repozytorium na GitHub
                    try:
                        url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Dziennik_b.txt'
                        response = requests.get(url)
                        response.raise_for_status()  # sprawdź, czy nie było błędu w pobieraniu
                        dziennik_z_online = response.content.decode(
                            'utf-8').strip()
                    except:
                        messagebox.showerror(
                            "Błąd", f'Wystąpił błąd połączenia z internetem. Nie można pobrać informacji o najnowszej wersji.')

                    # Odczytaj zawartość pliku version.txt w twoim programie
                    path = os.path.join(os.getcwd(), "version.txt")
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf-8") as f:
                            version_local = f.read().strip()
                    else:
                        version_local = "BRAK DANYCH"

                    version_online_lines = version_online.split('\n')
                    version_local_lines = version_local.split('\n')
                    dziennik_z_online_lines = dziennik_z_online.split('\n')

                    informacje_wersji = tk.Toplevel()
                    informacje_wersji.title(f"Informacje o wersji")
                    informacje_wersji.iconbitmap(file_path_ikonka)

                    if blokada_klamstwa == True:
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"Wersja na komputerze: {version_local_lines[0]}", justify="left")
                        label_informacja.pack()
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"{version_local_lines[1]}", justify="left")
                        label_informacja.pack()
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"{version_local_lines[2]}", justify="left")
                        label_informacja.pack()
                        pustka = tk.Label()
                        pustka.pack()

                        label_informacja = tk.Label(
                            informacje_wersji, text=f"Najnowsza wersja: {version_local_lines[0]}", justify="left")
                        label_informacja.pack()
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"{version_local_lines[1]}", justify="left")
                        label_informacja.pack()
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"{version_local_lines[2]}", justify="left")
                        label_informacja.pack()
                    else:
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"Wersja na komputerze: {version_local_lines[0]}", justify="left")
                        label_informacja.pack()
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"{version_local_lines[1]}", justify="left")
                        label_informacja.pack()
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"{version_local_lines[2]}", justify="left")
                        label_informacja.pack()
                        pustka = tk.Label()
                        pustka.pack()

                        label_informacja = tk.Label(
                            informacje_wersji, text=f"Najnowsza wersja: {version_online_lines[0]}", justify="left")
                        label_informacja.pack()
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"{version_online_lines[1]}", justify="left")
                        label_informacja.pack()
                        label_informacja = tk.Label(
                            informacje_wersji, text=f"{version_online_lines[2]}", justify="left")
                        label_informacja.pack()

                    def dziennik_zmian():
                        global dziennik_z_online
                        if dziennik_z_online != "BRAK DANYCH":
                            dziennik_zmian_okno = tk.Toplevel()
                            dziennik_zmian_okno.title(f"Dziennik zmian")
                            dziennik_zmian_okno.iconbitmap(file_path_ikonka)

                            label_informacja = tk.Label(
                                dziennik_zmian_okno, text=f"Ostatni wpis w wersji: {dziennik_z_online_lines[0]}")
                            label_informacja.pack()

                            def co_znaczniki():
                                messagebox.showinfo(
                                    'Wyjaśnienia', 'Używamy ich, aby uprścić nasz dziennik, oto ich znaczenia:\n'
                                    + '"[]" - Notatka i/lub zapowiedź\n'
                                    + '"/" - Całkowite usunięcie błędu bez wieloetapowych napraw\n'
                                    + '"/\\" - Usunięcie wcześniej wykrytego błędu, który mógł być wielokrotnie naprawiany z wykorzystaniem znacznika "///" i/lub "!", '  # Nowa linia kodu
                                    + 'lub zakończenie dodawania funkcji\n'
                                    + '"///" - Kolejny etap usuwania/szukania wcześniej wykrytego błędu lub dodawania funkcji\n'
                                    + '"\\/" - Wykrycie błędu lub rozpoczęcie procesu dodawania funkcji\n'
                                    + '"+" - Dodanie nowej funkcjonalności\n'
                                    + '"-" - Usunięcie funkcjonalności\n'
                                    + '"!" - Próba usunięcia błędu (nieznany rezultat)\n'
                                    + '"~" - Zmiana działania\n'
                                    + '"#!" - Zablokowanie możliwości pobierania wersji (błąd krytyczny, wersja jest niedostępna dla nowych użytkowników)\n')
                            # "[]" - Notatka i/lub zapowiedź
                            # "/" - Całkowite usunięcie błędu bez wieloetapowych napraw
                            # "/\" - Usunięcie wcześniej wykrytego błędu, który mógł być wielokrotnie naprawiany z wykorzystaniem znacznika "///" i/lub "!", lub zakończenie dodawania funkcji
                            # "///" - Kolejny etap usuwania/szukania wcześniej wykrytego błędu lub dodawania funkcji
                            # "\/" - Wykrycie błędu lub rozpoczęcie procesu dodawania funkcji
                            # "+" - Dodanie nowej funkcjonalności
                            # "-" - Usunięcie funkcjonalności
                            # "!" - Próba usunięcia błędu (niezaawansowany błąd, nieznany rezultat)
                            # "~" - Zmiana działania
                            # "#!" - Zablokowanie możliwości pobierania wersji (błąd krytyczny, wersja jest niedostępna dla nowych użytkowników)

                            # Dodanie kontenera typu Frame
                            frame_przyciski = tk.Frame(dziennik_zmian_okno)
                            frame_przyciski.pack()
                            button_dziennik_b = tk.Button(
                                frame_przyciski, text=f"Co oznaczają te symbole?", command=co_znaczniki)
                            button_dziennik_b.pack(side=tk.LEFT)

                            def nieuzupelnione_zmiany():
                                messagebox.showinfo('Dlaczego dziennik zmian nie jest uzupełniany?', 'Dziennik zmian nie jest uzupełniany jeżeli aktualizacja nie ma żadnego znaczenia dla  użytkowania programu, np. jeśli usuniemy literówki, zmienimy formatowanie kodu lub nazwę zminnej. Takie wpisy byłyby zbyt częste\nJeśli uważasz, że zmiana   powinna zostac wpisana - zgłoś nam to za pomocą opcji "Zgłoś problemy lub propozycje".')

                            button_dziennik_b = tk.Button(
                                frame_przyciski, text=f"Dziennik zmian nie jest uzupełniany", command=nieuzupelnione_zmiany)
                            button_dziennik_b.pack(side=tk.RIGHT)
                            if blokada_klamstwa == False:
                                label_informacja = tk.Label(
                                    dziennik_zmian_okno, text=f"Odkryj najnowsze zmiany i uaktualnienia, które wprowadziliśmy do programu! (od najnowszych)")
                                label_informacja.pack()

                            zmiany = []
                            zmiana = ""
                            # Pomijamy pierwszą linię z wersją
                            for line in dziennik_z_online_lines[1:]:
                                if line.startswith(" [] ") or line.startswith(" / ") or line.startswith(" /\\ ") or line.startswith(" /// ") or line.startswith(" \\/ ") or line.startswith(" + ") or line.startswith(" - ") or line.startswith(" ! ") or line.startswith(" ~ ") or line.startswith(" #! ") or line.startswith(" /\\ "):

                                    if zmiana:
                                        zmiany.append(zmiana)
                                    zmiana = line
                                else:
                                    zmiana += f"\n{line}"

                            if zmiana:
                                zmiany.append(zmiana)

                            limit = 16  # Maksymalna liczba zmian do wyświetlenia
                            ilosc_zmian = 0
                            numer_zmiany = len(zmiany)
                            for zmiana in zmiany:
                                # if numer_zmiany < limit or ilosc_zmian == limit:
                                if ilosc_zmian == limit:
                                    break
                                label_opis_wersji = tk.Label(
                                    dziennik_zmian_okno, text=f"{numer_zmiany}. {zmiana}", justify="left", anchor="w")
                                label_opis_wersji.pack(fill="x", padx=(20, 0))
                                numer_zmiany -= 1
                                ilosc_zmian += 1

                            # Dopasowanie rozmiaru okna do zawartości
                            dziennik_zmian_okno.update_idletasks()
                            width = dziennik_zmian_okno.winfo_width() + 30
                            height = dziennik_zmian_okno.winfo_height() + 10
                            dziennik_zmian_okno.geometry(
                                f"{width}x{height}+1170+0")
                        else:
                            messagebox.showerror(
                                'Błąd', "Niestety nie można wczytać dziennika błędów. Spróbuj ponownie później")

                    for line in version_online_lines[6:]:
                        label_opis_wersji = tk.Label(
                            informacje_wersji, text=f"{line}", justify="left", anchor="w")
                        label_opis_wersji.pack(fill="x", padx=(20, 0))

                    # Dopasowanie rozmiaru okna do zawartości
                    informacje_wersji.update_idletasks()
                    width = informacje_wersji.winfo_width() + 40
                    height = informacje_wersji.winfo_height() + 35
                    informacje_wersji.geometry(f"{width}x{height}+1170+0")
                    informacje_wersji.geometry("+1170+0")

                    informacje_wersji.protocol(
                        "WM_DELETE_WINDOW", zamknij_okno)
                    informacje_wersji.bind(
                        "<Map>", lambda event: otworz_okno())

                    button_dziennik_b = tk.Button(
                        informacje_wersji, text=f"Pełen dziennik (ostatni wpis: {dziennik_z_online_lines[0]})", command=dziennik_zmian)
                    button_dziennik_b.pack()

                    informacje_wersji.mainloop()
                else:
                    messagebox.showerror("Błąd", "To okno jest już otwarte!")
            else:
                blad_poczatkowe()
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
                    "Błąd", 'Zapytaj twórcę programu o informacje')

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
                        "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za program   ")
            else:
                messagebox.showwarning(
                    'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                return

            # ustawienia konta
            username = f'{nazwa_uzytkownika}'
            password = f'{token_do_wpisania}'
            repository_name = 'Ksao0/Repozytorium-magnesy-t'
            issue_title = 'Automatyczne zgłoszenie błędu z informacje_o_wersji_utworz_okno()'
            a = traceback.format_exc()
            aktualna_data_czas = datetime.datetime.now()
            format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
            issue_body = f"Data: {format_data_czas} Błąd funkcji informacje_o_wersji_utworz_okno():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}  \nTraceback:\n\n{a}"

            # autentykacja
            g = Github(username, password)

            # pobierz repozytorium
            repo = g.get_repo(repository_name)

            # utwórz nowe zgłoszenie błędu
            repo.create_issue(title=issue_title, body=issue_body)

            messagebox.showinfo("Problem został zgłoszony",
                                "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
            exit()
    else:
        ukrywanie_bledu()


def edycja_kosztow():
    try:
        global file_path_ikonka

        global okno_edycja_kosztow_otwarte
        global okno_problemu_otwarte

        def otworz_okno():
            global okno_edycja_kosztow_otwarte
            okno_edycja_kosztow_otwarte = 1

        def zamknij_okno():
            global okno_edycja_kosztow_otwarte
            okno_edycja_kosztow_otwarte = 0
            okno_zmiany.destroy()

        if okno_edycja_kosztow_otwarte == 0:
            if not okno_problemu_otwarte == 0:
                okno_zmiany = tk.Toplevel()
                okno_zmiany.title("Zmiana kosztów")
                okno_zmiany.geometry("370x300+1170+510")
                okno_zmiany.iconbitmap(file_path_ikonka)
            else:
                okno_zmiany = tk.Toplevel()
                okno_zmiany.title("Zmiana kosztów")
                okno_zmiany.geometry("370x300+800+510")
                okno_zmiany.iconbitmap(file_path_ikonka)

            okno_zmiany.protocol("WM_DELETE_WINDOW", zamknij_okno)
            okno_zmiany.bind("<Map>", lambda event: otworz_okno())

            def edycja_kosztow_wczytaj():
                ceny_tektura = str(entry_cena_tektura.get())
                ceny_nadruk = str(entry_cena_nadruk.get())
                ceny_foliamg = str(entry_cena_foliamg.get())
                ceny_woreczkipp = str(entry_cena_woreczkipp.get())

                path = os.path.join(os.getcwd(), "Ceny.txt")

                if os.path.exists(path):
                    os.remove(path)

                with open("Ceny.txt", "a", encoding='utf-8') as plik:
                    plik.write(ceny_tektura)
                    plik.write('\n')
                    plik.write(ceny_nadruk)
                    plik.write('\n')
                    plik.write(ceny_foliamg)
                    plik.write('\n')
                    plik.write(ceny_woreczkipp)
                if not os.path.isfile("Ceny.txt"):
                    open("Ceny.txt", "w", encoding='utf-8').close()
                    plik.write(ceny_tektura)
                    plik.write('\n')
                    plik.write(ceny_nadruk)
                    plik.write('\n')
                    plik.write(ceny_foliamg)
                    plik.write('\n')
                    plik.write(ceny_woreczkipp)

            def edycja_kosztow_domyslna():
                ceny_tektura = str(entry_cena_tektura.get())
                ceny_nadruk = str(entry_cena_nadruk.get())
                ceny_foliamg = str(entry_cena_foliamg.get())
                ceny_woreczkipp = str(entry_cena_woreczkipp.get())

                path = os.path.join(os.getcwd(), "Ceny.txt")

                if os.path.exists(path):
                    os.remove(path)

                with open("Ceny.txt", "a", encoding='utf-8') as plik:
                    plik.write('13')
                    plik.write('\n')
                    plik.write('35')
                    plik.write('\n')
                    plik.write('18')
                    plik.write('\n')
                    plik.write('11')
                if not os.path.isfile("Ceny.txt"):
                    open("Ceny.txt", "w", encoding='utf-8').close()
                    plik.write('13')
                    plik.write('\n')
                    plik.write('35')
                    plik.write('\n')
                    plik.write('18')
                    plik.write('\n')
                    plik.write('11')

            # ścieżka do pliku Ceny.txt w bieżącym folderze
            path = os.path.join(os.getcwd(), "Ceny.txt")

            # zapisz zawartość pliku Ceny.txt do zmiennej teraz_ceny
            if os.path.exists(path):
                with open(path, "r", encoding='utf-8') as f:
                    teraz_ceny = f.read()
                if not os.path.isfile("Ceny.txt"):
                    open("Ceny.txt", "w", encoding='utf-8').close()
                    f.write('13')
                    f.write('35')
                    f.write('18')
                    f.write('11')
            else:
                teraz_ceny = "13\n35\n18\n11"

            ceny_tektura = round(float(teraz_ceny.split('\n')[0]), 2)
            if ceny_tektura == '' or ceny_tektura == 201:
                ceny_tektura = 13
            ceny_nadruk = round(float(teraz_ceny.split('\n')[1]), 2)
            if ceny_nadruk == '' or ceny_nadruk == 201:
                ceny_nadruk = 35
            ceny_foliamg = round(float(teraz_ceny.split('\n')[2]), 2)
            if ceny_foliamg == '' or ceny_foliamg == 201:
                ceny_foliamg = 18
            ceny_woreczkipp = round(float(teraz_ceny.split('\n')[3]), 2)
            if ceny_woreczkipp == '' or ceny_woreczkipp == 201:
                ceny_woreczkipp = 11

            label_tektura = tk.Label(
                okno_zmiany, text=f"Aktualna cena za tekturę: {ceny_tektura}zł,    Domyślna: 13,00zł".rjust(50))
            label_tektura.pack()
            label_nadruk = tk.Label(
                okno_zmiany, text=f"Aktualna cena za nadruk: {ceny_nadruk}zł,    Domyślna: 35,00zł".rjust(50))
            label_nadruk.pack()
            label_foliamg = tk.Label(
                okno_zmiany, text=f"Aktualna cena za folię: {ceny_foliamg}zł,    Domyślna: 18,00zł".rjust(50))
            label_foliamg.pack()
            label_woreczkipp = tk.Label(
                okno_zmiany, text=f"Aktualna cena za woreczki: {ceny_woreczkipp}zł,    Domyślna: 11,00zł".rjust(50))
            label_woreczkipp.pack()

            label_cena_tektura = tk.Label(
                okno_zmiany, text="Zmiana ceny za tekturę:")
            label_cena_tektura.pack()
            entry_cena_tektura = tk.Entry(okno_zmiany)
            entry_cena_tektura.pack()

            label_cena_nadruk = tk.Label(
                okno_zmiany, text="Zmiana ceny za nadruk:")
            label_cena_nadruk.pack()
            entry_cena_nadruk = tk.Entry(okno_zmiany)
            entry_cena_nadruk.pack()

            label_cena_foliamg = tk.Label(
                okno_zmiany, text="Zmiana ceny za folię:")
            label_cena_foliamg.pack()
            entry_cena_foliamg = tk.Entry(okno_zmiany)
            entry_cena_foliamg.pack()

            label_cena_woreczkipp = tk.Label(
                okno_zmiany, text="Zmiana ceny za woreczki:")
            label_cena_woreczkipp.pack()
            entry_cena_woreczkipp = tk.Entry(okno_zmiany)
            entry_cena_woreczkipp.pack()

            pustka = tk.Label(okno_zmiany)
            pustka.pack()

            edycja = tk.Frame(okno_zmiany)
            edycja.pack()

            button_zmien = tk.Button(
                edycja, text="Zapisz zmiany", command=edycja_kosztow_wczytaj)
            button_zmien.pack(side=tk.LEFT)

            button_zmien_domyslne = tk.Button(
                edycja, text="Wczytaj domyślne", command=edycja_kosztow_domyslna)
            button_zmien_domyslne.pack(side=tk.RIGHT)
            okno_zmiany.mainloop()
        else:
            messagebox.showerror("Błąd", "To okno jest już otwarte!")
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
                "Błąd", 'Zapytaj twórcę programu o informacje')

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
                    "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
        else:
            messagebox.showwarning(
                'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
            return

        # ustawienia konta
        username = f'{nazwa_uzytkownika}'
        password = f'{token_do_wpisania}'
        repository_name = 'Ksao0/Repozytorium-magnesy-t'
        issue_title = 'Automatyczne zgłoszenie błędu z edycja_kosztow()'
        a = traceback.format_exc()
        aktualna_data_czas = datetime.datetime.now()
        format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
        issue_body = f"Data: {format_data_czas} Błąd funkcji edycja_kosztow():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


def oblicz_zyski():
    try:
        # Ścieżka do pliku Aktualizator_aktualizatora.py w bieżącym folderze
        path = os.path.join(os.getcwd(), "Aktualizator_aktualizatora.py")

        # Usuń plik Aktualizator_aktualizatora.py, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
        # Pobierz plik Aktualizator_aktualizatora.py z repozytorium
        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Aktualizator_aktualizatora.py"
        urllib.request.urlretrieve(url, path)

        # Sprawdzenie, czy plik istnieje i ewentualne jego utworzenie
        if not os.path.isfile("Zapisy.txt"):
            open("Zapisy.txt", "w", encoding='utf-8').close()

        liczba_pakietow = float(entry_pakietow.get())
        if not liczba_pakietow.is_integer():
            messagebox.showerror(
                "Błąd", "Liczba pakietów nie może być liczbą z przecinkiem")
        if liczba_pakietow <= 0:
            messagebox.showerror("Błąd", "Liczba pakietów musi być dodatnia")
            return

        cena_za_magnes = float(entry_ceny.get().replace(",", "."))

        if cena_za_magnes <= 0:
            messagebox.showerror("Błąd", "Cena za magnes musi być dodatnia")
            return

        now = datetime.datetime.now()

        data_obliczenia = now.strftime("%d.%m.%Y %H:%M:%S")

        # Liczenie kosztów

        # # Pobieranie kosztów z pliku
        path = os.path.join(os.getcwd(), "Ceny.txt")

        # zapisz zawartość pliku Ceny.txt do zmiennej teraz_ceny
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                teraz_ceny = f.read()
        else:
            teraz_ceny = "13\n35\n18\n11"

        ceny_tektura = round(float(teraz_ceny.split('\n')[0]), 2)
        ceny_nadruk = round(float(teraz_ceny.split('\n')[1]), 2)
        ceny_foliamg = round(float(teraz_ceny.split('\n')[2]), 2)
        ceny_woreczkipp = round(float(teraz_ceny.split('\n')[3]), 2)

        magnesy_w_pakiecie = liczba_pakietow * 224
        cena_za_pakiet = cena_za_magnes * 224
        razem = cena_za_pakiet * liczba_pakietow

        tektura = ceny_tektura * liczba_pakietow
        nadruk = ceny_nadruk * liczba_pakietow
        foliamg = ceny_foliamg * liczba_pakietow
        woreczkipp = ceny_woreczkipp * liczba_pakietow

        koszty = tektura + nadruk + foliamg + woreczkipp
        bilans = razem - koszty

        wyniki = f"Data: {data_obliczenia}\n\nLiczba pakietów: {liczba_pakietow} szt.\nLiczba magnesów: {magnesy_w_pakiecie} szt.\nCena za 1 magnes: {cena_za_magnes:.2f} zł\nJeden pakiet to: {cena_za_pakiet:.2f} zł\nKoszty: {koszty:.2f} zł\nZysk sprzedaży: {bilans:.2f} zł\nCena za wszystkie pakiety: {razem:.2f} zł\n\n"
        label_wyniki.configure(text=wyniki.rjust(200))

        if bilans < 0:
            messagebox.showwarning(
                'To się nie opłaca', f"Na tej transakcji stracisz pieniądze!\nBilans: {bilans:.2f}zł\nPoniesione koszty (za jeden pakiet):\nTektura: {ceny_tektura}zł\nNadruk: {ceny_nadruk}zł\nFolia magnetyczna: {ceny_foliamg}zł\nWoreczki: {woreczkipp}zł")

        # Zapis wyników do pliku, jeśli zmienna zapis_do_pliku jest ustawiona na True

        # ścieżka do pliku Zapisy.txt w bieżącym folderze
        path = os.path.join(os.getcwd(), "Zapisy.txt")

        # zapisz zawartość pliku Zapisy.txt do zmiennej stare_zapisy
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as f:
                stare_zapisy = f.read()
        else:
            stare_zapisy = ""

        # usuń plik Zapisy.txt, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
            # print("Usunięto plik Zapisy.txt")

        if zapis_do_pliku.get():
            with open("Zapisy.txt", "a", encoding='utf-8') as plik:
                plik.write(wyniki)
                plik.write(stare_zapisy)
            if not os.path.isfile("Zapisy.txt"):
                open("Zapisy.txt", "w", encoding='utf-8').close()
                plik.write(wyniki)
                plik.write(stare_zapisy)
    except Exception as e:
        if messagebox.askyesno("Zgłaszanie błędu", "Czy wpisane dane są prawidłowe (są liczbą i nie zawierają liter)?"):
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
                    "Błąd", 'Zapytaj twórcę programu o informacje')

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
                        "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj, jak najszybciej zgłoś się do osoby odpowiedzialnej za program   ")
            else:
                messagebox.showwarning(
                    'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                return

            # ustawienia konta
            username = f'{nazwa_uzytkownika}'
            password = f'{token_do_wpisania}'
            repository_name = 'Ksao0/Repozytorium-magnesy-t'
            issue_title = 'Automatyczne zgłoszenie błędu z oblicz_zyski()'
            a = traceback.format_exc()
            aktualna_data_czas = datetime.datetime.now()
            format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
            issue_body = f"Data: {format_data_czas} Błąd funkcji oblicz_zyski():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

            # autentykacja
            g = Github(username, password)

            # pobierz repozytorium
            repo = g.get_repo(repository_name)

            # utwórz nowe zgłoszenie błędu
            repo.create_issue(title=issue_title, body=issue_body)

            messagebox.showinfo("Problem został zgłoszony",
                                "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
            exit()
        else:
            messagebox.showinfo("Błąd leży po twojej stronie",
                                "Błąd, który wystąpił jest spowodowany twoją niedokładnością. Jego przyczyną jest wpisanie liczb typu 7.g5 czy 7,k Wykonaj obliczenia wpisując poprawne dane")


# Tworzenie głównego okna
if internet == 1:
    if blokada_bledu == True:
        # pobierz zawartość pliku version.txt z repozytorium na GitHub
        url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt'
        response = requests.get(url)

        version_online = response.content.decode('utf-8').strip()

        # odczytaj zawartość pliku version.txt w twoim programie
        path = os.path.join(os.getcwd(), "version.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                version_local = f.read().strip()
        else:
            version_local = "BRAK DANYCH"
        if version_local != "BRAK DANYCH":
            # wyświetl tylko pierwszą linijkę wersji
            version_local_first_line = version_local.split('\n')[0]
            version_online_first_line = version_online.split('\n')[0]
            version_local_pop_line = version_local.split('\n')[2]
            version_online_pop_line = version_online.split('\n')[2]

            # 100% Kł:
            version_local_pop_line = version_local.split('\n')[2]
            # odczytaj zawartość pliku version.txt w twoim programie
            path = os.path.join(os.getcwd(), "version.txt")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    version_local = f.read().strip()
            else:
                version_local = "BRAK DANYCH"
            wersja = version_local_first_line

            # wyświetl tylko pierwszą linijkę wersji kłamstwo
            version_local_first_line = version_local.split('\n')[0]

            version_local_pop_line = version_local.split('\n')[2]

            # pobierz zawartość pliku version.txt z repozytorium na GitHub
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Komunikat_yN.txt'
            response = requests.get(url)

            Komunikat_yN = response.content.decode('utf-8').split('\n')
            Komunikat_yN_first_line = response.content.decode(
                'utf-8').split('\n')[0]
            # porównaj wersje kłamstwo
            print(Fore.LIGHTMAGENTA_EX +
                  f'\nWersja na komputerze: {version_local_first_line}\nStatus: ' + Fore.LIGHTBLACK_EX + 'yN')
            print(Fore.CYAN +
                  f'Wersja w repozytorium: {version_online_first_line}\nStatus: ' + Fore.RED + 'yN')
            print(Fore.CYAN +
                  f'\nPole informacyjne (automatyczne): ' + Fore.RED + 'Błąd prawdopodobnie krytyczny\nPrace nad naprawą błędu wciąż trwają. Dokładne informacje znajdziesz w polu opis precyzyjny.\nZalecamy, abyś nie korzystał z opcji dodatkowych (przycisk "Więcej opcji") oraz eksperymentalnych\nDokładne informacje w komunikacie precyzyjnym' + Style.    RESET_ALL)

            print(Fore.RED +
                  f"\nKomunikat precyzyjny: {Komunikat_yN_first_line}")
            for linia in Komunikat_yN[1:]:
                print(Fore.RED + linia)
            print(Style.RESET_ALL)
        else:
            # wyświetl tylko pierwszą linijkę wersji
            version_online_first_line = version_online.split('\n')[0]
            version_online_pop_line = version_online.split('\n')[2]

            # 100% Kł:
            # odczytaj zawartość pliku version.txt w twoim programie
            path = os.path.join(os.getcwd(), "version.txt")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    version_local = f.read().strip()
            else:
                version_local = "BRAK DANYCH"
            wersja = "BRAK DANYCH"

            # pobierz zawartość pliku version.txt z repozytorium na GitHub
            url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Komunikat_yN.txt'
            response = requests.get(url)

            Komunikat_yN = response.content.decode('utf-8').split('\n')
            Komunikat_yN_first_line = response.content.decode(
                'utf-8').split('\n')[0]
            # porównaj wersje kłamstwo
            print(Fore.LIGHTMAGENTA_EX +
                  f'\nWersja na komputerze: ' + Fore.RED + 'Brak danych\n' + Fore.LIGHTMAGENTA_EX+'Status: ' + Fore.LIGHTBLACK_EX + 'yN')
            print(Fore.CYAN +
                  f'Wersja w repozytorium: {version_online_first_line}\nStatus: ' + Fore.RED + 'yN')
            print(Fore.CYAN +
                  f'\nPole informacyjne (automatyczne): ' + Fore.RED + 'Błąd prawdopodobnie krytyczny\nPrace nad naprawą błędu wciąż trwają. Dokładne informacje znajdziesz w polu komunikat precyzyjny.\nZalecamy, abyś nie korzystał z opcji dodatkowych (przycisk "Więcej opcji") oraz eksperymentalnych\nDokładne informacje w opisie precyzyjnym' + Style.    RESET_ALL)

            print(Fore.RED +
                  f"\nOpis precyzyjny: {Komunikat_yN_first_line}")
            for linia in Komunikat_yN[1:]:
                print(Fore.RED + linia)
            print(Style.RESET_ALL)
    elif blokada_klamstwa == True:
        # odczytaj zawartość pliku version.txt w twoim programie
        path = os.path.join(os.getcwd(), "version.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                version_local = f.read().strip()
        else:
            version_local = "BRAK DANYCH"

        version_local_pop_line = version_local.split('\n')[2]

        # wyświetl tylko pierwszą linijkę wersji kłamstwo
        version_local_first_line = version_local.split('\n')[0]

        version_local_pop_line = version_local.split('\n')[2]
        wersja = version_local_first_line

        # porównaj wersje kłamstwo
        print(Fore.LIGHTMAGENTA_EX +
              f'\nWersja na komputerze: {version_local_first_line}\nStatus: ' + Fore.LIGHTBLACK_EX + 'yN' + Fore.LIGHTMAGENTA_EX)
        print(Fore.CYAN +
              f'Wersja w repozytorium: {version_local_first_line}\nStatus: ' + Fore.RED + 'yN' + Fore.LIGHTMAGENTA_EX)
        print(Fore.CYAN +
              f'\nOpis najnowszej wersji (repozytorium): {version_local}' + Style.RESET_ALL)
    else:
        # pobierz zawartość pliku version.txt z repozytorium na GitHub
        url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt'
        response = requests.get(url)

        version_online = response.content.decode('utf-8').strip()

        # odczytaj zawartość pliku version.txt w twoim programie
        path = os.path.join(os.getcwd(), "version.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                version_local = f.read().strip()
        else:
            version_local = "BRAK DANYCH"

        # wyświetl tylko pierwszą linijkę wersji
        version_local_first_line = version_local.split('\n')[0]
        version_online_first_line = version_online.split('\n')[0]

        version_local_pop_line = version_local.split('\n')[2]
        version_online_pop_line = version_online.split('\n')[2]

        # porównaj wersje
        print(Fore.LIGHTMAGENTA_EX +
              f'\nWersja na komputerze: {version_local_first_line}\n{version_local_pop_line}')
        print(Fore.CYAN +
              f'Wersja w repozytorium: {version_online_first_line}\n{version_online_pop_line}')
        print(Fore.CYAN +
              f'\nOpis najnowszej wersji (repozytorium): {version_online}' + Style.RESET_ALL)
        if version_local != "BRAK DANYCH":
            if version_online.strip() == version_local.strip():
                if version_local_pop_line == version_online_pop_line:
                    print(Fore.GREEN + 'Masz najnowszą wersję programu.')
                    path = os.path.join(os.getcwd(), "version.txt")
                    if os.path.exists(path):
                        with open(path, "r", encoding="utf-8") as f:
                            version_local = f.readline().strip()
                    wersja = version_local_first_line
                else:
                    if blokada_bledu == False:
                        print(Fore.RED + 'Dostępna jest nowa wersja')
                        wersja = 'DOSTĘPNA NOWA WERSJA'
                    else:
                        print(Fore.GREEN + 'Masz najnowszą wersję programu.')
                        path = os.path.join(os.getcwd(), "version.txt")
                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                version_local = f.readline().strip()
                        wersja = version_local_first_line
            else:
                if version_local_first_line == version_online_first_line:
                    print(Fore.GREEN + 'Masz najnowszą wersję programu.')
                    wersja = version_local_first_line
                    # ścieżka do pliku version.txt w bieżącym folderze
                    path = os.path.join(os.getcwd(), "version.txt")

                    # usuń plik version.txt, jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                    # print("Usunięto plik version.txt")

                    # pobierz plik version.txt z repozytorium i utwórz go
                    url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/version.txt"
                    urllib.request.urlretrieve(url, path)
                else:
                    if blokada_bledu == False:
                        print(Fore.RED + 'Dostępna jest nowa wersja')
                        wersja = 'DOSTĘPNA NOWA WERSJA'
                    else:
                        print(Fore.GREEN + 'Masz najnowszą wersję programu.')
                        path = os.path.join(os.getcwd(), "version.txt")
                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                version_local = f.readline().strip()
                        wersja = version_local_first_line

        else:
            print(
                '\n\nWykryto brak niektórych plików. Zaktualizuj program, aby działał prawidłowo')
            wersja = "ZAKTUALIZUJ PROGRAM"
    root = tk.Tk()
    root.title(f"Kalkulator zysków ver. {wersja}")
    root.geometry("410x350+250+200")
    zapis_do_pliku = tk.BooleanVar()
    zapis_do_pliku.set(True)

    # Utworzenie folderu "rei", jeśli nie istnieje
    folder_path = "rei"

    # Usunięcie folderu "rei" wraz z jego zawartością, jeśli istnieje
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Pobranie ikony z repozytorium GitHub
    url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/ikona_magnesy.ico'
    file_path_ikonka = os.path.join(folder_path, 'ikona_magnesy.ico')
    urllib.request.urlretrieve(url, file_path_ikonka)

    # Przeskalowanie ikony na rozmiar 32x32
    img = Image.open(file_path_ikonka)
    img = img.resize((32, 32), Image.LANCZOS)
    resized_file_path = os.path.join(folder_path, 'resized_ikona_magnesy.ico')
    img.save(resized_file_path)

    # Zaktualizowanie globalnej zmiennej file_path_ikonka
    file_path_ikonka = resized_file_path

    # Ustawienie ikonki
    root.iconbitmap(file_path_ikonka)

# Przeskalowanie ikony do rozmiaru 32x32
# icon = Image.open(icon_path)
# icon = icon.resize((32, 32), Image.ANTIALIAS)

# Przypisanie przeskalowanej ikony jako ikony aplikacji
# root.iconphoto(True, ImageTk.PhotoImage(icon))

else:
    root = tk.Tk()
    root.title(f"Kalkulator zysków")
    root.geometry("410x350")
    zapis_do_pliku = tk.BooleanVar()
    zapis_do_pliku.set(True)


# Dodatkowe pytania itp. od twórcy programu będą wyświetlane tutaj, treść ustalaj na początku kodu
if dodatkowe_od_tworcy != None:
    print(Fore.LIGHTBLUE_EX + f"{dodatkowe_od_tworcy}")


def otworz_okno_zapisy():
    global file_path_ikonka
    try:
        # Utworzenie folderu "rei", jeśli nie istnieje
        folder_path = "rei"

        # Usunięcie folderu "rei" wraz z jego zawartością, jeśli istnieje
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Pobranie ikony z repozytorium GitHub
        url = 'https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/ikona_magnesy.ico'
        file_path_ikonka = os.path.join(folder_path, 'ikona_magnesy.ico')
        urllib.request.urlretrieve(url, file_path_ikonka)

        path = os.path.join(os.getcwd(), "Zapisy.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                zawartosc = f.read().strip()
        else:
            zawartosc = ''

        # Tworzenie nowego okna
        okno_zapisy = tk.Toplevel()
        okno_zapisy.title("Historia")
        okno_zapisy.geometry("800x900")
        okno_zapisy.grab_set()
        okno_zapisy.iconbitmap(file_path_ikonka)

        # Dodanie elementu ScrolledText
        pole_tekstowe = scrolledtext.ScrolledText(okno_zapisy, wrap=tk.WORD)
        pole_tekstowe.pack(expand=True, fill=tk.BOTH)

        # Wstawienie zawartości pliku do elementu ScrolledText
        pole_tekstowe.insert(tk.END, zawartosc)
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
                "Błąd", 'Zapytaj twórcę programu o informacje')

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
                    "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
        else:
            messagebox.showwarning(
                'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
            return

        # ustawienia konta
        username = f'{nazwa_uzytkownika}'
        password = f'{token_do_wpisania}'
        repository_name = 'Ksao0/Repozytorium-magnesy-t'
        issue_title = 'Automatyczne zgłoszenie błędu z otworz_okno_zapisy()'
        a = traceback.format_exc()
        aktualna_data_czas = datetime.datetime.now()
        format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
        issue_body = f"Data: {format_data_czas} Błąd funkcji otworz_okno_zapisy():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


def Opcje_eksperymentalne(okno_wyborowe):
    global token_zaufania
    if token_zaufania == True:
        global blokada_bledu
        if blokada_bledu == False:
            # Tworzenie nowego okna dialogowego
            dialog = tk.Toplevel(okno_wyborowe)
            dialog.title("Wybierz opcję")

            def opcja_1():
                aplikacja_Android()
                dialog.destroy()

            def opcja_2():
                moi_klienci()
                dialog.destroy()

            label_info = tk.Label(
                dialog, text="Opcje eksperymentalne to opcje, które dopiero powstały, są funkcjonalne, ale będą zmieniane")
            label_info.pack()

            button_opcja_1 = tk.Button(
                dialog, text="Zainstaluj/aktualizuj aplkację na telefon", command=opcja_1)
            button_opcja_2 = tk.Button(
                dialog, text="Dane o klientach", command=opcja_2)

            button_opcja_1.pack()
            button_opcja_2.pack()

            def aplikacja_Android():
                try:
                    global internet
                    # Aktualizacja

                    # ścieżka do w bieżącym folderze
                    path = os.path.join(os.getcwd(), "Androidow.py")

                    # usuń plik, jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                    try:
                        # pobierz plik z repozytorium
                        url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Androidow.py"
                        urllib.request.urlretrieve(url, path)
                        Gra = ["python", "Androidow.py"]
                        subprocess.run(Gra)
                    except:
                        print('Wykryto brak połączenia z internetem')
                        messagebox.showerror(
                            "Błąd", f'Wystąpił błąd połączenia z internetem. Sprawdź połączenie z internetem, a następnie naciśnij ok')
                        internet = 0
                        try:
                            # pobierz plik z repozytorium
                            url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Androidow.py"
                            urllib.request.urlretrieve(url, path)
                            Gra = ["python", "Androidow.py"]
                            subprocess.run(Gra)
                        except:
                            messagebox.showerror(
                                "Błąd", f'Ponownie wystąpił błąd połączenia z internetem. Nie można wykonać uruchomić.')
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
                            "Błąd", 'Zapytaj twórcę programu o informacje')

                    if plik_od_dewelopera != "BRAK PLIKU D":
                        informacje_do_zgloszenia = plik_od_dewelopera.split(
                            '\n')
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
                                "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                            return
                        elif dzisiaj == wygasa_data:
                            messagebox.showwarning(
                                "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                    else:
                        messagebox.showwarning(
                            'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
                        return

                    # ustawienia konta
                    username = f'{nazwa_uzytkownika}'
                    password = f'{token_do_wpisania}'
                    repository_name = 'Ksao0/Repozytorium-magnesy-t'
                    issue_title = 'Automatyczne zgłoszenie błędu z Opcje_eksperymentalne()'
                    a = traceback.format_exc()
                    aktualna_data_czas = datetime.datetime.now()
                    format_data_czas = aktualna_data_czas.strftime(
                        "%d.%m.%Y %H:%M")
                    issue_body = f"Data: {format_data_czas} Błąd funkcji Opcje_eksperymentalne():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value }   \nTraceback:\n\n{a}"

                    # autentykacja
                    g = Github(username, password)

                    # pobierz repozytorium
                    repo = g.get_repo(repository_name)

                    # utwórz nowe zgłoszenie błędu
                    repo.create_issue(title=issue_title, body=issue_body)

                    messagebox.showinfo("Problem został zgłoszony",
                                        "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
                    exit()

            def moi_klienci():

                def create_client_file(name, city, phone, additional_info):
                    folder = "klienci"
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                    file_path = os.path.join(folder, f"KLIENT.{name}.txt")
                    with open(file_path, "w") as file:
                        file.write(
                            f"{name}\n{city}\n{phone}\n{additional_info}")

                def delete_client_file(name):
                    client_name, client_city = name.split(" - ")
                    client_file_prefix = f"KLIENT.{client_name}"

                    # Usuń pliki klienta
                    folder = "klienci"
                    for file in os.listdir(folder):
                        if file.startswith(client_file_prefix):
                            file_path = os.path.join(folder, file)
                            if os.path.exists(file_path):
                                os.remove(file_path)

                    # Usuń plik historii klienta, jeśli istnieje
                    history_file_path = f"klienci/KLIENT_HISTORIA.{client_name} - {client_city}.txt"
                    if os.path.exists(history_file_path):
                        os.remove(history_file_path)

                def load_clients_list():
                    folder = "klienci"
                    clients_list.delete(0, tk.END)
                    if not os.path.exists(folder):
                        return

                    client_names = []

                    for file in os.listdir(folder):
                        if file.startswith("KLIENT.") and file.endswith(".txt"):
                            client_name = file.split(".")[1]
                            client_names.append(client_name)

                    client_names.sort()  # Sortuj nazwy klientów alfabetycznie

                    for client_name in client_names:
                        client_file_path = os.path.join(
                            folder, f"KLIENT.{client_name}.txt")
                        with open(client_file_path, "r") as client_file:
                            client_data = client_file.read().splitlines()
                        if len(client_data) >= 2:
                            client_city = client_data[1]
                        else:
                            client_city = "Brak danych o miejscowości"
                        clients_list.insert(
                            tk.END, f"{client_name} - {client_city}")

                def obliczenia(liczba_pakietow, cena_za_magnes, selected_client):

                    # Zamiana na liczbę zmiennoprzecinkową
                    if not liczba_pakietow.is_integer():
                        messagebox.showerror(
                            "Błąd", "Liczba pakietów nie może być liczbą z przecinkiem")
                    if liczba_pakietow <= 0:
                        messagebox.showerror(
                            "Błąd", "Liczba pakietów musi być dodatnia")
                        return

                    if cena_za_magnes <= 0:
                        messagebox.showerror(
                            "Błąd", "Cena za magnes musi być dodatnia")
                        return

                    now = datetime.datetime.now()

                    data_obliczenia = now.strftime(
                        "%d.%m.%Y %H:%M:%S")

                    # Liczenie kosztów

                    # # Pobieranie kosztów z pliku
                    path = os.path.join(os.getcwd(), "Ceny.txt")

                    # zapisz zawartość pliku Ceny.txt do zmiennej teraz_ceny
                    if os.path.exists(path):
                        with open(path, "r", encoding='utf-8') as f:
                            teraz_ceny = f.read()
                    else:
                        teraz_ceny = "13\n35\n18\n11"

                    ceny_tektura = round(
                        float(teraz_ceny.split('\n')[0]), 2)
                    ceny_nadruk = round(
                        float(teraz_ceny.split('\n')[1]), 2)
                    ceny_foliamg = round(
                        float(teraz_ceny.split('\n')[2]), 2)
                    ceny_woreczkipp = round(
                        float(teraz_ceny.split('\n')[3]), 2)

                    magnesy_w_pakiecie = liczba_pakietow * 224
                    cena_za_pakiet = cena_za_magnes * 224
                    razem = cena_za_pakiet * liczba_pakietow

                    tektura = ceny_tektura * liczba_pakietow
                    nadruk = ceny_nadruk * liczba_pakietow
                    foliamg = ceny_foliamg * liczba_pakietow
                    woreczkipp = ceny_woreczkipp * liczba_pakietow

                    koszty = tektura + nadruk + foliamg + woreczkipp
                    bilans = razem - koszty

                    wyniki_a = f"Data: {data_obliczenia}\n\nLiczba pakietów: {liczba_pakietow} szt.\nLiczba magnesów: {magnesy_w_pakiecie} szt.\nCena za 1 magnes: {cena_za_magnes:.2f} zł\nJeden pakiet to: {cena_za_pakiet:.2f} zł\nKoszty: {koszty:.2f} zł\nZysk sprzedaży: {bilans:.2f} zł\nCena za wszystkie pakiety: {razem:.2f} zł\n\n"

                    history_file_path = f"klienci/KLIENT_HISTORIA.{selected_client}.txt"

                    # Pobranie starej zawartości pliku historii
                    old_history = ""
                    if os.path.exists(history_file_path):
                        with open(history_file_path, "r") as history_file:
                            old_history = history_file.read()

                    # Zapis nowego wpisu do pliku historii
                    with open(history_file_path, "w") as history_file:
                        history_file.write(f"{wyniki_a}\n{old_history}")

                def show_client_info():
                    selected_client = clients_list.get(tk.ACTIVE)
                    if selected_client:
                        okno_rozwin_klienta = tk.Toplevel(okno_glowne_klientow)
                        okno_rozwin_klienta.title(selected_client)

                        # Ustawienie modality, aby wyłączyć możliwość używania innych okien
                        okno_rozwin_klienta.transient(okno_glowne_klientow)
                        # okno_rozwin_klienta.grab_set()

                        label_pakietow = tk.Label(
                            okno_rozwin_klienta, text="Liczba magnesów:")
                        label_pakietow.pack()
                        entry_pakietow_klient = tk.Entry(okno_rozwin_klienta)
                        entry_pakietow_klient.pack()

                        label_ceny = tk.Label(
                            okno_rozwin_klienta, text="Cena za magnes:")
                        label_ceny.pack()
                        entry_ceny_klient = tk.Entry(okno_rozwin_klienta)
                        entry_ceny_klient.pack()

                        def dodaj_do_klienta():
                            pakietow = entry_pakietow_klient.get()
                            cena = entry_ceny_klient.get()

                            if not pakietow or not cena:
                                messagebox.showerror(
                                    "Błąd", "Wszystkie pola muszą być wypełnione.")
                                return

                            try:
                                # Zamiana na liczbę zmiennoprzecinkową
                                liczba_pakietow = float(pakietow)
                            except ValueError:
                                messagebox.showerror(
                                    "Błąd", "Niepoprawna wartość liczby pakietów.")
                                return

                            try:
                                # Zamiana na liczbę zmiennoprzecinkową
                                cena_za_magnes = float(cena.replace(",", "."))
                            except ValueError:
                                messagebox.showerror(
                                    "Błąd", "Niepoprawna wartość ceny za magnes.")
                                return

                            obliczenia(liczba_pakietow,
                                       cena_za_magnes, selected_client)

                        def pokaz_historie_klienta():
                            history_file_path = f"klienci/KLIENT_HISTORIA.{selected_client}.txt"
                            if os.path.exists(history_file_path):
                                with open(history_file_path, "r") as history_file:
                                    history_data = history_file.read()

                                # Tworzenie nowego okna
                                okno_historii = tk.Toplevel()
                                okno_historii.title(
                                    f"Historia klienta: {selected_client}")
                                okno_historii.geometry("800x900")
                                okno_historii.iconbitmap(file_path_ikonka)

                                # Dodanie elementu ScrolledText
                                pole_tekstowe = scrolledtext.ScrolledText(
                                    okno_historii, wrap=tk.WORD)
                                pole_tekstowe.pack(expand=True, fill=tk.BOTH)

                                # Wstawienie zawartości historii do elementu ScrolledText
                                pole_tekstowe.insert(tk.END, history_data)

                        frame_przyciski = tk.Frame(okno_rozwin_klienta)
                        frame_przyciski.pack()

                        button_dodaj = tk.Button(
                            frame_przyciski, text="Dodaj", command=dodaj_do_klienta)
                        button_dodaj.pack(side=tk.LEFT)

                        button_historia = tk.Button(
                            frame_przyciski, text="Historia z klientem", command=pokaz_historie_klienta)
                        button_historia.pack(side=tk.LEFT)

                def edit_client_info():
                    selected_client = clients_list.get(tk.ACTIVE)
                    if selected_client:
                        client_name = selected_client.split(" - ")[0]
                        client_file_path = f"klienci/KLIENT.{client_name}.txt"

                        if os.path.exists(client_file_path):
                            with open(client_file_path, "r") as client_file:
                                client_data = client_file.read().splitlines()

                            okno_edytuj_klienta = tk.Toplevel(
                                okno_glowne_klientow)
                            okno_edytuj_klienta.title(
                                f"Edycja danych klienta: {selected_client}")

                            okno_edytuj_klienta.transient(okno_glowne_klientow)

                            label_name = tk.Label(
                                okno_edytuj_klienta, text="Nazwa klienta*:")
                            label_name.pack()
                            entry_name = tk.Entry(okno_edytuj_klienta)
                            entry_name.pack()
                            entry_name.insert(0, client_data[0])

                            label_city = tk.Label(
                                okno_edytuj_klienta, text="Miejscowość*:")
                            label_city.pack()
                            entry_city = tk.Entry(okno_edytuj_klienta)
                            entry_city.pack()
                            entry_city.insert(0, client_data[1])

                            label_phone = tk.Label(
                                okno_edytuj_klienta, text="Telefon:")
                            label_phone.pack()
                            entry_phone = tk.Entry(okno_edytuj_klienta)
                            entry_phone.pack()

                            if len(client_data) >= 3:
                                entry_phone.insert(0, client_data[2])

                            label_additional_info = tk.Label(
                                okno_edytuj_klienta, text="Informacje dodatkowe:")
                            label_additional_info.pack()
                            entry_additional_info = tk.Entry(
                                okno_edytuj_klienta)
                            entry_additional_info.pack()

                            if len(client_data) >= 4:
                                entry_additional_info.insert(0, client_data[3])

                            def save_edited_client():
                                name = entry_name.get()
                                if not name:
                                    messagebox.showerror(
                                        "Błąd", "Nazwa klienta jest wymagana.")
                                    return
                                city = entry_city.get()
                                if not city:
                                    messagebox.showerror(
                                        "Błąd", "Miejscowość klienta jest wymagana.")
                                    return
                                phone = entry_phone.get()
                                additional_info = entry_additional_info.get()

                                with open(client_file_path, "w") as client_file:
                                    client_file.write(
                                        f"{name}\n{city}\n{phone}\n{additional_info}")
                                okno_edytuj_klienta.destroy()
                                load_clients_list()

                            button_save = tk.Button(
                                okno_edytuj_klienta, text="Zapisz zmiany", command=save_edited_client)
                            button_save.pack()

                def new_client():
                    top = tk.Toplevel(okno_glowne_klientow)
                    top.title("Nowy klient")
                    top.geometry("210x250+250+200")

                    top.transient(okno_glowne_klientow)

                    label_name = tk.Label(top, text="Nazwa klienta*:")
                    label_name.pack()
                    entry_name = tk.Entry(top)
                    entry_name.pack()

                    label_city = tk.Label(top, text="Miejscowość*:")
                    label_city.pack()
                    entry_city = tk.Entry(top)
                    entry_city.pack()

                    label_phone = tk.Label(top, text="Telefon:")
                    label_phone.pack()
                    entry_phone = tk.Entry(top)
                    entry_phone.pack()

                    label_additional_info = tk.Label(
                        top, text="Informacje dodatkowe:")
                    label_additional_info.pack()
                    entry_additional_info = tk.Entry(top)
                    entry_additional_info.pack()

                    def create_new_client():
                        name = entry_name.get()
                        if not name:
                            messagebox.showerror(
                                "Błąd", "Nazwa klienta jest wymagana.")
                            return
                        city = entry_city.get()
                        if not city:
                            messagebox.showerror(
                                "Błąd", "Miejscowość klienta jest wymagana.")
                            return
                        phone = entry_phone.get()
                        additional_info = entry_additional_info.get()

                        create_client_file(name, city, phone, additional_info)
                        top.destroy()
                        load_clients_list()

                    button_create = tk.Button(
                        top, text="Utwórz", command=create_new_client)
                    button_create.pack()

                def delete_client():
                    selected_client = clients_list.get(tk.ACTIVE)
                    if selected_client:
                        response = messagebox.askyesno(
                            "Usuń klienta", f"Czy na pewno chcesz usunąć klienta: {selected_client}?")
                        if response == tk.YES:
                            delete_client_file(selected_client)
                            load_clients_list()

                okno_glowne_klientow = tk.Tk()
                okno_glowne_klientow.title("Lista klientów")
                okno_glowne_klientow.geometry("410x250+250+200")

                button_new_client = tk.Button(
                    okno_glowne_klientow, text="Nowy klient", command=new_client)
                button_new_client.pack(side=tk.LEFT)

                button_edit_client = tk.Button(
                    okno_glowne_klientow, text="Edytuj klienta", command=edit_client_info)
                button_edit_client.pack(side=tk.LEFT)

                button_delete_client = tk.Button(
                    okno_glowne_klientow, text="Usuń klienta", command=delete_client)
                button_delete_client.pack(side=tk.LEFT)

                clients_list = tk.Listbox(okno_glowne_klientow)
                clients_list.pack(side=tk.RIGHT)

                clients_list.bind("<Double-Button-1>",
                                  lambda event: show_client_info())

                load_clients_list()

                okno_glowne_klientow.mainloop()

        else:
            ukrywanie_bledu()
    else:
        token_zaufania_wygasl_f()


def otworz_okno_wybor():
    try:
        global file_path_ikonka
        if blokada_bledu == 0:
            if random.choices([True, False], [0.15, 0.85])[0]:
                ankieta()

        def otworz_okno():
            global okno_wyborowe_otwarte
            okno_wyborowe_otwarte = 1

        def zamknij_okno():
            global okno_wyborowe_otwarte
            okno_wyborowe_otwarte = 0
            okno_wyborowe.destroy()

        if okno_wyborowe_otwarte == 0:
            okno_wyborowe = tk.Toplevel()
            okno_wyborowe.title("Okno wyborowe")
            okno_wyborowe.geometry("370x480+800+0")
            okno_wyborowe.iconbitmap(file_path_ikonka)

            # Dodanie przycisku do nowego okna
            button = tk.Button(okno_wyborowe, text="Aktualizacja (terminal)",
                               command=aktul)
            button.pack()
            label_informacja = tk.Label(
                okno_wyborowe, text="Zaktualizuj program ręcznie i zapisz tę informację do historii.\nMożesz też zmienić wersję programu")
            label_informacja.pack()
            button_wykasuj_zapisy = tk.Button(okno_wyborowe, text="Wykasuj informacje o zapisach",
                                              command=wykasuj_zapisy)
            button_wykasuj_zapisy.pack()
            label_informacja = tk.Label(
                okno_wyborowe, text="Zostaną usunięte informacje o poprzednich oblczeniach.\nTej operacji nie można cofnąć.")
            label_informacja.pack()

            button_zmiana_danych = tk.Button(
                okno_wyborowe, text="Edytuj dane", command=edycja_kosztow)
            button_zmiana_danych.pack()

            label_informacja = tk.Label(
                okno_wyborowe, text="Zmień przyjęte przez program parametry.\nJeśli wystąpią problemy z funkcją: Stwórz plik Ceny.txt\nz zawartością czterech dowolnych cyfr, każda w nowej linii")
            label_informacja.pack()

            button_rozwiaz_problemy = tk.Button(
                okno_wyborowe, text="Rozwiąż problemy (terminal)", command=rozwiaz_problemy)
            button_rozwiaz_problemy.pack()
            label_informacja = tk.Label(
                okno_wyborowe, text="Program wykona czynność podobną do resetu.\nWszystkie dane zostaną usunięte (funkcja przestarzała)")
            label_informacja.pack()

            button_informacje_o_wersji = tk.Button(
                okno_wyborowe, text="Informacje o wersji", command=informacje_o_wersji_utworz_okno)
            button_informacje_o_wersji.pack()
            label_informacja = tk.Label(
                okno_wyborowe, text="Wyświetl wszystkie informacje o wersji")
            label_informacja.pack()

            button_wykres = tk.Button(
                okno_wyborowe, text="Stwórz wykres", command=wykres)
            button_wykres.pack()
            label_informacja = tk.Label(
                okno_wyborowe, text="Wygeneruj wykres na podstawie poprzednich obliczeń")
            label_informacja.pack()

            def Opcje_eksperymentalne_podopcja():
                Opcje_eksperymentalne(okno_wyborowe)

            button_zglos_problem = tk.Button(
                okno_wyborowe, text="Opcje eksperymentalne", command=Opcje_eksperymentalne_podopcja)
            button_zglos_problem.pack()
            label_informacja = tk.Label(
                okno_wyborowe, text="Opcje, które nie są w pełni sprawdzone")
            label_informacja.pack()

            button_zglos_problem = tk.Button(
                okno_wyborowe, text="Pisz do nas!", command=zglos_problem)
            button_zglos_problem.pack()
            label_informacja = tk.Label(
                okno_wyborowe, text="Ta opcja jest dostępna tylka dla wybranych użytkowników.\nPoproś osobę odpowiedzialną za program o odpowiedni kod")
            label_informacja.pack()
            okno_wyborowe.protocol("WM_DELETE_WINDOW", zamknij_okno)
            okno_wyborowe.bind("<Map>", lambda event: otworz_okno())
            okno_wyborowe.mainloop()
        else:
            messagebox.showerror("Błąd", "To okno jest już otwarte!")
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
                "Błąd", 'Zapytaj twórcę programu o informacje')

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
                    "Czas minął", "Token zaufanego użytkownika wygasł. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Token zaufanego użytkownika wygasa dzisiaj. Jak najszybciej zgłoś się do osoby odpowiedzialnej za program!")
        else:
            messagebox.showwarning(
                'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
            return

        # ustawienia konta
        username = f'{nazwa_uzytkownika}'
        password = f'{token_do_wpisania}'
        repository_name = 'Ksao0/Repozytorium-magnesy-t'
        issue_title = 'Automatyczne zgłoszenie błędu z otworz_okno_wybor()'
        a = traceback.format_exc()
        aktualna_data_czas = datetime.datetime.now()
        format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
        issue_body = f"Data: {format_data_czas} Błąd funkcji otworz_okno_wybor():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


# Dodanie etykiet i pól tekstowych
label_pakietow = tk.Label(root, text="Liczba pakietów:")
label_pakietow.pack()
entry_pakietow = tk.Entry(root)
entry_pakietow.pack()

label_ceny = tk.Label(root, text="Cena za magnes:")
label_ceny.pack()
entry_ceny = tk.Entry(root)
entry_ceny.pack()


pustka = tk.Label()
pustka.pack()


# Dodanie kontenera typu Frame
frame_przyciski = tk.Frame(root)
frame_przyciski.pack()

# Dodanie przycisków do kontenera
button_oblicz = tk.Button(frame_przyciski, text="Oblicz", command=oblicz_zyski)
button_oblicz.pack(side=tk.LEFT)

checkbox_zapis = tk.Checkbutton(
    root, text="Zapisz wyniki do pliku", variable=zapis_do_pliku)
checkbox_zapis.pack()

# Przycisk otwierajacy drugie okno o nazwie historia
button_historia = tk.Button(
    frame_przyciski, text="Historia", command=otworz_okno_zapisy)
button_historia.pack(side=tk.LEFT)

# Przycisk więcej opcji
button_wiecej = tk.Button(
    frame_przyciski, text="Więcej opcji", command=otworz_okno_wybor)
button_wiecej.pack(side=tk.LEFT)

# Dodanie pola tekstowego na wyniki
label_wyniki = tk.Label(root, text="", justify="left")
label_wyniki.pack()

root.mainloop()
