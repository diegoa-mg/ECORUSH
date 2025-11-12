import pygame, os, math, sys
import settings
from settings import WIDTH, HEIGHT, FPS, load_img, make_blur, make_hover_pair, blit_hoverable, play_music, pause_music, resume_music, consume_next_music

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    # === Música de menú niveles ===
    # Si desde la escena anterior se solicitó una pista, la aplicamos;
    # de lo contrario, reanudamos la música existente y solo iniciamos
    # si no hay nada reproduciéndose.
    try:
        next_track = consume_next_music()
        if next_track:
            play_music(next_track, volume=0.6, loops=-1)
        else:
            try:
                resume_music()
            except Exception:
                pass
            if not pygame.mixer.music.get_busy():
                play_music("musica_menu_niveles.mp3", volume=0.6, loops=-1)
    except Exception:
        # En caso de error, aseguremos la música del menú.
        try:
            play_music("musica_menu_niveles.mp3", volume=0.6, loops=-1)
        except Exception:
            pass

    # === Cargar imágenes ===
    bg_niv       = load_img("fondoniv.png", alpha=False)
    boton_volver   = load_img("flecha_para_regresar.png")    
    boton_config_niv = load_img("configuracion_niveles.png")
    config_x     = load_img("config_x.png")
    esp_on       = load_img("esp_on.png")
    esp_off      = load_img("esp_off.png")
    eng_on       = load_img("eng_on.png")
    eng_off      = load_img("eng_off.png")

    # --- Diccionario para imágenes de idioma ---
    btn_images = { "esp": {}, "eng": {} }

    # Carga imágenes en Español
    btn_images["esp"]["titulo_niveles"] = load_img("tituloniveles.png")
    btn_images["esp"]["boton_nivel1"] = load_img("nivel_uno_menu.png")
    btn_images["esp"]["boton_nivel2"] = load_img("nivel_dos_menu.png")
    btn_images["esp"]["boton_nivel3"] = load_img("nivel_tres_menu.png")
    btn_images["esp"]["config"] = load_img("config.png")
    btn_images["esp"]["botones_config"] = load_img("botonesconfig.png")

    # Carga tus nuevas imágenes en Inglés
    btn_images["eng"]["titulo_niveles"] = load_img("tituloniveles_eng.png")
    btn_images["eng"]["boton_nivel1"] = load_img("nivel_uno_menu_eng.png")
    btn_images["eng"]["boton_nivel2"] = load_img("nivel_dos_menu_eng.png")
    btn_images["eng"]["boton_nivel3"] = load_img("nivel_tres_menu_eng.png")
    btn_images["eng"]["config"] = load_img("config_eng.png")
    btn_images["eng"]["botones_config"] = load_img("botonesconfig_eng.png")

    # === Escalar las imagenes ===
    bg_niv         = pygame.transform.scale(bg_niv, (3840, 1080))
    boton_volver    = pygame.transform.scale(boton_volver, (175, 174.5))
    boton_config_niv = pygame.transform.scale(boton_config_niv, (175.5, 175))
    config_x     = pygame.transform.scale(config_x, (48, 48.5))
    esp_on       = pygame.transform.scale(esp_on, (364, 131.5))
    esp_off      = pygame.transform.scale(esp_off, (364, 131.5))
    eng_on       = pygame.transform.scale(eng_on, (364, 131.5))
    eng_off      = pygame.transform.scale(eng_off, (364, 131.5))

    for lang in ["esp", "eng"]:
        btn_images[lang]["titulo_niveles"] = pygame.transform.scale(btn_images[lang]["titulo_niveles"], (1669.5, 250))
        btn_images[lang]["boton_nivel1"] = pygame.transform.scale(btn_images[lang]["boton_nivel1"], (466.5, 192.5))
        btn_images[lang]["boton_nivel2"] = pygame.transform.scale(btn_images[lang]["boton_nivel2"], (466.5, 192.5))
        btn_images[lang]["boton_nivel3"] = pygame.transform.scale(btn_images[lang]["boton_nivel3"], (466.5, 192.5))
        btn_images[lang]["config"] = pygame.transform.scale(btn_images[lang]["config"], (1290, 733.5))
        btn_images[lang]["botones_config"] = pygame.transform.scale(btn_images[lang]["botones_config"], (768, 259.5))

    # === Animacion de botones ===
    boton_volver_orig, boton_volver_hover = make_hover_pair(boton_volver, 1.05)
    boton_config_niv_orig, boton_config_niv_hover = make_hover_pair(boton_config_niv, 1.05)
    config_x_orig, config_x_hover = make_hover_pair(config_x, 1.05)

    # Diccionario para guardar las animaciones (orig, hover)
    btn_anim = { "esp": {}, "eng": {} } 

    # Anima las imágenes que cambian de idioma
    for lang in ["esp", "eng"]:
        btn_anim[lang]["boton_nivel1_orig"], btn_anim[lang]["boton_nivel1_hover"] = make_hover_pair(btn_images[lang]["boton_nivel1"], 1.05)
        btn_anim[lang]["boton_nivel2_orig"], btn_anim[lang]["boton_nivel2_hover"] = make_hover_pair(btn_images[lang]["boton_nivel2"], 1.05)
        btn_anim[lang]["boton_nivel3_orig"], btn_anim[lang]["boton_nivel3_hover"] = make_hover_pair(btn_images[lang]["boton_nivel3"], 1.05)

    # === Definir rects de botones (hitboxes) ===
    # Rects de botones que cambian de idioma (usamos "esp" como referencia)
    rect_nivel1 = btn_images["esp"]["boton_nivel1"].get_rect(topleft=(210.25, 545))
    rect_nivel2 = btn_images["esp"]["boton_nivel2"].get_rect(topleft=(726.75, 545))
    rect_nivel3 = btn_images["esp"]["boton_nivel3"].get_rect(topleft=(1243.25, 545))
    config_rect   = btn_images["esp"]["config"].get_rect(center=(WIDTH//2, HEIGHT//2))

    # Resto rects
    rect_volver = boton_volver.get_rect(topleft=(30, 875.5))
    rect_config_niv = boton_config_niv.get_rect(topleft=(1714.5, 875.5))
    config_x_rect = config_x.get_rect(topright=(config_rect.right-20, config_rect.top+20))
    rect_esp   = esp_on.get_rect(topleft=(576, 680))
    rect_eng   = eng_on.get_rect(topleft=(980, 680))

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
                        
                        elif rect_esp.collidepoint(event.pos):
                            settings.language = "esp"
                            print("Idioma: Español")
                        elif rect_eng.collidepoint(event.pos):
                            settings.language = "eng"
                            print("Idioma: Inglés")

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
        current_lang = settings.language
        current_anim = btn_anim[current_lang]
        current_img = btn_images[current_lang]

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
            screen.blit(current_img["titulo_niveles"], (125.25, 100))

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # BOTON NIVEL 1
            if rect_nivel1.collidepoint(mouse_pos):
                r = current_anim["boton_nivel1_hover"].get_rect(center=rect_nivel1.center)
                screen.blit(current_anim["boton_nivel1_hover"], r.topleft)
            else:
                screen.blit(current_anim["boton_nivel1_orig"], rect_nivel1.topleft)

            # BOTON NIVEL 2
            if rect_nivel2.collidepoint(mouse_pos):
                r = current_anim["boton_nivel2_hover"].get_rect(center=rect_nivel2.center)
                screen.blit(current_anim["boton_nivel2_hover"], r.topleft)
            else:
                screen.blit(current_anim["boton_nivel2_orig"], rect_nivel2.topleft)

            # BOTON NIVEL 3
            if rect_nivel3.collidepoint(mouse_pos):
                r = current_anim["boton_nivel3_hover"].get_rect(center=rect_nivel3.center)
                screen.blit(current_anim["boton_nivel3_hover"], r.topleft)
            else:
                screen.blit(current_anim["boton_nivel3_orig"], rect_nivel3.topleft)

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
            menu_surface.blit(current_img["titulo_niveles"], (125.25, 100))
            menu_surface.blit(current_img["boton_nivel1"], rect_nivel1.topleft)
            menu_surface.blit(current_img["boton_nivel2"], rect_nivel2.topleft)
            menu_surface.blit(current_img["boton_nivel3"], rect_nivel3.topleft)
            menu_surface.blit(boton_volver, rect_volver.topleft)
            menu_surface.blit(boton_config_niv, rect_config_niv.topleft)

            blurred = make_blur(menu_surface, factor=0.40, passes=2)
            screen.blit(blurred, (0, 0))
            menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

            # Dibujar el panel (depende del idioma)
            screen.blit(current_img["config"], config_rect.topleft)
            
            # Dibujar el contenido del panel (depende del idioma)
            screen.blit(current_img["botones_config"], (576, 410.25))

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # Dificultad: elige la imagen en base al estado
            esp = esp_on if settings.language == "esp" else esp_off
            eng = eng_on if settings.language == "eng" else eng_off

            blit_hoverable(screen, esp, rect_esp, mouse_pos)
            blit_hoverable(screen, eng, rect_eng, mouse_pos)

            # X
            if config_x_rect.collidepoint(mouse_pos):
                r = config_x_hover.get_rect(center=config_x_rect.center)
                screen.blit(config_x_hover, r.topleft)
            else:
                screen.blit(config_x_orig, config_x_rect.topleft)

        pygame.display.flip()
    
    return "menu"