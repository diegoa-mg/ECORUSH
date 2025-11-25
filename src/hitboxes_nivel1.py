import pygame

ROOM_HITBOXES_NIVEL1: dict[str, list[pygame.Rect]] = {
    # Nivel 1
    "entrada_nivel1.png": [
        pygame.Rect(1318,340,329,277),
        pygame.Rect(214,184,159,169),
        pygame.Rect(464,234,111,139),
        pygame.Rect(24,633,202,166),
        pygame.Rect(27,3,597,262),
        pygame.Rect(1318,2,573,257),


        
    ],
    "sala_nivel1.png": [
        pygame.Rect(30,18,241,202),  
        pygame.Rect(672,9,1036,199),
        pygame.Rect(732, 40, 993, 209),
        pygame.Rect(1422, 380, 31, 421),
        pygame.Rect(1424,624,489,239),
        pygame.Rect(1464,461,110,144),
        pygame.Rect(451,389,105,34),
        pygame.Rect(315,573,370,76),
        
    ],
    "cocina_nivel1.png": [
        pygame.Rect(1485, 35,426,411),
        pygame.Rect(230,30,1001,406),
        pygame.Rect(651,609,748,274),

    ],
    "garaje_nivel1.png": [
        pygame.Rect(9,9,262,151),
        pygame.Rect(195,18,1711,232),
        pygame.Rect(138,684,919,235),
        pygame.Rect(366,588,493,85),

    ],
    "cuarto1_nivel1.png": [
        pygame.Rect(27, 27, 304, 484),
        pygame.Rect(330, 21, 274,235),
        pygame.Rect(414, 234, 190, 88),
        pygame.Rect(1219, 4, 33, 797),
        pygame.Rect(1519, 544, 397, 254),
        pygame.Rect(1251, 8, 122, 308),
        pygame.Rect(1382, 46, 509, 149),
    ],
    "cuarto2_nivel1.png": [
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
    # Nivel 2
    # Nivel 3
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