import pygame

ROOM_HITBOXES_NIVEL2: dict[str, list[pygame.Rect]] = {
    "entrada_nivel2.png": [
        pygame.Rect(648,8,793,285),
        pygame.Rect(984,148,113,213),
        pygame.Rect(1144,260,305,181),
        pygame.Rect(1596,12,313,273),

    ],
    "sala_nivel2.png": [
        pygame.Rect(30,202,301,137),
        pygame.Rect(380,134,525,187),
        pygame.Rect(880,14,1033,245),
        pygame.Rect(1368,567,430,166),

    ],
    "cuarto_nivel2.png": [
        pygame.Rect(588,48,445,208),
        pygame.Rect(669,78,193,292),
        pygame.Rect(1188,12,319,253),
        pygame.Rect(9,861,430,211),
        pygame.Rect(1224,6,667,238),

    ],
    "cocina_nivel2.png": [
        pygame.Rect(633,22,514,415),
        pygame.Rect(318,255,487,181),
        pygame.Rect(1323,51,382,394),
        pygame.Rect(656,580,625,300), # Mesa del centro
        pygame.Rect(492,676,137,197),
        pygame.Rect(1288,664,149,221),

    ],
    "baño_nivel2.png": [
        pygame.Rect(404,26,1141,233),
        pygame.Rect(1546,8,361,193),
        pygame.Rect(606,464,29,393),
        pygame.Rect(4,616,625,247),
        pygame.Rect(1290,468,331,165),
        pygame.Rect(1292,612,621,245),
        pygame.Rect(32,20,169,295),
       
    ],
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