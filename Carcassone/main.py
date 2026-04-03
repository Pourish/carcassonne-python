import os

import pygame
import sys
from Frontend.Button import *
from Backend.control import *
from Backend.model import *
from Frontend.spielboard import GameField
from Frontend.karten_frontend import get_random_card
from Frontend.left_panel import LeftPanel
from Frontend.drag_manager import DragManager
from Frontend.tutorial import TutorialManager, TutorialAction

# pygame Setup
pygame.init()
pygame.font.init()

# Spieleranzahl (kann über Kommandozeile gesetzt werden)
if len(sys.argv) > 1:
    player_count = int(sys.argv[1])
else:
    player_count = 2
aktiverSpielstand.setSpieleranzahl(player_count)

# Vollbild
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
print(f"Bildschirmgröße: {WIDTH}x{HEIGHT}")

background_path = os.path.join("Frontend", "Images", "hintergrund.png")
try:
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    use_background = True
    print("Background loaded")
except FileNotFoundError:
    print(f"Warning: {background_path} not found. Using black background.")
    use_background = False

music_path = os.path.join("Frontend", "sound", "background.mp3")
try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
    update_music_volume()  # Wende Lautstärke-Einstellungen an
    print("Background music started")
except Exception as e:
    print(f"Could not load music: {e}")

# --- Sound Effects laden ---
use_sfx = True
city_sound = None
church_sound = None
field_sound = None
turn_around_sound = None
meeple_sound = None
click_sound = None

try:
    print("Loading: city.mp3...")
    city_sound = pygame.mixer.Sound(os.path.join("Frontend", "sound", "city.mp3"))
    city_sound.set_volume(0.8)
    print("✓ city.mp3 loaded")
except Exception as e:
    print(f"✗ Could not load city.mp3: {e}")
    
try:
    print("Loading: field.mp3...")
    field_sound = pygame.mixer.Sound(os.path.join("Frontend", "sound", "field.mp3"))
    field_sound.set_volume(1.5)
    print("✓ field.mp3 loaded")
except Exception as e:
    print(f"✗ Could not load field.mp3: {e}")
    
try:
    print("Loading: turn_around.mp3...")
    turn_around_sound = pygame.mixer.Sound(os.path.join("Frontend", "sound", "turn_around.mp3"))
    turn_around_sound.set_volume(0.8)
    print("✓ turn_around.mp3 loaded")
except Exception as e:
    print(f"✗ Could not load turn_around.mp3: {e}")
    
try:
    print("Loading: meeple.mp3...")
    meeple_sound = pygame.mixer.Sound(os.path.join("Frontend", "sound", "meeple.mp3"))
    meeple_sound.set_volume(0.8)
    print("✓ meeple.mp3 loaded")
except Exception as e:
    print(f"✗ Could not load meeple.mp3: {e}")
    
try:
    print("Loading: click.wav...")
    click_sound = pygame.mixer.Sound(os.path.join("Frontend", "sound", "click.wav"))
    click_sound.set_volume(0.8)
    print("✓ click.wav loaded")
except Exception as e:
    print(f"✗ Could not load click.wav: {e}")
    
try:
    print("Loading: church.mp3...")
    church_sound = pygame.mixer.Sound(os.path.join("Frontend", "sound", "church.mp3"))
    church_sound.set_volume(0.8)
    print("✓ church.mp3 loaded")
except Exception as e:
    print(f"✗ Could not load church.mp3: {e}")

print("Carcassonne Sound effects loaded")

# --- Globale Einstellungsvariablen ---
music_enabled = True
sfx_enabled = True
master_volume = 0.7  # 0.0 - 1.0
music_volume = 0.3   # 0.0 - 1.0 (Background-Musik auf 0.3)

def play_sfx(sound, maxtime=0):
    if sfx_enabled and sound:
        sound.set_volume(master_volume)
        if maxtime > 0:
            sound.play(maxtime=maxtime)
        else:
            sound.play()

def update_music_volume():
    """Aktualisiert die Musik-Lautstärke basierend auf Einstellungen"""
    if music_enabled:
        pygame.mixer.music.set_volume(master_volume * music_volume)
    else:
        pygame.mixer.music.set_volume(0)

