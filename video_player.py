import pygame
import cv2
from pathlib import Path
from settings import WIDTH, HEIGHT, stop_music, play_music

def reproducir_video(screen, nombre_video, nombre_audio=None):
    """
    Reproduce video. 
    Retorna: "juego" (si termina o presiona E) o "niveles" (si presiona ESC).
    """
    base_dir = Path(__file__).parent
    ruta_video = base_dir / "assets" / "video" / nombre_video
    
    cap = cv2.VideoCapture(str(ruta_video))
    
    if not cap.isOpened():
        print(f"[Video] Error al abrir: {ruta_video}")
        return "juego" # Si falla, pasamos directo al juego

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0: fps = 30
    clock = pygame.time.Clock()
    
    resultado = "juego" # Por defecto, al terminar va al juego

    reproduciendo = True
    while reproduciendo:
        ret, frame = cap.read()
        if not ret:
            break 
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                # ESC -> Salir al menú
                if event.key == pygame.K_ESCAPE:
                    resultado = "salir"
                    reproduciendo = False
                
                # E -> Saltar al juego inmediatamente
                if event.key == pygame.K_e:
                    resultado = "saltar"
                    reproduciendo = False

        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        
        video_surf = pygame.surfarray.make_surface(frame)
        screen.blit(video_surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)

    cap.release()
    stop_music()
    return resultado