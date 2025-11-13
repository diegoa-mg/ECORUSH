# === Importar bibliotecas ===
import pygame, math
from pathlib import Path

# === Variable Idioma ===
language = "esp" # esp/eng

# === DIFICULTAD ===
DIFICULTAD = "sencillo"  # Puede ser "sencillo" o "extremo"

# Este diccionario guarda lo que significa cada dificultad
# Es mucho más limpio que tener TIEMPO_SENCILLO, TIEMPO_EXTREMO, etc.
VALORES_DIFICULTAD = {
    "sencillo": {
        "TIEMPO_LIMITE": 150,      # segundos
        "VELOCIDAD_ENERGIA": 2,    # El drenaje de energía es 2
        "VELOCIDAD_ENERGIA_CORRER": 4, # El drenaje al correr es 4
        "RECARGA_ENERGIA": 10 # Recarga 10 de energia
    },
    "extremo": {
        "TIEMPO_LIMITE": 90,       # segundos
        "VELOCIDAD_ENERGIA": 4,    # El drenaje de energía es 4
        "VELOCIDAD_ENERGIA_CORRER": 8, # El drenaje al correr es 8
        "RECARGA_ENERGIA": 5 # Recarga 5 de energia
    }
}

# === Personaje seleccionado ===
# Valores posibles: "niño" | "niña"
selected_character = "niño"

def set_selected_character(name: str):
    global selected_character
    name = (name or "").strip().lower()
    if name in ("niño", "nino", "niña", "nina"):
        # normalizar a formas con tilde
        selected_character = "niña" if name in ("niña", "nina") else "niño"
    else:
        selected_character = "niño"

def get_selected_character() -> str:
    return selected_character

# === Colores ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW= (255, 255, 0)
ENERGIA_COLOR= (255, 175, 0)

# === Configurar la ventana ===
FPS = 60 
WIDTH, HEIGHT = 1920, 1080

# === Rutas relativas con pathlib ===
# BASE_DIR: carpeta donde esta el archivo main.py
BASE_DIR = Path(__file__).resolve().parent
# IMG_DIR: carpeta donde se guardan las imagenes del proyecto
IMG_DIR = BASE_DIR / "assets" / "img"
# MUSIC_DIR: carpeta donde se guardan las músicas del proyecto
MUSIC_DIR = BASE_DIR / "assets" / "musica"

# === Helper para cargar imagen ===
"""
- name: nombre del archivo
- alpha: True usa conver_alpha() para png con transparencia
         False usa convert() para png sin transparencia
"""
def load_img(name, alpha=True):
    path = IMG_DIR / name # une la carpeta con el nombre del archivo
    surf = pygame.image.load(str(path)) # pygame necesita string, por eso se usa el str
    return surf.convert_alpha() if alpha else surf.convert()

# === Música ===
def play_music(name: str, volume: float = 0.6, loops: int = -1):
    """Carga y reproduce música desde assets/musica.
    - name: nombre del archivo (ej. "musica_menu_niveles.mp3")
    - volume: 0.0 a 1.0
    - loops: -1 para loop infinito
    """
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        ruta = MUSIC_DIR / name
        pygame.mixer.music.load(str(ruta))
        pygame.mixer.music.set_volume(max(0.0, min(1.0, float(volume))))
        pygame.mixer.music.play(loops)
    except Exception as e:
        print(f"[Audio] No se pudo reproducir '{name}': {e}")

def stop_music():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass

# === Paso de pista entre escenas ===
# Variable global simple para solicitar la siguiente pista al entrar a una escena.
_AUDIO_NEXT_TRACK = None

def set_next_music(name: str | None):
    global _AUDIO_NEXT_TRACK
    _AUDIO_NEXT_TRACK = name

def consume_next_music() -> str | None:
    global _AUDIO_NEXT_TRACK
    name = _AUDIO_NEXT_TRACK
    _AUDIO_NEXT_TRACK = None
    return name

def pause_music():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()
    except Exception:
        pass

def resume_music():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()
    except Exception:
        pass

# === ANIMACION AL TITULO ===
def draw_title_animated(screen, base_surf, center_pos, mode="bob", t_ms=0, amp=1.5,): # amp = amplitud px
    """Dibuja el título con una animación elegida por 'mode' en 'center_pos'."""
    # tiempo en segundos para funciones senoidales
    t = t_ms / 750.0

    surf = base_surf
    rect = surf.get_rect(topleft=center_pos)

    if mode == "bob":
        dy = int(math.sin(t * 2.5) * amp)  # velocidad 2 Hz aprox.
        rect.centery += dy
        screen.blit(surf, rect.topleft)

# === BLUR (downscale/upscale) ===
def make_blur(surf, factor=0.25, passes=2):
    # Devuelve una copia borrosa de 'surf' aplicando smoothscale down/up.
    out = surf
    for _ in range(passes):
        w = max(1, int(out.get_width()  * factor))
        h = max(1, int(out.get_height() * factor))
        out = pygame.transform.smoothscale(out, (w, h))
        out = pygame.transform.smoothscale(out, surf.get_size())
    return out

# === ANIMACION A BOTONES ===
def make_hover_pair(surf, scale=1.05):
    w, h = surf.get_size()
    hover = pygame.transform.smoothscale(surf, (int(w*scale), int(h*scale)))
    return surf, hover

# === Transiciones ===
def fade_to_black(screen, duration_ms=150):
    """Escena visible → negro."""
    overlay = pygame.Surface((WIDTH, HEIGHT)).convert()
    overlay.fill((0, 0, 0))
    clk = pygame.time.Clock()
    t = 0
    while t < duration_ms:
        alpha = int(255 * (t / duration_ms))      # 0 → 255
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        t += clk.tick(FPS)                        # usa tu FPS global

def fade_from_black(screen, duration_ms=150):
    """Negro → escena visible."""
    overlay = pygame.Surface((WIDTH, HEIGHT)).convert()
    overlay.fill((0, 0, 0))
    clk = pygame.time.Clock()
    t = 0
    while t < duration_ms:
        alpha = int(255 - 255 * (t / duration_ms))  # 255 → 0
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        t += clk.tick(FPS)

def with_fade(run_fn, in_ms=100, out_ms=100):
    """Aplica fade-in automático al entrar a una escena."""
    def _wrapped(screen, clock):
        fade_from_black(screen, in_ms)
        return run_fn(screen, clock)
    return _wrapped

def blit_hoverable(screen, surf_base, rect_base, mouse_pos):
        if rect_base.collidepoint(mouse_pos):
            w, h = surf_base.get_size()
            hover = pygame.transform.smoothscale(surf_base, (int(w*1.05), int(h*1.05)))
            r = hover.get_rect(center=rect_base.center)
            screen.blit(hover, r.topleft)
        else:
            screen.blit(surf_base, rect_base.topleft)