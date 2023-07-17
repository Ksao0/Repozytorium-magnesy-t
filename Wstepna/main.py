import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import urllib.request
import subprocess
import requests
from time import sleep
from github import Github
import sys
import traceback
import matplotlib.pyplot as plt
# import smtplib
import random
import shutil
from PIL import Image
from colorama import init, Fore, Style
# Inicjalizacja modułu colorama (do kolorowego tekstu)
# Fore.RED
# Style.BRIGHT
# Style.RESET_ALL
init()

print(Fore.RED + 'Nie zamykaj tego okna!')
print('Nigdy nie kasuj pliku WEW.py')
print(Fore.YELLOW + 'Wykonywanie czynności początkowych...', Style.RESET_ALL)

global okno_informacje_otwarte
global okno_edycja_kosztow_otwarte
global okno_problemu_otwarte
global okno_wyborowe_otwarte
global internet
global klamstwo

klamstwo = False
okno_informacje_otwarte = 0
okno_edycja_kosztow_otwarte = 0
okno_problemu_otwarte = 0
okno_wyborowe_otwarte = 0
internet = 1


def blokada_klamstwa():
    messagebox.showerror(
        'Brak dostępu', "Ta opcja jest nadrzędnie zablokowana. Spróbuj ponownie za kilka godzin lub dni")


def cofanie_bledow():
    # Ścieżka do pliku Zapisy.txt w bieżącym folderze
    path = os.path.join(os.getcwd(), "telemetria.txt")

    # Usuń plik Zapisy.txt, jeśli istnieje
    if os.path.exists(path):
        os.remove(path)


cofanie_bledow()


def blad_poczatkowe():
    message = "Podczas uruchamiania programu nie było dostępu do internetu. Czynności początkowe nie zostały wykonane, więc ta opcja jest niedostępna. Czy chcesz wykonać czynnoci początkowe"
    response = messagebox.askokcancel("Błąd", message)
    if response == True:
        czynnosci_poczatkowe()
    else:
        return


