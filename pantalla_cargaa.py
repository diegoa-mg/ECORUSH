import pygame
import settings
from settings import WIDTH, HEIGHT, FPS, load_img


def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    """
    Pantalla de carga / tutorial previa al nivel.
    - Fondo: "pantalla_tutorial.png"
    - Avanza al nivel al presionar la tecla E
    - Si no se presiona E en 10 segundos, avanza automáticamente
    - ESC regresa al menú de niveles
    """

    # Cargar fondo y ayudas según idioma
    bg = load_img("pantalla_tutorial.png", alpha=False)
    
   
    inicio_ms = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "niveles"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return "nivel1"
                if event.key == pygame.K_ESCAPE:
                    return "niveles"

        # Avance automático después de 10 segundos si no se presiona E
        elapsed_ms = pygame.time.get_ticks() - inicio_ms
        if elapsed_ms >= 10_000:
            return "nivel1"

        # Dibujo
        screen.blit(bg, (0, 0))
       
        pygame.display.flip()

    # Por seguridad, si saliera del bucle
    return "nivel1"