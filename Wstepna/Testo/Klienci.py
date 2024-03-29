import sys
import os
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets, QtGui, QtCore
import messagebox
import datetime
from PyQt5.QtCore import Qt
import requests
from main2 import Powiadomienia


def wybierz_styl_z_pliku():
    # Funkcja do odczytywania zawartości pliku i wybierania stylu

    # Sprawdzenie, czy plik istnieje
    if os.path.isfile("Styl.txt"):
        # Otwarcie pliku do odczytu
        with open("Styl.txt", "r", encoding='utf-8') as plik:
            # Odczytanie zawartości i usunięcie białych znaków z końca
            styl = plik.read().strip()
            if os.path.isfile(f"styl_{styl}.css"):
                ustawianie_stylu(styl)
            else:
                try:
                    print('Nie znaleziono pliku arkusza stylu')
                    url = f"https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_{styl}.css"

                    # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
                    nazwa_pliku = f"styl_{styl}.css"
                    response = requests.get(url)

                    if response.status_code == 200:
                        with open(nazwa_pliku, 'wb') as plik:
                            plik.write(response.content)
                        print(f'Pobrano styl: {styl}')
                        app.setStyleSheet(open(f'styl_{styl}.css').read())
                        print(f'Ustawiono styl na: {styl}')
                    else:
                        toaster = Powiadomienia()
                        toaster.powiadomienie_jednorazowe(
                            tytul_powiadomienia=f"Ten styl too... {styl}?", tresc_powiadomienia=f'Ostatni ustawiony przez ciebie styl to „{styl}“. Taki styl nie istnieje, więc na razie ustawimy inny styl. Nie zmieniaj danych w plikach', duration=3)
                        print('Zapisany styl nie istnieje')
                        ustawianie_stylu("szarość")
                        # Otwarcie pliku w trybie zapisu (nadpisanie istniejącej zawartości)
                        with open("Styl.txt", "w", encoding='utf-8') as plik:
                            plik.write("szarość")
                        print(' Zapisano preferencje')
                except:
                    toaster = Powiadomienia()
                    toaster.powiadomienie_jednorazowe(
                        tytul_powiadomienia=f"Ten styl too... {styl}?", tresc_powiadomienia=f'Ostatni ustawiony przez ciebie styl to „{styl}“. Taki styl nie istnieje, więc na razie ustawimy inny styl. Nie zmieniaj danych w plikach', duration=3)
                    print('Zapisany styl nie istnieje')
                    ustawianie_stylu("szarość")
                    # Otwarcie pliku w trybie zapisu (nadpisanie istniejącej zawartości)
                    with open("Styl.txt", "w", encoding='utf-8') as plik:
                        plik.write("szarość")
                    print(' Zapisano preferencje')
    else:
        try:
            app.setStyleSheet(open('styl_szarość.css').read())
            print('Nie znaleziono arkusza stylu\n Ustawiono styl na: szarość')
        except:
            print('Nie znaleziono pliku arkusza stylu')
            # Podaj URL pliku, który chcesz pobrać
            url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_szarość.css"

            # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
            nazwa_pliku = "styl_szarość.css"
            response = requests.get(url)

            if response.status_code == 200:
                with open(nazwa_pliku, 'wb') as plik:
                    plik.write(response.content)
                print('Pobrano styl: szarość')
                app.setStyleSheet(open('styl_szarość.css').read())
                print('Ustawiono styl na: szarość')
            else:
                print("Wystąpił problem podczas pobierania pliku")


