import pygame

ROOM_HITBOXES_NIVEL1: dict[str, list[pygame.Rect]] = {
    "entrada_nivel1.png": [],
    "sala_nivel1.png": [],
    "cocina_nivel1.png": [],
    "garaje_nivel1.png": [],
    "cuarto1_nivel1.png": [],
    "cuarto2_nivel1.png": [
        pygame.Rect(9, 616, 412, 244),
        pygame.Rect(705, 6, 30, 858),
        pygame.Rect(736, 12, 265, 245),
        pygame.Rect(1126, 12, 89, 241),
        pygame.Rect(1452, 16, 157, 405),
        pygame.Rect(1176, 304, 285, 29),
        pygame.Rect(45, 168, 211, 433),
        pygame.Rect(1642, 766, 245, 313),
        pygame.Rect(1623, 63, 223, 391),
    ],
}

def dibujar_overlay(screen: pygame.Surface, habitacion: str,
                    color_relleno: tuple = (0, 255, 0, 90),
                    color_borde: tuple = (0, 255, 0, 180),
                    grosor_borde: int = 3):
    rects = ROOM_HITBOXES_NIVEL1.get(habitacion, [])
    if not rects:
        return
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for r in rects:
        pygame.draw.rect(overlay, color_relleno, r)
        pygame.draw.rect(overlay, color_borde, r, grosor_borde)
    screen.blit(overlay, (0, 0))