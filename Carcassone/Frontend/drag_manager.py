import pygame
from Backend.control import *

class DragManager:
    def __init__(self, game_field, right_half_rect):
        self.game_field = game_field
        self.right_half_rect = right_half_rect
        self.dragging = False
        self.drag_card = None
        self.drag_image = None
        self.drag_offset = (0, 0)

    def start_drag(self, card):
        """Startet das Ziehen einer Karte."""
        if card is None:
            return
        self.dragging = True
        self.drag_card = card
        # Erzeuge ein skaliertes Bild für das Ziehen
        if card.image:
            orig_w, orig_h = card.image.get_size()
            target_w = 100
            target_h = int(orig_h * (target_w / orig_w))
            angle = getattr(card, 'angle', 0)
            angle = -card.rotation*90
            rotated_image = pygame.transform.rotate(card.image, angle)
            self.drag_image = pygame.transform.smoothscale(rotated_image, (target_w, target_h))
        else:
            self.drag_image = pygame.Surface((100, 140))
            self.drag_image.fill((200, 200, 200))
            pygame.draw.rect(self.drag_image, (0, 0, 0), self.drag_image.get_rect(), 2)
        self.drag_offset = (self.drag_image.get_width() // 2, self.drag_image.get_height() // 2)

    def end_drag(self, mouse_pos):
        """Beendet das Ziehen und versucht, die Karte auf dem Spielfeld abzulegen.
        Gibt True zurück, wenn die Karte platziert wurde, sonst False."""
        if not self.dragging:
            return False

        placed = False
        if self.right_half_rect.collidepoint(mouse_pos):
            cell = self.game_field.get_cell_at_screen(mouse_pos[0], mouse_pos[1])
            if cell is not None:
                lx, ly = cell
                # print(kachelAnlegen(lx, ly))
                if kachelAnlegenErlaubt(lx, ly) and self.game_field.is_cell_empty(lx, ly):
                    kachelAnlegen(lx, ly)
                    self.game_field.place_card(self.drag_card, lx, ly) 
                    placed = True

        # Zurücksetzen des Drag‑Zustands
        self.dragging = False
        self.drag_card = None
        self.drag_image = None
        return placed

    def is_dragging(self):
        return self.dragging

    def draw(self, screen):
        """Zeichnet die gezogene Karte, falls aktiv."""
        if self.dragging and self.drag_image:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(self.drag_image, (mouse_x - self.drag_offset[0], mouse_y - self.drag_offset[1]))