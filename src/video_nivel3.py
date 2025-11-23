import pygame
import cv2
from pathlib import Path
import settings

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    pj = settings.get_selected_character()
    nombre = "video_niñaNV3.mp4" if pj == "niña" else "video_niñoNV3.mp4"
    base_dir = Path(__file__).parent.parent
    ruta = base_dir / "assets" / "videos_niveles" / nombre
    cap = cv2.VideoCapture(str(ruta))
    if not cap.isOpened():
        return "nivel3"
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0: fps = 30
    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cap.release()
                    return "niveles"
                if event.key == pygame.K_e:
                    running = False
        frame = cv2.resize(frame, (settings.WIDTH, settings.HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        surf = pygame.surfarray.make_surface(frame)
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)
    cap.release()
    return "nivel3"