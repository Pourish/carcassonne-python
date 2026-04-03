import json
from Backend.klassen import *
from Backend import Karteninfo

# Kartentypen einmalig aufbauen – MIT bereiche, damit geladene Kacheln funktionieren
_alleKartenTypen: dict[str, Kartentyp] = {}
for _key in Karteninfo.info.keys():
    _kanten, _kloster_wappen = Karteninfo.info[_key]
    _kantenTypen = list(map(lambda x: KantenTyp(x), _kanten))
    _bereiche = Karteninfo.bereichInfo[_key]
    _alleKartenTypen[_key] = Kartentyp(
        _key, _kantenTypen, _kloster_wappen[0], _kloster_wappen[1], _bereiche
    )


# ── Figur ──────────────────────────────────────────────────────────────────────

def _figurZuDict(figur: Figur) -> dict:
    return {
        "besitzer": figur.besitzer,
        "x": figur.x,
        "y": figur.y,
        "bereichId": figur.bereichId,
    }

def _figurAusDict(d: dict) -> Figur:
    return Figur(d["besitzer"], d["x"], d["y"], d["bereichId"])


# ── Bereich ────────────────────────────────────────────────────────────────────

def _bereichZuDict(bereich: Bereich) -> dict:
    d = {
        "typ": type(bereich).__name__,
        "kanten": [r.value for r in bereich.verbundeneKanten],
    }
    if isinstance(bereich, StadtBereich):
        d["wappen"] = bereich.wappen
    return d

def _bereichAusDict(d: dict) -> Bereich:
    kanten = [Richtung(v) for v in d["kanten"]]
    typ = d["typ"]
    match typ:
        case "WiesenBereich":
            b = WiesenBereich(kanten)
        case "StadtBereich":
            b = StadtBereich(kanten)
            b.wappen = d.get("wappen", False)
        case "WegBereich":
            b = WegBereich(kanten)
        case "KlosterBereich":
            b = KlosterBereich(kanten)
        case _:
            b = Bereich(kanten)
    return b


# ── Kachel ─────────────────────────────────────────────────────────────────────

def _kachelZuDict(kachel: Kachel) -> dict:
    return {
        "karte_id": kachel.karte.id if kachel.karte is not None else None,
        "position": list(kachel.position),
        "rotation": kachel.rotation,
        "figur": _figurZuDict(kachel.figur) if kachel.figur is not None else None,
        "bereiche": [_bereichZuDict(b) for b in kachel.karte.bereiche]
                    if kachel.karte is not None and kachel.karte.bereiche is not None
                    else [],
    }

def _kachelAusDict(d: dict, alleKartenTypen: dict) -> Kachel:
    karte_id = d["karte_id"]
    kachel = Kachel(alleKartenTypen[karte_id])
    kachel.position = tuple(d["position"])
    kachel.rotation = d["rotation"]
    gespeicherteBereiche = d.get("bereiche", [])
    if gespeicherteBereiche and kachel.karte.bereiche is not None:
        eigeneBereiche = [_bereichAusDict(bd) for bd in gespeicherteBereiche]
        kachel.karte = Kartentyp(
            kachel.karte.id,
            kachel.karte.kanten,
            kachel.karte.kloster,
            kachel.karte.wappen,
            eigeneBereiche,
        )
    if d.get("figur") is not None:
        kachel.figur = _figurAusDict(d["figur"])
    return kachel


# ── Save ───────────────────────────────────────────────────────────────────────

def save(data: Spielzustand, filename="spiel.json") -> None:
    daten = {
        "aktuellerSpieler": data.aktuellerSpieler,

        "field": {
            f"{pos[0]},{pos[1]}": _kachelZuDict(kachel)
            for pos, kachel in data.field.items()
        },

        "spieler": [
            {
                "name": s.name,
                "farbe": s.farbe,
                "anzahlFiguren": s.anzahlFiguren,
                "figurenPositionen": [
                    _figurZuDict(f) for f in s.figurenPositionen
                ],
                "punkte": s.punkte,
            }
            for s in data.spielerListe
        ],

        "kartenstapel": [_kachelZuDict(k) for k in data.kartenstapel],

        "aktuelleKachel": _kachelZuDict(data.aktuelleKachel)
                          if data.aktuelleKachel is not None else None,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)


# ── Load ───────────────────────────────────────────────────────────────────────

def load(filename="spiel.json", alleKartenTypen: dict = None) -> Spielzustand:
    if alleKartenTypen is None:
        alleKartenTypen = _alleKartenTypen

    with open(filename, "r", encoding="utf-8") as f:
        daten = json.load(f)

    zustand = Spielzustand(0, [])   # 0 Spieler, damit keine Duplikate entstehen
    zustand.aktuellerSpieler = daten["aktuellerSpieler"]

    # Spieler
    for s in daten["spieler"]:
        spieler = Spieler(s["name"])
        spieler.farbe = s["farbe"]
        spieler.anzahlFiguren = s["anzahlFiguren"]
        spieler.figurenPositionen = [
            _figurAusDict(fp) for fp in s["figurenPositionen"]
        ]
        spieler.punkte = s["punkte"]
        zustand.spielerListe.append(spieler)

    # Kartenstapel
    for k in daten["kartenstapel"]:
        zustand.kartenstapel.append(_kachelAusDict(k, alleKartenTypen))

    # aktuelleKachel
    if daten["aktuelleKachel"] is not None:
        zustand.aktuelleKachel = _kachelAusDict(daten["aktuelleKachel"], alleKartenTypen)

    # field
    for key, kachel_daten in daten["field"].items():
        x, y = map(int, key.split(","))
        zustand.field[(x, y)] = _kachelAusDict(kachel_daten, alleKartenTypen)

    return zustand