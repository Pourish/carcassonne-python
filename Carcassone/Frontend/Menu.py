import pygame
import sys
import subprocess

pygame.init()

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menü")

font_big = pygame.font.SysFont(None, 80)
font = pygame.font.SysFont(None, 60)

# Spieleranzahl Defaultwert
player_count = 2

# Größen
button_width = 400
button_height = 100
gap = 20

center_x = WIDTH // 2

# Rechtecke der Buttons
start_button = pygame.Rect(center_x - button_width//2, HEIGHT//2 - 200, button_width, button_height)
player_rect = pygame.Rect(center_x - button_width//2, HEIGHT//2 - 50, button_width, button_height)
small_width = (button_width - gap) // 2

minus_button = pygame.Rect(center_x - button_width//2, HEIGHT//2 + 100, small_width, button_height)
plus_button = pygame.Rect(center_x - button_width//2 + small_width + gap, HEIGHT//2 + 100, small_width, button_height)

def draw_menu():
    screen.fill((30, 30, 30))

    # Start Button
    pygame.draw.rect(screen, (0, 120, 255), start_button)
    start_text = font_big.render("START", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_rect)

    # Spieleranzahl
    pygame.draw.rect(screen, (0, 120, 255), player_rect)
    player_text = font.render(f"Spieler: {player_count}", True, (255, 255, 255))
    screen.blit(player_text, (player_rect.x + 80, player_rect.y + 25))

    # Minus Button
    pygame.draw.rect(screen, (0, 120, 255), minus_button)
    minus_text = font.render("-", True, (255, 255, 255))
    screen.blit(minus_text, (minus_button.x + small_width//2 - 10, minus_button.y + 20))

    # Plut Button
    pygame.draw.rect(screen, (0, 120, 255), plus_button)
    plus_text = font.render("+", True, (255, 255, 255))
    screen.blit(plus_text, (plus_button.x + small_width//2 - 10, plus_button.y + 20))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Start Button Funktionalität & Drawing
            if start_button.collidepoint(event.pos):
                pygame.quit()
                subprocess.run(["python", "main.py", str(player_count)])
                sys.exit()

            # Plus Button Funktionalität & Drawing
            if plus_button.collidepoint(event.pos):
                if player_count < 5:
                    player_count += 1

            # Minus Button Funktionalität & Drawing
            if minus_button.collidepoint(event.pos):
                if player_count > 2:
                    player_count -= 1

    draw_menu()
    pygame.display.flip()