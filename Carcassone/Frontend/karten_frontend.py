import pygame
import random
import os
from Backend.klassen import Kachel

card_images = dict()

class Card:
    """Repräsentiert eine Karte mit Name und Bild."""
    def __init__(self, name, image, rotation = 0):
        self.name = name
        self.image = image
        self.rotation = rotation
    
def card_from_kachel(kachel: Kachel):
    name = kachel.getImageName()
    image = load_card_image(name)
    rotation = kachel.getRotation()
    return Card(name, image, rotation)


def get_random_card(target_size=(150, 200)):
    """
    Lädt alle PNG-Bilder aus dem Ordner "./Frontend/Images/tiles/"
    und wählt eine zufällig aus. Gibt Debug-Infos auf der Konsole aus.
    """
    # Korrigierter Pfad – jetzt im gleichen Ordner wie figure2.png und rotation.png
    card_folder = "./Frontend/Images/tiles/"
    card_images = []

    # Prüfe, ob der Ordner existiert
    if not os.path.isdir(card_folder):
        print(f"WARNUNG: Ordner '{card_folder}' nicht gefunden!")
    else:
        files = os.listdir(card_folder)
        print(f"Gefundene Dateien: {files}")
        for filename in files:
            if filename.lower().endswith('.jpg'):
                full_path = os.path.join(card_folder, filename)
                try:
                    img = pygame.image.load(full_path).convert_alpha()
                    if target_size:
                        img = pygame.transform.smoothscale(img, target_size)
                    card_name = os.path.splitext(filename)[0]
                    card_images.append((card_name, img))
                    #print(f"Geladen: {card_name}")
                except pygame.error as e:
                    print(f"Fehler beim Laden von {full_path}: {e}")

    # Falls keine echten Karten geladen wurden, erzeuge Platzhalter
    if not card_images:
        print("Keine echten Karten geladen – erstelle Platzhalter.")
        for i in range(5):
            surf = pygame.Surface(target_size if target_size else (150, 200))
            surf.fill((240, 240, 240))
            pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 3)
            font = pygame.font.SysFont(None, 24)
            text = font.render(f"Karte {i+1}", True, (0, 0, 0))
            text_rect = text.get_rect(center=surf.get_rect().center)
            surf.blit(text, text_rect)
            card_images.append((f"Karte {i+1}", surf))

    selected_name, selected_image = random.choice(card_images)
    print(f"Ausgewählte Karte: {selected_name}")
    return Card(selected_name, selected_image)

def load_card_image(card_id, target_size = (200, 200)):
    if card_id in card_images.keys():
        return card_images[card_id]
    card_folder = "./Frontend/Images/tiles/"
    img = None
    # Prüfe, ob der Ordner existiert
    if not os.path.isdir(card_folder):
        print(f"WARNUNG: Ordner '{card_folder}' nicht gefunden!")
    else:
        files = os.listdir(card_folder)
        # print(f"Gefundene Dateien: {files}")

        full_path = os.path.join(card_folder, card_id + ".jpg")
        try:
            img = pygame.image.load(full_path).convert_alpha()
            if target_size:
                img = pygame.transform.smoothscale(img, target_size)
            card_name = card_id
            #print(f"Geladen: {card_name}")
        except pygame.error as e:
            print(f"Fehler beim Laden von {full_path}: {e}")
    card_images[card_id] = img
    return img