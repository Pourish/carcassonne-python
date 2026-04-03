import Karteninfo
import random
from klassen import *


# Dies ist eine Test Datei
# Tests werden in Zukunftsiterationen implementiert


alleKartenTypen = {}
for key in Karteninfo.info.keys():
    kanten, kloster_wappen = Karteninfo.info[key]
    kantenTypen = list(map(lambda x: KantenTyp(x), kanten))
    bereiche = Karteninfo.bereichInfo[key]
    alleKartenTypen[key] = Kartentyp(key, kantenTypen, kloster_wappen[0], kloster_wappen[1], bereiche)

#kartenstapel = []
#for key in Karteninfo.info.keys():
#    for i in range(Karteninfo.kartenAnzahl[key]):
#        kartenstapel.append(Kachel(alleKartenTypen[key]))
#keys = list(Karteninfo.info.keys())
#key = random.choice(list(Karteninfo.info.keys()))
#testkarte = Kachel(alleKartenTypen[key])


#random.shuffle(kartenstapel)
#test_Spielzustand = Spielzustand(5, kartenstapel, alleKartenTypen["D"])
#test_Spielzustand.field[(0,0)] = Kachel(alleKartenTypen["D"])




richtungen: Richtung = [ 
    Richtung.TOP_LEFT,
    Richtung.TOP, 
    Richtung.TOP_RIGHT,

    Richtung.RIGHT_TOP,
    Richtung.RIGHT,
    Richtung.RIGHT_BOTTOM,

    Richtung.BOTTOM_RIGHT,
    Richtung.BOTTOM,
    Richtung.BOTTOM_LEFT,

    Richtung.LEFT_BOTTOM,
    Richtung.LEFT,
    Richtung.LEFT_TOP
]


richtungMirrorPairs: dict[Richtung, Richtung] = {
    Richtung.TOP_LEFT:Richtung.BOTTOM_LEFT,
    Richtung.TOP:Richtung.BOTTOM, 
    Richtung.TOP_RIGHT:Richtung.BOTTOM_RIGHT,

    Richtung.RIGHT_TOP:Richtung.LEFT_TOP,
    Richtung.RIGHT: Richtung.LEFT,
    Richtung.RIGHT_BOTTOM:Richtung.LEFT_BOTTOM,

    Richtung.BOTTOM_LEFT:Richtung.TOP_LEFT,
    Richtung.BOTTOM:Richtung.TOP,
    Richtung.BOTTOM_RIGHT:Richtung.TOP_RIGHT,

    Richtung.LEFT_TOP:Richtung.RIGHT_TOP,
    Richtung.LEFT:Richtung.RIGHT,
    Richtung.LEFT_BOTTOM:Richtung.RIGHT_BOTTOM
}

# Leander
def test_mirror(richtungMirrorPairs:dict[Richtung, Richtung])->bool:
    for key in richtungMirrorPairs.keys():
        if richtungMirrorPairs[key] != key.mirror():
            return False
    return True
# Leander
def test_mirror_id_property(richtungen:list[Richtung])->bool:
    for richtung in richtungen:
        if richtung != richtung.mirror().mirror():
            return False
    else: return True

#print(f"Test: Richtung spiegeln, alle Ergebnisse korrekt: {test_mirror(richtungMirrorPairs)}")
#print(f"Test-Property: Zweimal spiegeln gibt selbes Tile: {test_mirror_id_property(richtungen)}")

# Leander
def rotation_test():
    kacheln = []
    testRotateLeft = None
    testRotateRight = None

    for i in range (4):
        key = random.choice(list(Karteninfo.info.keys()))
        kacheln.append(Kachel(alleKartenTypen[key]))

    #Testteil: Rotate Left
    kacheln[0].setRotation(0)
    kacheln[1].setRotation(1)
    kacheln[2].setRotation(2)
    kacheln[3].setRotation(3)

    for i in range (4):
        kacheln[i].rotateLeft()
    
    if (kacheln[0].getRotation() == 3) and (kacheln[1].getRotation() == 0) and (kacheln[2].getRotation() == 1) and (kacheln[3].getRotation() == 2):
        testRotateLeft = True


    #Testteil: Rotate Right
    kacheln[0].setRotation(0)
    kacheln[1].setRotation(1)
    kacheln[2].setRotation(2)
    kacheln[3].setRotation(3)

    for i in range (4):
        kacheln[i].rotateRight()
    
    if (kacheln[0].getRotation() == 1) and (kacheln[1].getRotation() == 2) and (kacheln[2].getRotation() == 3) and (kacheln[3].getRotation() == 0):
        testRotateRight = True
    
    return (testRotateLeft, testRotateRight)
 
  
rotationsTest = rotation_test()
print(f"Rotation zufälliger Kachel Test \n-> für Links: {rotationsTest[0]}; \n-> für Rechts: {rotationsTest[1]}")
 

# Leander
def eineListeFigurEntfernen(figuren:list[Figur]):
    spieler = Spieler("Dieter-Hermann Meier-Klotz")

    spieler.setFigurenListe(figuren)

    vor_entfernen = len(spieler.getFigurenListe())
    spieler.entferneFigur(1,1)
    nach_entfernen = len(spieler.getFigurenListe())

    return (vor_entfernen == nach_entfernen+1)

# Leander
def allefigurVonEntfernen():
    spieler = Spieler("Dieter-Hermann Meier-Klotz")
    tests = []

    test_keine_Figur = []
    tests.append(eineListeFigurEntfernen(test_keine_Figur))

    test_eine_Figur = [Figur(1, 1, 1, 1)]
    tests.append(eineListeFigurEntfernen(test_eine_Figur))

    test_max_anzahl_Figuren = [Figur(0, 0, 0, 0), Figur(1, 1, 1, 1), Figur(2, 2, 2, 2),Figur(3, 3, 3, 3), Figur(4, 4, 4, 4), Figur(5, 5, 5, 5),Figur(6, 6, 6, 6)]
    tests.append(eineListeFigurEntfernen(test_max_anzahl_Figuren))
    

    test_normale_anzahl_Figuren = [Figur(0, 0, 0, 0), Figur(1, 1, 1, 1), Figur(2, 2, 2, 2),Figur(3, 3, 3, 3), Figur(4, 4, 4, 4), Figur(5, 5, 5, 5)]
    tests.append(eineListeFigurEntfernen(test_normale_anzahl_Figuren))
    
    #test_zu_viele_Figuren = [Figur(0, 0, 0, 0), Figur(1, 1, 1, 1), Figur(2, 2, 2, 2),Figur(3, 3, 3, 3), Figur(4, 4, 4, 4), Figur(5, 5, 5, 5),Figur(6, 6, 6, 6), Figur(7, 7, 7, 7), Figur(8, 8, 8, 8)]
    #tests.append(eineListeFigurEntfernen(test_zu_viele_Figuren))
    ## Throws error weil soll => Korrekt :)

    return (False in tests)

print(f"Testen alle möglichen entferneFigur() Fälle => Funktion funktioniert: {allefigurVonEntfernen()}")