import pygame

ROOM_HITBOXES_NIVEL3: dict[str, list[pygame.Rect]] = {
    "cuarto_nivel3.png": [
        pygame.Rect(9, 616, 412, 244),
        pygame.Rect(705, 6, 30, 858),
        pygame.Rect(736, 12, 265, 245),
        pygame.Rect(1126, 12, 89, 241),
        pygame.Rect(1452, 16, 157, 405),
        # pygame.Rect(1176, 304, 285, 29),
        # pygame.Rect(45, 168, 211, 433),
        pygame.Rect(1642, 766, 245, 313),
        pygame.Rect(1623, 63, 223, 391),
        pygame.Rect(279,153,136,231),
        pygame.Rect(750,72,387,347),
    ],
    "cuarto2_nivel3.png": [
        pygame.Rect(27, 27, 304, 484),
        pygame.Rect(330, 21, 274,235),
        pygame.Rect(414, 234, 190, 88),
        pygame.Rect(1219, 4, 33, 797),
        pygame.Rect(1519, 544, 397, 254),
        pygame.Rect(1251, 8, 122, 308),
        pygame.Rect(1382, 46, 509, 149),
    ],
    "cocina_nivel3.png": [
        pygame.Rect(1205,70,386,331),
        pygame.Rect(335,130,456,271),
        pygame.Rect(651,609,748,274),

    ],
    "comedor_nivel3.png": [
        pygame.Rect(1425,405,178,274),
        pygame.Rect(1263,276,16,224),
        pygame.Rect(1290,525,103,223),
        pygame.Rect(1638,303,97,211),
        pygame.Rect(1638,552,106,205),
        pygame.Rect(124,642,289,107),
        pygame.Rect(156,794,221,63),
        pygame.Rect(34,4,585,255),
        pygame.Rect(1328,0,561,253),

    ],
    "entrada_nivel3.png": [
        pygame.Rect(41,6,1645,247),
        pygame.Rect(465,309,229,85),
        pygame.Rect(1797,681,13,157),
        pygame.Rect(99,189,340,118),
        
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