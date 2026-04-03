import pygame
import Frontend.Button as Button
import math
import time
from Frontend.karten_frontend import card_from_kachel
from Backend.model import *#
from Frontend.tutorial import punktvergabe


class LeftPanel:
    def __init__(self, rect, font_name, font_score, figure_images, rotation_image, player_count):
        self.rect = rect
        self.font_name = font_name
        self.font_score = font_score
        self.figure_images = figure_images
        self.rotation_image = rotation_image
        self.rotate_angle = 0
        self.player_count = player_count
        self.info_scroll_offset = 0

        # Spielerdaten
        self.players = [
            {"name": f"Spieler {i+1}", "score": 0} for i in range(player_count)
        ]

        # Blink-Variablen
        self.blink_timer = 0
        self.blink_state = True  # True = Grün, False = Rot
        self.blink_speed = 0.5  # Sekunden pro Wechsel (0.5 = 2x pro Sekunde)
        
        # Geometrie
        self.margin = 20
        self.spacing = 15
        self.circle_radius = 80
        self.circle_height = 2 * self.circle_radius
        self.spieler_height = 80
        self.middle_height = 200
        

        # Höhenberechnung für Zentrierung
        total_height = (5 * self.spieler_height +
                        self.middle_height +
                        self.circle_height +
                        (5 + 1 + 1) * self.spacing)
        start_y = self.margin + (self.rect.height - 2 * self.margin - total_height) // 2

        # Spieler-Rechtecke
        self.player_rects = []
        self.activePlayerIndex = 0
        for i in range(self.player_count):
            x = self.margin
            y = start_y + i * (self.spieler_height + self.spacing)
            rect = pygame.Rect(x, y, self.rect.width - 2 * self.margin, self.spieler_height)
            self.player_rects.append(rect)

        sample_rect = self.player_rects[0]
        self.player_gb_image = pygame.image.load("Frontend/Images/spieler_rechtecke.png").convert()
        self.player_gb_image = pygame.transform.smoothscale(self.player_gb_image, (sample_rect.width, sample_rect.height))

        # Mittleres Rechteck.Surface((self.rect.width - 2 * self.margin, self.middle_height))
        self.image = pygame.image.load("Frontend/Images/Rückseite.jpeg").convert()
        #self.image = pygame.transform.smoothscale(self.image, (self.rect.width - 2 * self.margin, self.middle_height))
        middle_rect_y = start_y + 5 * (self.spieler_height + self.spacing)
        self.middle_rect = pygame.Rect(self.margin, middle_rect_y,
                                       self.rect.width - 4 * self.margin, self.middle_height)
        
        self.background_image = pygame.image.load("Frontend/Images/left_panel.png").convert()
        self.background_image = pygame.transform.smoothscale(self.background_image, (self.rect.width, self.rect.height))

        # Kreis-Button
        circle_x = self.rect.width // 2
        circle_y = middle_rect_y + self.middle_height + self.spacing + self.circle_radius
        self.circle_button = Button.CircleButton(
            (self.rect.x + circle_x, self.rect.y + circle_y),
            self.circle_radius,
            (0, 255, 0)
        )
        # INFO BUTTON
        self.info_button_radius = 20
        self.info_button_center = (
            self.circle_button.center[0] + self.circle_radius + 50,
            self.circle_button.center[1] + self.circle_radius + 40
        )

        self.show_info = False
        self.info_text = ""
        self.info_font = pygame.font.SysFont("arial", 18)

        self.current_card = card_from_kachel(aktiverSpielstand.getAktuelleKachel())

        card_w, card_h = self.current_card.image.get_size()

        self.image = pygame.image.load("Frontend/Images/Rückseite.jpeg").convert()
        max_w = self.middle_rect.width * 0.8
        max_h = self.middle_rect.height * 0.8
        orig_w, orig_h = self.image.get_size()
        scale = min(max_w / orig_w, max_h / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        self.image = pygame.transform.smoothscale(self.image, (new_w, new_h))

    def updatePunkte(self, punkteListe:list[int]):
        """übernimmt übergebene Punkteliste als neue Punkte"""
        for i in range(len(self.players)):
            self.players[i]['score'] = punkteListe[i]

    def update(self, dt):
        """Aktualisiert den Blink-Timer (muss in der Hauptschleife aufgerufen werden)"""
        self.blink_timer += dt
        if self.blink_timer >= self.blink_speed:
            self.blink_timer = 0
            self.blink_state = not self.blink_state  # Farbe wechseln

    def draw(self, screen):
        self.activePlayerIndex = aktiverSpielstand.getAktuellerSpielerIndex()
        """Zeichnet die linke Hälfte komplett."""
        # Hintergrund
        if self.background_image:
            screen.blit(self.background_image, self.rect)
        else:
            pygame.draw.rect(screen, (40, 40, 40), self.rect) 



        # Spieler-Rechtecke
        for i, rect in enumerate(self.player_rects):
            if self.activePlayerIndex == i:
                scale_factor = 1.10
                new_h = int(rect.height * scale_factor)
                new_w = int(rect.width * scale_factor)
                scaled_bg = pygame.transform.smoothscale(self.player_gb_image, (new_w, new_h))
                bg_rect = scaled_bg.get_rect(center=rect.center)
                screen.blit(scaled_bg, bg_rect)
                border_color = (20, 160, 0)  if self.blink_state else (255, 0, 0)
                pygame.draw.rect(screen, border_color, bg_rect, 6)
            else:
                screen.blit(self.player_gb_image, rect)
                pygame.draw.rect(screen, (0, 0, 255), rect, 2)

            if hasattr(self, 'player_gb_image'):
                screen.blit(self.player_gb_image, rect)
            else:
                pygame.draw.rect(screen, (0,0,255), rect)  # Blau als Platzhalter
            if self.activePlayerIndex == i:
                pygame.draw.rect(screen, (20, 160, 0), rect)  # Grün für aktiven Spieler
                screen.blit(self.player_gb_image, rect)
            # Standardfarbe für inaktive Spieler
            
            if self.activePlayerIndex == i:
                # Aktiver Spieler - blinkt zwischen Grün und Rot
                if self.blink_state:
                    color = (20, 160, 0)  # Grün
                else:
                    color = (255, 0, 0)   # Rot
            else:
                color = (0, 0, 255)  # Blau für inaktive
            
            
            player = self.players[i]

            name_surface = self.font_name.render(player["name"], True, (255, 255, 255))
            screen.blit(name_surface, (rect.x + 10, rect.y + 5))

            score_surface = self.font_score.render(f"Punkte: {player['score']}", True, (200, 200, 200))
            screen.blit(score_surface, (rect.x + 10, rect.y + 40))

            # Figuren anzeigen
            figure_size = 20
            spacing = 5
            figuren_anzahl = aktiverSpielstand.getFigurenanzahl(i)
            start_x = rect.right - (figuren_anzahl * (figure_size + spacing)) + spacing
            start_y = rect.bottom - figure_size - 5
            for f in range(figuren_anzahl):
                fx = start_x + f * (figure_size + spacing)
                fy = start_y
                # Schatten-effekt
                img = self.figure_images[i].copy()
                img.fill((150, 150, 150, 255), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(img, (fx+2, fy-1))
                screen.blit(self.figure_images[i], (fx, fy))

        # Bild zentriert im middle_rect zeichnen
        bg_rect = self.image.get_rect(center=self.middle_rect.center)
        screen.blit(self.image, bg_rect)
        # Aktuelle Karte
        if self.current_card.image:
            if aktiverSpielstand.aktuelleKachel.getPosition() == (0,0):
                rotated_image = pygame.transform.rotate(self.current_card.image, -self.current_card.rotation*90)

                max_w = self.middle_rect.width * 0.8
                max_h = self.middle_rect.height * 0.8
                orig_w, orig_h = rotated_image.get_size()
                scale = min(max_w / orig_w, max_h / orig_h)
                new_w, new_h = int(orig_w * scale), int(orig_h * scale)

                scaled_card = pygame.transform.smoothscale(rotated_image, (new_w, new_h))
                card_rect = scaled_card.get_rect(center=self.middle_rect.center)
                screen.blit(scaled_card, card_rect)

        # Kreis-Button
        self.circle_button.draw(screen)
        img_rect = self.rotation_image.get_rect(center=self.circle_button.center)
        screen.blit(self.rotation_image, img_rect)

        # INFO BUTTON zeichnen
        pygame.draw.circle(screen, (70, 130, 255), self.info_button_center, self.info_button_radius)
        i_text = self.info_font.render("i", True, (255, 255, 255))
        screen.blit(i_text, i_text.get_rect(center=self.info_button_center))

    def draw_overlay(self, screen):
        if self.show_info:
            self.draw_info_popup(screen)


    def circle_handle_event(self, event):
        """Leitet Events an den Kreis‑Button weiter."""
        self.circle_button.handle_event(event)

        # Mausrad scrollt das Popup
        if self.show_info and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.info_scroll_offset = max(0, self.info_scroll_offset - 30)
                return True
            if event.button == 5:
                self.info_scroll_offset += 30
                return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # X-Button schließt Popup
            if self.show_info and hasattr(self, 'info_close_rect'):
                if self.info_close_rect.collidepoint(mx, my):
                    self.show_info = False
                    return True

            # Info-Button
            cx, cy = self.info_button_center
            if math.hypot(mx - cx, my - cy) <= self.info_button_radius:
                print("Info")
                self.show_info = not self.show_info
                self.info_scroll_offset = 0  # Scroll zurücksetzen beim Öffnen
                self.info_text = punktvergabe()
                return True

            # Rotations-Button
            cx, cy = self.circle_button.center

            if math.hypot(mx - cx, my - cy) <= self.circle_radius:
                # self.rotate_angle = (self.rotate_angle + 90) % 360
                aktiverSpielstand.aktuelleKachelRotateLeft()
                self.current_card = card_from_kachel(aktiverSpielstand.getAktuelleKachel())
                self.rotate_angle = 90 * self.current_card.rotation
                print(self.rotate_angle)
                return True

        return False

    def get_card_at_middle(self, mouse_pos):
        """Prüft, ob der Mausklick auf der Karte im mittleren Rechteck war."""
        if self.middle_rect.collidepoint(mouse_pos):
            self.current_card.angle = self.rotate_angle 
            return True, self.current_card
        return False, None

    def replace_current_card(self):
        """Ersetzt die aktuelle Karte durch eine neue."""
        self.current_card = card_from_kachel(aktiverSpielstand.getAktuelleKachel())
        self.rotate_angle = (90 * self.current_card.rotation) % 360

        card_w, card_h = self.current_card.image.get_size()
        self.image = pygame.transform.smoothscale(self.image, (card_w, card_h))

    def draw_info_popup(self, screen):
        width, height = 750, 700
        rect = pygame.Rect(
            screen.get_width() // 2 - width // 2,
            screen.get_height() // 2 - height // 2,
            width, height
        )

        pygame.draw.rect(screen, (30, 30, 30), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        # X-Button
        self.info_close_rect = pygame.Rect(rect.right - 35, rect.top + 5, 28, 28)
        pygame.draw.rect(screen, (180, 50, 50), self.info_close_rect, border_radius=5)
        close_txt = self.info_font.render("X", True, (255, 255, 255))
        screen.blit(close_txt, close_txt.get_rect(center=self.info_close_rect.center))

        replacements = {
            "🏆": "(Punkte) ", "🏰": "(Stadt)  ", "👉": "->  ",
            "🛣": "(Weg)    ", "⛪": "(Kloster)", "👥": "(Figuren)",
            "🧾": "(Ende)   ",
        }

        info_font = pygame.font.SysFont("arial", 19)
        title_font = pygame.font.SysFont("arial", 22, bold=True)

        line_height = 26
        padding = 20
        content_top = rect.y + 45
        content_bottom = rect.bottom - 15

        # Alle Zeilen vorbereiten
        lines = []
        for line in self.info_text.split("\n"):
            line = line.strip()
            for emoji, rep in replacements.items():
                line = line.replace(emoji, rep)
            lines.append(line)

        # Gesamthöhe berechnen für Scrollbar
        total_height = len(lines) * line_height
        visible_height = content_bottom - content_top
        max_scroll = max(0, total_height - visible_height)
        self.info_scroll_offset = max(0, min(self.info_scroll_offset, max_scroll))

        # Clipping auf Popup-Inhalt
        clip_rect = pygame.Rect(rect.x, content_top, width, visible_height)
        screen.set_clip(clip_rect)

        y = content_top - self.info_scroll_offset
        for line in lines:
            if y + line_height < content_top:
                y += line_height
                continue

            if line.startswith("---") or line.startswith("___"):
                pygame.draw.line(screen, (120, 120, 120),
                                 (rect.x + 10, y + 8), (rect.right - 10, y + 8), 1)
            else:
                is_title = any(line.startswith(p) for p in
                               ["(Punkte)", "(Stadt)", "(Weg)", "(Kloster)", "(Figuren)", "(Ende)"])
                font = title_font if is_title else info_font
                color = (255, 220, 50) if is_title else (220, 220, 220)
                txt = font.render(line, True, color)
                screen.blit(txt, (rect.x + padding, y))

            y += line_height

        screen.set_clip(None)

        # Scrollbar zeichnen
        if max_scroll > 0:
            bar_x = rect.right - 12
            bar_total = visible_height
            bar_h = max(30, int(bar_total * visible_height / total_height))
            bar_y = content_top + int((self.info_scroll_offset / max_scroll) * (bar_total - bar_h))
            pygame.draw.rect(screen, (100, 100, 100), (bar_x, content_top, 8, bar_total), border_radius=4)
            pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, 8, bar_h), border_radius=4)