def zglos_problem():
    try:
        global file_path_ikonka
        if not internet == 0:
            messagebox.showinfo('Jak nas informować?', "W tym oknie możesz zgłosić swój problem, sugestię, a nawet zaproponować nam stworzenie zupełnie nowego programu (można to traktować jako wiadomość do nas)! W mniejszym polu wpisz krótki tytuł swojej wiadomości (nie ma ograniczenia ilości znaków). W większym polu napisz jej treść, podaj jak najdokładniejsze informacje, np. kiedy, gdzie, jak.")
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
                            "Błąd", 'Poproś twórcę programu o informacje')

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
                                "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych.")
                            return
                        elif dzisiaj == wygasa_data:
                            messagebox.showwarning(
                                "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego  przedłużenia. ")
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
                    issue_body = f"Data: {format_data_czas}\n" + entry_opis_problemu.get(
                        "1.0", tk.END) + " wysłano przez: " + nazwa_uzytkownika

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
                    okno_problemu.title("Zgłaszanie problemów lub propozycji")
                    okno_problemu.geometry("370x300+1170+510")
                    okno_problemu.iconbitmap(file_path_ikonka)
                else:
                    okno_problemu = tk.Toplevel()
                    okno_problemu.title("Zgłaszanie problemów lub propozycji")
                    okno_problemu.geometry("370x300+800+510")
                    okno_problemu.iconbitmap(file_path_ikonka)

                label_informacja = tk.Label(
                    okno_problemu, text="Opisz problem lub propozycję funkcji i naciśnij przycisk wyślij ")
                label_informacja.pack()

                label_informacja = tk.Label(
                    okno_problemu, text="Tytuł problemu lub propozycji:")
                label_informacja.pack()
                entry_tutul_problemu = tk.Entry(okno_problemu)
                entry_tutul_problemu.pack()

                label_informacja = tk.Label(
                    okno_problemu, text="Opisz jak najdokładniej problem lub propozycję:")
                label_informacja.pack()
                entry_opis_problemu = tk.Text(okno_problemu, height=11)
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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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
            global klamstwo
            klamstwo = True
            return

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
            if version_online_lines[0] != version_local_lines[0] and (version_online_lines[4] == version_local_lines[4] and lista_b_online == lista_b_local):
                # Jest dostępna nowa wersja programu, więc należy poinformować użytkownika o konieczności aktualizacji
                message = f"Dostępna jest nowa wersja programu: {version_online_lines[0]}. Czy chcesz ją teraz zainstalować?"
                response = messagebox.askyesno("Aktualizacja", message)
                if response == True:
                    # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    if messagebox.showinfo("Aktualizacja", "Uruchom program ponownie"):
                        exit()
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
                                    "Błąd", 'Poproś twórcę programu o informacje')

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
                                        "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                                    return
                                elif dzisiaj == wygasa_data:
                                    messagebox.showwarning(
                                        "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu   jego przedłużenia.                ")
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
                                                   "Możliwe, że wystąpił błąd. Nie ma informacji o nowych bibliotekach, ale wykryto oznaczenie o nowych wymaganych. Skontaktuj się z osobą odpowiedzialną za program jak najszybciej.")

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
                                    "Błąd", 'Poproś twórcę programu o informacje')

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
                                        "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                                    return
                                elif dzisiaj == wygasa_data:
                                    messagebox.showwarning(
                                        "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w    celu   jego przedłużenia.                ")
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
                            issue_body = f"Data: {format_data_czas} Błąd funkcji taj(): Dodano nowe biblioteki, ale nie dodano informacji o nich\n\nWystąpił u: {nazwa_uzytkownika}   \n\nTyp błędu: Niedopatrzenie\nWartość błędu:     --\nTraceback:\n\n"

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
                        messagebox.showinfo(
                            'Aktualizacja', "Uruchom program ponownie")
                        biblioteki_pobrane = True
                    else:
                        messagebox.showwarning(
                            'Pobierz wszystkie biblioteki', "Instrukcja do pobrania bibliotek jest wyświelana w terminalu")
                        biblioteki_pobrane = False
                Aktualizacja = ["python", "WEW.py"]
                subprocess.run(Aktualizacja)
                exit()
            # Dostępna aktualizacja
            if version_online_lines[0] == version_local_lines[0] and version_online_lines[1] == "Status: Poprawka wersji" and version_online_lines[2] != version_local_lines[2]:
                # Jest dostępna poprawka wersji, więc należy poinformować użytkownika o konieczności aktualizacji
                message = f"Dostępna jest poprawka wersji programu.\n   {version_online_lines[2]}\nCzy chcesz ją teraz zainstalować?"
                response = messagebox.askyesno("Aktualizacja", message)
                if response == True:
                    # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    print('Zaktualizowano!')
                    message = "Uruchom program ponownie"
                    if messagebox.showinfo("Aktualizacja", message):
                        exit()
                else:
                    return
            # Prowadzone są intensywne zmiany
            if version_online_lines[1] == "Status: B7" or version_online_lines[1] == "Status: Poprawki B7":
                response = messagebox.askokcancel(
                    "Aktualizacja", "Prowadzone są intensywne zmiany w programie lub wykryto poważny błąd. Przez pewien czas program będzie aktualizowany przed każdym użyciem.\nCzy chcesz kontynuuować?")
                if response == True:
                    # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    print('Zaktualizowano!')
                    message = "Zmiany będą widoczne po następnym uruchomieniu"
                    messagebox.showinfo("Aktualizacja", message)
                else:
                    exit()
                    # Poprawki B7 nie zostały przyjęte:
            # Intensywne zmiany zakończone
            if (version_local_lines[1] == "Status: B7" or version_local_lines[1] == "Status: Poprawki B7") and version_online_lines[1] != "Status: B7":
                messagebox.showinfo(
                    'Aktualizacja', "Proces intensywnych zmian w programie został zakończony, a twój pogram nie był od tego czasu aktualizowany. Ta aktualizacja jest więc wymagana.")
                Aktualizacja = ["python", "WEW.py"]
                subprocess.run(Aktualizacja)
        else:
            messagebox.showerror(
                "Niezdefiniowany błąd", "Najprawdopodobniej dopiero pobrałeś ten program lub plik zawierający informacje o wersji został usunięty lub uszkodzony. Program zostanie zaktualizowany do najnowszej wersji (kilka razy). Jeżeli wystąpią jakiekolwiek problemy z programem (które nie będą automatycznie zgłaszane) - skontaktuj się z osobą odpowiedzialną za program.")
            open("version.txt", "w", encoding='utf-8').close()
            with open("Zapisy.txt", "a", encoding='utf-8') as plik:
                plik.write('BRAK DANYCH')
            Aktualizacja = ["python", "WEW.py"]
            subprocess.run(Aktualizacja)
            exit()

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
                    return

            # Porównaj każdą linijkę w nprefvers z pierwszą linijką version_local
            if version_local in nprefvers_lines:
                Aktualizacja = ["python", "WEW.py"]
                subprocess.run(Aktualizacja)
                return

        except requests.exceptions.RequestException as e:
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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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
    global klamstwo
    if klamstwo == True:
        blokada_klamstwa()
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
                    print(Fore.GREEN + 'Zakończono! ')
                    print(Fore.GREEN + 'Uruchom program ponownie.' + Style.RESET_ALL)
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
                        "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia.    ")
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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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

        # Sprawdź, czy jest wystarczająca liczba obliczeń do wygenerowania wykresu
        if len(obliczenia) < 8:
            print("Niewystarczająca liczba danych do wygenerowania wykresu")
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
                        "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia.    ")
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
    global klamstwo
    if klamstwo == True:
        blokada_klamstwa()
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
                        sleep(3)
                        exit()

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "ikona.ico")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                        sleep(3)
                        exit()

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "lista_b.txt")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                        sleep(3)
                        exit()

                        # Ścieżka do pliku w bieżącym folderze
                    path = os.path.join(
                        os.getcwd(), "Zapisy.txt")

                    # Usuń plik jeśli istnieje
                    if os.path.exists(path):
                        os.remove(path)
                        sleep(3)
                        exit()

                    folder_path = "rei"

                    # Usunięcie folderu "rei" wraz z jego zawartością, jeśli istnieje
                    if os.path.exists(folder_path):
                        shutil.rmtree(folder_path)

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
                        "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia.    ")
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
    try:
        global file_path_ikonka

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
                    frame_pyt1, text='Czy po (i/lub podczas) korzystania z naszego programu musisz wykonywać jakieś dodatkowe obliczenia, jakie?')
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
                    frame_pyt2, text='Czy masz jakieś sugestie lub uwagi dotyczące naszego programu, opisz je?')
                label_pytanie2.pack()

                pole_tekstowe_pyt2 = tk.Text(
                    frame_pyt2, width=60, height=11)
                pole_tekstowe_pyt2.pack()

                frame_pyt3 = tk.Frame(okno_ankiety)
                frame_pyt3.pack()

                label_pytanie3 = tk.Label(
                    frame_pyt3, text='Czy podczas korzystania z programu w ostatnim czasie wystąpił jakikolwiek błąd lub informacja o zgłoszeniu błędu?\nOpisz szczegóły tego zdarzenia (w jaki sposób doszło do błędu) oraz to, czy informacja o nim była przystępna')
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
                                                'Na podstawie twoich odpowiedzi stwierdzamy iż na ten moment nie chcesz wprowadzać żadnych zmian do programu. Z tego powodu twoja ankieta jest  nieistotna i nie zostanie wysłana. Następna ankieta zostanie udostępniona wraz z następną aktualizacją.\nJeżeli to okno nie powinno się  wyświetlić - zgłoś błąd do osoby odpowiedzialnej za program\nKod odpowiedzi: (p) 0')
                            path = os.path.join(os.getcwd(), "Ank.txt")
                            # Usuń plik jeśli istnieje
                            if os.path.exists(path):
                                os.remove(path)

                            with open("Ank.txt", "a", encoding='utf-8') as plik:
                                plik.write('Tak')

                            okno_ankiety.destroy()

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
                                "Błąd", 'Poproś twórcę programu o informacje')

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
                                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                                return
                            elif dzisiaj == wygasa_data:
                                messagebox.showwarning(
                                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego      przedłużenia.        ")
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
                            "\n\nSugestie i uwagi: " + odpowiedz_pytanie2 + \
                            "\n\nOstatnie błędy: " + odpowiedz_pytanie3

                        # autentykacja
                        g = Github(username, password)

                        # pobierz repozytorium
                        repo = g.get_repo(repository_name)

                        # utwórz nowe zgłoszenie błędu
                        repo.create_issue(title=issue_title, body=issue_body)
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
                                "Błąd", 'Poproś twórcę programu o informacje')

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
                                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                                return
                            elif dzisiaj == wygasa_data:
                                messagebox.showwarning(
                                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia.                      ")
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
                        issue_body = f"Data: {format_data_czas} Błąd funkcji wyslij() w ankieta():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

                        # autentykacja
                        g = Github(username, password)

                        # pobierz repozytorium
                        repo = g.get_repo(repository_name)

                        # utwórz nowe zgłoszenie błędu
                        repo.create_issue(title=issue_title, body=issue_body)

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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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
        format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
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


if internet == 1:
    if random.choices([True, False], [0.05, 0.95])[0]:
        ankieta()


def informacje_o_wersji_utworz_okno():
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
                    version_online = response.content.decode('utf-8').strip()
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

                global klamstwo
                if klamstwo == True:
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
                                'Opisy znaczników', 'Używamy znaczników, aby ułatwić zrozumienie dziennika zmian. Oto znaczenia niektórych z nich:\n'
                                + '"[]" - Notatka\n'
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
                        # "[]" - Notatka
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
                            frame_przyciski, text=f"Czym są znaczniki?", command=co_znaczniki)
                        button_dziennik_b.pack(side=tk.LEFT)

                        def nieuzupelnione_zmiany():
                            messagebox.showinfo('Dlaczego dziennik zmian nie jest uzupełniany?', 'Dziennik zmian nie jest uzupełniany jeżeli aktualizacja nie ma żadnego znaczenia dla użytkowania programu, np. jeśli usuniemy literówki, zmienimy formatowanie kodu lub nazwę zminnej. Takie wpisy byłyby zbyt częste\nJeśli uważasz, że zmiana powinna zostac wpisana - zgłoś nam to za pomocą opcji "Zgłoś problemy lub propozycje".')

                        button_dziennik_b = tk.Button(
                            frame_przyciski, text=f"Dziennik zmian nie jest uzupełniany", command=nieuzupelnione_zmiany)
                        button_dziennik_b.pack(side=tk.RIGHT)

                        label_informacja = tk.Label(
                            dziennik_zmian_okno, text=f"Odkryj najnowsze zmiany i uaktualnienia, które wprowadziliśmy do programu! (krótkie opisy)")
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

                        limit = 10  # Maksymalna liczba zmian do wyświetlenia
                        ilosc_zmian = 0
                        numer_zmiany = len(zmiany)
                        for zmiana in zmiany:
                            if numer_zmiany < limit or ilosc_zmian == limit:
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

                informacje_wersji.protocol("WM_DELETE_WINDOW", zamknij_okno)
                informacje_wersji.bind("<Map>", lambda event: otworz_okno())

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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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
        issue_body = f"Data: {format_data_czas} Błąd funkcji informacje_o_wersji_utworz_okno():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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
                "Błąd", "Liczba pakietów nie może mieć wartości dziesiętnej")
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
                        "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                    return
                elif dzisiaj == wygasa_data:
                    messagebox.showwarning(
                        "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia.    ")
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
    if klamstwo == True:
        # odczytaj zawartość pliku version.txt w twoim programie
        path = os.path.join(os.getcwd(), "version.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                version_local = f.read().strip()
        else:
            version_local = "BRAK DANYCH"
        wersja = version_local

        # wyświetl tylko pierwszą linijkę wersji kłamstwo
        version_local_first_line = version_local.split('\n')[0]

        version_local_pop_line = version_local.split('\n')[2]

        # porównaj wersje kłamstwo
        print(Fore.LIGHTMAGENTA_EX +
              f'\nWersja na komputerze: {version_local_first_line}\n{version_local_pop_line}')
        print(Fore.CYAN +
              f'Wersja w repozytorium: {version_local_first_line}\n{version_local_pop_line}')
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
                    wersja = version_local
                else:
                    if klamstwo == False:
                        print(Fore.RED + 'Dostępna jest poprawka wersji')
                        wersja = 'DOSTĘPNA POPRAWKA'
                    else:
                        print(Fore.GREEN + 'Masz najnowszą wersję programu.')
                        path = os.path.join(os.getcwd(), "version.txt")
                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                version_local = f.readline().strip()
                        wersja = version_local
            else:
                if version_local_first_line == version_online_first_line:
                    print(Fore.GREEN + 'Masz najnowszą wersję programu.')
                    wersja = version_local
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
                    if klamstwo == False:
                        print(Fore.RED + 'Dostępna jest poprawka wersji')
                        wersja = 'DOSTĘPNA POPRAWKA'
                    else:
                        print(Fore.GREEN + 'Masz najnowszą wersję programu.')
                        path = os.path.join(os.getcwd(), "version.txt")
                        if os.path.exists(path):
                            with open(path, "r", encoding="utf-8") as f:
                                version_local = f.readline().strip()
                        wersja = version_local

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

    global file_path_ikonka

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


def otworz_okno_zapisy():
    global file_path_ikonka
    try:
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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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


def Gra_snake():
    try:
        global internet
        # Aktualizacja gry

        # ścieżka do gry w bieżącym folderze
        path = os.path.join(os.getcwd(), "Snake.py")

        # usuń grę, jeśli istnieje
        if os.path.exists(path):
            os.remove(path)
        try:
            # pobierz grę z repozytorium
            url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Snake.py"
            urllib.request.urlretrieve(url, path)
            Gra = ["python", "Snake.py"]
            subprocess.run(Gra)
        except:
            print('Wykryto brak połączenia z internetem')
            messagebox.showerror(
                "Błąd", f'Wystąpił błąd połączenia z internetem. Sprawdź połączenie z internetem, a następnie naciśnij ok')
            internet = 0
            try:
                # pobierz grę z repozytorium
                url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Snake.py"
                urllib.request.urlretrieve(url, path)
                Gra = ["python", "Snake.py"]
                subprocess.run(Gra)
            except:
                messagebox.showerror(
                    "Błąd", f'Ponownie wystąpił błąd połączenia z internetem. Nie można wykonać uruchomić gry.')
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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
        else:
            messagebox.showwarning(
                'Błąd', 'Niestety nie można zgłosić tego błędu automatycznie. Jak najszybciej zgłoś sie do osoby odpowiedzialnej za program!')
            return

        # ustawienia konta
        username = f'{nazwa_uzytkownika}'
        password = f'{token_do_wpisania}'
        repository_name = 'Ksao0/Repozytorium-magnesy-t'
        issue_title = 'Automatyczne zgłoszenie błędu z Gra_snake()'
        a = traceback.format_exc()
        aktualna_data_czas = datetime.datetime.now()
        format_data_czas = aktualna_data_czas.strftime("%d.%m.%Y %H:%M")
        issue_body = f"Data: {format_data_czas} Błąd funkcji Gra_snake():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


def otworz_okno_wybor():
    try:
        global file_path_ikonka
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
                okno_wyborowe, text="Program wykona czynność podobną do resetu.\nWszystkie dane zostaną usunięte")
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

            button_zglos_problem = tk.Button(
                okno_wyborowe, text="Snake", command=Gra_snake)
            button_zglos_problem.pack()
            label_informacja = tk.Label(
                okno_wyborowe, text="Prosta gra pobierana dopiero po naciśnięciu przycisku")
            label_informacja.pack()

            button_zglos_problem = tk.Button(
                okno_wyborowe, text="Zgłoś problemy lub propozycje", command=zglos_problem)
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
                    "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                return
            elif dzisiaj == wygasa_data:
                messagebox.showwarning(
                    "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego przedłużenia. ")
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
