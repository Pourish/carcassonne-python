import pygame
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


# ============================================================
# ENUMS
# ============================================================

class TutorialHighlight(Enum):
    NONE = auto()
    CURRENT_CARD = auto()
    ROTATE_BUTTON = auto()
    BOARD = auto()
    PLAYERS = auto()


class TutorialAction(Enum):
    NONE = auto()
    CLICK_NEXT = auto()
    ROTATE_CARD = auto()
    PLACE_CARD = auto()
    PAN_BOARD = auto()
    ZOOM_BOARD = auto()
    FINISH = auto()


# ============================================================
# DATENKLASSE
# ============================================================

@dataclass
class TutorialStep:
    title: str
    text: str
    hint: str = ""
    highlight: TutorialHighlight = TutorialHighlight.NONE
    expected_action: TutorialAction = TutorialAction.NONE
    show_next_button: bool = True


# ============================================================
# SCHRITTE / TEXTE
# ============================================================

def punktvergabe() -> str:
    text = """
PUNKTESYSTEM
____________________________________________________________

STAEDTE
    Jede Kachel = 1 Punkt
    Jedes Wappen = +1 Punkt
    Abgeschlossene Staedte: +2 Punkte pro Kachel und Wappen

    Beispiel:
    3 Kacheln + 1 Wappen = 4  ->  abgeschlossen = 8 Punkte
____________________________________________________________

WEGE
    Jede Kachel im Weg = 1 Punkt
    Keine Verdopplung

    Beispiel:
    5 Kacheln = 5 Punkte
____________________________________________________________

KLOESTER
    Vollstaendig umgeben (8 Karten) = 9 Punkte
    Nicht vollstaendig = 1 Punkt pro umliegender Karte

    Beispiel:
    Kloster + 5 umliegende Karten = 6 Punkte
____________________________________________________________

FIGUREN
    Spieler mit den meisten Figuren erhalten die Punkte
    Bei Gleichstand teilen sich die Spieler die Punkte
____________________________________________________________

ENDAUSWERTUNG
    Staedte: 1 Punkt pro Kachel + 1 pro Wappen
    Wege:    1 Punkt pro Kachel
    Kloester: je nach Umgebung
    """
    return text


