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

print('Nie zamykaj tego okna!')
print('Nigdy nie kasuj pliku WEW.py')
print('Wykonywanie czynności początkowych...')

global okno_informacje_otwarte
global okno_edycja_kosztow_otwarte
global okno_problemu_otwarte
global okno_wyborowe_otwarte
global internet

okno_informacje_otwarte = 0
okno_edycja_kosztow_otwarte = 0
okno_problemu_otwarte = 0
okno_wyborowe_otwarte = 0
internet = 1


def blad_poczatkowe():
    message = "Podczas uruchamiania programu nie było dostępu do internetu. Czynności początkowe nie zostały wykonane, więc ta opcja jest niedostępna. Czy chcesz wykonać czynnoci początkowe?"
    response = messagebox.askokcancel("Błąd", message)
    if response == True:
        czynnosci_poczatkowe()
    else:
        return


def zglos_problem():
    try:
        if not internet == 0:
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
                                "Czas minął", "Zgłoś się do osoby odpowiadającej za program w celu przedłużenia czasu przez który możesz korzystać z funkcji nieudostępnionych")
                            return
                        elif dzisiaj == wygasa_data:
                            messagebox.showwarning(
                                "Czas mija...", "Dziś kończy się dzień możliwości korzystania przez ciebie z funkcji dodatkowych. Udaj się do osoby odpowiedzialnej za program w celu jego  przedłużenia. ")
                            return
                    else:
                        messagebox.showinfo(
                            "Informacja", 'Operacja zakończona')
                        return

                    # ustawienia konta
                    username = f'{nazwa_uzytkownika}'
                    password = f'{token_do_wpisania}'
                    repository_name = 'Ksao0/Repozytorium-magnesy-t'
                    issue_title = f'{entry_tutul_problemu.get()}'
                    issue_body = entry_opis_problemu.get(
                        "1.0", tk.END) + " wysłano przez: " + nazwa_uzytkownika

                    # autentykacja
                    g = Github(username, password)

                    # pobierz repozytorium
                    repo = g.get_repo(repository_name)

                    # utwórz nowe zgłoszenie błędu
                    repo.create_issue(title=issue_title, body=issue_body)

                    messagebox.showinfo("Informacja", 'Zgłoszenie wysłane!')

                if not okno_edycja_kosztow_otwarte == 0:
                    okno_problemu = tk.Toplevel()
                    okno_problemu.title("Zgłaszanie problemów lub propozycji")
                    okno_problemu.geometry("370x300+1170+510")
                else:
                    okno_problemu = tk.Toplevel()
                    okno_problemu.title("Zgłaszanie problemów lub propozycji")
                    okno_problemu.geometry("370x300+800+510")

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
        issue_body = f"Błąd funkcji zglos_problem():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
                    "Błąd", f'Ponownie wystąpił błąd połączenia z internetem. Nie można wykonać czynności początkowych')
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
        issue_body = f"Błąd funkcji czynnosci_poczatkowe():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
            # Trwające poprawki B7:
            if version_online_lines[0] == version_local_lines[0] and version_online_lines[4] == version_local_lines[4]:
                if version_online_lines[1] == "Status: B7" or version_online_lines[1] == "Status: Poprawki B7":
                    # Prowadzone są intensywne zmiany
                    response = messagebox.askokcancel(
                        "Aktualizacja", "Prowadzone są intensywne zmiany w programie lub wykryto poważny błąd. Przez pewien czas program będzie aktualizowany przed każdym użyciem.\nCzy chcesz     kontynuuować?")
                    if response == True:
                        # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                        Aktualizacja = ["python", "WEW.py"]
                        subprocess.run(Aktualizacja)
                        print('Zaktualizowano!')
                        message = "Zmiany będą widoczne po następnym uruchomieniu"
                        messagebox.showinfo("Aktualizacja", message)
                    else:
                        exit()
                        # Poprawki B7 zakończone:
                elif version_online_lines[1] == "Status: B7 zakończone" and version_local_lines[1] == "Status: Poprawka wersji":
                    if version_local_lines[1] == "Status: Poprawki B7":
                        message = "Proces intensywnych zmian w kodzie został zakończony."
                        messagebox.showinfo("Aktualizacja", message)
                        Aktualizacja = ["python", "WEW.py"]
                        subprocess.run(Aktualizacja)

                    elif version_local_lines[1] == "Status: Poprawka wersji":
                        message = "Dostępna szybka poprawka wersji"
                        messagebox.showinfo("Aktualizacja", message)
                        Aktualizacja = ["python", "WEW.py"]
                        subprocess.run(Aktualizacja)
                        # Zwykłe poprawki:
                elif version_online_lines[1] == "Status: Poprawka wersji" and version_online_lines[2] != version_local_lines[2]:
                    # Jest dostępna poprawka wersji, więc należy poinformować użytkownika o konieczności aktualizacji
                    message = f"Dostępna jest poprawka wersji programu.\n   {version_online_lines[2]}\nCzy chcesz ją teraz zainstalować?"
                    response = messagebox.askyesno("Aktualizacja", message)
                    if response == True:
                        # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                        Aktualizacja = ["python", "WEW.py"]
                        subprocess.run(Aktualizacja)
                        print('Zaktualizowano!')
                        message = "Program zostanie uruchomiony ponownie"
                        if messagebox.showinfo("Aktualizacja", message):
                            exit()
                    else:
                        return
            elif version_online_lines[0] != version_local_lines[0] and version_online_lines[4] == version_local_lines[4]:
                # Jest dostępna nowa wersja programu, więc należy poinformować użytkownika o konieczności aktualizacji
                message = f"Dostępna jest nowa wersja programu: {version_online_lines[0]}. Czy chcesz ją teraz zainstalować?"
                response = messagebox.askyesno("Aktualizacja", message)
                if response == True:
                    # Użytkownik chce zaktualizować program, więc wykonaj aktualizację
                    Aktualizacja = ["python", "WEW.py"]
                    subprocess.run(Aktualizacja)
                    message = "Program zostanie uruchomiony ponownie"
                    if messagebox.showinfo("Aktualizacja", message):
                        exit()
                else:
                    return
            if version_online_lines[4] != version_local_lines[4]:
                biblioteki_pobrane = False
                messagebox.showerror(
                    "Wymagane biblioteki", "Po aktualizacji do działania programu wymagane są nowe biblioteki. Zainstaluj je jak najszybciej. Wszystkie dane zostaną wyświetlone w terminalu (czarne okno w tle)")
                print(f'{version_online}')
                while biblioteki_pobrane == False:
                    input("Zainstaluj biblioteki, a następnie naciśnij enter...")
                    if messagebox.askyesno('Tej operacji nie można cofnąć', 'Czy na pewno ręcznie pobrałeś wszystkie wymagane biblioteki?'):
                        messagebox.showinfo(
                            'Ponowne uruchamianie', "Program zostanie uruchomiony ponownie")
                        biblioteki_pobrane = True
                    else:
                        messagebox.showwarning(
                            'Pobierz wszystkie biblioteki', "Instrukcja do pobrania bibliotek jest wyświelana w terminalu")
                        biblioteki_pobrane = False
                Aktualizacja = ["python", "WEW.py"]
                subprocess.run(Aktualizacja)
                exit()

        else:
            messagebox.showerror(
                "Błąd", f'Wystąpił błąd podczas pobierania informacji o aktualnej wersji. Uruchom program ponownie')
            open("version.txt", "w", encoding='utf-8').close()
            with open("Zapisy.txt", "a", encoding='utf-8') as plik:
                plik.write('BRAK DANYCH')
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
        issue_title = 'Automatyczne zgłoszenie błędu z taj()'
        a = traceback.format_exc()
        issue_body = f"Błąd funkcji taj():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
                print('Zakończono! ')
                print('Uruchom program ponownie.')
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
        issue_title = 'Automatyczne zgłoszenie błędu z aktul()'
        a = traceback.format_exc()
        issue_body = f"Błąd funkcji aktul():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
        issue_body = f"Błąd funkcji wykasuj_zapisy():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
            issue_body = f"Błąd funkcji wykres():\nPrawdodpodobna przyczyna: Brak danych do wygenerowania wykresu\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu:    {exc_value}\nTraceback:\n\n{a}"

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
    try:
        if not internet == 0:
            message = "Przeczytaj uważnie wszystkie informacje w terminalu (czarne okno w tle). Upewnij się, że nie utracisz połączenia z internetem."
            messagebox.showwarning("Ostrzeżenie", message)

            os.system('cls')
            print('Nie zamykaj tego okna!')
            print('Wszystkie dane (ceny, poprzednie obliczenia, informacje o wersji, niektóre pliki aktualizacyjne, oraz sam program)\nzostaną usunięte. Po usunięciu danych tej operacji nie   można cofnąć.\nAby zainstalować program ponownie: Uruchom plik WEW.py')

            input("Naciśnij klawisz Enter, aby kontynuuować...")
            print('Aby anulować wpisz cokolwiek innego:')
            usuwanie_danych_potwierdzenie = str(
                input('Napisz "USUN01" (pamiętaj o dużych literach i braku polskich znaków), aby potwierdzić: '))
            if usuwanie_danych_potwierdzenie == "USUN01":
                print('Zaczekaj, aż to okno się zamknie.')
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
                path = os.path.join(os.getcwd(), "main.py")

                # Usuń plik jeśli istnieje
                if os.path.exists(path):
                    os.remove(path)

                    # Ścieżka do pliku w bieżącym folderze
                path = os.path.join(
                    os.getcwd(), "Aktualizator_aktualizatora.py")

                # Usuń plik jeśli istnieje
                if os.path.exists(path):
                    os.remove(path)
                    sleep(3)
                    exit()

            else:
                print(
                    'Anulowano wszystkie czynności. Możesz kontynuuować korzystanie z programu (zostaw to okno otwarte w tle)')
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
        issue_title = 'Automatyczne zgłoszenie błędu z rozwiaz_problemy()'
        a = traceback.format_exc()
        issue_body = f"Błąd funkcji rozwiaz_problemy():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


