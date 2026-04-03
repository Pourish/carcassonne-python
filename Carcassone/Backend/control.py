from Backend.klassen import *
import Backend.model as model
import copy

# Frodo
class Knoten:
    # Frodo
    def __init__(self, koordinaten: tuple[int, int], kante: Richtung):
        self.koordinaten = koordinaten
        self.kante = kante
    # Frodo
    def __str__(self):
        return f"Knoten [{self.koordinaten}, {self.kante}]"
    # Frodo
    def __eq__(self, other):
        return type(other) == Knoten and str(self) == str(other)
    # Frodo
    def __hash__(self):
        return hash(str(self))

# Frodo
class BreitensucheErgebnis:
    # Frodo
    def __init__(
            self,
            enthalteneFiguren: set[Figur], 
            enthalteneKoordinaten: set[tuple[int,int]], 
            abgeschlossen: bool,
            durchsuchteKnoten: list[Knoten]
            ):
        self.enthalteneFiguren: set[Figur] = enthalteneFiguren.copy()
        self.enthalteneKoordinaten: set[tuple[int,int]] = enthalteneKoordinaten.copy()
        self.abgeschlossen: bool = abgeschlossen
        self.durchsuchteKnoten: list[Knoten] = durchsuchteKnoten
    # Frodo
    def __str__(self):
        return f"BreitensucheErgebnis: enthalteneFiguren = {self.enthalteneFiguren}, abgeschlossen = {self.abgeschlossen}, koordinaten = {self.enthalteneKoordinaten}"


# Frodo
def breitensuche(koordinaten: tuple[int, int], bereichId: int) -> BreitensucheErgebnis:
    """Breitensuche macht nur für einen Bereich die Breitensuche
    Gibt Liste von Figuren zurück, Anzahl der Kacheln und Wappen, und ob der Bereich abgeschlossen ist"""
    print("Breitensuche")
    print(bereichId)
    erforscht: list[Knoten] = []
    gesehen: list[Knoten] = []
    spielzustand = model.aktiverSpielstand
    bereichAbgeschlossen = True
    
    enthalteneFiguren: set[Figur] = set()
    startKachel = spielzustand.getKachel(*koordinaten)
    print(startKachel.getPosition())
    # print(startKachel.getBereiche())

    bereich = startKachel.getBereiche()[bereichId]
    offeneKanten = bereich.getKanten()

    startFigur = startKachel.getFigur()
    if startFigur is not None and startFigur.bereichId == bereichId:
        enthalteneFiguren.add(startFigur)

    enthalteneKoordinaten: set[tuple[int,int]] = set()
    enthalteneKoordinaten.add(koordinaten)
    for richtung in offeneKanten:
        gesehen.append(Knoten(koordinaten, richtung))

    while len(gesehen) > 0:
        suchKnoten = gesehen.pop()
        erforscht.append(suchKnoten)
        
        suchKoordinaten = suchKnoten.koordinaten
        suchKante = suchKnoten.kante
        x = suchKoordinaten[0] + suchKante.getDirection()[0]
        y = suchKoordinaten[1] + suchKante.getDirection()[1]
        angrenzendeKoordinaten = (x, y)
        angrenzendeKachel = spielzustand.getKachel(x,y)

        # Testen, ob ein leeres Feld angrenzt
        if angrenzendeKachel is None:
            bereichAbgeschlossen = False
        else:
            # Koordinaten hinzufügen
            enthalteneKoordinaten.add(angrenzendeKoordinaten)
            # Über alle Bereiche der angrenzenden Kachel iterieren, um die Verbindung zu finden
            for bereichIndex in range(len(angrenzendeKachel.getBereiche())):
                angrenzenderBereich = angrenzendeKachel.getBereiche()[bereichIndex]
                if type(bereich) != type(angrenzenderBereich):
                    continue
                testKanten = angrenzenderBereich.getKanten()
                if suchKante.mirror() not in testKanten:
                    continue
                # angrenzenderBereich ist mit dem Suchbereich verbunden,
                # falls eine Figur vorhanden ist, wird sie zu den im Gesamtbereich enthaltenen Figuren hinzugefügt
                figur = angrenzendeKachel.getFigur()
                if figur is not None and figur.bereichId == bereichIndex:
                    enthalteneFiguren.add(figur)
                # entgegengesetzte Kante auf erforscht setzen, um Schritt zurück zu sparen
                testKnoten = Knoten((x,y), suchKante.mirror())
                erforscht.append(testKnoten)
                

                # neu entdeckte Knoten speichern
                for kante in testKanten:
                    neuerKnoten = Knoten((x,y), kante)
                    if neuerKnoten in erforscht or neuerKnoten in gesehen:
                        continue
                    gesehen.append(neuerKnoten)
        
    return BreitensucheErgebnis(enthalteneFiguren, enthalteneKoordinaten, bereichAbgeschlossen, erforscht)
        # Test: gibt überhaupt ein Bereich typ match
        # Test: berühren sich matchende bereiche
        # gibt erforschte Knoten als erforscht an
        # testkanten = alle Kanten wo Bereich übereingestimmt hat und Bereiche sich berühren, ohne die || Kante
        #       (|| bedeutet sich berührenden Kanten/neighbouring Kanten)
        # neue Knoten hinzugefügt, wenn noch nicht erforscht/gesehen
                    






