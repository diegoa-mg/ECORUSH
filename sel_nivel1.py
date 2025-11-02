import pygame, os, math, sys
from settings import WIDTH, HEIGHT, FPS, load_img, make_blur, make_hover_pair, blit_hoverable, resume_music, play_music, pause_music, set_next_music

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
    nivel_selector = load_img("selector_nivel.png")  # Ventana azul selector
    titulo_niv1 = load_img("tituloniv1.png")
    btn_sencillo   = load_img("dificultad_sencillo.png")         # Botón fácil
    btn_extremo    = load_img("dificultad_extremo.png")       # Botón difícil  
    personaje1     = load_img("selec_pjizq.png")   # Personaje 1
    personaje2     = load_img("selec_pjder.png")    # Personaje 2
    btn_jugar      = load_img("play_jugar_N.png")                 # Botón play
    nivel_x        = load_img("niv_x.png")

    btn_sencillo2 = load_img("btn_sencillo2.png")
    btn_extremo2  = load_img("btn_extremo2.png")
    personaje1_2 = load_img("selec_pjizq2.png")
    personaje2_2 = load_img("selec_pjder2.png")

    # === Escalar las imagenes ===
    bg_niv         = pygame.transform.scale(bg_niv, (3840, 1080))
    titulo_niv1     = pygame.transform.scale(titulo_niv1, (1669.5, 250))

    nivel_selector  = pygame.transform.scale(nivel_selector, (1061, 437))
    btn_sencillo     = pygame.transform.scale(btn_sencillo, (276, 105.5))
    btn_extremo     = pygame.transform.scale(btn_extremo, (276, 105.5))
    personaje1      = pygame.transform.scale(personaje1, (276, 174.5))
    personaje2      = pygame.transform.scale(personaje2, (276, 174.5))
    btn_jugar       = pygame.transform.scale(btn_jugar, (146.5, 146.5))
    nivel_x         = pygame.transform.scale(nivel_x, (48, 48))

    btn_sencillo2 = pygame.transform.scale(btn_sencillo2, (276, 105.5))
    btn_extremo2  = pygame.transform.scale(btn_extremo2, (276, 105.5))
    personaje1_2      = pygame.transform.scale(personaje1_2, (276, 174.5))
    personaje2_2      = pygame.transform.scale(personaje2_2, (276, 174.5))

    # === BOTONES ANIMADOS ===
    btn_sencillo_orig, btn_sencillo_hover = make_hover_pair(btn_sencillo, 1.05)
    btn_extremo_orig, btn_extremo_hover = make_hover_pair(btn_extremo, 1.05)
    btn_jugar_orig, btn_jugar_hover = make_hover_pair(btn_jugar, 1.05)
    personaje1_orig, personaje1_hover = make_hover_pair(personaje1, 1.05)
    personaje2_orig, personaje2_hover = make_hover_pair(personaje2, 1.05)
    nivel_x_orig, nivel_x_hover = make_hover_pair(nivel_x, 1.05)

    # === Definir rects de botones (hitboxes) ===
    nivel_selector_rect = nivel_selector.get_rect(topleft=(429.5, 455))
    rect_sencillo = btn_sencillo.get_rect(topleft=(710, 500))
    rect_extremo = btn_extremo.get_rect(topleft=(1010, 500))
    rect_personaje1 = personaje1.get_rect(topleft=(710, 650))
    rect_personaje2 = personaje2.get_rect(topleft=(1010, 650))
    rect_jugar = btn_jugar.get_rect(topleft=(1320, 590))
    nivel_x_rect = nivel_x.get_rect(topleft=(1412.5, 485))
    rect_sencillo2 = btn_sencillo2.get_rect(topleft=(480, 330))
    rect_extremo2 = btn_extremo2.get_rect(topleft=(680, 330))
    rect_personaje1_2 = personaje1_2.get_rect(topleft=(480, 430))
    rect_personaje2_2 = personaje2_2.get_rect(topleft=(680, 430))

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
    dificultad_seleccionada = "sencillo" # sencillo o extremo
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
                    if rect_sencillo.collidepoint(event.pos):
                        dificultad_seleccionada = "sencillo"
                        print("Dificultad: Sencillo")
                    elif rect_extremo.collidepoint(event.pos):
                        dificultad_seleccionada = "extremo"
                        print("Dificultad: Extremo")
                    elif rect_personaje1.collidepoint(event.pos):
                        personaje_seleccionado = 1
                        print("Personaje 1 seleccionado")
                    elif rect_personaje2.collidepoint(event.pos):
                        personaje_seleccionado = 2
                        print("Personaje 2 seleccionado")
                    elif rect_jugar.collidepoint(event.pos):
                        print(f"Iniciando Nivel {nivel_seleccionado} - Dificultad: {dificultad_seleccionada} - Personaje: {personaje_seleccionado}")
                        # Solicita música del nivel según dificultad
                        if dificultad_seleccionada == "sencillo" and nivel_seleccionado == 1:
                            set_next_music("musica_nivel_facil.mp3")
                        # Pausar música de menú antes de entrar al nivel
                        pause_music()
                        return "nivel1"
                    
                    # Regresar a niveles
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if nivel_x_rect.collidepoint(event.pos):
                            print("Cerrando selector.")
                            return "niveles"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        print("Cerrando selector.")
                        return "niveles"
                        
        # === ZONA DE DIBUJO ===
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
            screen.blit(titulo_niv1, (125.25, 100))

            # Ventana azul del selector
            screen.blit(nivel_selector, nivel_selector_rect.topleft)
            screen.blit(nivel_x, nivel_x_rect.topleft)

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # Dificultad: elige la imagen en base al estado
            sencillo_img = btn_sencillo2 if dificultad_seleccionada == "sencillo" else btn_sencillo
            extremo_img  = btn_extremo2  if dificultad_seleccionada == "extremo" else btn_extremo

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