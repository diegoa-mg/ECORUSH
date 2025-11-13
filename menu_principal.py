import pygame, os, math, sys
import settings
from settings import WIDTH, HEIGHT, FPS, load_img, make_blur, make_hover_pair, draw_title_animated, make_hover_pair, blit_hoverable, resume_music, play_music, consume_next_music

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    # === Música en menú principal ===
    # Aplica pista solicitada desde la escena anterior; si no hay solicitud,
    # reanuda la música actual y sólo inicia si no hay nada reproduciéndose.
    try:
        next_track = consume_next_music()
        if next_track:
            play_music(next_track, volume=0.6, loops=-1)
        else:
            try:
                resume_music()
            except Exception:
                pass
            if not pygame.mixer.get_init() or not pygame.mixer.music.get_busy():
                play_music("musica_menu_niveles.mp3", volume=0.6, loops=-1)
    except Exception:
        try:
            play_music("musica_menu_niveles.mp3", volume=0.6, loops=-1)
        except Exception:
            pass

    # === Cargar imágenes ===
    bg_prin      = load_img("fondoprinci.png", alpha=False) # Se pone ya que no necesita transparencia
    titulo       = load_img("titulo.png")
    botoninicio  = load_img("botoninicio.png")
    botonsalir   = load_img("botonsalir.png")
    tuto         = load_img("tuto.png")
    config_x     = load_img("config_x.png")
    esp_on       = load_img("esp_on.png")
    esp_off      = load_img("esp_off.png")
    eng_on       = load_img("eng_on.png")
    eng_off      = load_img("eng_off.png")

    # --- Diccionario para imágenes de idioma ---
    btn_images = { "esp": {}, "eng": {} }

    # Carga imágenes en Español
    btn_images["esp"]["botonconfig"] = load_img("botonconfig.png")
    btn_images["esp"]["botontuto"]   = load_img("botontuto.png")
    btn_images["esp"]["config"]     = load_img("config.png")
    btn_images["esp"]["botones_tuto"]   = load_img("botones_tutorial.png")
    btn_images["esp"]["botones_config"] = load_img("botonesconfig.png")

    # Carga tus nuevas imágenes en Inglés   
    btn_images["eng"]["botonconfig"] = load_img("botonconfig_eng.png")
    btn_images["eng"]["botontuto"]   = load_img("botontuto_eng.png")
    btn_images["eng"]["config"]   = load_img("config_eng.png")
    btn_images["eng"]["botones_tuto"]   = load_img("botones_tutorial_eng.png")
    btn_images["eng"]["botones_config"] = load_img("botonesconfig_eng.png")

    # === Escalar las imagenes ===
    bg_prin    = pygame.transform.scale(bg_prin, (3840, 1080))
    titulo       = pygame.transform.scale(titulo, (1669.5, 250))
    botoninicio  = pygame.transform.scale(botoninicio, (335, 333))
    botonsalir   = pygame.transform.scale(botonsalir, (175.5, 174))
    config_x     = pygame.transform.scale(config_x, (48, 48.5))
    tuto         = pygame.transform.scale(tuto, (1290, 733.5))
    esp_on       = pygame.transform.scale(esp_on, (364, 131.5))
    esp_off      = pygame.transform.scale(esp_off, (364, 131.5))
    eng_on       = pygame.transform.scale(eng_on, (364, 131.5))
    eng_off      = pygame.transform.scale(eng_off, (364, 131.5))

    for lang in ["esp", "eng"]:
        btn_images[lang]["botonconfig"] = pygame.transform.scale(btn_images[lang]["botonconfig"], (500, 123.5))
        btn_images[lang]["botontuto"]   = pygame.transform.scale(btn_images[lang]["botontuto"], (500, 123.5))
        btn_images[lang]["config"] = pygame.transform.scale(btn_images[lang]["config"], (1290, 733.5))
        btn_images[lang]["botones_tuto"] = pygame.transform.scale(btn_images[lang]["botones_tuto"], (924, 482.5))
        btn_images[lang]["botones_config"] = pygame.transform.scale(btn_images[lang]["botones_config"], (768, 259.5))

    # === Animacion de botones ===
    botoninicio_orig, botoninicio_hover = make_hover_pair(botoninicio, 1.05)
    botonsalir_orig, botonsalir_hover = make_hover_pair(botonsalir, 1.05)
    config_x_orig, config_x_hover = make_hover_pair(config_x, 1.05)

    # Diccionario para guardar las animaciones (orig, hover)
    btn_anim = { "esp": {}, "eng": {} } 

    # Anima las imágenes que cambian de idioma
    for lang in ["esp", "eng"]:
        btn_anim[lang]["botonconfig_orig"], btn_anim[lang]["botonconfig_hover"] = make_hover_pair(btn_images[lang]["botonconfig"], 1.05)
        btn_anim[lang]["botontuto_orig"],   btn_anim[lang]["botontuto_hover"]   = make_hover_pair(btn_images[lang]["botontuto"], 1.05) 

    # === Definir rects de botones (hitboxes) ===
    rect_inicio   = botoninicio.get_rect(topleft=(792.5, 455))
    rect_salir    = botonsalir.get_rect(topleft=(30, 876))
    tuto_rect     = tuto.get_rect(center=(WIDTH//2, HEIGHT//2))

    # Rects de botones que cambian de idioma (usamos "esp" como referencia)
    rect_config   = btn_images["esp"]["botonconfig"].get_rect(topleft=(242.5, 555))
    rect_tuto     = btn_images["esp"]["botontuto"].get_rect(topleft=(1177.5, 555))
    config_rect   = btn_images["esp"]["config"].get_rect(center=(WIDTH//2, HEIGHT//2))

    # Rects
    config_x_rect = config_x.get_rect(topright=(config_rect.right-20, config_rect.top+20))
    rect_esp   = esp_on.get_rect(topleft=(576, 680))
    rect_eng   = eng_on.get_rect(topleft=(980, 680))

    # BARRA DE VOLUMEN
    # Este rect es el "canal" oscuro de fondo de tu mockup
    VOL_BAR_X = 565
    VOL_BAR_Y = 481
    VOL_BAR_ANCHO = 790
    VOL_BAR_ALTO = 80
    rect_vol_bar = pygame.Rect(VOL_BAR_X, VOL_BAR_Y, VOL_BAR_ANCHO, VOL_BAR_ALTO)
    
    # Colores para dibujar la barra (puedes cambiarlos)
    COLOR_VOLUMEN_RELLENO = (255, 255, 255) # Blanco
    COLOR_VOLUMEN_POMO = (211, 211, 211) # Gris claro

    # === Offset Menu Principal (movimiento del fondo menu principal) ===
    bg_width = bg_prin.get_width()
    bg_height = bg_prin.get_height()
    bg_x = 0  # desplazamiento inicial
    scroll_speed = 2  # velocidad (px por frame)

    # === Superficie para renderizar el menú (para blur) ===
    menu_surface = pygame.Surface((WIDTH, HEIGHT)).convert()

    # === Estado del juego ===
    game_state = "menu"
    is_dragging_volume = False

    # === Bucle principal ===
    running = True
    while running:     
        clock.tick(FPS)  
            
        for event in pygame.event.get():         
            if event.type == pygame.QUIT:             
                return "quit"

            # === Botones ===
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Botones del menu principal
                if game_state == "menu":
                    if rect_config.collidepoint(event.pos):
                        game_state = "config"
                        print("Ir a CONFIGURACIÓN")
                    elif rect_tuto.collidepoint(event.pos):
                        game_state = "tutorial"
                        print("Ir a TUTORIAL")
                    elif rect_inicio.collidepoint(event.pos):
                        print("Ir a MENU NIVELES")
                        return "niveles"
                    elif rect_salir.collidepoint(event.pos):
                        print("Cerrando el juego...")
                        return "quit"

                # Botones en config y tutorial
                elif game_state == "config":
                    if config_x_rect.collidepoint(event.pos):
                        game_state = "menu"
                        print("Cerrando configuración.")
                    
                    # Idioma
                    elif rect_esp.collidepoint(event.pos):
                        settings.language = "esp"
                        print("Idioma: Español")
                    elif rect_eng.collidepoint(event.pos):
                        settings.language = "eng"
                        print("Idioma: Inglés")

                    # BARRA DE VOLUMEN (Clic)
                    elif rect_vol_bar.collidepoint(event.pos):
                        is_dragging_volume = True
                        # Actualizar volumen al primer clic
                        mouse_x = event.pos[0]
                        relative_x = mouse_x - rect_vol_bar.x
                        volume_pct = max(0, min(1, relative_x / rect_vol_bar.width))
                        settings.GLOBAL_VOLUME = volume_pct
                        pygame.mixer.music.set_volume(settings.GLOBAL_VOLUME)

                elif game_state == "tutorial":
                    if config_x_rect.collidepoint(event.pos):
                        game_state = "menu"
                        print("Cerrando tutorial.") 

            # --- BARRA DE VOLUMEN (Soltar Clic) ---
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_dragging_volume = False

            # --- BARRA DE VOLUMEN (Arrastrar) ---
            if event.type == pygame.MOUSEMOTION:
                if is_dragging_volume:
                    mouse_x = event.pos[0]
                    relative_x = mouse_x - rect_vol_bar.x
                    volume_pct = max(0, min(1, relative_x / rect_vol_bar.width))
                    settings.GLOBAL_VOLUME = volume_pct
                    pygame.mixer.music.set_volume(settings.GLOBAL_VOLUME)

            # Usar la tecla ESC para salir de configuracion
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state in "config":
                    game_state = "menu"
                    print("Cerrando configuración.")
            
            # Usar la tecla ESC para salir de tutorial
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state in "tutorial":
                    game_state = "menu"
                    print("Cerrando tutorial.") 
                        
        # === ZONA DE DIBUJO ===
        current_lang = settings.language
        current_anim = btn_anim[current_lang]
        current_img = btn_images[current_lang]

        # MENU
        if game_state == "menu":

            # Actualizar posicion del fondo
            bg_x -= scroll_speed
            if bg_x <= -bg_width:
                bg_x = 0

            # Fondo con un poco de blur
            menu_surface.blit(bg_prin, (bg_x, 0))
            menu_surface.blit(bg_prin, (bg_x + bg_width, 0))
            blurred = make_blur(menu_surface, factor=0.60, passes=2)
            screen.blit(blurred, (0, 0))
            menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

            # Centro del título a partir del topleft (81, 65)
            title_center = (125.25, 100)
            t_ms = pygame.time.get_ticks()

            # Titulo animado
            draw_title_animated(screen, titulo, title_center, mode="bob", t_ms=t_ms, amp=10)

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # BOTON INICIO
            if rect_inicio.collidepoint(mouse_pos):
                r = botoninicio_hover.get_rect(center=rect_inicio.center)
                screen.blit(botoninicio_hover, r.topleft)
            else:
                screen.blit(botoninicio_orig, rect_inicio.topleft)

            # BOTON CONFIGURACION
            if rect_config.collidepoint(mouse_pos):
                r = current_anim["botonconfig_hover"].get_rect(center=rect_config.center)
                screen.blit(current_anim["botonconfig_hover"], r.topleft)
            else:
                screen.blit(current_anim["botonconfig_orig"], rect_config.topleft)

            # BOTON TUTORIAL
            if rect_tuto.collidepoint(mouse_pos):
                r = current_anim["botontuto_hover"].get_rect(center=rect_tuto.center)
                screen.blit(current_anim["botontuto_hover"], r.topleft)
            else:
                screen.blit(current_anim["botontuto_orig"], rect_tuto.topleft)

            # BOTON SALIR
            if rect_salir.collidepoint(mouse_pos):
                r = botonsalir_hover.get_rect(center=rect_salir.center)
                screen.blit(botonsalir_hover, r.topleft)
            else:
                screen.blit(botonsalir_orig, rect_salir.topleft)

        # CONFIGURACION
        elif game_state == "config":
            bg_x -= scroll_speed
            if bg_x <= -bg_width:
                bg_x = 0

            # Poner blur al menu principal
            menu_surface.blit(bg_prin, (bg_x, 0))
            menu_surface.blit(bg_prin, (bg_x + bg_width, 0))

            # Título animado sobre menu_surface
            t_ms = pygame.time.get_ticks()
            title_center = (125.25, 100)
            draw_title_animated(menu_surface, titulo, title_center, mode="bob", t_ms=t_ms, amp=6)

            menu_surface.blit(botoninicio, rect_inicio.topleft)
            menu_surface.blit(current_img["botonconfig"], rect_config.topleft)
            menu_surface.blit(current_img["botontuto"],   rect_tuto.topleft)
            menu_surface.blit(botonsalir,  rect_salir.topleft)

            blurred = make_blur(menu_surface, factor=0.40, passes=2)
            screen.blit(blurred, (0, 0))
            menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

            # Dibujar el panel (depende del idioma)
            screen.blit(current_img["config"], config_rect.topleft)
            
            # Dibujar el contenido del panel (depende del idioma)
            screen.blit(current_img["botones_config"], (576, 410.25))

            # --- DIBUJAR LA BARRA DE VOLUMEN ---
            
            # Ajusta estos valores para que la barra blanca tenga el tamaño exacto del canal azul
            # y el pomo sobresalga ligeramente.
            
            # --- Ajustes para el mockup de la Image 2 ---
            # Estos padding_x y padding_y determinan el tamaño real de la barra blanca y el pomo.
            # Puedes ajustarlos finamente si tu imagen de fondo tiene diferentes márgenes.
            padding_x = 10   # Distancia desde el borde izquierdo del rect_vol_bar al inicio de la barra blanca
            padding_y = 10   # Distancia desde el borde superior/inferior del rect_vol_bar a la barra blanca

            # El radio de los extremos redondeados de la barra y el pomo
            knob_and_bar_radius = int((rect_vol_bar.height - (padding_y * 2)) / 2) # Mitad de la altura efectiva de la barra

            # Calcular el ancho total que puede ocupar el relleno (sin contar el pomo)
            fillable_width_without_knob = rect_vol_bar.width - (padding_x * 2) - knob_and_bar_radius 
            
            # El ancho real del relleno blanco, considerando el volumen
            current_fill_width = fillable_width_without_knob * settings.GLOBAL_VOLUME
            
            # La altura de la barra blanca (se mantiene constante)
            fill_height = rect_vol_bar.height - (padding_y * 2) 

            # 1. Dibuja el relleno blanco (la parte principal de la barra)
            # Este rectángulo se extiende hasta el punto donde debería comenzar la parte redondeada del pomo
            rect_vol_fill = pygame.Rect(
                rect_vol_bar.x + padding_x,
                rect_vol_bar.y + padding_y,
                current_fill_width + knob_and_bar_radius, # El ancho se extiende para cubrir el pomo parcialmente
                fill_height
            )
            pygame.draw.rect(screen, COLOR_VOLUMEN_RELLENO, rect_vol_fill, border_radius=knob_and_bar_radius)

            # 2. Dibuja el pomo (círculo) en el extremo de la barra
            # Su posición central se calcula con el ancho del relleno, más el padding_x
            knob_x = rect_vol_bar.x + padding_x + current_fill_width
            knob_y = rect_vol_bar.centery # El pomo siempre está centrado verticalmente
            
            # Asegúrate de que el pomo no se salga de la barra visualmente por la derecha
            # Clamp the knob_x position so it stays within the visual bounds of the bar
            # knob_x = min(knob_x, rect_vol_bar.right - padding_x - knob_and_bar_radius)
            
            pygame.draw.circle(screen, COLOR_VOLUMEN_POMO, (int(knob_x), int(knob_y)), knob_and_bar_radius)

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

        # TUTORIAL
        elif game_state == "tutorial":
            bg_x -= scroll_speed
            if bg_x <= -bg_width:
                bg_x = 0

            # Poner blur al menu principal
            menu_surface.fill((0, 0, 0))  
            menu_surface.blit(bg_prin, (bg_x, 0))
            menu_surface.blit(bg_prin, (bg_x + bg_width, 0))
            
            # Título animado sobre menu_surface
            t_ms = pygame.time.get_ticks()
            title_center = (125.25, 100)
            draw_title_animated(menu_surface, titulo, title_center, mode="bob", t_ms=t_ms, amp=6)
            
            menu_surface.blit(botoninicio, rect_inicio.topleft)
            menu_surface.blit(current_img["botonconfig"], rect_config.topleft)
            menu_surface.blit(current_img["botontuto"],   rect_tuto.topleft)
            menu_surface.blit(botonsalir,  rect_salir.topleft)

            blurred = make_blur(menu_surface, factor=0.40, passes=2)
            screen.blit(blurred, (0, 0))
            menu_surface.fill((0, 0, 0))  # limpiar para el próximo frame

            # Dibujar el panel
            screen.blit(tuto, tuto_rect.topleft)

            # Dibujar el contenido del panel (depende del idioma)
            screen.blit(current_img["botones_tuto"], (485, 350))
            
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