# Thomas, Frodo, Leander
def kachelAnlegenErlaubt(x:int, y:int) -> bool:
    """Prüft:
    a) ob irgendeine angrenzende Karte existiert
    \nb) ob die Kantentypen mit den anliegenden Kantentypen übereinstimmen
    """
    angrenzendeFelder = [(x, y+1), (x+1, y), (x, y-1), (x-1, y)]
    aktuelleKachel = model.aktiverSpielstand.getAktuelleKachel()
    anzahlNachbarn = 0
    for i in range(4):
        richtung = Richtung((i, 1))
        vergleichsKachel = model.aktiverSpielstand.getKachel(angrenzendeFelder[i][0], angrenzendeFelder[i][1])
        if vergleichsKachel is not None:
            anzahlNachbarn += 1
            vergleichsKante = vergleichsKachel.getKante(richtung.rotateClockwise(2))
            if aktuelleKachel.getKante(richtung) != vergleichsKante:
                return False
    return anzahlNachbarn > 0 # Anlegen erlaubt, wenn mind. 1 existierender Nachbar

    # plus 2 => rotateClockwise(2)

# Thomas, Frodo, Leander
def kachelAnlegen(x:int, y:int) -> bool: # Bool => Erfolg / Misserfolg
    """Nimmt: x, y Koordinate"""
    if kachelAnlegenErlaubt(x, y):
        model.aktiverSpielstand.feldErweitern(model.aktiverSpielstand.aktuelleKachel, x, y)
        model.aktiverSpielstand.setPositionAktuelleKachel(x, y)
        neueKachel = model.aktiverSpielstand.getKachel(x, y)
        for bereichId in range(len(neueKachel.getBereiche())):
            ergebnis = breitensuche((x,y), bereichId)
            bereich = neueKachel.getBereiche()[bereichId]
            print(f"Breitensuche durchgeführt, Bereich {bereich}")
            if ergebnis.abgeschlossen:
                print(f"Bereich abgeschlossen. Ergebnis:\n: {ergebnis}")
        # provisorisch, muss später getrennt behandelt werden!
        # model.aktiverSpielstand.karteZiehen()
        return True
    else: 
        return False



# Leander, Thomas
def removeFigur(figur:Figur):
    x, y = figur.x, figur.y
    spielerIndex =figur.getBesitzer()

    model.aktiverSpielstand.entferneFigur(spielerIndex, x,y) #entfernt Figur aus Spieler
    model.aktiverSpielstand.field[(x,y)].removeFigur()


# Thomas, Leander
def addFigur(bereichIndex:int): #Annahme: Kachel bleibt aktuelle Kachel
    spielerIndex = model.aktiverSpielstand.getAktuellerSpielerIndex()
    x, y = model.aktiverSpielstand.letztePlatzierung
    kachel = model.aktiverSpielstand.getKachel(x,y)
    anzahlBereiche = len(kachel.getBereiche())

    # Wenn Figuren zu legen übrig sind
    if model.aktiverSpielstand.spielerListe[spielerIndex].getFiguren() > 0:
        # Wenn der BereichIndex für den Kartentyp existiert
        if 0 <= bereichIndex < anzahlBereiche:
            figur = Figur(spielerIndex, x, y, bereichIndex)
            model.aktiverSpielstand.spielerListe[spielerIndex].appendFigur(figur)
            model.aktiverSpielstand.field[x, y].addFigur(figur)
        else: raise ValueError ("Möglicher BereichIndex über oder unterschritten")
   # else:
       # raise ValueError ("Keine Figuren übrig")



# Leander, Frodo, Thomas
def figurSetzen(x:int, y:int, bereichIndex:int) -> bool:
    x, y = model.aktiverSpielstand.letztePlatzierung
    kachel = model.aktiverSpielstand.getKachel(x,y)
    if darfPlatzieren(x, y, bereichIndex):
        addFigur(bereichIndex)
        if type(kachel.getBereiche()[bereichIndex]) == KlosterBereich:
            return model.aktiverSpielstand.addKloster(x, y) #Kloster zu Spielstand hinzufügen
        else: True
    #else:
     #   raise ValueError ("Dieser verbundene Bereich wird schon durch eine Figur belegt")
    
