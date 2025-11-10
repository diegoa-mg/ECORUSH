import pygame, os, math, sys
import settings
from settings import WIDTH, HEIGHT, FPS, load_img, make_blur, make_hover_pair, play_music, pause_music, resume_music

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    # === Música de menú niveles ===
    # Reanuda si estaba pausada; si no hay música, la inicia.
    try:
        resume_music()
    except Exception:
        pass
    if not pygame.mixer.music.get_busy():
        play_music("musica_menu_niveles.mp3", volume=0.6, loops=-1)

    # === Cargar imágenes ===
    bg_niv       = load_img("fondoniv.png", alpha=False)
    boton_volver   = load_img("flecha_para_regresar.png")    
    boton_config_niv = load_img("configuracion_niveles.png")
    config_x     = load_img("config_x.png")

    # --- Diccionario para imágenes de idioma ---
    btn_images = { "esp": {}, "eng": {} }

    # Carga imágenes en Español
    btn_images["esp"]["titulo_niveles"] = load_img("tituloniveles.png")
    btn_images["esp"]["boton_nivel1"] = load_img("nivel_uno_menu.png")
    btn_images["esp"]["boton_nivel2"] = load_img("nivel_dos_menu.png")
    btn_images["esp"]["boton_nivel3"] = load_img("nivel_tres_menu.png")
    btn_images["eng"]["config"] = load_img("config.png")

    # Carga tus nuevas imágenes en Inglés
    btn_images["eng"]["titulo_niveles"] = load_img("tituloniveles_eng.png")
    btn_images["eng"]["boton_nivel1"] = load_img("nivel_uno_menu_eng.png")
    btn_images["eng"]["boton_nivel2"] = load_img("nivel_dos_menu_eng.png")
    btn_images["eng"]["boton_nivel3"] = load_img("nivel_tres_menu_eng.png")
    btn_images["eng"]["config"] = load_img("config_eng.png")

    # === Escalar las imagenes ===
    bg_niv         = pygame.transform.scale(bg_niv, (3840, 1080))
    titulo_niveles  = pygame.transform.scale(titulo_niveles, (1669.5, 250))
    boton_nivel1    = pygame.transform.scale(boton_nivel1, (466.5, 192.5))
    boton_nivel2    = pygame.transform.scale(boton_nivel2, (466.5, 192.5))
    boton_nivel3    = pygame.transform.scale(boton_nivel3, (466.5, 192.5))
    boton_volver    = pygame.transform.scale(boton_volver, (175, 174.5))
    boton_config_niv = pygame.transform.scale(boton_config_niv, (175.5, 175))
    config       = pygame.transform.scale(config, (1290, 733.5))
    config_x     = pygame.transform.scale(config_x, (48, 48.5))

    # === Animacion de botones ===
    boton_nivel1_orig, boton_nivel1_hover = make_hover_pair(boton_nivel1, 1.05)
    boton_nivel2_orig, boton_nivel2_hover = make_hover_pair(boton_nivel2, 1.05)
    boton_nivel3_orig, boton_nivel3_hover = make_hover_pair(boton_nivel3, 1.05)
    boton_volver_orig, boton_volver_hover = make_hover_pair(boton_volver, 1.05)
    boton_config_niv_orig, boton_config_niv_hover = make_hover_pair(boton_config_niv, 1.05)
    config_x_orig, config_x_hover = make_hover_pair(config_x, 1.05)

    # === Definir rects de botones (hitboxes) ===
    rect_nivel1 = boton_nivel1.get_rect(topleft=(210.25, 545))
    rect_nivel2 = boton_nivel2.get_rect(topleft=(726.75, 545))
    rect_nivel3 = boton_nivel3.get_rect(topleft=(1243.25, 545))
    rect_volver = boton_volver.get_rect(topleft=(30, 875.5)) # Esquina inferior izquierda
    rect_config_niv = boton_config_niv.get_rect(topleft=(1714.5, 875.5))  # Esquina inferior derecha
    config_rect   = config.get_rect(center=(WIDTH//2, HEIGHT//2))
    config_x_rect = config_x.get_rect(topright=(config_rect.right-20, config_rect.top+20))

    # === Offset Menu Niveles (movimiento del fondo menu niveles) ===
    bg_niv_width = bg_niv.get_width()
    bg_niv_height = bg_niv.get_height()
    bg_niv_x = 0  # desplazamiento inicial
    scroll_speed_niv = 1.4  # velocidad (px por frame)

    # === Superficie para renderizar el menú (para blur) ===
    menu_surface = pygame.Surface((WIDTH, HEIGHT)).convert()

    # === Estado del juego ===
    game_state = "niveles"

    # === Bucle principal ===
    running = True
    while running:     
        clock.tick(FPS)  
            
        for event in pygame.event.get():         
            if event.type == pygame.QUIT:             
                running = False  

            # === Botones ===
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Botones en config
                if game_state == "config_niv":
                    # Regresar al menu (click en X)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if config_x_rect.collidepoint(event.pos):
                            game_state = "niveles"
                            print("Cerrando configuración.")

                # Botones del menu niveles
                elif game_state == "niveles":
                    if rect_nivel1.collidepoint(event.pos):
                        print("Ir a Selector Nivel 1")
                        return "sel_nivel1"
                    elif rect_nivel2.collidepoint(event.pos):
                        print("Ir Selector Nivel 2")
                        pause_music()
                        return "sel_nivel2"
                    elif rect_nivel3.collidepoint(event.pos):
                        print("Ir Selector Nivel 3")
                        pause_music()
                        return "sel_nivel3"
                    elif rect_volver.collidepoint(event.pos):
                        print("Regresando al menú principal")
                        return "menu"
                    elif rect_config_niv.collidepoint(event.pos):
                        previous_state = "niveles"
                        game_state = "config_niv"
                        print("Ir a CONFIGURACIÓN en niveles")

            # Usar la tecla ESC para salir de configuracion
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state in "config_niv":
                    print("Cerrando configuración.")
                    game_state = "niveles"
                        
        # === ZONA DE DIBUJO según el estado ===

        # === Menú de niveles ===
        if game_state == "niveles":
            # Actualizar posicion del fondo    
            bg_niv_x -= scroll_speed_niv
            if bg_niv_x <= -bg_niv_width:
                bg_niv_x = 0

            # Fondo
            menu_surface.blit(bg_niv, (bg_niv_x, 0))
            menu_surface.blit(bg_niv, (bg_niv_x + bg_niv_width, 0))
            blurred = make_blur(menu_surface, factor=0.60, passes=2)
            screen.blit(blurred, (0, 0))
            menu_surface.fill((0, 0, 0))
            
            # Titulo
            screen.blit(titulo_niveles, (125.25, 100))

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # BOTON NIVEL 1
            if rect_nivel1.collidepoint(mouse_pos):
                r = boton_nivel1_hover.get_rect(center=rect_nivel1.center)
                screen.blit(boton_nivel1_hover, r.topleft)
            else:
                screen.blit(boton_nivel1_orig, rect_nivel1.topleft)

            # BOTON NIVEL 2
            if rect_nivel2.collidepoint(mouse_pos):
                r = boton_nivel2_hover.get_rect(center=rect_nivel2.center)
                screen.blit(boton_nivel2_hover, r.topleft)
            else:
                screen.blit(boton_nivel2_orig, rect_nivel2.topleft)

            # BOTON NIVEL 3
            if rect_nivel3.collidepoint(mouse_pos):
                r = boton_nivel3_hover.get_rect(center=rect_nivel3.center)
                screen.blit(boton_nivel3_hover, r.topleft)
            else:
                screen.blit(boton_nivel3_orig, rect_nivel3.topleft)

            # BOTON VOLVER
            if rect_volver.collidepoint(mouse_pos):
                r = boton_volver_hover.get_rect(center=rect_volver.center)
                screen.blit(boton_volver_hover, r.topleft)
            else:
                screen.blit(boton_volver_orig, rect_volver.topleft)

            # BOTON CONFIG
            if rect_config_niv.collidepoint(mouse_pos):
                r = boton_config_niv_hover.get_rect(center=rect_config_niv.center)
                screen.blit(boton_config_niv_hover, r.topleft)
            else:
                screen.blit(boton_config_niv_orig, rect_config_niv.topleft)

        # === Config niveles ===
        elif game_state == "config_niv":
            # Actualizar posicion del fondo
            bg_niv_x -= scroll_speed_niv
            if bg_niv_x <= -bg_niv_width:
                bg_niv_x = 0
            
            # Poner blur al menu principal
            menu_surface.blit(bg_niv, (bg_niv_x, 0))
            menu_surface.blit(bg_niv, (bg_niv_x + bg_niv_width, 0))
            menu_surface.blit(titulo_niveles, (125.25, 100))
            menu_surface.blit(boton_nivel1, rect_nivel1.topleft)
            menu_surface.blit(boton_nivel2, rect_nivel2.topleft)
            menu_surface.blit(boton_nivel3, rect_nivel3.topleft)
            menu_surface.blit(boton_volver, rect_volver.topleft)
            menu_surface.blit(boton_config_niv, rect_config_niv.topleft)

            blurred = make_blur(menu_surface, factor=0.40, passes=2)
            screen.blit(blurred, (0, 0))
            menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

            # Dibujar el panel
            screen.blit(config, config_rect.topleft)
            
            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # X
            if config_x_rect.collidepoint(mouse_pos):
                r = config_x_hover.get_rect(center=config_x_rect.center)
                screen.blit(config_x_hover, r.topleft)
            else:
                screen.blit(config_x_orig, config_x_rect.topleft)

        pygame.display.flip()
    
    return "menu"