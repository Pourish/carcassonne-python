import os
from Backend.klassen import *
import Backend.save_system as save_system
import Backend.Karteninfo
import random

# --- 1. Karten initialisieren ---
alleKartenTypen = {}
for key in Backend.Karteninfo.info.keys():
    kanten, kloster_wappen = Backend.Karteninfo.info[key]
    kantenTypen = list(map(lambda x: KantenTyp(x), kanten))
    bereiche = Backend.Karteninfo.bereichInfo[key]
    alleKartenTypen[key] = Kartentyp(key, kantenTypen, kloster_wappen[0], kloster_wappen[1], bereiche)


# --- 2. Save/Load Funktionen definieren ---
def load(file_name="spiel.json"):
    global aktiverSpielstand
    aktiverSpielstand = save_system.load(file_name, alleKartenTypen)
    print("Spielstand manuell geladen!")

def save(file_name="spiel.json"):
    save_system.save(aktiverSpielstand, file_name)


# --- 3. IMMER EIN NEUES SPIEL ERSTELLEN (Start from Zero) ---
kartenstapel = []
for key in Backend.Karteninfo.info.keys():
    for i in range(Backend.Karteninfo.kartenAnzahl[key]):
        kartenstapel.append(Kachel(alleKartenTypen[key]))

random.shuffle(kartenstapel)
aktiverSpielstand = Spielzustand(5, kartenstapel, alleKartenTypen["D"])
aktiverSpielstand.field[(0,0)] = Kachel(alleKartenTypen["D"])
aktiverSpielstand.karteZiehen()

# Speichert diesen brandneuen Zustand sofort, damit die Datei von Anfang an existiert
save("spiel.json")