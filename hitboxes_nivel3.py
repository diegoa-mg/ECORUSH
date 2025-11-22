import pygame

ROOM_HITBOXES_NIVEL3: dict[str, list[pygame.Rect]] = {
    "cuarto_nivel3.png": [],
    "cuarto2_nivel3.png": [
        pygame.Rect(34, 138, 228, 464),
        pygame.Rect(484, 162, 215, 258),
        pygame.Rect(742, 576, 144, 305),
        pygame.Rect(1210, 162, 212, 143),
    ],
}

def dibujar_overlay(screen: pygame.Surface, habitacion: str,
                    color_relleno: tuple = (0, 255, 0, 90),
                    color_borde: tuple = (0, 255, 0, 180),
                    grosor_borde: int = 3):
    rects = ROOM_HITBOXES_NIVEL3.get(habitacion, [])
    if not rects:
        return
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for r in rects:
        pygame.draw.rect(overlay, color_relleno, r)
        pygame.draw.rect(overlay, color_borde, r, grosor_borde)
    screen.blit(overlay, (0, 0))