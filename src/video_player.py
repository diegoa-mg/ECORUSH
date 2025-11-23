import pygame
import cv2
from pathlib import Path
from settings import WIDTH, HEIGHT, stop_music, play_music

def reproducir_video(screen, nombre_video, nombre_audio=None):
    """
    Reproduce video. 
    Retorna: "termino", "saltar" (E), "salir" (ESC) o "quit".
    """
    # 1. Rutas (Ajustado para estar dentro de 'src')
    # __file__ es src/video_player.py -> parent es src -> parent es ECORUSH
    base_dir = Path(__file__).parent.parent
    ruta_video = base_dir / "assets" / "video" / nombre_video
    
    cap = cv2.VideoCapture(str(ruta_video))
    
    if not cap.isOpened():
        print(f"[Video] Error al abrir: {ruta_video}")
        return "saltar" # Si falla, saltamos

    # 2. AUDIO (ESTA ES LA PARTE CORREGIDA)
    # Simplemente reproducimos el archivo que nos pasaron
    if nombre_audio:
        stop_music()
        try:
            # Usamos volumen 1.0 para que se escuche bien el video
            # loops=0 para que suene solo una vez
            play_music(nombre_audio, volume=1.0, loops=0)
        except Exception as e:
            print(f"[Video] Error de audio: {e}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0: fps = 30
    clock = pygame.time.Clock()
    
    estado_salida = "termino" 

    reproduciendo = True
    while reproduciendo:
        ret, frame = cap.read()
        if not ret:
            break # Fin del video
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                # ESC -> Salir
                if event.key == pygame.K_ESCAPE:
                    estado_salida = "salir"
                    reproduciendo = False
                
                # E -> Saltar
                if event.key == pygame.K_e:
                    estado_salida = "saltar"
                    reproduciendo = False

        # Dibujar frame
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        # frame = cv2.flip(frame, 1) # Descomenta si se ve en espejo
        
        video_surf = pygame.surfarray.make_surface(frame)
        screen.blit(video_surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)

    cap.release()
    stop_music() # Detener audio al terminar/saltar
    return estado_salida