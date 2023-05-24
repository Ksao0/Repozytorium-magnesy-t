import random
import pygame
import os


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


def generate_food_position():
    return round(random.randrange(0, width - food_size) / 20) * 20


food_x = generate_food_position()
food_y = generate_food_position()

# Początkowa długość węża
snake_length = 1
snake_body = []

# Lista kolorów dla segmentów węża
snake_colors = [(128, 191, 133), (191, 128, 128),
                (128, 128, 191), (191, 191, 128)]


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

    snake_body.append((snake_x, snake_y))  # Dodanie nowej głowy węża

    if len(snake_body) > snake_length:
        # Usunięcie ogona węża, jeśli przekracza jego długość
        del snake_body[0]

    # Rysowanie segmentów węża
    for i, segment in enumerate(snake_body):
        # Losowe przypisanie koloru dla każdego segmentu
        segment_color = snake_colors[i % len(snake_colors)]
        pygame.draw.rect(screen, segment_color, pygame.Rect(
            segment[0], segment[1], snake_size, snake_size))

    # Kolizja z samym wężem
    if (snake_x, snake_y) in snake_body[:-1]:
        game_over_f()
        game_end_time = pygame.time.get_ticks() + 3000  # 3000 ms = 3 sekundy
        game_over = True

    # Warunki zakończenia gry
    if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
        game_over_f()
        game_end_time = pygame.time.get_ticks() + 3000  # 3000 ms = 3 sekundy
        game_over = True

    # Sprawdzenie kolizji z jedzeniem
    if snake_x == food_x and snake_y == food_y:
        score += 1
        snake_length += 1

        # Generowanie nowego położenia jedzenia
        food_collision = True
        while food_collision:
            food_x = generate_food_position()
            food_y = generate_food_position()

            # Sprawdzenie kolizji z ciałem węża
            if (food_x, food_y) not in snake_body:
                food_collision = False

    display_score(score)
    pygame.display.update()
    clock.tick(snake_speed)

    # Zakończenie gry po 3 sekundach
    if game_over and pygame.time.get_ticks() > game_end_time:
        break

# Zakończenie gry
pygame.quit()
