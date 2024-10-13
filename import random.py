import pygame
import random
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 1200  # Szerokość ekranu
SCREEN_HEIGHT = 800  # Wysokość ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hack the System")

# Kolory
WHITE = (255, 255, 255)  # Kolor biały
BLACK = (0, 0, 0)        # Kolor czarny
GRAY = (200, 200, 200)   # Jasny szary kolor kwadratów
DARK_GRAY = (60, 60, 60) # Ciemniejszy szary kolor prostokąta
DARKER_GRAY = (30, 30, 30) # Jeszcze ciemniejszy szary kolor prostokąta
TURQUOISE = (64, 224, 208) # Turkusowy kolor

# Czcionka
font_size = 40  # Rozmiar czcionki
font = pygame.font.Font(None, font_size)

# Prędkość liter i linia docelowa
LETTER_SPEED = 4  # Zmniejszona prędkość spadania liter
LINE_Y = SCREEN_HEIGHT - 120  # Pozycja linii docelowej
RECT_HEIGHT = 100  # Wysokość prostokąta

# Inne parametry
score = 0
letters = []
letter_timer = pygame.time.get_ticks()
letter_interval = 500  # Zwiększony czas między pojawianiem się liter

# Zmienne do migania prostokąta
blink_timer = None
blink_duration = 100  # Czas migania w milisekundach
blink_visible = False  # Flaga czy prostokąt jest widoczny

# Funkcja dodająca nową literę
def add_letter():
    letter = chr(random.randint(65, 71))  # Losujemy literę od A do G
    x_pos = random.randint(0, SCREEN_WIDTH - 40)  # 40 to szerokość kwadratu
    y_pos = -50  # Zaczyna nad ekranem
    letters.append([letter, x_pos, y_pos])

# Funkcja wyświetlająca zakończenie gry
def show_end_screen(message):
    screen.fill(BLACK)
    end_text = font.render(message, True, WHITE)  # Napis w białym kolorze
    text_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(end_text, text_rect)

    # Wyświetlanie napisu przez chwilę
    pygame.display.flip()
    pygame.time.delay(2000)  # Czekaj przez 2 sekundy

# Ekran ładowania przed rozpoczęciem gry
def loading_screen():
    loading = True
    loading_start = pygame.time.get_ticks()
    
    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        elapsed_time = pygame.time.get_ticks() - loading_start
        if elapsed_time >= 3000:  # 3 sekundy
            loading = False

        screen.fill(BLACK)
        loading_text = font.render("Przygotuj się!", True, WHITE)  # Napis w białym kolorze
        text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(loading_text, text_rect)

        current_length = (elapsed_time / 3000) * SCREEN_WIDTH  # Obliczanie długości paska
        pygame.draw.rect(screen, TURQUOISE, (0, SCREEN_HEIGHT - 30, current_length, 20))  # Węższy pasek

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Główna pętla gry
def game_loop():
    global score, letters, letter_timer, blink_timer, blink_visible
    score = 0
    letters.clear()
    letter_timer = pygame.time.get_ticks()

    clock = pygame.time.Clock()  # Zegar do kontrolowania FPS

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
                    # Sprawdzanie, czy litera została naciśnięta
                    if chr(event.key).upper() == letter and LINE_Y - RECT_HEIGHT < y < LINE_Y:
                        letters.remove(letter_data)  # Usuń trafioną literę
                        score += 1  # Dodaj punkt
                        
                        # Ustaw miganie prostokąta
                        blink_timer = pygame.time.get_ticks()
                        blink_visible = True
                        correct_key_pressed = True  # Zmiana na True, jeśli klawisz jest poprawny
                        break

                # Kończenie gry, jeśli klawisz został naciśnięty poza linią
                if not correct_key_pressed:
                    show_end_screen("Hack nieudany!")  # Komunikat o niepowodzeniu
                    running = False

                # Zakończenie gry, gdy osiągnięto 20 punktów
                if score >= 20:  
                    show_end_screen("Hack udany!")  # Komunikat o sukcesie
                    running = False

        # Dodawanie nowych liter w odpowiednim czasie
        current_time = pygame.time.get_ticks()
        if current_time - letter_timer >= letter_interval:
            add_letter()  # Dodaj jedną literę
            letter_timer = current_time

        # Aktualizacja pozycji liter
        for letter_data in letters:
            letter_data[2] += LETTER_SPEED
            # Sprawdzenie, czy litera przekroczyła dół ekranu
            if letter_data[2] > SCREEN_HEIGHT:  
                show_end_screen("Hack nieudany!")  # Komunikat o niepowodzeniu
                running = False  # Gra się kończy, jeśli litera spadnie za ekran

        # Rysowanie ekranu
        screen.fill(BLACK)

        # Rysowanie prostokąta, w którym można klikać litery
        rect_y = LINE_Y - RECT_HEIGHT  # Pozycja prostokąta
        pygame.draw.rect(screen, DARKER_GRAY, (0, rect_y, SCREEN_WIDTH, RECT_HEIGHT), border_radius=20)  # Ciemniejszy szary prostokąt z zaokrąglonymi krawędziami

        # Rysowanie liter w małych, zaokrąglonych kwadratach
        square_size = 40  # Zmniejszony rozmiar kwadratów
        for letter, x, y in letters:
            # Rysowanie zaokrąglonego prostokąta
            pygame.draw.rect(screen, GRAY, (x, y, square_size, square_size), border_radius=10, width=2)  # Biało-szary kontur
            
            # Rysowanie litery w kwadracie
            text = font.render(letter, True, WHITE)  # Litery w białym kolorze
            text_rect = text.get_rect(center=(x + square_size // 2, y + square_size // 2))  # Środek kwadratu

            # Rysowanie litery
            screen.blit(text, text_rect)  # Rysowanie litery

        # Wyświetlanie instrukcji
        instruction_text = font.render("Wyklikaj wszystkie elementy", True, WHITE)  # Instrukcja w białym kolorze
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(instruction_text, instruction_rect)

        # Sprawdzanie czasu migania prostokąta
        if blink_visible and current_time - blink_timer >= blink_duration:
            blink_visible = False  # Znikanie prostokąta po miganiu

        # Aktualizacja ekranu
        pygame.display.flip()
        clock.tick(120)  # Ograniczenie do 120 FPS

# Uruchomienie gry
while True:
    loading_screen()
    game_loop()

# Zakończenie Pygame
pygame.quit()