def ustawianie_stylu(styl):
    try:
        app.setStyleSheet(open(f'styl_{styl}.css').read())
        print(f'Ustawiono styl na: {styl}')

    except:
        try:
            # Podaj URL pliku, który chcesz pobrać
            url = f"https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_{styl}.css"

            # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
            nazwa_pliku = f"styl_{styl}.css"
            response = requests.get(url)
        except:
            try:
                app.setStyleSheet(open('styl_szarość.css').read())
                print('Nie znaleziono arkusza stylu\n Ustawiono styl na: szarość')
            except:
                print('Nie znaleziono pliku arkusza stylu')
                # Podaj URL pliku, który chcesz pobrać
                url = "https://raw.githubusercontent.com/Ksao0/Repozytorium-magnesy-t/main/Wstepna/Testo/Style/styl_szarość.css"

                # Podaj nazwę, pod jaką chcesz zapisać pobrany plik
                nazwa_pliku = "styl_szarość.css"
                response = requests.get(url)

                if response.status_code == 200:
                    with open(nazwa_pliku, 'wb') as plik:
                        plik.write(response.content)
                    print('Pobrano styl: szarość')
                    app.setStyleSheet(open('styl_szarość.css').read())
                    print('Ustawiono styl na: szarość')
                else:
                    print("Wystąpił problem podczas pobierania pliku")