# -------------------- Start Screen --------------------
def show_start_screen():
    font_name = pygame.font.SysFont(None, 100)
    button_image_path = os.path.join("Frontend", "Images", "Start_button.png")
    try:
        start_button_img = pygame.image.load(button_image_path).convert_alpha()
        # Scale the image to a reasonable size, e.g., 300x100
        start_button_img = pygame.transform.scale(start_button_img, (300, 100))
        use_img_button = True
    except FileNotFoundError:
        print(f"Warning: {button_image_path} not found. Using rectangle button.")
        use_img_button = False

    # Create rect for the button (same size regardless)
    button_width = 300
    button_height = 100
    button_rect = pygame.Rect(WIDTH // 2 - button_width // 2,
                              HEIGHT // 2 - button_height // 2,
                              button_width, button_height)
    
    start_screen_running = True
    while start_screen_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    play_sfx(click_sound)
                    return  # Start button clicked -> exit start screen

        # Draw
        if use_background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((30, 30, 30))
        
        # Draw start button
        if use_img_button:
            screen.blit(start_button_img, button_rect)
        else:
            pygame.draw.rect(screen, (0, 150, 0), button_rect, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), button_rect, 3, border_radius=15)
            start_text = font_name.render("START", True, (255, 255, 255))
            screen.blit(start_text, start_text.get_rect(center=button_rect.center))
        
        pygame.display.flip()
        pygame.time.wait(10)  

# Show start screen
show_start_screen()

