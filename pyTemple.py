import pygame
import sys
import random

# --- KONFIGURATION ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
FONT_SIZE = 12
BG_COLOR = (0, 0, 191) 
TEXT_COLOR = (255, 255, 255)

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TempleOS Py - Graphic Mode")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier New", FONT_SIZE, bold=True)

# --- SYSTEM ZUSTAND ---
console_lines = ["TempleOS v0.01", "Definiere eine Funktion 'loop()', um zu animieren."]
current_input = ""
cursor_visible = True
blink_timer = 0
show_console = True # Toggle, um Konsole auszublenden für Spiele

# --- GRAFIK API (Die Werkzeuge für den User) ---

def cls():
    """Löscht die Konsole"""
    global console_lines
    console_lines = []

def toggle():
    """Schaltet Text an/aus"""
    global show_console
    show_console = not show_console

def rect(x, y, w, h, color=(255, 255, 255)):
    pygame.draw.rect(screen, color, (x, y, w, h))

def circle(x, y, r, color=(255, 255, 0)):
    pygame.draw.circle(screen, color, (x, y), r)

def line(x1, y1, x2, y2, color=(255, 0, 0)):
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)

# Hilfsfunktion, um Tasten im Loop abzufragen
def is_key_pressed(key_name):
    keys = pygame.key.get_pressed()
    # Mapping von String zu Pygame Key (vereinfacht)
    if key_name == "left": return keys[pygame.K_LEFT]
    if key_name == "right": return keys[pygame.K_RIGHT]
    if key_name == "up": return keys[pygame.K_UP]
    if key_name == "down": return keys[pygame.K_DOWN]
    return False

# --- KERNEL ---

def execute_command(command):
    console_lines.append(f"> {command}")
    try:
        # Führt Code im globalen Kontext aus
        exec(command, globals())
    except Exception as e:
        console_lines.append(f"Err: {e}")

# --- MAIN LOOP ---
running = True
while running:
    # 1. Standard Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                execute_command(current_input)
                current_input = ""
            elif event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]
            elif event.key == pygame.K_F1: # F1 zum Umschalten der Konsole
                toggle()
            else:
                current_input += event.unicode

    # 2. Background Reset
    screen.fill(BG_COLOR)

    # 3. USER LOOP HOOK (Das Herzstück)
    # Wir schauen, ob der User eine Funktion 'loop' definiert hat
    if 'loop' in globals() and callable(globals()['loop']):
        try:
            globals()['loop']()
        except Exception as e:
            # Wenn der User-Code crasht, löschen wir den Loop, damit das OS nicht abstürzt
            console_lines.append(f"Crash in loop(): {e}")
            del globals()['loop']

    # 4. GUI Overlay (Konsole)
    if show_console:
        y_offset = 10
        line_height = FONT_SIZE + 2
        max_lines = (SCREEN_HEIGHT - 60) // line_height
        
        # Halbtransparenter Hintergrund für Text, damit man Spiel dahinter sieht
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(50)
        s.fill((0,0,0))
        screen.blit(s, (0,0))

        for line in console_lines[-max_lines:]:
            txt = font.render(str(line), True, TEXT_COLOR)
            screen.blit(txt, (10, y_offset))
            y_offset += line_height

        # Input Zeile
        inp = font.render(f"> {current_input}", True, (0, 255, 0))
        screen.blit(inp, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()