def create_tutorial_steps() -> list[TutorialStep]:
    return [
        TutorialStep(
            title="Willkommen",
            text=(
                "Willkommen im Spiel.\n\n"
                "Dieses Tutorial zeigt dir kurz die wichtigsten Bedienelemente. "
                "Du lernst, wie du eine Karte drehst, auf das Spielfeld legst "
                "und dich auf dem Spielbrett bewegst."
            ),
            hint="Klicke auf „Weiter“.",
            highlight=TutorialHighlight.NONE,
            expected_action=TutorialAction.CLICK_NEXT,
            show_next_button=True,
        ),

        TutorialStep(
            title="Die aktuelle Karte",
            text=(
                "Links in der Seitenleiste siehst du die Karte, "
                "die du in diesem Zug verwenden kannst.\n\n"
                "Diese Karte kannst du drehen und anschließend "
                "auf ein passendes Feld im Spielfeld legen."
            ),
            hint="Schau dir die Karte links an.",
            highlight=TutorialHighlight.CURRENT_CARD,
            expected_action=TutorialAction.CLICK_NEXT,
            show_next_button=True,
        ),

        TutorialStep(
            title="Karte drehen",
            text=(
                "Unter der aktuellen Karte befindet sich der grüne Rotationsbutton.\n\n"
                "Damit kannst du die Karte drehen, bevor du sie legst."
            ),
            hint="Klicke jetzt einmal auf den grünen Button.",
            highlight=TutorialHighlight.ROTATE_BUTTON,
            expected_action=TutorialAction.ROTATE_CARD,
            show_next_button=False,
        ),

        TutorialStep(
            title="Sehr gut",
            text=(
                "Die Karte wurde gedreht.\n\n"
                "Du kannst sie vor dem Legen so oft drehen, wie du möchtest."
            ),
            hint="Klicke auf „Weiter“.",
            highlight=TutorialHighlight.ROTATE_BUTTON,
            expected_action=TutorialAction.CLICK_NEXT,
            show_next_button=True,
        ),

        TutorialStep(
            title="Karte platzieren",
            text=(
                "Ziehe jetzt die aktuelle Karte aus dem linken Bereich "
                "auf das Spielfeld.\n\n"
                "Die Karte kann nur auf ein gültiges Feld gelegt werden."
            ),
            hint="Ziehe die Karte mit der Maus auf das Spielfeld und lege sie ab.",
            highlight=TutorialHighlight.CURRENT_CARD,
            expected_action=TutorialAction.PLACE_CARD,
            show_next_button=False,
        ),

        TutorialStep(
            title="Figur setzen",
            text=(
                "Super! Die Karte wurde gelegt.\n\n"
                "Auf der gelegten Karte erscheinen jetzt farbige Buttons "
                "– einer für jeden Bereich (Stadt, Weg, Wiese, Kloster).\n\n"
                "Klicke auf einen dieser Buttons, um dort eine Figur zu setzen. "
                "Du kannst aber auch darauf verzichten und den Zug direkt beenden.\n\n"
                "Zum Beenden klicke auf den grünen \"Zug beenden\"-Button unten im Bildschirm."
            ),
            hint="Setze eine Figur oder beende deinen Zug.",
            highlight=TutorialHighlight.BOARD,
            expected_action=TutorialAction.CLICK_NEXT,
            show_next_button=True,
        ),

        TutorialStep(
            title="Spielfeld erkunden",
            text=(
                "Das Spielfeld ist größer als der sichtbare Bereich.\n\n"
                "Du kannst es mit gedrückter linker Maustaste verschieben, "
                "wenn du direkt auf dem Spielfeld ziehst."
            ),
            hint="Bewege jetzt das Spielfeld ein Stück.",
            highlight=TutorialHighlight.BOARD,
            expected_action=TutorialAction.PAN_BOARD,
            show_next_button=False,
        ),

        TutorialStep(
            title="Zoomen",
            text=(
                "Mit dem Mausrad kannst du in das Spielfeld hinein- und herauszoomen.\n\n"
                "Das hilft dir, den Überblick zu behalten oder genauer zu arbeiten."
            ),
            hint="Benutze jetzt einmal das Mausrad auf dem Spielfeld.",
            highlight=TutorialHighlight.BOARD,
            expected_action=TutorialAction.ZOOM_BOARD,
            show_next_button=False,
        ),

        TutorialStep(
            title="Spielerbereich",
            text=(
                "Im linken Bereich siehst du außerdem die Spielerübersicht.\n\n"
                "Dort werden Namen, Punkte und Figuren angezeigt."
            ),
            hint="Hier behältst du den Stand des Spiels im Blick.",
            highlight=TutorialHighlight.PLAYERS,
            expected_action=TutorialAction.CLICK_NEXT,
            show_next_button=True,
        ),

        TutorialStep(
            title="Grundidee des Spiels",
            text=(
                "Im Spiel baust du Schritt für Schritt eine gemeinsame Landschaft auf.\n\n"
                "Später können Figuren und Punkte eine Rolle spielen. "
                "Für den Einstieg ist jetzt vor allem wichtig, "
                "dass du die Bedienung des Spielfelds sicher beherrschst."
            ),
            hint="Klicke auf „Weiter“.",
            highlight=TutorialHighlight.NONE,
            expected_action=TutorialAction.CLICK_NEXT,
            show_next_button=True,
        ),

        TutorialStep(
            title="Tutorial abgeschlossen",
            text=(
                "Du kennst jetzt die wichtigsten Bedienelemente:\n\n"
                "• aktuelle Karte ansehen\n"
                "• Karte drehen\n"
                "• Karte legen\n"
                "• Spielfeld verschieben\n"
                "• Spielfeld zoomen\n\n"
                "Viel Spaß beim Spielen."
            ),
            hint="Klicke auf „Fertig“.",
            highlight=TutorialHighlight.NONE,
            expected_action=TutorialAction.FINISH,
            show_next_button=True,
        ),
    ]