# -------------------- Einstellungen Menü --------------------
def show_settings():
    """Zeigt das Einstellungs-Menü an"""
    global music_enabled, sfx_enabled, master_volume
    
    font_big = pygame.font.SysFont(None, 70)
    font = pygame.font.SysFont(None, 50)
    font_small = pygame.font.SysFont(None, 40)
    
    button_width = 400
    button_height = 80
    gap = 20
    center_x = WIDTH // 2
    
    # Musik Toggle
    music_button = pygame.Rect(center_x - button_width//2, HEIGHT//2 - 250, button_width, button_height)
    
    # SFX Toggle
    sfx_button = pygame.Rect(center_x - button_width//2, HEIGHT//2 - 100, button_width, button_height)
    
    # Lautstärke Regler
    volume_bar_width = 400
    volume_bar_height = 50
    volume_bar = pygame.Rect(center_x - volume_bar_width//2, HEIGHT//2 + 50, volume_bar_width, volume_bar_height)
    
    # Zurück Button
    back_button_width = 300
    back_button = pygame.Rect(center_x - back_button_width//2, HEIGHT//2 + 200, back_button_width, button_height)
    
    if use_background:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
    else:
        overlay = None
    
    def draw_settings():
        if use_background:
            screen.blit(background, (0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill((30, 30, 30))
        
        # Titel
        title_text = font_big.render("EINSTELLUNGEN", True, (255, 255, 255))
        screen.blit(title_text, (center_x - title_text.get_width()//2, 50))
        
        # Musik Button
        music_color = (0, 200, 0) if music_enabled else (100, 100, 100)
        pygame.draw.rect(screen, music_color, music_button)
        music_text = font.render(f"Musik: {'ON' if music_enabled else 'OFF'}", True, (255, 255, 255))
        screen.blit(music_text, (music_button.x + 50, music_button.y + 15))
        
        # SFX Button
        sfx_color = (0, 200, 0) if sfx_enabled else (100, 100, 100)
        pygame.draw.rect(screen, sfx_color, sfx_button)
        sfx_text = font.render(f"Effekte: {'ON' if sfx_enabled else 'OFF'}", True, (255, 255, 255))
        screen.blit(sfx_text, (sfx_button.x + 50, sfx_button.y + 15))
        
        # Lautstärke Label
        vol_label = font.render("Lautstärke:", True, (255, 255, 255))
        screen.blit(vol_label, (center_x - volume_bar_width//2, HEIGHT//2 + 10))
        
        # Lautstärke Bar Hintergrund
        pygame.draw.rect(screen, (50, 50, 50), volume_bar)
        pygame.draw.rect(screen, (255, 255, 255), volume_bar, 3)
        
        # Lautstärke Füllbalken
        fill_width = int(volume_bar_width * master_volume)
        fill_rect = pygame.Rect(volume_bar.x, volume_bar.y, fill_width, volume_bar_height)
        pygame.draw.rect(screen, (0, 200, 100), fill_rect)
        
        # Lautstärke Wert anzeigen
        vol_value = font_small.render(f"{int(master_volume * 10)}/10", True, (255, 255, 255))
        screen.blit(vol_value, (volume_bar.x + volume_bar_width + 20, volume_bar.y + 5))
        
        # Zurück Button
        pygame.draw.rect(screen, (180, 50, 50), back_button)
        back_text = font.render("ZURÜCK", True, (255, 255, 255))
        screen.blit(back_text, (back_button.x + 50, back_button.y + 15))
    
    settings_running = True
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if music_button.collidepoint(event.pos):
                    play_sfx(click_sound)
                    music_enabled = not music_enabled
                    update_music_volume()
                    
                if sfx_button.collidepoint(event.pos):
                    play_sfx(click_sound)
                    sfx_enabled = not sfx_enabled
                    
                if back_button.collidepoint(event.pos):
                    play_sfx(click_sound)
                    settings_running = False
                    
            # Lautstärke mit Mausklick auf Bar
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volume_bar.collidepoint(event.pos):
                    # Berechne neue Lautstärke basierend auf Klick
                    click_x = event.pos[0] - volume_bar.x
                    master_volume = max(0.0, min(1.0, click_x / volume_bar_width))
                    update_music_volume()
                    play_sfx(click_sound)
        
        draw_settings()
        pygame.display.flip()

# -------------------- Menü --------------------
def show_menu():
    """Zeigt das Menü an und gibt (player_count, tutorial_enabled) zurück."""
    font_big = pygame.font.SysFont(None, 80)
    font = pygame.font.SysFont(None, 60)

    player_count = 2
    tutorial_enabled = False

    button_width = 400
    button_height = 100
    gap = 20
    center_x = WIDTH // 2

    start_button = pygame.Rect(center_x - button_width//2, HEIGHT//2 - 250, button_width, button_height)
    settings_button = pygame.Rect(center_x - button_width//2, HEIGHT//2 - 100, button_width, button_height)
    player_rect = pygame.Rect(center_x - button_width//2, HEIGHT//2 + 50, button_width, button_height)
    small_width = (button_width - gap) // 2
    minus_button = pygame.Rect(center_x - button_width//2, HEIGHT//2 + 170, small_width, button_height)
    plus_button = pygame.Rect(center_x - button_width//2 + small_width + gap, HEIGHT//2 + 170, small_width, button_height)
    tutorial_button = pygame.Rect(center_x - button_width//2, HEIGHT//2 + 290, button_width, button_height)

    if use_background:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
    else:
        overlay = None

    def draw_menu():
        if use_background:
            screen.blit(background, (0, 0))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill((30, 30, 30))
        # Start
        pygame.draw.rect(screen, (0, 120, 255), start_button)
        start_text = font_big.render("START", True, (255, 255, 255))
        screen.blit(start_text, start_text.get_rect(center=start_button.center))
        # Settings
        pygame.draw.rect(screen, (120, 120, 0), settings_button)
        settings_text = font.render("EINSTELLUNGEN", True, (255, 255, 255))
        screen.blit(settings_text, (settings_button.x + 30, settings_button.y + 20))
        # Spieleranzahl
        pygame.draw.rect(screen, (0, 120, 255), player_rect)
        player_text = font.render(f"Spieler: {player_count}", True, (255, 255, 255))
        screen.blit(player_text, (player_rect.x + 80, player_rect.y + 25))
        # Minus
        pygame.draw.rect(screen, (0, 120, 255), minus_button)
        minus_text = font.render("-", True, (255, 255, 255))
        screen.blit(minus_text, (minus_button.x + small_width//2 - 10, minus_button.y + 20))
        # Plus
        pygame.draw.rect(screen, (0, 120, 255), plus_button)
        plus_text = font.render("+", True, (255, 255, 255))
        screen.blit(plus_text, (plus_button.x + small_width//2 - 10, plus_button.y + 20))
        # Tutorial Toggle
        color = (0, 200, 0) if tutorial_enabled else (100, 100, 100)
        pygame.draw.rect(screen, color, tutorial_button)
        tutorial_text = font.render(f"Tutorial: {'ON' if tutorial_enabled else 'OFF'}", True, (255, 255, 255))
        screen.blit(tutorial_text, (tutorial_button.x + 80, tutorial_button.y + 25))

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    play_sfx(click_sound)
                    menu_running = False
                if settings_button.collidepoint(event.pos):
                    play_sfx(click_sound)
                    show_settings()
                if plus_button.collidepoint(event.pos) and player_count < 5:
                    play_sfx(click_sound)
                    player_count += 1
                if minus_button.collidepoint(event.pos) and player_count > 2:
                    play_sfx(click_sound)
                    player_count -= 1
                if tutorial_button.collidepoint(event.pos):
                    play_sfx(click_sound)
                    tutorial_enabled = not tutorial_enabled
        draw_menu()
        pygame.display.flip()

    return player_count, tutorial_enabled

# -------------------- Spiel starten --------------------
player_count, tutorial_enabled = show_menu()
model.aktiverSpielstand.setSpieleranzahl(player_count)


# Spiel initialisieren
clock = pygame.time.Clock()
running = True

# Bereiche
left_rect = pygame.Rect(0, 0, WIDTH // 5, HEIGHT)
right_rect = pygame.Rect(WIDTH // 5, 0, WIDTH * 4 // 5, HEIGHT)

# Schriften
font_name = pygame.font.SysFont(None, 36)
font_score = pygame.font.SysFont(None, 28)
font_toolbar = pygame.font.SysFont(None, 28)
font_skip = pygame.font.SysFont(None, 48)

# Bilder
figure_images = []
for i in range(player_count):
    figure_image = pygame.image.load(rf"./Frontend/Images/{i}.png").convert_alpha()
    figure_image = pygame.transform.smoothscale(figure_image, (20, 20))
    figure_images.append(figure_image)

rotation_image = pygame.image.load(r"./Frontend/Images/rotation.png").convert_alpha()
rotation_image = pygame.transform.smoothscale(rotation_image, (80 * 1.5, 80 * 1.5))

# Linkes Panel
left_panel = LeftPanel(left_rect, font_name, font_score, figure_images, rotation_image, player_count)

# Spielfeld
start_card = get_random_card()
game_field = GameField(right_rect)
game_field.place_card(start_card, 0, 0)
# game_field.place_figure(0, 0, figure_image)

# Drag Manager
drag_manager = DragManager(game_field, right_rect)

# Close‑Button
close_button = pygame.Rect(WIDTH - 40, 10, 30, 25)

# Tutorial nur bei Bedarf erstellen
if tutorial_enabled:
    tutorial = TutorialManager(screen, left_panel, game_field)
else:
    tutorial = None

# -------------------- Skip‑Buttons --------------------
# Skip‑Button für das gesamte Spiel (unten mittig)
skip_button_width = 250
skip_button_height = 60
skip_button = pygame.Rect(
    (WIDTH // 2) - (skip_button_width // 2),
    HEIGHT - skip_button_height - 40,
    skip_button_width,
    skip_button_height
)

# Skip‑Button für die Karte (im linken Panel)
skip_button_karte_width = 200
skip_button_karte_height = 40
skip_button_karte = pygame.Rect(
    left_rect.centerx - (skip_button_karte_width // 2),
    left_rect.bottom - skip_button_karte_height - 20,
    skip_button_karte_width,
    skip_button_karte_height
)

# Farben
skip_button_color = (100, 100, 100)
skip_button_hover_color = (150, 150, 150)
skip_button_current_color = skip_button_color


# -------------------- Hauptschleife --------------------
while running:
    dt = clock.tick(60) / 1000.0

    # Mausposition für Hover-Effekt
    mouse_pos = pygame.mouse.get_pos()
    skip_button_current_color = skip_button_hover_color if skip_button.collidepoint(mouse_pos) else skip_button_color

    # Event‑Verarbeitung
    for event in pygame.event.get():
        if tutorial and tutorial.handle_event(event):
            continue
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                zugBeenden()
                game_field.clear_current_buttons()
            if event.key == pygame.K_LEFT:
                model.aktiverSpielstand.aktuelleKachelRotateLeft()
                play_sfx(turn_around_sound, maxtime=1000)
            if event.key == pygame.K_RIGHT:
                model.aktiverSpielstand.aktuelleKachelRotateRight()
                play_sfx(turn_around_sound, maxtime=1000)

        # 1. NEW: Handle Left Panel first (Info Button, Scrolling in Popup, Rotation)
        handled_by_left = left_panel.circle_handle_event(event)
        if handled_by_left:
            play_sfx(click_sound, maxtime=1000)
            play_sfx(turn_around_sound, maxtime=1000)  # ROTATION SOUND (1 Sekunde)
            if tutorial:
                tutorial.report_action(TutorialAction.ROTATE_CARD)
            continue # Skip the rest if the panel handled the click/scroll
            
        # 2. NEW: Block all other interactions (Zoom, Pan, Drag) if the info popup is open
        if left_panel.show_info:
            continue
        
        # Close‑Button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if close_button.collidepoint(event.pos):
                play_sfx(click_sound)
                running = False

        # Skip‑Button (unterer Bildschirmrand)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if skip_button.collidepoint(event.pos):
                play_sfx(click_sound)
                print("=== SKIP WURDE GEDRÜCKT! ===")
                #left_panel.replace_current_card()
                zugBeenden()
                game_field.clear_current_buttons()

        # Skip‑Button für Karte (linkes Panel)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if skip_button_karte.collidepoint(event.pos):
                play_sfx(click_sound)
                print("=== SKIP KARTE WURDE GEDRÜCKT! ===")
                aktiverSpielstand.karteZiehen()        # nächste Karte im Backend holen
                left_panel.replace_current_card()      # aktuelle Karte im Frontend aktualisieren

        # Drag‑Start (Karte vom linken Panel ziehen)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not drag_manager.is_dragging():
                clicked, card = left_panel.get_card_at_middle(event.pos)
                if clicked:
                    play_sfx(click_sound)
                    drag_manager.start_drag(card)

        # Drag‑Ende (Karte auf dem Spielfeld ablegen) - TILE PLATZIERUNG
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drag_manager.is_dragging():
                placed = drag_manager.end_drag(event.pos)
                if placed:
                    # Sound abhängig vom Kartentyp abspielen - TILE/FIELD SOUND (1 Sekunde)
                    try:
                        kachel = model.aktiverSpielstand.aktuelleKachel
                        if getattr(kachel, 'kloster', False) or getattr(kachel, 'cloister', False):
                            play_sfx(church_sound, maxtime=1000)
                        elif getattr(kachel, 'stadt', False) or getattr(kachel, 'cities', []):
                            play_sfx(city_sound, maxtime=1000)
                        else:
                            play_sfx(field_sound, maxtime=1000)
                    except:
                        play_sfx(field_sound, maxtime=1000) # Standard-Feld Sound als Fallback

                    game_field.clear_current_buttons()      
                    game_field.create_buttons_for_current_kachel()
                    if tutorial:
                        tutorial.report_action(TutorialAction.PLACE_CARD)
                    #zugBeenden()# Backend: Spielzug beenden
                    #left_panel.replace_current_card()   # Neue Karte anzeigen
                # (Keine weitere Verwendung von 'placed' ausserhalb dieses Blocks)

        # Mausrad zum Zoomen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5):   # 4 = nach oben scrollen, 5 = nach unten
                if right_rect.collidepoint(mouse_pos):
                    if tutorial:
                        tutorial.report_action(TutorialAction.ZOOM_BOARD)

        # Spielfeld-Events (nur wenn nicht gezogen wird)
        if not drag_manager.is_dragging():
            # Meeple-Platzierung - Sound bei Klick auf Spielfeld
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if right_rect.collidepoint(event.pos):
                    play_sfx(meeple_sound, maxtime=1000)  # MEEPLE SOUND (1 Sekunde)
            game_field.handle_event(event)

    # --- Zeichnen ---
    if use_background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((30, 30, 30))

    left_panel.updatePunkte(aktiverSpielstand.getPunkte())
    left_panel.draw(screen)
    game_field.draw(screen)
    game_field.update(dt)
    drag_manager.draw(screen)
    left_panel.draw_overlay(screen)
    left_panel.replace_current_card()


    # Close‑Button zeichnen
    pygame.draw.rect(screen, (180, 50, 50), close_button, border_radius=6)
    text = font_toolbar.render("X", True, (255, 255, 255))
    text_rect = text.get_rect(center=close_button.center)
    screen.blit(text, text_rect)

    # Skip‑Button (unten) zeichnen
    pygame.draw.rect(screen, (0, 200, 100), skip_button, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), skip_button, 3, border_radius=10)
    if model.aktiverSpielstand.spielende:
        skip_text = font_skip.render("Spielende", True, (255, 255, 255))
    else:
        skip_text = font_skip.render("Zug beenden", True, (255, 255, 255))
    screen.blit(skip_text, skip_text.get_rect(center=skip_button.center))

    # Skip‑Button (Karte im linken Panel) zeichnen
    pygame.draw.rect(screen, (0, 200, 100), skip_button_karte, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), skip_button_karte, 3, border_radius=10)
    skip_karte_text = font_skip.render("SKIP KARTE", True, (255, 255, 255))
    screen.blit(skip_karte_text, skip_karte_text.get_rect(center=skip_button_karte.center))

    # Tutorial zeichnen (nur wenn aktiv)
    if tutorial:
        tutorial.draw()

    pygame.display.flip()

pygame.quit()