# Leander, Thomas
def darfPlatzieren(x:int,y:int, bereichId:int)->bool:
    """Breitensuche: sind bislang keine Figuren im verbundenen Bereich?"""
    ergebnis = breitensuche((x, y), bereichId)
    return ergebnis.enthalteneFiguren == set()



# Leander, Frodo
def getAnzahlWappen(koordinaten:set[tuple[int, int]]) -> int:
    kacheln:list[Kachel] = (map(
                                lambda xy: model.aktiverSpielstand.field[(xy[0], xy[1])],
                                koordinaten)) 
    wappenTrue: list[bool] = [x.getWappen() for x in kacheln]
    return wappenTrue.count(True)


# Leander, Thomas
def klosterAuswerten(x:int, y:int) -> tuple[int, int]: #rückgabe Liste von Punkte und Spielerindex
    print(f" x {model.aktiverSpielstand.klosterÜberprüfen(x,y)}")
    if model.aktiverSpielstand.klosterÜberprüfen(x, y):
        del model.aktiverSpielstand.klosterListe[(x,y)] # entfernt Eintrag des kompletten Kloster
        besitzerIndex = model.aktiverSpielstand.field[(x,y)].getFigur().getBesitzer()
        removeFigur(model.aktiverSpielstand.field[(x,y)].getFigur())
        print("a")
        print(besitzerIndex)
        return 9, besitzerIndex
    return 0, 0

        # kloster enternen wenn gebiet komplett
        # figur aus bereich entfernen
        # figur aus spieler entfernen
        # figur Spieler zurückgeben

# Leander
def klosterEndAuswertung(x:int, y:int) -> tuple[int, int]:
    """Rückgabe Liste von Punkte und Spielerindex"""
    klosterAuswerten(x, y)
    punkte = model.aktiverSpielstand.klosterÜberprüfenInt(x,y)                         # anzahl angrenzender Gebiete
    del model.aktiverSpielstand.klosterListe[(x,y)]                                 # entfernt Eintrag des kompletten Kloster
    besitzerIndex = model.aktiverSpielstand.field[(x,y)].getFigur().getBesitzer()
    removeFigur(model.aktiverSpielstand.field[(x,y)].getFigur())                    # entferne Figur
    return punkte, besitzerIndex


#  Thomas, Frodo, Leander
def punkteAuswertungZug(spielEnde = False): #keine Ausgabe - sollte es ausgeben wie viele Punkte wer bekommt?  
    klosterlisteCopie = copy.deepcopy(model.aktiverSpielstand.klosterListe)
    if not spielEnde:
        kachel = model.aktiverSpielstand.getAktuelleKachel()  
        punkteAuswertungKachel(kachel)
        # Klosterauswertung nach Zug
        for (x, y) in klosterlisteCopie:
            punkte, spielerIndex = klosterAuswerten(x, y)
            model.aktiverSpielstand.addPunkte(spielerIndex, punkte)
    else:                     
        # Klosterauswertung Spielende
        for (x, y) in klosterlisteCopie:
            punkte, spielerIndex = klosterEndAuswertung(x, y)
            model.aktiverSpielstand.addPunkte(spielerIndex, punkte)
        kachelListe = model.aktiverSpielstand.field.keys()
        for koordinaten in kachelListe:       # aktuell gelegte Kacheln
            kachel = model.aktiverSpielstand.getKachel(*koordinaten)
            print(kachel)
            punkteAuswertungKachel(kachel)