# ============================================================
# OVERLAY
# ============================================================

class TutorialOverlay:
    BG = (0, 0, 0, 60)
    BOX_BG = (30, 30, 45, 240)
    BOX_BORDER = (110, 190, 255)
    TEXT = (240, 240, 240)
    TITLE = (120, 210, 255)
    HINT = (255, 220, 120)
    BUTTON = (70, 140, 230)
    BUTTON_HOVER = (95, 165, 255)
    BUTTON_TEXT = (255, 255, 255)
    DIM = (0, 0, 0, 100)
    HIGHLIGHT_BORDER = (255, 220, 120)

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_title = pygame.font.SysFont("segoeui", 28, bold=True)
        self.font_text = pygame.font.SysFont("segoeui", 20)
        self.font_hint = pygame.font.SysFont("segoeui", 17)
        self.font_button = pygame.font.SysFont("segoeui", 20, bold=True)
        self.font_small = pygame.font.SysFont("segoeui", 15)

        self.next_button_rect = pygame.Rect(0, 0, 0, 0)
        self.skip_rect = pygame.Rect(0, 0, 0, 0)

        self.box_width = 560
        self.padding = 22
        self.button_width = 140
        self.button_height = 42

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        lines = []
        for paragraph in text.split("\n"):
            if paragraph.strip() == "":
                lines.append("")
                continue

            words = paragraph.split(" ")
            current = ""

            for word in words:
                candidate = f"{current} {word}".strip()
                if font.size(candidate)[0] <= max_width:
                    current = candidate
                else:
                    if current:
                        lines.append(current)
                    current = word

            if current:
                lines.append(current)

        return lines

    def draw_rounded(self, surface, rect, color, radius=14):
        tmp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(tmp, color, tmp.get_rect(), border_radius=radius)
        surface.blit(tmp, rect.topleft)

    def draw(self, step: TutorialStep, index: int, total: int, highlight_rect: Optional[pygame.Rect]):
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill(self.BG)
        self.screen.blit(overlay, (0, 0))

        if highlight_rect:
            dim = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
            dim.fill(self.DIM)

            clear = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
            clear.fill((0, 0, 0, 0))
            dim.blit(clear, highlight_rect.topleft)

            self.screen.blit(dim, (0, 0))
            pygame.draw.rect(
                self.screen,
                self.HIGHLIGHT_BORDER,
                highlight_rect.inflate(8, 8),
                3,
                border_radius=8
            )

        max_text_width = self.box_width - 2 * self.padding
        wrapped = self.wrap_text(step.text, self.font_text, max_text_width)
        line_h = self.font_text.get_linesize()

        title_h = self.font_title.get_linesize() + 8
        text_h = len(wrapped) * line_h
        hint_h = self.font_hint.get_linesize() + 14 if step.hint else 0
        button_h = self.button_height + 12 if step.show_next_button else 0
        footer_h = 28

        box_h = self.padding + title_h + text_h + hint_h + button_h + footer_h + self.padding

        box_x = (screen_w - self.box_width) // 2
        box_y = (screen_h - box_h) // 2

        if highlight_rect:
            margin = 30
            if highlight_rect.right + margin + self.box_width < screen_w:
                box_x = highlight_rect.right + margin
                box_y = max(20, highlight_rect.centery - box_h // 2)
            elif highlight_rect.left - margin - self.box_width > 0:
                box_x = highlight_rect.left - margin - self.box_width
                box_y = max(20, highlight_rect.centery - box_h // 2)
            else:
                box_y = screen_h - box_h - 30

        box_x = max(10, min(box_x, screen_w - self.box_width - 10))
        box_y = max(10, min(box_y, screen_h - box_h - 10))
        box_rect = pygame.Rect(box_x, box_y, self.box_width, box_h)

        self.draw_rounded(self.screen, box_rect, self.BOX_BG, 16)
        pygame.draw.rect(self.screen, self.BOX_BORDER, box_rect, 2, border_radius=16)

        y = box_y + self.padding

        title_surface = self.font_title.render(step.title, True, self.TITLE)
        self.screen.blit(title_surface, (box_x + self.padding, y))
        y += title_h

        for line in wrapped:
            if line == "":
                y += line_h // 2
                continue
            surf = self.font_text.render(line, True, self.TEXT)
            self.screen.blit(surf, (box_x + self.padding, y))
            y += line_h

        if step.hint:
            y += 8
            hint_surface = self.font_hint.render(f"Hinweis: {step.hint}", True, self.HINT)
            self.screen.blit(hint_surface, (box_x + self.padding, y))
            y += hint_h

        if step.show_next_button:
            btn_x = box_x + self.box_width - self.padding - self.button_width
            btn_rect = pygame.Rect(btn_x, y + 4, self.button_width, self.button_height)
            self.next_button_rect = btn_rect

            mouse_pos = pygame.mouse.get_pos()
            color = self.BUTTON_HOVER if btn_rect.collidepoint(mouse_pos) else self.BUTTON
            self.draw_rounded(self.screen, btn_rect, color, 8)

            label = "Fertig" if index == total - 1 else "Weiter"
            label_surface = self.font_button.render(label, True, self.BUTTON_TEXT)
            label_rect = label_surface.get_rect(center=btn_rect.center)
            self.screen.blit(label_surface, label_rect)
        else:
            self.next_button_rect = pygame.Rect(0, 0, 0, 0)

        skip_surface = self.font_small.render("Überspringen", True, (170, 170, 190))
        self.skip_rect = skip_surface.get_rect(topright=(box_x + self.box_width - self.padding, box_y + 8))
        self.screen.blit(skip_surface, self.skip_rect)

        counter = self.font_small.render(f"{index + 1} / {total}", True, (160, 160, 180))
        self.screen.blit(counter, (box_x + self.padding, box_y + box_h - 24))


# ============================================================
# MANAGER
# ============================================================

class TutorialManager:
    def __init__(self, screen: pygame.Surface, left_panel, game_field):
        self.screen = screen
        self.left_panel = left_panel
        self.game_field = game_field

        self.steps = create_tutorial_steps()
        self.index = 0
        self.active = True

        self.overlay = TutorialOverlay(screen)

        self._pan_started = False
        self._pan_start_pos = None

    @property
    def current_step(self) -> Optional[TutorialStep]:
        if 0 <= self.index < len(self.steps):
            return self.steps[self.index]
        return None

    def restart(self):
        self.index = 0
        self.active = True
        self._pan_started = False
        self._pan_start_pos = None

    def finish(self):
        self.active = False

    def next_step(self):
        self.index += 1
        self._pan_started = False
        self._pan_start_pos = None

        if self.index >= len(self.steps):
            self.finish()

    def report_action(self, action: TutorialAction):
        if not self.active:
            return

        step = self.current_step
        if step is None:
            return

        if step.expected_action == action:
            print("Tutorial erkannt:", action)  # DEBUG
            self.next_step()

    def get_highlight_rect(self) -> Optional[pygame.Rect]:
        step = self.current_step
        if step is None:
            return None

        if step.highlight == TutorialHighlight.CURRENT_CARD:
            return self.left_panel.middle_rect.copy()

        if step.highlight == TutorialHighlight.ROTATE_BUTTON:
            cb = self.left_panel.circle_button
            return pygame.Rect(
                cb.center[0] - cb.radius,
                cb.center[1] - cb.radius,
                cb.radius * 2,
                cb.radius * 2
            )

        if step.highlight == TutorialHighlight.BOARD:
            return self.game_field.rect.copy()

        if step.highlight == TutorialHighlight.PLAYERS:
            if self.left_panel.player_rects:
                top = self.left_panel.player_rects[0]
                bottom = self.left_panel.player_rects[-1]
                return pygame.Rect(top.x, top.y, top.width, bottom.bottom - top.top)

        return None

    def handle_event(self, event) -> bool:
        if not self.active:
            return False

        step = self.current_step
        if step is None:
            return False

        # ------------------------------------------------
        # Overlay-Buttons
        # ------------------------------------------------
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.overlay.skip_rect.collidepoint(event.pos):
                self.finish()
                return True

            if step.show_next_button and self.overlay.next_button_rect.collidepoint(event.pos):
                if step.expected_action in (TutorialAction.CLICK_NEXT, TutorialAction.FINISH):
                    self.next_step()
                    return True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.finish()
                return True
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if step.show_next_button and step.expected_action in (TutorialAction.CLICK_NEXT, TutorialAction.FINISH):
                    self.next_step()
                    return True

        # 2. FOR PANNING STEP: Track progress but let the event pass to the game_field
        if step.expected_action == TutorialAction.PAN_BOARD:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_field.rect.collidepoint(event.pos):
                    self._pan_started = True
                    self._pan_start_pos = event.pos
            elif event.type == pygame.MOUSEMOTION and self._pan_started and self._pan_start_pos is not None:
                dx = abs(event.pos[0] - self._pan_start_pos[0])
                dy = abs(event.pos[1] - self._pan_start_pos[1])
                if dx + dy > 20:  # Slightly higher threshold for better feel
                    self.report_action(TutorialAction.PAN_BOARD)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._pan_started = False
            return False  # Let the game field handle the actual movement

        # 3. FOR OTHER INTERACTIVE STEPS (Rotate, Place, Zoom):
        # Allow events to pass through so the player can actually do the action
        if step.expected_action in (TutorialAction.ROTATE_CARD, TutorialAction.PLACE_CARD, TutorialAction.ZOOM_BOARD):
            return False

        # 4. FOR INFORMATIVE STEPS: Block ALL mouse/keyboard events 
        # so the background cannot be moved while reading.
        if step.expected_action in (TutorialAction.CLICK_NEXT, TutorialAction.FINISH):
            # We return True to "consume" the event so main.py hits 'continue'
            return True

        #return False

        # ------------------------------------------------
        # Interaktive Schritte
        # ------------------------------------------------
        if step.expected_action == TutorialAction.ROTATE_CARD:
            return False

        if step.expected_action == TutorialAction.PLACE_CARD:
            return False

        if step.expected_action == TutorialAction.PAN_BOARD:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_field.rect.collidepoint(event.pos):
                    self._pan_started = True
                    self._pan_start_pos = event.pos

            elif event.type == pygame.MOUSEMOTION and self._pan_started and self._pan_start_pos is not None:
                dx = abs(event.pos[0] - self._pan_start_pos[0])
                dy = abs(event.pos[1] - self._pan_start_pos[1])
                if dx + dy > 12:
                    self.next_step()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._pan_started = False
                self._pan_start_pos = None

            return False

        if step.expected_action == TutorialAction.ZOOM_BOARD:
            return False

        # ------------------------------------------------
        # Rein informative Schritte: Spiel blockieren
        # ------------------------------------------------
        if step.expected_action in (TutorialAction.CLICK_NEXT, TutorialAction.FINISH):
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                if self.overlay.next_button_rect.collidepoint(getattr(event, "pos", (-1, -1))):
                    return False
                if self.overlay.skip_rect.collidepoint(getattr(event, "pos", (-1, -1))):
                    return False
                return True

        return False

    def draw(self):
        if not self.active:
            return

        step = self.current_step
        if step is None:
            return

        self.overlay.draw(
            step=step,
            index=self.index,
            total=len(self.steps),
            highlight_rect=self.get_highlight_rect()
        )