import pygame
import settings
from video_player import reproducir_video

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    """
    Pantalla de carga / tutorial previa al nivel.
    - Reproduce el video tutorial.mp4
    - ESC -> Regresa a "niveles"
    - E (o fin del video) -> Entra al nivel actual
    """
    
    # Reproducimos el video y guardamos qué decidió el usuario
    accion = reproducir_video(screen, "pantalla_tutorial.mp4")

    # Si el usuario presionó ESC, regresamos
    if accion == "niveles":
        return "niveles"
    
    # Si el usuario presionó E o el video terminó, vamos al nivel
    return settings.CURRENT_LEVEL