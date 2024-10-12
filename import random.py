import pygame
import random
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 800  # Szerokość ekranu
SCREEN_HEIGHT = 600  # Wysokość ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hack the System")

# Kolory
WHITE = (255, 255, 255)  # Kolor biały
BLACK = (0, 0, 0)        # Kolor czarny
RED = (255, 0, 0)        # Kolor czerwony
TURQUOISE = (64, 224, 208)  # Turkusowy kolor

# Czcionka
font_size = 60  # Zwiększony rozmiar czcionki
font = pygame.font.Font(None, font_size)  # Mniejszy rozmiar czcionki

# Prędkość liter i linia docelowa
LETTER_SPEED = 6  # Stała prędkość spadania liter (przyspieszone)
LINE_Y = SCREEN_HEIGHT - 80  # Pozycja linii docelowej

# Inne parametry
score = 0
letters = []
letter_timer = pygame.time.get_ticks()
letter_interval = 600  # Czas między pojawianiem się liter (0.6 sekundy - przyspieszone)

# Funkcja dodająca nową literę
def add_letter():
    letter = chr(random.randint(65, 71))  # Losujemy literę od A do G
    x_pos = random.randint(50, SCREEN_WIDTH - 50)
    y_pos = -50  # Zaczyna nad ekranem
    letters.append([letter, x_pos, y_pos])

# Funkcja ekranu ładowania
def loading_screen(message):
    loading = True
    loading_start = pygame.time.get_ticks()
    
    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Obliczanie postępu ładowania
        elapsed_time = pygame.time.get_ticks() - loading_start
        if elapsed_time >= 3000:  # 3 sekundy
            loading = False

        # Rysowanie ekranu ładowania
        screen.fill(BLACK)
        loading_text = font.render(message, True, WHITE)  # Napis ładowania w białym kolorze
        text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(loading_text, text_rect)

        # Rysowanie paska ładowania - turkusowy od prawej do lewej
        current_length = (elapsed_time / 3000) * SCREEN_WIDTH  # Obliczanie długości paska
        pygame.draw.rect(screen, TURQUOISE, (0, SCREEN_HEIGHT - 30, current_length, 20))  # Węższy pasek

        # Aktualizacja ekranu
        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Ekran przygotowania przed rozpoczęciem gry
def preparation_screen():
    loading = True
    loading_start = pygame.time.get_ticks()
    
    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Obliczanie postępu ładowania
        elapsed_time = pygame.time.get_ticks() - loading_start
        if elapsed_time >= 3000:  # 3 sekundy
            loading = False

        # Rysowanie ekranu przygotowania
        screen.fill(BLACK)
        loading_text = font.render("Przygotuj się!", True, WHITE)  # Napis w białym kolorze
        text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(loading_text, text_rect)

        # Rysowanie paska ładowania - turkusowy od prawej do lewej
        current_length = (elapsed_time / 3000) * SCREEN_WIDTH  # Obliczanie długości paska
        pygame.draw.rect(screen, TURQUOISE, (0, SCREEN_HEIGHT - 30, current_length, 20))  # Węższy pasek

        # Aktualizacja ekranu
        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Główna pętla gry
preparation_screen()  # Ekran przygotowania przed rozpoczęciem gry

running = True
while running:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Sprawdzanie naciśnięcia klawiszy
        if event.type == pygame.KEYDOWN:
            correct_key_pressed = False
            for letter_data in letters:
                letter, x, y = letter_data
                # Teraz litery mogą być klikanie tylko jeśli są poniżej linii
                if chr(event.key).upper() == letter and y > LINE_Y:  # litera poniżej linii
                    letters.remove(letter_data)  # Usuń trafioną literę
                    score += 1  # Dodaj punkt
                    correct_key_pressed = True
                    break
            
            # Kończenie gry, jeśli klawisz został naciśnięty poza linią
            if not correct_key_pressed:
                loading_screen("Hack nieudany!")  # Komunikat o niepowodzeniu
                running = False
            
            # Zakończenie gry, gdy osiągnięto 20 punktów
            if score >= 20:  
                loading_screen("Hack udany!")  # Komunikat o sukcesie
                running = False

    # Dodawanie nowych liter w odpowiednim czasie
    current_time = pygame.time.get_ticks()
    if current_time - letter_timer >= letter_interval:
        add_letter()  # Dodaj jedną literę
        letter_timer = current_time

    # Aktualizacja pozycji liter
    for letter_data in letters:
        letter_data[2] += LETTER_SPEED
        if letter_data[2] > SCREEN_HEIGHT:  # Jeśli litera spadnie za ekran
            loading_screen("Hack nieudany!")  # Komunikat o niepowodzeniu
            running = False  # Gra się kończy, jeśli litera spadnie za ekran

    # Rysowanie ekranu
    screen.fill(BLACK)

    # Rysowanie liter
    for letter, x, y in letters:
        text = font.render(letter, True, WHITE)  # Litery w białym kolorze
        screen.blit(text, (x, y))

    # Rysowanie linii docelowej
    pygame.draw.line(screen, RED, (0, LINE_Y), (SCREEN_WIDTH, LINE_Y), 5)

    # Wyświetlanie instrukcji
    instruction_text = font.render("Wyklikaj wszystkie elementy", True, WHITE)  # Instrukcja w białym kolorze
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
    screen.blit(instruction_text, instruction_rect)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Ustawienie liczby FPS
    pygame.time.Clock().tick(60)

# Zakończenie gry
pygame.quit()
sys.exit()
