from enum import Enum

# Frodo
class Richtung(Enum):
    # Richtung.TOP = Richtung(0,1) = Richtung["TOP"]
    # zweiter Index gibt die Position auf der Kante an (im Uhrzeigersinn 0 -> 1 -> 2)
    TOP_LEFT = (0, 0)
    TOP = (0, 1)
    TOP_RIGHT = (0, 2)

    RIGHT_TOP = (1, 0)
    RIGHT = (1, 1)
    RIGHT_BOTTOM = (1, 2)

    BOTTOM_RIGHT = (2, 0)
    BOTTOM = (2, 1)
    BOTTOM_LEFT = (2, 2)

    LEFT_BOTTOM = (3, 0)
    LEFT = (3, 1)
    LEFT_TOP = (3, 2)

    # Frodo
    def rotateClockwise(self, quarterRotations = 1, singleSteps = 0):
        return Richtung(((self.value[0] + quarterRotations + (self.value[1]+singleSteps)//3) % 4, (self.value[1]+singleSteps)%3))
    # Frodo
    def mirror(self):
        return Richtung((((self.value[0] + 2) % 4), -(self.value[1]-1)+1))
    # Frodo
    def getDirection(self) -> tuple[int,int]:
        match self.value[0]:
            case 0:
                return 0, 1
            case 1:
                return 1, 0
            case 2:
                return 0, -1
            case 3:
                return -1, 0
    # Frodo
    def getVector(self, scale = 0.8) -> tuple[float, float]:
        x, y = self.getDirection()
        dx, dy = 0, 0
        if self.value[1] != 1:
            dx, dy = self.rotateClockwise(-1+self.value[1]).getDirection()
        return (scale*(x + dx*0.55), scale*(y + dy*0.55))
    # Frodo
    def isAdjacent(self, other):
        # Wird verwendet, um zu testen, ob Wiesen an Städte grenzen
        if self.value[1] == 1:
            for i in range(7):
                if self.rotateClockwise(-1, i) == other:
                    return True
        
        if self.value[1] == 0:
            for i in range(4):
                if self.getDirection().rotateClockwise(-1, i) == other:
                    return True
        
        if self.value[1] == 2:
            for i in range(4):
                if self.getDirection().rotateClockwise(0, i) == other:
                    return True



# Frodo
class KantenTyp(Enum):
    WIESE = 0
    STADT = 1
    WEG = 2
# Frodo
class Figur:
    # Frodo, Leander, Thomas
    def __init__(self, besitzerIndex: int, x: int, y: int, bereichId: int):
        self.besitzer = besitzerIndex
        self.x = x
        self.y = y
        self.bereichId = bereichId
    # Frodo
    def __eq__(self, value):
        if type(value) == Figur:
            return (
                    self.x == value.x 
                    and self.y == value.y 
                    and self.bereichId == value.bereichId 
                    and self.besitzer == value.besitzer
                )
    # Thomas
    def __str__(self):
        return f"Spieler{self.besitzer}, x:{self.x}, y:{self.y}, Bereich:{self.bereichId}"
    # Thomas, Frodo
    def __hash__(self):
        return hash(str(self))

    # Frodo
    def getBesitzer(self):
        return self.besitzer
    # Frodo
    def getPosition(self):
        return self.x, self.y

# Leander
class Bereich:
    # Leander
    def __init__(self, kanten: list[Richtung]):
        self.verbundeneKanten: list[Richtung] = kanten.copy()
        
    # Leander
    def rotiert(self, rotation):
        rotierteKanten = list(map(lambda x: x.rotateClockwise(rotation), self.getKanten()))
        return type(self)(rotierteKanten)
    # Leander
    def getKanten(self) -> list[Richtung]:
        return self.verbundeneKanten.copy()
    # Frodo, Thomas, Miguel
    def getKnopfPosition(self) -> tuple[float, float]:
        kanten = self.getKanten()
        if not kanten:
            return 0, 0
        return self.getKanten()[0].getVector()

# Leander
class Spieler: 
    # Leander, Frodo
    def __init__(self, name:str):
        self.name: str = name
        self.farbe: str = ""
        self.anzahlFiguren: int = 7
        self.figurenPositionen: list[Figur] = []
        # Pro Spieler eine Liste mit Standorten der Figuren und Richtung
        self.punkte:int = 0
    # Leander
    def __str__(self):
        return (f"Spieler Ausgabe: \n  Name: {self.getName()}, \n  Gesetzte Figuren: {7-self.getFiguren()}") #, \n  figuren:{self.getFigurenListe}")
    # Leander
    def addPunkte (self, punkte):
        self.punkte = self.punkte + punkte
    # Leander
    def getPunkte (self):
        return self.punkte
    # Leander
    def setFarbe (self, farbe:str):
        self.farbe = farbe
    # Leander
    def getFarbe (self):
        return self.farbe
    # Leander
    def setName (self, name:str):
        self.name = name
    # Leander
    def getName (self):
        return self.name

    # Leander
    def setFigurenListe(self, figuren:list[Figur]):
        """Hilfsfunktion für Tests: Setzt Figurenliste komplett neu"""
        figurenAnzahl = len(figuren)
        if figurenAnzahl <= 7:
            self.figurenPositionen = figuren
            self.anzahlFiguren = 7 - figurenAnzahl
        else:
            raise ValueError(f"Zu viele Figuren ({figurenAnzahl} Stück) hinzugefügt zu {self.name}")

    # Leander
    def appendFigur(self, figur:Figur):
        self.figurenPositionen.append(figur)
        self.decrementFiguren()

    # Leander
    def entferneFigur(self, x:int, y:int)->bool:
        for figur in self.figurenPositionen:
            if figur.getPosition()[0] == x and figur.getPosition()[1] == y:
                self.figurenPositionen.remove(figur)
                self.incrementFiguren()
                return True
        return False

    # Leander, Thomas
    def setFiguren (self, figuren:int): # Setzt neue Anzahl von Figuren
        if 7 >= figuren > 0:
            self.anzahlFiguren = figuren
        else: raise ValueError("setFiguren: Nicht zugelassene Figuren-anzahl")

    # Leander, Thomas
    def incrementFiguren (self): # Setzt neue Anzahl von Figuren
        if  6 >= self.anzahlFiguren >= 0:
            self.anzahlFiguren += 1
        else: raise ValueError("Increment: Nicht zugelassene Figuren-anzahl")
    # Leander, Thomas
    def decrementFiguren (self): # Setzt neue Anzahl von Figuren
        if  7 >= self.anzahlFiguren > 0:
            self.anzahlFiguren -= 1
        else: raise ValueError("Decrement: Nicht zugelassene Figuren-anzahl")
    # Leander
    def getFigurenListe(self)->list[Figur]:
        return self.figurenPositionen
    # Leander
    def getFiguren (self) -> int:
        return self.anzahlFiguren


# Frodo
class WiesenBereich(Bereich):
    def __init__(self, kanten: list[Richtung | tuple[Richtung, int]]):
        super().__init__(kanten)
# Frodo
class StadtBereich(Bereich):
    def __init__(self, kanten: list[Richtung]):
        super().__init__(kanten)
        self.wappen = False
# Frodo
class WegBereich(Bereich):
    def __init__(self, kanten: list[Richtung]):
        super().__init__(kanten)
# Frodo
class KlosterBereich(Bereich):
    def __init__(self, kanten: list[Richtung]):
        super().__init__(kanten)
# Frodo
class Kartentyp:
    # Frodo
    def __init__(self, kartenId:str, kanten: list[KantenTyp], kloster: bool, wappen: bool, bereiche: list[Bereich] = None):
        self.id:str = kartenId
        self.bild = f"./Frontend/Images/tiles/{kartenId}.jpg"
        self.kanten: list[KantenTyp] = kanten #fixed length 4, TOP, RIGHT, BOTTOM, LEFT
                                               # Kanten im Uhrzeigersinn
        self.wappen = wappen
        self.kloster = kloster
        self.bereiche = bereiche
    # Frodo
    def getWappen(self) -> bool:
        return self.wappen
    # Frodo
    def getKante(self, richtung) -> KantenTyp:
        return self.kanten[richtung.value[0]]
    # Frodo
    def getId(self):
        return self.id
    # Frodo
    def __str__(self):
        return f"Kartentyp({self.id}, {self.kanten}, {self.kloster}, {self.wappen})"
# Thomas
class Kachel:
    # Thomas
    def __init__(self, typ: Kartentyp):
        self.position = (0, 0)
        self.rotation = 0
        self.karte: Kartentyp = typ
        self.figur: Figur = None
    # Leander   
    def __str__(self):
        """Hilfsfunktion für Tests"""
        return (f"\nPosition: {self.position},\n Rotation: {self.rotation},\n Karte: {self.karte},\n Figur: {self.figur}")
    # Leander
    def addFigur(self, figur:Figur):
        self.figur = figur
    # Thomas, Leander
    def getFigur(self)->Figur:
        return self.figur
    # Thomas, Leander
    def removeFigur(self):
        self.figur = None
    # Thomas
    def getWappen(self)->bool:
        return self.karte.getWappen()
    # Thomas
    def setPosition(self, x, y):
        self.position = (x, y)
    # Thomas
    def getPosition(self):
        return self.position
    # Leander
    def setRotation(self, rotation:int):
        """Hilfsfunktion für Tests"""
        if 4 > rotation >= 0:
            self.rotation = rotation
    # Leander
    def rotateRight(self):
        if self.position == (0, 0):
            self.rotation = (self.rotation + 1) % 4
    # Leander
    def rotateLeft(self):
        if self.position == (0, 0):
            self.rotation = (self.rotation - 1) % 4
    # Leander
    def getRotation(self):
        return self.rotation
    
    # Thomas, Frodo, Leander
    def getKante(self, richtung: Richtung) -> KantenTyp:
        """1 KantenTypen von Uhrzeigersinn aus gelesen"""
        rotierteRichtung = richtung.rotateClockwise(-self.rotation)
        return self.karte.getKante(rotierteRichtung)
    # Frodo
    def getBereiche(self): 
        return [b.rotiert(self.rotation) for b in self.karte.bereiche]
    # Frodo
    def getBesetztenBereich(self):
        if self.figur == None:
            return None
        return self.getBereiche()[self.figur.bereichId]
    
    def getImageName(self):
        return self.karte.getId()

# Thomas
class Spielzustand:
    # Thomas, Frodo, Leander
    def __init__(self, spielerzahl: int, kartenstapel: list[Kachel], startKarte: Kartentyp):
        self.field: dict[tuple[int, int], Kachel] = {}
        self.spielerListe: list[Spieler] = [Spieler(f'Spieler {i + 1}') for i in range(spielerzahl)]
        self.aktuellerSpieler: int = 0
        self.kartenstapel: list[Kachel] = kartenstapel
        self.aktuelleKachel: Kachel = Kachel(startKarte)           # Anpassen auf start Karte, sobald dies exsistiert
        self.klosterListe: dict[tuple[int, int], list[tuple[int, int]]] = {} # Liste aller Kloster mit Figur drauf
        self.letztePlatzierung: tuple[int, int] = (0,0)
        self.karteAngelegt = False
        self.spielende = False
        # Key: Kloster Koordinate | Value: Liste aus Tupeln von unbesetzten Nachbar x, y koordinaten
    
    
    def getGewinnerListe(self)->list[tuple[int, int]]: #spielerid, punkte
        ersteListe = []
        anzahlSpieler = len(self.spielerListe)

        for i in range(anzahlSpieler):
            ersteListe.append((i, self.spielerListe[i].getPunkte()))


        def bubbleSort(arr):
            n = len(arr)
            for i in range(n):
                swapped = False
                for j in range(0, n - i - 1):
                    if arr[j][1] < arr[j + 1][1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        swapped = True
                if not swapped:
                    break  

        bubbleSort(ersteListe)
            
        gewinnerString = f"Endauswertung: \n  "
        for index,punkte in ersteListe:
            gewinnerString += f"Spieler {index+1} hat {punkte} Punkte.\n  "
        #print(gewinnerString)

        return ersteListe




    # Leander
    def getAktuellerSpielerName(self):
        return self.spielerListe[self.aktuellerSpieler].getName()

    # Thomas, Leander
    def klosterÜberprüfen(self, x:int, y:int)->bool:

        for koordinate in self.klosterListe[(x,y)]:
            if koordinate in self.field.keys() or koordinate == (x, y):
                self.klosterListe[(x,y)].remove(koordinate)
        return len(self.klosterListe[(x, y)]) <= 0 # gibt zurück ob Kloster komplett
    
        # Thomas, Leander
    def klosterÜberprüfenInt(self, x:int, y:int)->int:

        for koordinate in self.klosterListe[(x,y)]:
            if koordinate in self.field.keys() or koordinate == (x, y):
                self.klosterListe[(x,y)].remove(koordinate)
        return 9-len(self.klosterListe[(x, y)]) 
        
    # Frodo, Thomas
    def getKoordinaten(self):
        return self.letztePlatzierung

    # Thomas, Leander
    def addKloster(self, x:int, y:int):
        koordinaten = []
        for i in range (3):
            koordinaten.append((x+i-1, y-1))
            koordinaten.append((x+i-1, y+0))
            koordinaten.append((x+i-1, y+1))
        self.klosterListe[(x, y)] = koordinaten
        self.klosterÜberprüfen(x, y)

    # Thomas
    def setSpieleranzahl(self, spieleranzahl: int):
        self.spielerListe = [Spieler(f'Spieler {i + 1}') for i in range(spieleranzahl)]
    # Frodo
    def getFigurenanzahl(self, spielerzahl: int)->int:
        return self.spielerListe[spielerzahl].getFiguren()
    # Frodo, ahassani
    def spielerAktualisieren (self):
        self.aktuellerSpieler = (self.aktuellerSpieler + 1) % len(self.spielerListe)

    # Leander
    def getSpielerIndex(self, name:str)->int:
        for k in range(len(self.spielerListe)):
            if name == self.spielerListe[k].getName(): return k
        raise ValueError ("Name existiert nicht")
    
    # Leander
    def getAktuellerSpielerIndex(self):
        return self.aktuellerSpieler

    # Leander
    def getPunkte(self) -> list[int]:
        punkte = []
        for spieler in self.spielerListe:
            punkte.append(spieler.getPunkte())
        return punkte

    # Thomas, Leander
    def addPunkte(self, spielerIndex:int, punkte:int):
        self.spielerListe[spielerIndex].addPunkte(punkte)

    # Thomas
    def feldErweitern(self, kachel:Kachel, x:int, y:int):
        self.karteAngelegt = True
        self.letztePlatzierung = (x, y)
        self.field[(x, y)] = kachel
    # Thomas
    def karteZiehen(self):
        if len(self.kartenstapel) > 0:
            self.aktuelleKachel = self.kartenstapel.pop()
            self.karteAngelegt = False
        else:
            self.spielende = True
        print(self.aktuelleKachel.getImageName())
    # Thomas
    def setPositionAktuelleKachel(self, x:int, y:int):
        self.aktuelleKachel.setPosition(x, y)
    # Leander
    def appendFigur(self, figur:Figur):
        self.spielerListe[self.aktuellerSpieler].appendFigur(figur)
    # Leander
    def entferneFigur(self, spielerIndex:int, x:int, y:int):
        self.spielerListe[spielerIndex].entferneFigur(x, y)
        #raise ValueError("Figur existiert an x, y bei Spieler nicht")
    # Thomas
    def aktuelleKachelRotateRight(self):
        self.aktuelleKachel.rotateRight()
    # Thomas
    def aktuelleKachelRotateLeft(self):
        self.aktuelleKachel.rotateLeft()
    # Thomas
    def getAktuelleKachel(self):
        return self.aktuelleKachel
    # Thomas, Leander
    def getKachel(self, x: int, y: int) -> Kachel:
        # gibt Kachel an x, y zurück oder None, wenn keine
        return self.field.get((x,y), None)
    # Thomas
    def spielerSetFarbe(self, spieler: int, farbe: str) -> None:
        self.spielerListe[spieler].setFarbe(farbe)