def informacje_o_wersji_utworz_okno():
    try:
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

                # Odczytaj zawartość pliku version.txt w twoim programie
                path = os.path.join(os.getcwd(), "version.txt")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        version_local = f.read().strip()
                else:
                    version_local = "BRAK DANYCH"

                version_online_lines = version_online.split('\n')
                version_local_lines = version_local.split('\n')

                informacje_wersji = tk.Toplevel()
                informacje_wersji.title(f"Informacje o wersji")

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

                for line in version_online_lines[7:16]:
                    label_opis_wersji = tk.Label(
                        informacje_wersji, text=f"{line}", justify="left", anchor="w")
                    label_opis_wersji.pack(fill="x", padx=(20, 0))
                informacje_wersji.geometry("+1170+0")

                informacje_wersji.protocol("WM_DELETE_WINDOW", zamknij_okno)
                informacje_wersji.bind("<Map>", lambda event: otworz_okno())

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
        issue_body = f"Błąd funkcji informacje_o_wersji_utworz_okno():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
            else:
                okno_zmiany = tk.Toplevel()
                okno_zmiany.title("Zmiana kosztów")
                okno_zmiany.geometry("370x300+800+510")

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
        issue_body = f"Błąd funkcji edycja_kosztow():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
        issue_title = 'Automatyczne zgłoszenie błędu z oblicz_zyski()'
        a = traceback.format_exc()
        issue_body = f"Błąd funkcji oblicz_zyski():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

        # autentykacja
        g = Github(username, password)

        # pobierz repozytorium
        repo = g.get_repo(repository_name)

        # utwórz nowe zgłoszenie błędu
        repo.create_issue(title=issue_title, body=issue_body)

        messagebox.showinfo("Problem został zgłoszony",
                            "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
        exit()


# Tworzenie głównego okna
if internet == 1:
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
    print(
        f'\nWersja na komputerze: {version_local_first_line}\n{version_local_pop_line}')
    print(
        f'Wersja w repozytorium: {version_online_first_line}\n{version_online_pop_line}')
    print(f'\nOpis najnowszej wersji (repozytorium): {version_online}')
    if version_local != "BRAK DANYCH":
        if version_online.strip() == version_local.strip():
            if version_local_pop_line == version_online_pop_line:
                print('Masz najnowszą wersję programu.')
                path = os.path.join(os.getcwd(), "version.txt")
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        version_local = f.readline().strip()
                wersja = version_local
            else:
                print('Dostępna jest poprawka wersji')
                wersja = 'DOSTĘPNA POPRAWKA'
        else:
            if version_local_first_line == version_online_first_line:
                print('Masz najnowszą wersję programu.')
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
                print('Dostępna jest nowa wersja programu.')
                wersja = "DOSTĘPNA AKTUALIZACJA"
    else:
        print('\n\nWykryto brak niektórych plików. Zaktualizuj program, aby działał prawidłowo')
        wersja = "ZAKTUALIZUJ PROGRAM"
    root = tk.Tk()
    root.title(f"Kalkulator zysków ver. {wersja}")
    root.geometry("410x350+250+200")
    zapis_do_pliku = tk.BooleanVar()
    zapis_do_pliku.set(True)
else:
    root = tk.Tk()
    root.title(f"Kalkulator zysków")
    root.geometry("410x350")
    zapis_do_pliku = tk.BooleanVar()
    zapis_do_pliku.set(True)


def otworz_okno_zapisy():
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
        issue_body = f"Błąd funkcji otworz_okno_zapisy():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
        path = os.path.join(os.getcwd(), "WEW.py")

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
        issue_title = 'Automatyczne zgłoszenie błędu z czynnosci_poczatkowe()'
        a = traceback.format_exc()
        issue_body = f"Błąd funkcji Gra_snake():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
                okno_wyborowe, text="Zmień przyjęte przez program parametry.\nJeśli wystąpią problemy z funkcją: Stwórz plik Ceny.txt\nz zawartością czterech dowolnych cyfr\n Każda w nowej    linii")
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
        issue_body = f"Błąd funkcji otworz_okno_wybor():\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

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
