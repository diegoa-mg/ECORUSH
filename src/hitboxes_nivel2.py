import pygame

ROOM_HITBOXES_NIVEL2: dict[str, list[pygame.Rect]] = {
    "entrada_nivel2.png": [],
    "sala nivel 2.png": [],
    "cuarto__nivel2.png": [],
    "cocina_nivel2.png": [],
    "baño_nivel2.png": [],
}

def dibujar_overlay(screen: pygame.Surface, habitacion: str,
                    color_relleno: tuple = (0, 255, 0, 90),
                    color_borde: tuple = (0, 255, 0, 180),
                    grosor_borde: int = 3):
    rects = ROOM_HITBOXES_NIVEL2.get(habitacion, [])
    if not rects:
        return
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for r in rects:
        pygame.draw.rect(overlay, color_relleno, r)
        pygame.draw.rect(overlay, color_borde, r, grosor_borde)
    screen.blit(overlay, (0, 0))