def punkteAuswertungKachel(kachel: Kachel):
    spielEnde = model.aktiverSpielstand.spielende
    bereiche = kachel.getBereiche()
    coords = kachel.getPosition()

    print("Bereiche auswerten")
    print(bereiche)
    for bereichId in range(len(bereiche)): 
        print(bereichId)
        bereich = bereiche[bereichId]                                                       # in aktuell gelegter Kachel, enthaltenden Bereiche
        bereichArt = type(bereich)       
        totalPunkte: int = 0   

        ergebnis: BreitensucheErgebnis = breitensuche(coords, bereichId) # Ergebnis der Breitensuche
        if not ergebnis.abgeschlossen and not spielEnde: continue
        figuren: set[Figur] = ergebnis.enthalteneFiguren                                    # Alle Figuren im Bereich
        kachelzahl = len(ergebnis.enthalteneKoordinaten)                                    # Anzahl der Kacheln die, Bereich enthalten

        # Kloster werden separat ausgewertet
        if bereichArt == KlosterBereich:
            continue
        # Wiesen sind kompliziert
        if bereichArt == WiesenBereich and spielEnde:
            # Um Städte nicht mehrfach zu zählen, werden die erforschten Stadtknoten gespeichert
            stadtKnotenErforscht = set()
            # Für jeden Wiesenknoten wird nach angrenzenden Stadtbereichen gesucht
            for knoten in ergebnis.durchsuchteKnoten:
                koordinaten = knoten.koordinaten
                knotenKante = knoten.kante
                kachel = model.aktiverSpielstand.getKachel(*koordinaten)
                for bereichId2 in range(len(kachel.getBereiche())):
                    bereich = kachel.getBereiche()[bereichId2]
                    # Uns interessieren nur Städte
                    if type(bereich) != StadtBereich:
                        continue
                    # hier wird getestet, ob die Stadt an die Wiese grenzt
                    for kante in bereich.getKanten():
                        if not kante.isAdjacent(knotenKante):
                            continue
                        # Wenn ja, wird geprüft, ob der Stadtknoten zu einer vorher durchsuchten Stadt gehört
                        stadtKnoten = Knoten(koordinaten, kante)
                        if stadtKnoten in stadtKnotenErforscht:
                            continue
                        # Ansonsten wird die Stadt durchsucht. Falls der Bereich abgeschlossen ist, werden Punkte vergeben
                        stadtErgebnis = breitensuche(koordinaten, bereichId2)
                        if stadtErgebnis.abgeschlossen:
                            totalPunkte += 3
                        stadtKnotenErforscht = stadtKnotenErforscht.union(stadtErgebnis.durchsuchteKnoten)


        if bereichArt == StadtBereich or bereichArt == WegBereich:
            totalPunkte = kachelzahl                                                           # => Punktezahl
            if bereichArt == StadtBereich:                                                     # Wenn Stadtbereich
                wappenzahl = getAnzahlWappen(ergebnis.enthalteneKoordinaten)                   # zählt Wappen im Bereich
                totalPunkte += wappenzahl                                                      # Wappen + Punkte
                if ergebnis.abgeschlossen:                                                     # abgeschlossener Bereich ⇒ Stadt=doppelt Punkte
                    totalPunkte *= 2
        punkteGewinner = besitzerMaxfigurenInBereich(figuren)      
        for figur in figuren:                                                              # entfernt alle Figuren des Bereiches
            removeFigur(figur)                                                              

        for player in punkteGewinner:                                                      # Teilt Punkte auf Gewinner auf
            model.aktiverSpielstand.addPunkte(player, totalPunkte)




# Leander
def besitzerMaxfigurenInBereich(figuren:set[Figur]) -> list[int]:
    """gibt eine Liste der Indices der Spieler zurück die sich die höchste Zahl Figuren im Bereich teilen """
    figurenbesitzer:list[int] = [x.getBesitzer() for x in figuren]                                        # Liste der Namen
    spielerListe: list[tuple[int, int]] = list(set(map(lambda x: (x, figurenbesitzer.count(x)),figurenbesitzer))) # (besitzer, n) # funktioniert das auch sicher it richtigen output?
    # 1) liste der namen
    # 2) liste mit Tupel von Name und wie oft der Name auftaucht
    # 3) liste zu Set damit unique, zurück zu Liste
    
    #spielerliste = {element: figurenbesitzer.count(element) for element in set(figurenbesitzer)}
    maxSpieler = []

    for (spielerIndex, figurenAnzahl) in spielerListe:
        if maxSpieler == []:
            maxSpieler = [(spielerIndex, figurenAnzahl)]
        else:
            if maxSpieler[0][1] == figurenAnzahl:
                maxSpieler.append((spielerIndex, figurenAnzahl))
            else:
                if maxSpieler[0][1] < figurenAnzahl:
                    maxSpieler = [(spielerIndex, figurenAnzahl)]
    return [p[0] for p in maxSpieler]



# wird eine neue Kachel erzeugt bei gelegt haben der aktuellen
# oder die Kachel im dictionary gespeichert


# nach Figur-platzieren Punkteauswertung
# Punkteauswertung: -> Rückgabewert erzielte Punktezahl
#   - Breitensuche angrenzende Felder
    #   - Figur zurück, wenn ein Bereich geschlossen
    #   - Punkte zugeteilt / berechnen
    #   - welche Figuren? - welche bekommt wie viel Punkte
#   - Klostercheck
    #   - Figur zurück, wenn ein Bereich geschlossen
    #   - Punkte zugeteilt
# neue Karte ziehen
# Spieler aktualisieren
# JSON speichern
# Signal nächster Spieler?

# Mehrere Figuren: Punkteverteilung


def zugBeenden():
    if model.aktiverSpielstand.karteAngelegt:
        punkteAuswertungZug(model.aktiverSpielstand.spielende) 
        
        model.aktiverSpielstand.karteZiehen()
        model.aktiverSpielstand.spielerAktualisieren()
        
        # Uncomment this line and give it a file name!
        model.save("spiel.json")