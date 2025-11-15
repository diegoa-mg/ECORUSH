import pygame, os, math, sys
import settings
from settings import WIDTH, HEIGHT, FPS, load_img, make_blur, make_hover_pair, blit_hoverable, resume_music, play_music, pause_music, set_next_music, set_selected_character

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    # === Música en selector de nivel 1: reanuda o inicia si no está activa ===
    try:
        resume_music()
    except Exception:
        pass
    if not pygame.mixer.get_init() or not pygame.mixer.music.get_busy():
        play_music("musica_menu_niveles.mp3", volume=0.6, loops=-1)

    # === Cargar imagenes ===
    bg_niv       = load_img("fondoniv.png", alpha=False)
    btn_jugar      = load_img("play_jugar_N.png")
    nivel_x        = load_img("niv_x.png")
    personaje1     = load_img("selec_pjizq.png")
    personaje2     = load_img("selec_pjder.png")
    personaje1_2   = load_img("selec_pjizq2.png")
    personaje2_2   = load_img("selec_pjder2.png")

    # --- Diccionario para imágenes de idioma ---
    btn_images = { "esp": {}, "eng": {} }

    # Carga imágenes en Español
    btn_images["esp"]["titulo_niv1"] = load_img("tituloniv1.png")
    btn_images["esp"]["selector_nivel"] = load_img("selector_nivel.png")
    btn_images["esp"]["btn_sencillo"] = load_img("dificultad_sencillo.png")
    btn_images["esp"]["btn_extremo"] = load_img("dificultad_extremo.png")
    btn_images["esp"]["btn_sencillo2"] = load_img("btn_sencillo2.png")
    btn_images["esp"]["btn_extremo2"] = load_img("btn_extremo2.png")

    # Carga tus nuevas imágenes en Inglés (Asumiendo nombres)
    btn_images["eng"]["titulo_niv1"] = load_img("tituloniv1_eng.png")
    btn_images["eng"]["selector_nivel"] = load_img("selector_nivel_eng.png")
    btn_images["eng"]["btn_sencillo"] = load_img("dificultad_sencillo_eng.png")
    btn_images["eng"]["btn_extremo"] = load_img("dificultad_extremo_eng.png")
    btn_images["eng"]["btn_sencillo2"] = load_img("btn_sencillo2_eng.png")
    btn_images["eng"]["btn_extremo2"] = load_img("btn_extremo2_eng.png")

    # === Escalar las imagenes ===
    bg_niv         = pygame.transform.scale(bg_niv, (3840, 1080))
    btn_jugar       = pygame.transform.scale(btn_jugar, (146.5, 146.5))
    nivel_x         = pygame.transform.scale(nivel_x, (48, 48))
    personaje1      = pygame.transform.scale(personaje1, (276, 174.5))
    personaje2      = pygame.transform.scale(personaje2, (276, 174.5))
    personaje1_2      = pygame.transform.scale(personaje1_2, (276, 174.5))
    personaje2_2      = pygame.transform.scale(personaje2_2, (276, 174.5))

    for lang in ["esp", "eng"]:
        btn_images[lang]["titulo_niv1"] = pygame.transform.scale(btn_images[lang]["titulo_niv1"], (1669.5, 250))
        btn_images[lang]["selector_nivel"] = pygame.transform.scale(btn_images[lang]["selector_nivel"], (1061, 437))
        btn_images[lang]["btn_sencillo"] = pygame.transform.scale(btn_images[lang]["btn_sencillo"], (276, 105.5))
        btn_images[lang]["btn_extremo"] = pygame.transform.scale(btn_images[lang]["btn_extremo"], (276, 105.5))
        btn_images[lang]["btn_sencillo2"] = pygame.transform.scale(btn_images[lang]["btn_sencillo2"], (276, 105.5))
        btn_images[lang]["btn_extremo2"] = pygame.transform.scale(btn_images[lang]["btn_extremo2"], (276, 105.5))

    # === BOTONES ANIMADOS ===
    btn_jugar_orig, btn_jugar_hover = make_hover_pair(btn_jugar, 1.05)
    nivel_x_orig, nivel_x_hover = make_hover_pair(nivel_x, 1.05)

    # === Definir rects de botones (hitboxes) ===
    nivel_selector_rect = btn_images["esp"]["selector_nivel"].get_rect(topleft=(429.5, 455))
    rect_sencillo = btn_images["esp"]["btn_sencillo"].get_rect(topleft=(710, 500))
    rect_extremo = btn_images["esp"]["btn_extremo"].get_rect(topleft=(1010, 500))
    rect_personaje1 = personaje1.get_rect(topleft=(710, 650))
    rect_personaje2 = personaje2.get_rect(topleft=(1010, 650))
    rect_jugar = btn_jugar.get_rect(topleft=(1320, 590))
    nivel_x_rect = nivel_x.get_rect(topleft=(1412.5, 485))

    # === Offset Menu Niveles (movimiento del fondo menu niveles) ===
    bg_niv_width = bg_niv.get_width()
    bg_niv_height = bg_niv.get_height()
    bg_niv_x = 0  # desplazamiento inicial
    scroll_speed_niv = 1.4  # velocidad (px por frame)

    # === Superficie para renderizar el menú (para blur) ===
    menu_surface = pygame.Surface((WIDTH, HEIGHT)).convert()

    # === Estado del juego ===
    game_state = "selector"

    # Variables del selector de nivel
    nivel_seleccionado = 1      # 1, 2 o 3
    personaje_seleccionado = 1  # 1 o 2

    # === Superficie para renderizar el menú (para blur) ===
    menu_surface = pygame.Surface((WIDTH, HEIGHT)).convert()

    # === Bucle principal ===
    running = True
    while running:     
        clock.tick(FPS)  
            
        for event in pygame.event.get():         
            if event.type == pygame.QUIT:             
                return "quit" 

            # === Botones ===
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Botones del selector de nivel individual
                if game_state == "selector":
                    # Seleccion de dificultad
                    if rect_sencillo.collidepoint(event.pos):
                        settings.DIFICULTAD = "sencillo" 
                        print("Dificultad: Sencillo")
                    elif rect_extremo.collidepoint(event.pos):
                        settings.DIFICULTAD = "extremo"
                        print("Dificultad: Extremo")

                    elif rect_personaje1.collidepoint(event.pos):
                        personaje_seleccionado = 1
                        # Establece personaje global para uso en nivel1
                        try:
                            set_selected_character("niño")
                        except Exception:
                            pass
                        print("Personaje 1 seleccionado")
                    elif rect_personaje2.collidepoint(event.pos):
                        personaje_seleccionado = 2
                        # Establece personaje global para uso en nivel1
                        try:
                            set_selected_character("niña")
                        except Exception:
                            pass
                        print("Personaje 2 seleccionado")
                    elif rect_jugar.collidepoint(event.pos):
                        print(f"Iniciando Nivel {nivel_seleccionado} - Dificultad: {settings.DIFICULTAD} - Personaje: {personaje_seleccionado}")
                        # Asegura que el personaje seleccionado se aplique antes de entrar al nivel
                        try:
                            set_selected_character("niña" if personaje_seleccionado == 2 else "niño")
                        except Exception:
                            pass
                        # Solicita música del nivel según dificultad
                        if nivel_seleccionado == 1:
                            if settings.DIFICULTAD == "sencillo":
                                set_next_music("musica_nivel_facil.mp3")
                            elif settings.DIFICULTAD == "extremo":
                                set_next_music("musica_nivel_extremo.mp3")
                        # Pausar música de menú antes de entrar al nivel
                        pause_music()
                        return "pantalla_carga"
                    
                    # Regresar a niveles
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if nivel_x_rect.collidepoint(event.pos):
                            print("Cerrando selector.")
                            return "niveles"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        print("Cerrando selector.")
                        return "niveles"
                        
        # === ZONA DE DIBUJO ===
        current_lang = settings.language
        current_img = btn_images[current_lang]

        if game_state == "selector":
            
            # Actualizar posicion del fondo
            bg_niv_x -= scroll_speed_niv
            if bg_niv_x <= -bg_niv_width:
                bg_niv_x = 0

            # Fondo con blur (puedes usar bg_niv o uno propio)
            menu_surface.blit(bg_niv, (bg_niv_x, 0))
            menu_surface.blit(bg_niv, (bg_niv_x + bg_niv_width, 0))
            blurred = make_blur(menu_surface, factor=0.60, passes=2)
            screen.blit(blurred, (0, 0))
            menu_surface.fill((0, 0, 0))

            # Titulo
            screen.blit(current_img["titulo_niv1"], (125.25, 100))

            # Ventana azul del selector
            screen.blit(current_img["selector_nivel"], nivel_selector_rect.topleft)
            screen.blit(nivel_x, nivel_x_rect.topleft)

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # Dificultad: elige la imagen en base al estado
            sencillo_img = current_img["btn_sencillo2"] if settings.DIFICULTAD == "sencillo" else current_img["btn_sencillo"]
            extremo_img  = current_img["btn_extremo2"]  if settings.DIFICULTAD == "extremo" else current_img["btn_extremo"]

            blit_hoverable(screen, sencillo_img, rect_sencillo, mouse_pos)
            blit_hoverable(screen, extremo_img,  rect_extremo,  mouse_pos)

            # Personajes
            pj1_img = personaje1_2 if personaje_seleccionado == 1 else personaje1
            pj2_img = personaje2_2 if personaje_seleccionado == 2 else personaje2

            blit_hoverable(screen, pj1_img, rect_personaje1, mouse_pos)
            blit_hoverable(screen, pj2_img, rect_personaje2, mouse_pos)

            # BOTON JUGAR
            if rect_jugar.collidepoint(mouse_pos):
                r = btn_jugar_hover.get_rect(center=rect_jugar.center)
                screen.blit(btn_jugar_hover, r.topleft)
            else:
                screen.blit(btn_jugar_orig, rect_jugar.topleft)

            # X
            if nivel_x_rect.collidepoint(mouse_pos):
                r = nivel_x_hover.get_rect(center=nivel_x_rect.center)
                screen.blit(nivel_x_hover, r.topleft)
            else:
                screen.blit(nivel_x_orig, nivel_x_rect.topleft)

        pygame.display.flip()