import pygame
# Importamos el reproductor genérico
from video_player import reproducir_video

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    """
    Pantalla de Introducción.
    - Reproduce 'introduccion.mp4' en bucle.
    - Si presionas E -> Va al Menú Principal ("menu").
    - Si presionas ESC o cierras -> Cierra el juego ("quit").
    """

    while True:
        # Reproduce el video (asegúrate de tener el mp4 y opcionalmente el mp3)
        # Si no tienes audio para la intro, borra el segundo argumento o pon None.
        accion = reproducir_video(screen, "introduccion.mp4", "musica_intro.mp3")
        
        # CASO 1: Presionó E (Saltar) -> Vamos al Menú
        if accion == "saltar":
            return "menu"
            
        # CASO 2: Presionó ESC (Salir) -> Cerramos el juego (es la primera pantalla)
        elif accion == "salir":
            return "quit"
            
        # CASO 3: Cerró la ventana
        elif accion == "quit":
            return "quit"
            
        # CASO 4: El video terminó solo (accion == "termino")
        # No hacemos nada, el 'while True' repite el video automáticamente.