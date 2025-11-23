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
    for i in range(3):
        accion = reproducir_video(screen, "pantalla_tutorial.mp4")

        # 1. Si presionó ESC, nos vamos al menú de niveles inmediatamente
        if accion == "salir":
            # "Cancelamos" la música del nivel y pedimos la del menú
            settings.set_next_music("musica_menu_niveles.mp3")
            return "niveles"
        
        # 2. Si presionó E ("saltar"), rompemos el ciclo y vamos al juego
        if accion == "saltar":
            return settings.CURRENT_LEVEL
    
    # Si el usuario presionó E o el video terminó, vamos al nivel
    return settings.CURRENT_LEVEL