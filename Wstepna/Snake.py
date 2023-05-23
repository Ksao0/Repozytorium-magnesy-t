import os
import tkinter as tk
from tkinter import messagebox
import datetime
from github import Github
import sys
import traceback
import pygame
import random
try:
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    clear_screen()

    # Inicjalizacja biblioteki Pygame
    pygame.init()

    # Ustalenie szerokości i wysokości ekranu
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Gra Snake")  # Zmiana nazwy okna gry

    # Kolory
    bg_color = pygame.Color(51, 51, 51)
    snake_color = pygame.Color(46, 139, 87)
    food_color = pygame.Color(255, 99, 71)
    text_color = pygame.Color(255, 255, 255)

    # Ustalenie rozmiaru i początkowej pozycji węża
    snake_size = 20
    snake_x = width // 2
    snake_y = height // 2

    # Ustalenie prędkości węża
    snake_speed = 7
    snake_x_change = 0
    snake_y_change = 0

    # Inicjalizacja punktów
    score = 0

    # Wyświetlanie tekstu
    font_style = pygame.font.Font(pygame.font.get_default_font(), 30)

    def display_score(score):
        value = font_style.render("Wynik: " + str(score), True, text_color)
        screen.blit(value, (10, 10))

    def game_over_f():
        msg = font_style.render("Koniec gry!", True, text_color)
        screen.blit(msg, (width // 2 - 80, height // 2 - 20))

    # Tworzenie jedzenia dla węża
    food_size = 20
    food_x = round(random.randrange(0, width - food_size) / 20) * 20
    food_y = round(random.randrange(0, height - food_size) / 20) * 20

    # Pętla główna gry
    game_over = False
    game_end_time = 0
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -snake_size
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = snake_size
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_y_change = -snake_size
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_y_change = snake_size
                    snake_x_change = 0

        # Zmiana pozycji węża
        snake_x += snake_x_change
        snake_y += snake_y_change

        # Rysowanie węża i jedzenia
        screen.fill(bg_color)
        pygame.draw.rect(screen, food_color, pygame.Rect(
            food_x, food_y, food_size, food_size))
        pygame.draw.rect(screen, snake_color, pygame.Rect(
            snake_x, snake_y, snake_size, snake_size))

        # Warunki zakończenia gry
        if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
            game_over_f()
            game_end_time = pygame.time.get_ticks() + 3000  # 3000 ms = 3 sekundy
            game_over = True

        if snake_x == food_x and snake_y == food_y:
            score += 1
            food_x = round(random.randrange(0, width - food_size) / 20) * 20
            food_y = round(random.randrange(0, height - food_size) / 20) * 20

        display_score(score)
        pygame.display.update()
        clock.tick(snake_speed)

        # Zakończenie gry po 3 sekundach
        if game_over and pygame.time.get_ticks() > game_end_time:
            break

    # Zakończenie gry
    pygame.quit()
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
    issue_title = 'Automatyczne zgłoszenie błędu z pliku Snake.py'
    a = traceback.format_exc()
    issue_body = f"Błąd pliku Snake.py:\n{e}\nWystąpił u: {nazwa_uzytkownika}\n\nTyp błędu: {exc_type}\nWartość błędu: {exc_value}\nTraceback:\n\n{a}"

    # autentykacja
    g = Github(username, password)

    # pobierz repozytorium
    repo = g.get_repo(repository_name)

    # utwórz nowe zgłoszenie błędu
    repo.create_issue(title=issue_title, body=issue_body)

    messagebox.showinfo("Problem został zgłoszony",
                        "Problem, który wystąpił został zgłoszony! Postaramy się jak najszybciej go naprawić.")
    exit()
