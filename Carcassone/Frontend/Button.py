import pygame
#Button Klasse by Arman
#Erweiterungen für Kachel Button by Frodo, Arman 
class RectButton():
    def __init__(self, rect, color = (255,0,0), action = lambda x: None):
        self.rect = rect
        self.color = color
        self.action = action

    def handle_event(self, event, world_to_screen = lambda x: x, zoom = 1):
        pos = event.pos
        if self.get_screen_rect(world_to_screen, zoom).collidepoint(pos):
            print("CLICKED")
            self.action()
            return True
    
    def get_screen_rect(self, world_to_screen, zoom):
        screen_x, screen_y = world_to_screen(self.rect.x, self.rect.y)

        # Skaliere das zu zeichnende Rechteck mit dem aktuellen Zoomfaktor
        scaled_w = self.rect.width * zoom
        scaled_h = self.rect.height * zoom
        return pygame.Rect(
            screen_x - (scaled_w / 2),
            screen_y - (scaled_h / 2),
            scaled_w,
            scaled_h
        )

    def set_rect(self,rect):
        self.rect = rect

    def draw(self,screen):
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        
        pygame.draw.rect(s, self.color, s.get_rect())
        screen.blit(s, (self.rect.x, self.rect.y))

    
    def draw_world_to_screen(self,screen, world_to_screen, zoom):
        # 4. Wandle die Weltkoordinate in Bildschirmkoordinaten um (inkl. Zoom & Kamera)
        screen_x, screen_y = world_to_screen(self.rect.x, self.rect.y)

        # 5. Skaliere das zu zeichnende Rechteck mit dem aktuellen Zoomfaktor
        scaled_w = self.rect.width * zoom
        scaled_h = self.rect.height * zoom

        s = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        
        pygame.draw.rect(s, self.color, s.get_rect())
        screen.blit(s, (screen_x- scaled_w//2, screen_y-scaled_h//2))


class CircleButton():
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def point_in_circle(self,point):
        px, py = point
        cx, cy = self.center

        return (px-cx)**2 + (py-cy)**2 <= self.radius**2
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = event.pos
                if self.point_in_circle(pos):
                    print("Clicked")
                    return True
    

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)
    
        