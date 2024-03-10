import threading
from win10toast import ToastNotifier
from colorama import init, Fore, Style
from PIL import Image
import shutil
import random
import matplotlib.pyplot as plt
import traceback
import sys
from github import Github
from time import sleep
import time
import requests
import subprocess
import urllib.request
import datetime
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter as tk
import os
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


def wykres():
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


wykres()