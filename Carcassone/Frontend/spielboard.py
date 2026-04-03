import pygame

import Backend.model as model
from Backend.klassen import *
from Frontend.karten_frontend import *
from Frontend.Button import *
import Backend.control as control

class GameField:
    def __init__(self, rect):
        self.rect = rect
        self.background_color = (20, 20, 20)

        self.grid_width = 100
        self.grid_height = 80
        self.cell_size = 60

        # Center cell indices (internal)
        self.center_col = self.grid_width // 2
        self.center_row = self.grid_height // 2

        self.total_width = self.grid_width * self.cell_size
        self.total_height = self.grid_height * self.cell_size

        # Grid boundaries in world coordinates (center = (0,0) in world)
        self.grid_left = -self.total_width / 2
        self.grid_right = self.total_width / 2
        self.grid_top = -self.total_height / 2
        self.grid_bottom = self.total_height / 2

        viewport_w = self.rect.width
        viewport_h = self.rect.height

        # Zoom Limits
        min_cell_size_px = 20
        min_zoom_by_cell = min_cell_size_px / self.cell_size
        min_zoom_fit = min(viewport_w / self.total_width, viewport_h / self.total_height)
        self.min_zoom = max(min_zoom_fit, min_zoom_by_cell, 0.2)
        self.max_zoom = 4.0

        self.zoom = 1.0
        self.offset_x = -viewport_w / 2   # center of grid initially
        self.offset_y = -viewport_h / 2
        self.clamp_offset()

        self.dragging = False
        self.drag_start = (0, 0)

        self.grid_color_light = (222, 184, 135)
        self.grid_color_dark = (139, 69, 19)
        self.cards = [[None for _ in range(self.grid_height)] for _ in range(self.grid_width)]
        
        # Liste für platzierte Figuren
        self.placed_figures = [] # Speichert dicts: {"lx": x, "ly": y, "img": surface, "local_x": cell_x, "local_y", cell_y}
        self.update_figures()

        self.current_buttons = [] #aktuelle kachel buttons

    def update_figures(self):
        self.placed_figures = []
        field = model.aktiverSpielstand.field
        for key in field.keys():
            col = key[0]
            row = key[1]
            kachel = model.aktiverSpielstand.getKachel(col, row)
            figure = kachel.getFigur()

            if figure is not None:
                # Bilder
                bereich = kachel.getBesetztenBereich()
                bereichPunkt = bereich.getKnopfPosition()
                figure_image = pygame.image.load(rf"./Frontend/Images/{figure.getBesitzer()}.png").convert_alpha()
                figure_image = pygame.transform.smoothscale(figure_image, (200, 200))
                self.place_figure(
                    *figure.getPosition(),
                    figure_image, bereichPunkt[0], 
                    bereichPunkt[1]+0.1, 
                    rotated = type(bereich) == WiesenBereich
                    )

    # ---------- Coordinate conversion (internal) ----------
    def world_to_screen(self, world_x, world_y):
        screen_x = (world_x - self.offset_x) * self.zoom + self.rect.x
        screen_y = (world_y - self.offset_y) * self.zoom + self.rect.y
        return screen_x, screen_y

    def screen_to_world(self, screen_x, screen_y):
        rel_x = screen_x - self.rect.x
        rel_y = screen_y - self.rect.y
        world_x = rel_x / self.zoom + self.offset_x
        world_y = rel_y / self.zoom + self.offset_y
        return world_x, world_y

    def clamp_offset(self):
        vpw = self.rect.width / self.zoom
        vph = self.rect.height / self.zoom

        if vpw >= (self.grid_right - self.grid_left):
            self.offset_x = self.grid_left - (vpw - (self.grid_right - self.grid_left)) / 2
        else:
            min_x = self.grid_left
            max_x = self.grid_right - vpw
            self.offset_x = max(min_x, min(self.offset_x, max_x))

        if vph >= (self.grid_bottom - self.grid_top):
            self.offset_y = self.grid_top - (vph - (self.grid_bottom - self.grid_top)) / 2
        else:
            min_y = self.grid_top
            max_y = self.grid_bottom - vph
            self.offset_y = max(min_y, min(self.offset_y, max_y))

    # ---------- Logical coordinates (center cell = 0,0) ----------
    def _cell_to_logical(self, col, row):
        """Convert internal cell indices (0..grid_width-1, 0..grid_height-1) to logical coordinates."""
        return col - self.center_col, self.center_row - row

    def _logical_to_cell(self, lx, ly):
        """Convert logical coordinates to internal cell indices."""
        return lx + self.center_col,  self.center_row - ly

    def get_cell_at_world(self, world_x, world_y):
        """Return logical coordinates (lx, ly) for a given world position, or None."""
        if not (self.grid_left <= world_x < self.grid_right and self.grid_top <= world_y < self.grid_bottom):
            return None
        col = int((world_x - self.grid_left) // self.cell_size)
        row = int((world_y - self.grid_top) // self.cell_size)
        if 0 <= col < self.grid_width and 0 <= row < self.grid_height:
            return self._cell_to_logical(col, row)
        return None

    def get_cell_at_screen(self, screen_x, screen_y):
        """Return logical coordinates for a screen position, or None."""
        world_x, world_y = self.screen_to_world(screen_x, screen_y)
        return self.get_cell_at_world(world_x, world_y)

    def get_cell_center(self, lx, ly):
        """Return world coordinates of the center of the cell at logical (lx, ly)."""
        col, row = self._logical_to_cell(lx, ly)
        if not (0 <= col < self.grid_width and 0 <= row < self.grid_height):
            raise ValueError(f"Logical coordinates out of bounds: ({lx}, {ly})")
        x = self.grid_left + col * self.cell_size + self.cell_size / 2
        y = self.grid_top + row * self.cell_size + self.cell_size / 2
        return x, y

    def get_cell_rect(self, lx, ly):
        """Return a pygame.Rect (in world coordinates) of the cell at logical (lx, ly)."""
        col, row = self._logical_to_cell(lx, ly)
        x = self.grid_left + col * self.cell_size
        y = self.grid_top + row * self.cell_size
        return pygame.Rect(x, y, self.cell_size, self.cell_size)
    
    def place_card(self, card, lx, ly):
        """Place a card at logical coordinates (lx, ly)."""
        col, row = self._logical_to_cell(lx, ly)

        if 0 <= col < self.grid_width and 0 <= row < self.grid_height:
            self.cards[col][row] = card
            return True
        return False
    
    def is_cell_empty(self, lx, ly):
        """Return True if the cell at logical (lx, ly) is empty."""
        col, row = self._logical_to_cell(lx, ly)
        return self.cards[col][row] is None

    def place_figure(self, lx, ly, figure_img, local_x = 0, local_y = 0, rotated = False):
        """Platziert eine Figur an den logischen Koordinaten (lx, ly)."""
        try:
            self._logical_to_cell(lx, ly) # Validierung der Koordinaten
            self.placed_figures.append({
                "lx": lx, 
                "ly": ly, 
                "local_x": local_x,
                "local_y": local_y,
                "img": figure_img,
                "rotated": rotated
            })
            return True
        except ValueError:
            return False
    
    def get_local_kachel_coords_at_world(self, world_x, world_y):
        """
        by Arman
        Gibt ein Tupel zurück: ((lx, ly), (local_x, local_y))
        lx, ly: Logische Koordinaten der Hauptzelle
        local_x, local_y: Fließkommawerte zwischen -1.0 und 1.0 innerhalb der Zelle
        (-1, -1) ist unten links, (1, 1) ist oben rechts.
        """
        cell = self.get_cell_at_world(world_x, world_y)
        if cell is None:
            return None

        lx, ly = cell
        col, row = self._logical_to_cell(lx, ly)

        # Weltkoordinaten der oberen linken Ecke der Zelle
        cell_left = self.grid_left + col * self.cell_size
        cell_top = self.grid_top + row * self.cell_size

        # Pixel-Position relativ zur oberen linken Ecke der Zelle (0 bis cell_size)
        px_x = world_x - cell_left
        px_y = world_y - cell_top

        # X-Achse mappen: 0 -> -1.0 | cell_size -> 1.0
        local_x = (px_x / self.cell_size) * 2.0 - 1.0
        
        # Y-Achse mappen und umdrehen (da Pygame Y nach unten wächst): 
        # 0 (oben) -> 1.0 | cell_size (unten) -> -1.0
        local_y = 1.0 - (px_y / self.cell_size) * 2.0

        return (lx, ly), (local_x, local_y)

    def get_local_coords_at_screen(self, screen_x, screen_y):
        """Konvertiert Bildschirmkoordinaten direkt in Zelle und lokale Koordinaten.
            by Arman"""
        world_x, world_y = self.screen_to_world(screen_x, screen_y)
        return self.get_local_kachel_coords_at_world(world_x, world_y)
    
    def create_button_at_local_kachel(self, lx, ly, local_x, local_y, color=(255, 0, 0), width=10, height=10, action = lambda x: None):
        """
        Zeichnet ein Rechteck an einer spezifischen lokalen Koordinate innerhalb einer Kachel.
        lx, ly: Logische Koordinaten der Kachel (z.B. 0, 0)
        local_x, local_y: Lokale Koordinaten (-1.0 bis 1.0)
        width, height: Basisgröße des Rechtecks in Pixeln (wird mitgezoomt)
        by Arman
        """
        # 1. Hole die Weltkoordinaten der oberen linken Ecke der Zelle
        cell_rect = self.get_cell_rect(lx, ly)

        # 2. Wandle lokale Koordinaten in Pixel relativ zur Zelle um
        # X: -1.0 -> 0 | 1.0 -> cell_size
        px_x = ((local_x + 1.0) / 2.0) * self.cell_size
        
        # Y: 1.0 -> 0 | -1.0 -> cell_size (Pygame Y-Achse ist umgedreht)
        px_y = ((1.0 - local_y) / 2.0) * self.cell_size

        # 3. Berechne die absolute Weltkoordinate dieses Punktes
        world_x = cell_rect.x + px_x
        world_y = cell_rect.y + px_y

        world_rect = pygame.Rect(
            world_x,
            world_y,
            width,
            height
        )

        button1 = RectButton(world_rect, color, action)
        self.current_buttons.append(button1)
        
        
        
        # 7. Zeichne das Rechteck auf den Bildschirm
        #pygame.draw.rect(screen, color, draw_rect)


    # ---------- Drawing ----------
    def draw_grid(self, screen):
        left = self.offset_x
        top = self.offset_y
        right = left + self.rect.width / self.zoom
        bottom = top + self.rect.height / self.zoom

        start_col = max(0, int((left - self.grid_left) // self.cell_size))
        end_col = min(self.grid_width, int((right - self.grid_left) // self.cell_size) + 1)
        start_row = max(0, int((top - self.grid_top) // self.cell_size))
        end_row = min(self.grid_height, int((bottom - self.grid_top) // self.cell_size) + 1)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                world_x = self.grid_left + col * self.cell_size
                world_y = self.grid_top + row * self.cell_size
                screen_x, screen_y = self.world_to_screen(world_x, world_y)

                cell_w = self.cell_size * self.zoom
                cell_h = self.cell_size * self.zoom

                color = self.grid_color_light if (row + col) % 2 == 0 else self.grid_color_dark
                pygame.draw.rect(screen, color, (screen_x, screen_y, cell_w, cell_h))
                pygame.draw.rect(screen, (100, 70, 40), (screen_x, screen_y, cell_w, cell_h), 1)

    def draw_cards(self, screen):
        field = model.aktiverSpielstand.field
        for key in field.keys():
            col = key[0]
            row = key[1]
            card = model.aktiverSpielstand.getKachel(key[0], key[1])
            
            if card is not None:
                card = card_from_kachel(card)
                # Welt-Rechteck der Zelle (logische Koordinaten)
                lx = col
                ly = row
                rect_world = self.get_cell_rect(lx, ly)
                # Bildschirm-Koordinaten
                screen_x = (rect_world.x - self.offset_x) * self.zoom + self.rect.x
                screen_y = (rect_world.y - self.offset_y) * self.zoom + self.rect.y
                cell_w = rect_world.width * self.zoom
                cell_h = rect_world.height * self.zoom
                # Bild skalieren und zeichnen
                rotationAngle = card.rotation*-90
                rotated_img = pygame.transform.rotate(card.image, rotationAngle)
                scaled_img = pygame.transform.smoothscale(rotated_img, (int(cell_w), int(cell_h)))
                screen.blit(scaled_img, (screen_x, screen_y))

    def create_buttons_for_current_kachel(self):
        lx, ly = model.aktiverSpielstand.getKoordinaten()
        kachel = model.aktiverSpielstand.getKachel(lx, ly)
        for i in range(len(kachel.getBereiche())):
            bereich = kachel.getBereiche()[i]
            local_x, local_y = bereich.getKnopfPosition()
            if control.darfPlatzieren(lx, ly, i):
                self.create_button_at_local_kachel(lx, ly, local_x, local_y, color=(250, 50, 0, 160), width=11, height=11, action = lambda i=i: control.figurSetzen(lx, ly, i))
        # self.draw_rect_at_local_kachel(screen, lx, ly, local_x=1.0, local_y=0.0, color=(0, 255, 0), width=15, height=15)
        # self.draw_rect_at_local_kachel(screen, lx, ly, local_x=0.0, local_y=1.0, color=(0, 255, 0), width=15, height=15)

    def clear_current_buttons(self):
        self.current_buttons = []

    
    def draw_figures(self, screen):
        """Zeichnet alle platzierten Figuren zentriert in ihren Zellen."""
        self.update_figures()
        for fig in self.placed_figures:
            try:
                # 1. Welt-Koordinaten des Zentrums holen
                world_x, world_y = self.get_cell_center(fig["lx"], fig["ly"])
                local_x, local_y = fig["local_x"], fig["local_y"]
                # Wandle lokale Koordinaten in Pixel relativ zur Zelle um
                px_x = (local_x / 2.0) * self.cell_size
                px_y = (local_y / 2.0) * self.cell_size

                # 2. In Bildschirm-Koordinaten umrechnen
                screen_x, screen_y = self.world_to_screen(world_x + px_x, world_y - px_y)
                
                # 3. Größe basierend auf Zoom (ca. 40% der Zellengröße)
                fig_size = int(self.cell_size * self.zoom * 0.4)
                if fig_size < 1: fig_size = 1
                
                # 4. Bild skalieren und zentriert zeichnen
                scaled_fig = pygame.transform.smoothscale(fig["img"], (fig_size, fig_size))
                rotated_fig = pygame.transform.rotate(scaled_fig, 90.0*fig["rotated"])
                dest_rect = scaled_fig.get_rect(center=(screen_x, screen_y))
                screen.blit(rotated_fig, dest_rect)
            except ValueError:
                continue

    # ---------- Event handling ----------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    self.drag_start = event.pos
                    # Debug: print logical coordinates of clicked cell
                    cell = self.get_cell_at_screen(event.pos[0], event.pos[1])
                    if cell:
                        print(f"Clicked cell (logical): {cell}")
                    
                    # Koordinaten in der Zelle
                    result = self.get_local_coords_at_screen(event.pos[0], event.pos[1])
                    if result:
                        (lx, ly), (loc_x, loc_y) = result
                        print(f"Zelle: ({lx}, {ly}) | Lokale Position in der Zelle: ({loc_x:.2f}, {loc_y:.2f})")
                #print(len(self.current_buttons))
                for buttons in self.current_buttons:
                    if buttons.handle_event(event, self.world_to_screen, self.zoom):
                        # control.figurSetzen(1, 0, 0)
                        self.clear_current_buttons()
                               
            elif event.button == 4:  # Scroll up (zoom in)
                self.zoom_in(event.pos)
            elif event.button == 5:  # Scroll down (zoom out)
                self.zoom_out(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = (event.pos[0] - self.drag_start[0]) / self.zoom
                dy = (event.pos[1] - self.drag_start[1]) / self.zoom
                self.offset_x -= dx
                self.offset_y -= dy
                self.clamp_offset()
                self.drag_start = event.pos

    def zoom_in(self, mouse_pos):
        if self.zoom >= self.max_zoom:
            return
        world_x, world_y = self.screen_to_world(mouse_pos[0], mouse_pos[1])
        self.zoom *= 1.2
        self.zoom = min(self.zoom, self.max_zoom)
        new_world_x, new_world_y = self.screen_to_world(mouse_pos[0], mouse_pos[1])
        self.offset_x += world_x - new_world_x
        self.offset_y += world_y - new_world_y
        self.clamp_offset()

    def zoom_out(self, mouse_pos):
        if self.zoom <= self.min_zoom:
            return
        world_x, world_y = self.screen_to_world(mouse_pos[0], mouse_pos[1])
        self.zoom /= 1.2
        self.zoom = max(self.zoom, self.min_zoom)
        new_world_x, new_world_y = self.screen_to_world(mouse_pos[0], mouse_pos[1])
        self.offset_x += world_x - new_world_x
        self.offset_y += world_y - new_world_y
        self.clamp_offset()

    def draw_buttons(self,screen):

        for button in self.current_buttons:
            button.draw_world_to_screen(screen, self.world_to_screen, self.zoom)

    def draw(self, screen):
        #by Azad, Arman, Miguel
        pygame.draw.rect(screen, self.background_color, self.rect)
        screen.set_clip(self.rect)
        self.draw_grid(screen)
        self.draw_cards(screen) 
        self.draw_figures(screen) # Figuren werden über den Karten gezeichnet
        self.draw_buttons(screen)
        screen.set_clip(None)

    def update(self, dt):
        pass