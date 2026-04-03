from Backend.klassen import *

"""Kanten, Kloster und Wappen informationen zu jeder der 24 Karten"""
info = dict()
info["A"]=((0,0,2,0),(True,False))
info["B"]=((0,0,0,0),(True,False))
info["C"]=((1,1,1,1),(False,True))
info["D"]=((2,1,2,0),(False,False))
info["E"]=((1,0,0,0),(False,False))
info["F"]=((0,1,0,1),(False,True))
info["G"]=((1,0,1,0),(False,False))
info["H"]=((0,1,0,1),(False,False))
info["I"]=((0,1,1,0),(False,False))
info["J"]=((1,2,2,0),(False,False))
info["K"]=((2,1,0,2),(False,False))
info["L"]=((2,1,2,2),(False,False))
info["M"]=((1,0,0,1),(False,True))
info["N"]=((1,0,0,1),(False,False))
info["O"]=((1,2,2,1),(False,True))
info["P"]=((1,2,2,1),(False,False))
info["Q"]=((1,1,0,1),(False,True))
info["R"]=((1,1,0,1),(False,False))
info["S"]=((1,1,2,1),(False,True))
info["T"]=((1,1,2,1),(False,False))
info["U"]=((2,0,2,0),(False,False))
info["V"]=((0,0,2,2),(False,False))
info["W"]=((0,2,2,2),(False,False))
info["X"]=((2,2,2,2),(False,False))

bereichInfo = dict()

R = Richtung.RIGHT
L = Richtung.LEFT
T = Richtung.TOP
B = Richtung.BOTTOM
RT = Richtung.RIGHT_TOP
RB = Richtung.RIGHT_BOTTOM
LB = Richtung.LEFT_BOTTOM
LT = Richtung.LEFT_TOP
TL = Richtung.TOP_LEFT
TR = Richtung.TOP_RIGHT
BR = Richtung.BOTTOM_RIGHT
BL = Richtung.BOTTOM_LEFT

bereichInfo["A"] = [
    KlosterBereich([]),
    WegBereich([B]),
    WiesenBereich([BL, L, T, R, BR]),
]
bereichInfo["B"] = [
    KlosterBereich([]),
    WiesenBereich([B, L, T, R])
]
bereichInfo["C"] = [
    StadtBereich([B, L, T, R]),
]
bereichInfo["D"] = [
    WegBereich([T, B]),
    StadtBereich([R]),
    WiesenBereich([TL, L, BL]),
    WiesenBereich([TR, BR])
]
bereichInfo["E"] = [
    StadtBereich([T]),
    WiesenBereich([R, B, L]),
]
bereichInfo["F"] = [
    StadtBereich([L, R]),
    WiesenBereich([T]),
    WiesenBereich([B])
]
bereichInfo["G"] = [
    StadtBereich([T, B]),
    WiesenBereich([L]),
    WiesenBereich([R]),
]
bereichInfo["H"] = [
    StadtBereich([L]),
    StadtBereich([R]),
    WiesenBereich([T, B])
]
bereichInfo["I"] = [
    StadtBereich([R]),
    StadtBereich([B]),
    WiesenBereich([T, L])
]
bereichInfo["J"] = [
    StadtBereich([T]),
    WegBereich([R, B]),
    WiesenBereich([L, BL, RT]),
    WiesenBereich([RB, BR])
]
bereichInfo["K"] = [
    WegBereich([T,L]),
    StadtBereich([R]),
    WiesenBereich([TL, LT]),
    WiesenBereich([B, LB, TR])
]
bereichInfo["L"] = [
    WegBereich([T]),
    WegBereich([L]),
    WegBereich([B]),
    StadtBereich([R]),
    WiesenBereich([TL, LT]),
    WiesenBereich([BL, LB]),
    WiesenBereich([TR, BR]),
]
bereichInfo["M"] = [
    StadtBereich([T, L]),
    WiesenBereich([B, R])
]
bereichInfo["N"] = [
    StadtBereich([T, L]),
    WiesenBereich([B, R])
]
bereichInfo["O"] = [
    StadtBereich([T, L]),
    WegBereich([R, B]),
    WiesenBereich([BL, RT]),
    WiesenBereich([BR, RB])
]
bereichInfo["P"] = [
    StadtBereich([T, L]),
    WegBereich([R, B]),
    WiesenBereich([BL, RT]),
    WiesenBereich([BR, RB])
]
bereichInfo["Q"] = [
    StadtBereich([L, T, R]),
    WiesenBereich([B])
]
bereichInfo["R"] = [
    StadtBereich([L, T, R]),
    WiesenBereich([B])
]
bereichInfo["S"] = [
    StadtBereich([L, T, R]),
    WegBereich([B]),
    WiesenBereich([BL]),
    WiesenBereich([BR])
]
bereichInfo["T"] = [
    StadtBereich([L, T, R]),
    WegBereich([B]),
    WiesenBereich([BL]),
    WiesenBereich([BR])
]
bereichInfo["U"] = [
    WegBereich([T, B]),
    WiesenBereich([L, TL, BL]),
    WiesenBereich([R, TR, BR])
]
bereichInfo["V"] = [
    WegBereich([L, B]),
    WiesenBereich([BL, LB]),
    WiesenBereich([R, T, BR, LT])
]
bereichInfo["W"] = [
    WegBereich([L]),
    WegBereich([B]),
    WegBereich([R]),
    WiesenBereich([T, RT, LT]),
    WiesenBereich([LB, BL]),
    WiesenBereich([RB, BR])
]
bereichInfo["X"] = [
    WegBereich([L]),
    WegBereich([B]),
    WegBereich([R]),
    WegBereich([T]),
    WiesenBereich([TL, LT]),
    WiesenBereich([TR, RT]),
    WiesenBereich([BR, RB]),
    WiesenBereich([BL, LB])
]


"""Information zur Anzahl von jeder Karte"""
kartenAnzahl = {"A": 2, "B": 0, "C": 0, "D": 0, "E": 0, "F":0, "G": 0, "H": 2, "I": 0, "J": 0, "K": 0, "L": 2, "M": 0,
               "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0, "W": 0, "X": 2}

# kartenAnzahl = {"A": 2, "B": 4, "C": 1, "D": 3, "E": 5, "F": 2, "G": 1, "H": 3, "I": 2, "J": 3, "K": 3, "L": 3, "M": 2,
#                 "N": 3, "O": 2, "P": 3, "Q": 1, "R": 3, "S": 2, "T": 1, "U": 8, "V": 9, "W": 4, "X": 1}