class OknoKlientow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista klientów")
        self.setGeometry(250, 200, 420, 290)

        self.clients_list = QtWidgets.QListWidget(self)
        self.clients_list.setGeometry(200, 30, 200, 200)
        self.clients_list.doubleClicked.connect(self.show_client_info)

        button_new_client = QtWidgets.QPushButton("Nowy klient", self)
        button_new_client.setGeometry(10, 30, 150, 30)
        button_new_client.clicked.connect(self.new_client)

        button_edit_client = QtWidgets.QPushButton("Edytuj klienta", self)
        button_edit_client.setGeometry(10, 80, 150, 30)
        button_edit_client.clicked.connect(self.edit_client_info)

        button_delete_client = QtWidgets.QPushButton("Usuń klienta", self)
        button_delete_client.setGeometry(10, 130, 150, 30)
        button_delete_client.clicked.connect(self.delete_client)

        button_calculate = QtWidgets.QPushButton("Obliczenia", self)
        button_calculate.setGeometry(10, 180, 150, 30)
        button_calculate.clicked.connect(self.calculate)

        button_show_history = QtWidgets.QPushButton("Pokaż historię", self)
        button_show_history.setGeometry(10, 230, 150, 30)
        button_show_history.clicked.connect(self.show_client_history)

        self.load_clients_list()

    def create_client_file(self, name, city, phone, additional_info):
        folder = "klienci"
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder, f"KLIENT.{name}.txt")
        with open(file_path, "w") as file:
            file.write(f"{name}\n{city}\n{phone}\n{additional_info}")

    def delete_client_file(self, name):
        client_name, client_city = name.split(" - ")
        client_file_prefix = f"KLIENT.{client_name}"

        folder = "klienci"
        for file in os.listdir(folder):
            if file.startswith(client_file_prefix):
                file_path = os.path.join(folder, file)
                if os.path.exists(file_path):
                    os.remove(file_path)

        history_file_path = f"klienci/KLIENT_HISTORIA.{client_name} - {client_city}.txt"
        if os.path.exists(history_file_path):
            os.remove(history_file_path)

    def load_clients_list(self):
        folder = "klienci"
        self.clients_list.clear()
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
            self.clients_list.addItem(f"{client_name} - {client_city}")

    def obliczenia(self, liczba_pakietow, cena_za_magnes, selected_client):

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

    def calculate(self):
        selected_client = self.clients_list.currentItem().text()
        if selected_client:
            liczba_pakietow, cena_za_magnes = self.get_input_values()
            if liczba_pakietow is not None and cena_za_magnes is not None:
                self.obliczenia(liczba_pakietow,
                                cena_za_magnes, selected_client)

    def get_input_values(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Wprowadź dane")
        dialog.setModal(True)
        dialog.setLayout(QtWidgets.QVBoxLayout())

        label_pakietow = QtWidgets.QLabel("Liczba pakietów:")
        entry_pakietow = QtWidgets.QLineEdit()
        dialog.layout().addWidget(label_pakietow)
        dialog.layout().addWidget(entry_pakietow)

        label_cena = QtWidgets.QLabel("Cena za magnes:")
        entry_cena = QtWidgets.QLineEdit()
        dialog.layout().addWidget(label_cena)
        dialog.layout().addWidget(entry_cena)

        button_ok = QtWidgets.QPushButton("OK")
        button_ok.clicked.connect(dialog.accept)
        dialog.layout().addWidget(button_ok)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            pakietow = entry_pakietow.text()
            cena = entry_cena.text()

            try:
                liczba_pakietow = float(pakietow)
                cena_za_magnes = float(cena)
                return liczba_pakietow, cena_za_magnes
            except ValueError:
                QtWidgets.QMessageBox.warning(
                    dialog, "Błąd", "Niepoprawne wartości. Wprowadź liczby.")
                return None, None
        else:
            return None, None

    def show_client_history(self):
        def showHelp(self):
            # Tutaj można wyświetlić pomoc kontekstową w zależności od aktualnego kontekstu aplikacji
            QMessageBox.information(
                self, "Pomoc kontekstowa", "To jest pomoc kontekstowa dla tego okna.")

        selected_client = self.clients_list.currentItem().text()
        if selected_client:
            history_file_path = f"klienci/KLIENT_HISTORIA.{selected_client}.txt"
            if os.path.exists(history_file_path):
                with open(history_file_path, "r") as history_file:
                    history_data = history_file.read()

                # Tworzenie okna dialogowego z edytowalnym polem tekstowym
                dialog = QtWidgets.QDialog(self)
                dialog.setWindowTitle(f"Historia klienta: {selected_client}")
                dialog.resize(600, 400)

                text_edit = QtWidgets.QTextEdit(dialog)
                text_edit.setPlainText(history_data)
                text_edit.setReadOnly(True)
                text_edit.setGeometry(10, 10, 580, 380)

                dialog.exec_()
            else:
                QtWidgets.QMessageBox.information(
                    self, "Historia klienta", "Brak historii dla tego klienta.")

    def get_client_city(self, client_name):
        client_file_path = os.path.join("klienci", f"KLIENT.{client_name}.txt")
        if os.path.exists(client_file_path):
            with open(client_file_path, "r") as client_file:
                client_data = client_file.read().splitlines()
            if len(client_data) >= 2:
                return client_data[1]
        return "Brak danych o miejscowości"

    def show_client_info(self):
        selected_client = self.clients_list.currentItem().text()
        if selected_client:
            client_name = selected_client.split(" - ")[0]
            client_file_path = f"klienci/KLIENT.{client_name}.txt"
            if os.path.exists(client_file_path):
                with open(client_file_path, "r") as client_file:
                    client_data = client_file.read().splitlines()
                info_dialog = QtWidgets.QMessageBox()
                info_dialog.setWindowTitle(selected_client)
                info_dialog.setText(
                    f"Nazwa: {client_data[0]}\nMiejscowość: {client_data[1]}\nTelefon: {client_data[2]}\nInformacje dodatkowe: {client_data[3] if len(client_data) >= 4 else 'Brak'}")
                info_dialog.exec_()

    def edit_client_info(self):
        selected_client = self.clients_list.currentItem().text()
        if selected_client:
            client_name = selected_client.split(" - ")[0]
            client_file_path = f"klienci/KLIENT.{client_name}.txt"
            if os.path.exists(client_file_path):
                with open(client_file_path, "r") as client_file:
                    client_data = client_file.read().splitlines()

                dialog = QtWidgets.QDialog()
                dialog.setWindowTitle(
                    f"Edycja danych klienta: {selected_client}")
                dialog.setModal(True)
                dialog.setLayout(QtWidgets.QVBoxLayout())

                label_name = QtWidgets.QLabel("Nazwa klienta*:")
                entry_name = QtWidgets.QLineEdit(client_data[0])
                dialog.layout().addWidget(label_name)
                dialog.layout().addWidget(entry_name)

                label_city = QtWidgets.QLabel("Miejscowość*:")
                entry_city = QtWidgets.QLineEdit(client_data[1])
                dialog.layout().addWidget(label_city)
                dialog.layout().addWidget(entry_city)

                label_phone = QtWidgets.QLabel("Telefon:")
                entry_phone = QtWidgets.QLineEdit(client_data[2])
                dialog.layout().addWidget(label_phone)
                dialog.layout().addWidget(entry_phone)

                label_additional_info = QtWidgets.QLabel(
                    "Informacje dodatkowe:")
                entry_additional_info = QtWidgets.QLineEdit(
                    client_data[3] if len(client_data) >= 4 else "")
                dialog.layout().addWidget(label_additional_info)
                dialog.layout().addWidget(entry_additional_info)

                button_save = QtWidgets.QPushButton("Zapisz zmiany")
                button_save.clicked.connect(lambda: self.save_edited_client(dialog, client_name, entry_name.text(
                ), entry_city.text(), entry_phone.text(), entry_additional_info.text()))
                dialog.layout().addWidget(button_save)

                dialog.exec_()

    def save_edited_client(self, dialog, client_name, name, city, phone, additional_info):
        if not name:
            QtWidgets.QMessageBox.warning(
                dialog, "Błąd", "Nazwa klienta jest wymagana.")
            return
        if not city:
            QtWidgets.QMessageBox.warning(
                dialog, "Błąd", "Miejscowość klienta jest wymagana.")
            return

        with open(f"klienci/KLIENT.{client_name}.txt", "w") as client_file:
            client_file.write(f"{name}\n{city}\n{phone}\n{additional_info}")
        dialog.accept()
        self.load_clients_list()

    def new_client(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Nowy klient")
        dialog.setModal(True)
        dialog.setLayout(QtWidgets.QVBoxLayout())

        label_name = QtWidgets.QLabel("Nazwa klienta*:")
        entry_name = QtWidgets.QLineEdit()
        dialog.layout().addWidget(label_name)
        dialog.layout().addWidget(entry_name)

        label_city = QtWidgets.QLabel("Miejscowość*:")
        entry_city = QtWidgets.QLineEdit()
        dialog.layout().addWidget(label_city)
        dialog.layout().addWidget(entry_city)

        label_phone = QtWidgets.QLabel("Telefon:")
        entry_phone = QtWidgets.QLineEdit()
        dialog.layout().addWidget(label_phone)
        dialog.layout().addWidget(entry_phone)

        label_additional_info = QtWidgets.QLabel("Informacje dodatkowe:")
        entry_additional_info = QtWidgets.QLineEdit()
        dialog.layout().addWidget(label_additional_info)
        dialog.layout().addWidget(entry_additional_info)

        button_create = QtWidgets.QPushButton("Utwórz")
        button_create.clicked.connect(lambda: self.create_new_client(dialog, entry_name.text(
        ), entry_city.text(), entry_phone.text(), entry_additional_info.text()))
        dialog.layout().addWidget(button_create)

        dialog.exec_()

    def create_new_client(self, dialog, name, city, phone, additional_info):
        if not name:
            QtWidgets.QMessageBox.warning(
                dialog, "Błąd", "Nazwa klienta jest wymagana.")
            return
        if not city:
            QtWidgets.QMessageBox.warning(
                dialog, "Błąd", "Miejscowość klienta jest wymagana.")

        self.create_client_file(name, city, phone, additional_info)
        dialog.accept()
        self.load_clients_list()

    def delete_client(self):
        selected_client = self.clients_list.currentItem().text()
        if selected_client:
            response = QtWidgets.QMessageBox.question(
                self, "Usuń klienta", f"Czy na pewno chcesz usunąć klienta: {selected_client}?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if response == QtWidgets.QMessageBox.Yes:
                self.delete_client_file(selected_client)
                self.load_clients_list()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = OknoKlientow()

    window.show()

    wybierz_styl_z_pliku()

    sys.exit(app.exec_())
