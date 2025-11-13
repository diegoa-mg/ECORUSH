import pygame
import settings
from pathlib import Path
from settings import WIDTH, HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, ENERGIA_COLOR, load_img, make_hover_pair, make_blur, blit_hoverable, play_music, consume_next_music, set_next_music
from movimiento_de_personaje import AnimacionPersonaje
from movimiento_de_personaje_niña import AnimacionPersonajeNina
from objetos_interactuables import GestorObjetosInteractuables
from objetos_decorativos import GestorObjetosDecorativos

def run(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    # === Música del nivel (si fue solicitada por el selector) ===
    try:
        next_track = consume_next_music()
        if next_track:
            play_music(next_track, volume=0.6, loops=-1)
    except Exception as e:
        print(f"[Audio] No se pudo configurar música del nivel: {e}")

    # === Importar teclas ===
    from pygame.locals import (
        K_UP, K_DOWN, K_LEFT, K_RIGHT,
        K_w, K_a, K_s, K_d,
        K_LSHIFT, K_e, K_ESCAPE, QUIT, K_SPACE # <-- AGREGADO K_SPACE
    )

    # === Cargar imagenes ===
    # Juego
    img_boton_E         = load_img("E_personaje.png")
    # MAPA dinámico: usaremos habitaciones desde assets/plano_mapa1
    img_temporizador    = load_img("temporizador.png")
    img_advertencia     = load_img("advertencia_objetos.png")
    barra_energia       = load_img("barra_energia.png")
    barra_energia_atras = load_img("barra_energia_detras.png")
    btn_pausa           = load_img("boton_pausa_juego.png")

    # Imagenes PAUSA
    config_x     = load_img("config_x.png")
    esp_on       = load_img("esp_on.png")
    esp_off      = load_img("esp_off.png")
    eng_on       = load_img("eng_on.png")
    eng_off      = load_img("eng_off.png")

    #  --- Pendiente de cambiar el idioma
    pantalla_ganador    = load_img("ganador.png")
    pantalla_perdedor   = load_img("perdedor.png")

    # --- Diccionario para imágenes de idioma ---
    btn_images = { "esp": {}, "eng": {} }

    # Carga imágenes en Español
    btn_images["esp"]["titulo_pausa"] = load_img("titulo_pausa.png")
    btn_images["esp"]["btn_continuar"] = load_img("btn_continuar.png")
    btn_images["esp"]["btn_config"] = load_img("btn_config.png")
    btn_images["esp"]["btn_salir"] = load_img("btn_salir.png")
    btn_images["esp"]["config"] = load_img("config.png")
    btn_images["esp"]["botones_config"] = load_img("botonesconfig.png")

    # Carga tus nuevas imágenes en Inglés
    btn_images["eng"]["titulo_pausa"] = load_img("titulo_pausa_eng.png")
    btn_images["eng"]["btn_continuar"] = load_img("btn_continuar_eng.png")
    btn_images["eng"]["btn_config"] = load_img("btn_config_eng.png")
    btn_images["eng"]["btn_salir"] = load_img("btn_salir_eng.png")
    btn_images["eng"]["config"] = load_img("config_eng.png")
    btn_images["eng"]["botones_config"] = load_img("botonesconfig_eng.png")

    # === Escalar imagenes ===
    # Juego
    # MAPA se gestiona dinámicamente más abajo (MAPA_SURF)
    img_boton_E         = pygame.transform.scale(img_boton_E, (100, 100))
    img_temporizador    = pygame.transform.scale(img_temporizador, (288, 108))
    img_advertencia     = pygame.transform.scale(img_advertencia, (150, 150))
    barra_energia       = pygame.transform.scale(barra_energia, (348, 102))
    barra_energia_atras = pygame.transform.scale(barra_energia_atras, (348, 102))
    btn_pausa           = pygame.transform.scale(btn_pausa, (102, 102))

    pantalla_ganador    = pygame.transform.scale(pantalla_ganador, (WIDTH, HEIGHT))
    pantalla_perdedor   = pygame.transform.scale(pantalla_perdedor, (WIDTH, HEIGHT))

    for lang in ["esp", "eng"]:
        btn_images[lang]["titulo_pausa"] = pygame.transform.scale(btn_images[lang]["titulo_pausa"], (969, 146.5))
        btn_images[lang]["btn_continuar"] = pygame.transform.scale(btn_images[lang]["btn_continuar"], (454, 113.5))
        btn_images[lang]["btn_config"] = pygame.transform.scale(btn_images[lang]["btn_config"], (454, 113.5))
        btn_images[lang]["btn_salir"] = pygame.transform.scale(btn_images[lang]["btn_salir"], (454, 113.5))
        btn_images[lang]["config"] = pygame.transform.scale(btn_images[lang]["config"], (1290, 733.5))
        btn_images[lang]["botones_config"] = pygame.transform.scale(btn_images[lang]["botones_config"], (768, 259.5))

    esp_on       = pygame.transform.scale(esp_on, (364, 131.5))
    esp_off      = pygame.transform.scale(esp_off, (364, 131.5))
    eng_on       = pygame.transform.scale(eng_on, (364, 131.5))
    eng_off      = pygame.transform.scale(eng_off, (364, 131.5))
    config_x     = pygame.transform.scale(config_x, (48, 48.5))

    # === Animacion de botones en pausa ===
    btn_pausa_orig, btn_pausa_hover = make_hover_pair(btn_pausa, 1.05)

    # Diccionario para guardar las animaciones (orig, hover)
    btn_anim = { "esp": {}, "eng": {} } 

    # Anima las imágenes que cambian de idioma
    for lang in ["esp", "eng"]:
        btn_anim[lang]["btn_continuar_orig"], btn_anim[lang]["btn_continuar_hover"] = make_hover_pair(btn_images[lang]["btn_continuar"], 1.05)
        btn_anim[lang]["btn_config_orig"], btn_anim[lang]["btn_config_hover"] = make_hover_pair(btn_images[lang]["btn_config"], 1.05)
        btn_anim[lang]["btn_salir_orig"], btn_anim[lang]["btn_salir_hover"] = make_hover_pair(btn_images[lang]["btn_salir"], 1.05)
        
    config_x_orig, config_x_hover           = make_hover_pair(config_x, 1.05)

    # === Hitbox de botones ===
    # Rects de botones que cambian de idioma (usamos "esp" como referencia)
    rect_pausa = btn_pausa.get_rect(topleft=(1788, 50))
    rect_conti = btn_images["esp"]["btn_continuar"].get_rect(topleft=(733, 450))
    rect_config = btn_images["esp"]["btn_config"].get_rect(topleft=(733, 600))
    rect_salir = btn_images["esp"]["btn_salir"].get_rect(topleft=(733, 750))
    config_rect = btn_images["esp"]["config"].get_rect(center=(WIDTH//2, HEIGHT//2))

    config_x_rect   = config_x.get_rect(topright=(config_rect.right-20, config_rect.top+20))
    rect_esp   = esp_on.get_rect(topleft=(576, 680))
    rect_eng   = eng_on.get_rect(topleft=(980, 680))

    # Inicializar gestor de objetos interactuables
    assets_path = Path(__file__).parent / "assets"
    gestor_objetos = GestorObjetosInteractuables(assets_path)
    
    # Configurar modo de colocación de hitbox y offsets por objeto
    gestor_objetos.configurar_modo_hitbox("centro")
    gestor_objetos.configurar_offset_hitbox_por_objeto({"pcencendida": (2, -1)})

    # Inicializar decorativos y crearlos según posiciones configuradas
    gestor_decorativos = GestorObjetosDecorativos(assets_path)
    decorativos = gestor_decorativos.crear_decorativos_por_defecto()

    # Fuente
    FONT_PATH = Path(__file__).parent / "assets" / "fonts" / "horizon.otf"
    font = pygame.font.Font(str(FONT_PATH), 40)  # tamaño 

    # === Gestor de habitaciones con portales (plano_mapa1) ===
    plano_dir = Path(__file__).parent / "assets" / "plano_mapa1"

    # Habitaciones disponibles (coinciden con archivos de la carpeta)
    ROOM_ENTRADA = "entrada_nivel1.png"
    ROOM_SALA    = "sala_nivel1.png"
    ROOM_COCINA  = "cocina_nivel1.png"
    ROOM_GARAJE  = "garaje_nivel1.png"
    ROOM_CUARTO1 = "cuarto1_nivel1.png"
    ROOM_CUARTO2 = "cuarto2_nivel1.png"

    def cargar_habitacion(nombre_archivo: str) -> pygame.Surface:
        ruta = plano_dir / nombre_archivo
        try:
            surf = pygame.image.load(str(ruta)).convert()  # fondos sin alpha
        except Exception as e:
            print(f"[Mapa] No se pudo cargar '{nombre_archivo}': {e}. Usando fondo negro.")
            surf = pygame.Surface((WIDTH, HEIGHT)).convert()
            surf.fill((0, 0, 0))
        return pygame.transform.scale(surf, (WIDTH, HEIGHT))

    def construir_mask(surf: pygame.Surface) -> pygame.Mask:
        THRESHOLD = 40  # tolerancia a casi negro
        mask = pygame.Mask((WIDTH, HEIGHT))
        # Recorremos con paso para mejorar rendimiento en mapas grandes
        for y in range(0, HEIGHT):
            for x in range(0, WIDTH):
                color = surf.get_at((x, y))
                if color[0] < THRESHOLD and color[1] < THRESHOLD and color[2] < THRESHOLD:
                    mask.set_at((x, y), 1)
        return mask

    # Estado actual de habitación
    current_room = ROOM_ENTRADA  # inicia en entrada para seguir el plano
    MAPA_SURF = cargar_habitacion(current_room)
    MAPA_MASK = construir_mask(MAPA_SURF)

    # Definición de portales por habitación con rectángulos aproximados
    # Los rects están pensados para 1920x1080 y pueden ajustarse luego.
    room_portals: dict[str, list[dict]] = {
        ROOM_ENTRADA: [
            {"rect": pygame.Rect(550, 3, 800, 60), "to": ROOM_SALA,    "spawn": (960, 900)},  # arriba → sala
            {"rect": pygame.Rect(60, 540, 80, 200),   "to": ROOM_GARAJE,  "spawn": (1700, 540)}, # izquierda → garaje
            {"rect": pygame.Rect(1780, 540, 80, 200), "to": ROOM_COCINA,  "spawn": (120, 540)},  # derecha → cocina
        ],
        ROOM_SALA: [
            {"rect": pygame.Rect(860, 980, 200, 80),  "to": ROOM_ENTRADA, "spawn": (960, 160)},  # abajo → entrada
            {"rect": pygame.Rect(40, 540, 80, 200),   "to": ROOM_CUARTO1, "spawn": (1700, 540)}, # izquierda → cuarto1
            {"rect": pygame.Rect(1800, 540, 80, 200), "to": ROOM_CUARTO2, "spawn": (120, 540)},  # derecha → cuarto2
        ],
        ROOM_GARAJE: [
            {"rect": pygame.Rect(1800, 540, 80, 200), "to": ROOM_ENTRADA, "spawn": (160, 540)},  # derecha → entrada
        ],
        ROOM_COCINA: [
            {"rect": pygame.Rect(40, 540, 80, 200),   "to": ROOM_ENTRADA, "spawn": (1760, 540)}, # izquierda → entrada
        ],
        ROOM_CUARTO1: [
            {"rect": pygame.Rect(1800, 540, 80, 200), "to": ROOM_SALA,    "spawn": (160, 540)},  # derecha → sala
        ],
        ROOM_CUARTO2: [
            {"rect": pygame.Rect(40, 540, 80, 200),   "to": ROOM_SALA,    "spawn": (1760, 540)}, # izquierda → sala
        ],
    }

    # Mostrar visualmente los portales en rojo (debug).
    SHOW_PORTALS = True

    def draw_portals_overlay(screen: pygame.Surface, portals: list[dict]):
        if not portals:
            return
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for p in portals:
            r = p["rect"]
            # Relleno rojo semitransparente + borde rojo más intenso
            pygame.draw.rect(overlay, (255, 0, 0, 90), r)
            pygame.draw.rect(overlay, (255, 0, 0, 180), r, 3)
        screen.blit(overlay, (0, 0))

    def transition_to(room_name: str, spawn_pos: tuple[int, int], player_obj: pygame.sprite.Sprite):
        nonlocal current_room, MAPA_SURF, MAPA_MASK
        try:
            settings.fade_to_black(screen, duration_ms=120)
        except Exception:
            pass
        current_room = room_name
        MAPA_SURF = cargar_habitacion(current_room)
        MAPA_MASK = construir_mask(MAPA_SURF)
        player_obj.rect.center = spawn_pos
        try:
            settings.fade_from_black(screen, duration_ms=120)
        except Exception:
            pass

    def check_portals_and_transition(player_obj: pygame.sprite.Sprite):
        portals = room_portals.get(current_room, [])
        for p in portals:
            if player_obj.rect.colliderect(p["rect"]):
                transition_to(p["to"], p["spawn"], player_obj)
                break

    def colisiona_con_obstaculo(rect):
        # Colisión con paredes del mapa (negras)
        for x in range(rect.left, rect.right, 5):
            for y in range(rect.top, rect.bottom, 5):
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    if MAPA_MASK.get_at((x, y)):
                        return True

        # Objetos interactuables
        for rb in gestor_objetos.obtener_rects_bloqueo():
            if rect.colliderect(rb):
                return True

        # Objetos decorativos
        for rb in gestor_decorativos.obtener_rects_bloqueo():
            if rect.colliderect(rb):
                return True

        return False

    # === Jugador ===
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            # Inicializar animaciones
            assets_path = Path(__file__).parent / "assets"
            # Elegir animación según personaje seleccionado
            try:
                personaje = getattr(settings, "selected_character", "niño")
            except Exception:
                personaje = "niño"

            if personaje == "niña":
                self.animacion = AnimacionPersonajeNina(assets_path)
            else:
                self.animacion = AnimacionPersonaje(assets_path)
            
            # Usar el primer frame como superficie inicial
            self.surf = self.animacion.obtener_frame_actual()
            self.rect = self.surf.get_rect(center=(WIDTH//2, HEIGHT//2))

            # ENERGÍA
            self.energy = 100  
            self.energy_max = 100 # MAX_ENERGY

        def add_energy(self, amount: float):
            self.energy = max(0, min(self.energy + amount, self.energy_max))

        def draw_energy_bar(self, screen, x=30, y=30, w=174, h=51,
                            bg_img=None, fg_img=None, color=ENERGIA_COLOR):
            # fondo (detrás)
            if bg_img:
                screen.blit(bg_img, (x, y))
            # barra rellena (un rectángulo recortado al ancho)
            pct = self.energy / self.energy_max
            inner_margin = 6  # ajusta al arte de tu barra
            fill_rect = pygame.Rect(x + inner_margin, y + inner_margin,
                                    int((w - inner_margin*2) * pct),
                                    h - inner_margin*2)
            pygame.draw.rect(screen, color, fill_rect, border_radius=4)
            # marco (encima)
            if fg_img:
                screen.blit(fg_img, (x, y))

        def update(self, pressed_keys):
            # Guardar la posición actual para poder volver a ella si hay colisión
            old_rect = self.rect.copy()
            
            # Obtener dirección y estado de movimiento para animaciones
            direccion, esta_moviendose = self.animacion.obtener_direccion_movimiento(pressed_keys)
            
            # Movimiento normal
            if pressed_keys[K_UP] or pressed_keys[K_w]: 
                self.rect.move_ip(0, -3)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect
                    
            elif pressed_keys[K_DOWN] or pressed_keys[K_s]: 
                self.rect.move_ip(0, 3)
                if colisiona_con_obstaculo(self.rect):
                    self.rect = old_rect
                    
            else:
                if pressed_keys[K_LEFT] or pressed_keys[K_a]: 
                    self.rect.move_ip(-3, 0)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect
                    
                elif pressed_keys[K_RIGHT] or pressed_keys[K_d]: 
                    self.rect.move_ip(3, 0)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect

            # Movimiento rápido con Shift
            if pressed_keys[K_LSHIFT]:  # correr más rápido
                old_rect = self.rect.copy()

                if pressed_keys[K_UP] or pressed_keys[K_w]: 
                    self.rect.move_ip(0, -3.5)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect

                if pressed_keys[K_DOWN] or pressed_keys[K_s]: 
                    self.rect.move_ip(0, 3.5)
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect    

                if pressed_keys[K_LEFT] or pressed_keys[K_a]: 
                    self.rect.move_ip(-3.5, 0)                   
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect     

                if pressed_keys[K_RIGHT] or pressed_keys[K_d]: 
                    self.rect.move_ip(3.5, 0) 
                    if colisiona_con_obstaculo(self.rect):
                        self.rect = old_rect

            # Actualizar animación (incluyendo si está corriendo)
            corriendo = pressed_keys[K_LSHIFT]
            self.animacion.actualizar(direccion, esta_moviendose, corriendo)
            self.surf = self.animacion.obtener_frame_actual()

            self.rect.clamp_ip(screen.get_rect())  # no salir de pantalla
            # Verificar transición de mapa por portales
            check_portals_and_transition(self)

            # Drenaje de energía según movimiento
            is_moving = any(pressed_keys[k] for k in (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d))
            is_sprinting = pressed_keys[K_LSHIFT] and is_moving and player.energy > 0

            if is_moving:
                drain_walk = 5.0    # energía por segundo caminando
                drain_run  = 10.0    # energía por segundo corriendo
                player.add_energy(-(drain_run if is_sprinting else drain_walk) * dt)

    # === Objeto interactivo ===
    class Objeto:
        def __init__(self, x, y, w, h):
            self.rect = pygame.Rect(x, y, w, h)
            self.encendido = True

        def draw(self, surface):
            # Dibujar objeto - siempre amarillo cuando está encendido
            if self.encendido:
                pygame.draw.rect(surface, YELLOW, self.rect)
            else:
                pygame.draw.rect(surface, RED, self.rect)

    # Crear jugador
    player = Player()

    # Crear objetos interactuables con imágenes (32x32)
    objetos = gestor_objetos.crear_objetos_por_defecto()
    
    # Mostrar objetos disponibles (opcional)
    gestor_objetos.listar_objetos_disponibles()

    # Control de super botón
    super_boton_visible = False
    objeto_actual = None  # guarda el objeto con el que chocamos

    # === Temporizador ===
    START_TIME = 2 * 60 + 30 # 2 minutos en segundos
    start_ticks = pygame.time.get_ticks()

    # === Estado del juego ===
    game_state = "juego" # juego, pausa, config
    total_pause_ms = 0  # acumulado de tiempo en pausa
    pause_started = None  # instante en que empezó la pausa (ms)

    # Imagen de fondo borrosa que se usará mientras esté en pausa
    paused_bg = None  # cache del blur 

    running = True
    while running:
        clock.tick(FPS)
        dt = clock.get_time() / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                # Solicita música de menú niveles al volver
                set_next_music("musica_menu_niveles.mp3")
                return "niveles"

            # === BOTONES PAUSA ===
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "juego":
                    if rect_pausa.collidepoint(event.pos):
                        snapshot = screen.copy()
                        paused_bg = make_blur(snapshot, factor=0.4, passes=2)
                        game_state = "pausa"
                        pause_started = pygame.time.get_ticks() # <-- se marca inicio de pausa
                
                elif game_state == "pausa":
                    if rect_conti.collidepoint(event.pos):
                        print("Continuando el nivel...")
                        # Ajuste del temporizador al salir de pausa:
                        delta = pygame.time.get_ticks() - pause_started
                        total_pause_ms += delta # <-- se acumula el tiempo pausado
                        start_ticks += delta # <-- si mantienes temporizador con start_ticks  
                        pause_started = None
                        game_state = "juego"
        
                    if rect_config.collidepoint(event.pos):
                        print("Ir a CONFIGURACION en el nivel")
                        game_state = "config"

                    if rect_salir.collidepoint(event.pos):
                        print("Regresando al menu Niveles")
                        # Solicita música de menú niveles al volver
                        set_next_music("musica_menu_niveles.mp3")
                        return "niveles"
                
                elif game_state == "config":
                    if config_x_rect.collidepoint(event.pos):
                        print("Cerrando configuración.")
                        game_state = "pausa"

                    elif rect_esp.collidepoint(event.pos):
                            settings.language = "esp"
                            print("Idioma: Español")
                    elif rect_eng.collidepoint(event.pos):
                        settings.language = "eng"
                        print("Idioma: Inglés")

<<<<<<< Updated upstream
=======
                    # BARRA DE VOLUMEN (Clic)
                    elif rect_vol_bar.collidepoint(event.pos):
                        is_dragging_volume = True
                        # Actualizar volumen al primer clic
                        mouse_x = event.pos[0]
                        relative_x = mouse_x - rect_vol_bar.x
                        volume_pct = max(0, min(1, relative_x / rect_vol_bar.width))
                        settings.GLOBAL_VOLUME = volume_pct
                        pygame.mixer.music.set_volume(settings.GLOBAL_VOLUME)

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
            
            # === INTERACCIÓN (Grifo/Objetos Toggable) ===
            # Usa la tecla K_SPACE para encender/apagar el grifo
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_state == "juego":
                # Verificar interacción usando el nuevo método
                hay_interaccion, objeto_interactuable = gestor_objetos.verificar_interaccion(player.rect, current_room)

                if hay_interaccion and objeto_interactuable.nombre == "grifoprendido":
                    # Alternar el estado del grifo
                    if objeto_interactuable.encendido:
                        objeto_interactuable.apagar() # Llama al método apagar del objeto
                        print("Grifo apagado 💧")
                    else:
                        objeto_interactuable.encender() # Llama al método encender del objeto
                        print("Grifo encendido 🌊")

>>>>>>> Stashed changes
            # === ESC ===
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if game_state == "juego":
                    print("Pausando.")
                    snapshot = screen.copy()
                    paused_bg = make_blur(snapshot, factor=0.4, passes=2)
                    game_state = "pausa"
                    pause_started = pygame.time.get_ticks() # <-- se marca inicio de pausa

                elif game_state == "pausa":
                    print("Continuando el nivel...")
                    delta = pygame.time.get_ticks() - pause_started
                    total_pause_ms += delta # <-- se acumula el tiempo pausado
                    start_ticks += delta # <-- si mantienes temporizador con start_ticks        
                    pause_started = None
                    game_state = "juego"
                    
                elif game_state == "config":
                    print("Cerrando configuración.")
                    game_state = "pausa"

        if game_state == "juego":
            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)

            # === Calcular tiempo ===
            seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
            time_left = max(0, START_TIME - seconds_passed)

            minutes = time_left // 60
            seconds = time_left % 60
            color = WHITE if time_left > 15 else RED
            timer_text = font.render(f"{minutes:02}:{seconds:02}", True, color)

           # === Detectar colisión con algún objeto ===
            super_boton_visible = False
            hay_colision, objeto_colisionado = gestor_objetos.verificar_colision(player.rect)
            
            # NOTA: La lógica de 'super_boton_visible' sigue funcionando
            # para objetos que colisionan (no el grifo, que fue excluido de colisión)
            if hay_colision:
                super_boton_visible = True
                objeto_actual = objeto_colisionado

            # Si presiono E y hay un objeto actual → se apaga
            if super_boton_visible and pressed_keys[K_e]:
                objeto_actual.encendido = False
                super_boton_visible = False
                objeto_actual = None
                player.add_energy(+10)  # recupera 10 puntos de energia
                print("⚡ Objeto apagado: +10 energía ⚡")

            # === No hay campo de visión limitada ===
        
        # === DIBUJAR ===
        # Variables para la traducción del juego
        current_lang = settings.language
        current_anim = btn_anim[current_lang]
        current_img = btn_images[current_lang]

        if game_state == "juego":
            screen.blit(MAPA_SURF, (0, 0))  # dibuja el mapa dinámico de fondo

            # Dibuja overlay de portales (en rojo) si está habilitado
            if SHOW_PORTALS:
                draw_portals_overlay(screen, room_portals.get(current_room, []))

            # Dibujar decorativos (muebles, alfombras, etc.)
            gestor_decorativos.dibujar_todos(screen)

            # (Estante removido: ahora no se dibuja ni carga)

            # Dibujar todos los objetos interactuables
            gestor_objetos.dibujar_todos(screen)

            # Dibujar personaje
            screen.blit(player.surf, player.rect)

            # Dibujar el temporizador arriba al centro
            # === Dibujar temporizador con fondo estilo ===
            timer_rect = img_temporizador.get_rect(midtop=(WIDTH//2, 50))
            screen.blit(img_temporizador, timer_rect.topleft)

            # Texto del tiempo (negro con borde blanco para efecto 2D)
            timer_str = f"{minutes:02}:{seconds:02}"
            base_text = font.render(timer_str, True, WHITE)   # texto negro

            # Dibujar barra de energia y boton de pausa
            screen.blit(barra_energia_atras, (50, 50))

            player.draw_energy_bar(
                screen,
                x=50, y=50, w=barra_energia.get_width(), h=barra_energia.get_height(),
                bg_img=barra_energia_atras,
                fg_img=barra_energia,
                color=ENERGIA_COLOR
            )

            screen.blit(barra_energia, (50, 50))

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # BOTON PAUSA
            if rect_pausa.collidepoint(mouse_pos):
                r = btn_pausa_hover.get_rect(center=rect_pausa.center)
                screen.blit(btn_pausa_hover, r.topleft)
            else:
                screen.blit(btn_pausa_orig, rect_pausa.topleft)

            # Dibujar el texto principal del timer
            screen.blit(base_text, (timer_rect.centerx - base_text.get_width()//2,
                                    timer_rect.centery - base_text.get_height()//2))

            if super_boton_visible:
                boton_rect = img_boton_E.get_rect(midbottom=(player.rect.centerx, player.rect.top - 10))
                screen.blit(img_boton_E, boton_rect.topleft)

        elif game_state == "pausa":
            # Fondo (nivel) con blur
            screen.blit(paused_bg, (0, 0))

            # (Opcional) oscurecer un poco encima
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, (0, 0))

            # Titulo 
            screen.blit(current_img["titulo_pausa"], (475.5, 250))

            # Posición del mouse para hover
            mouse_pos = pygame.mouse.get_pos()

            # BOTON CONTINUAR
            if rect_conti.collidepoint(mouse_pos):
                r = current_anim["btn_continuar_hover"].get_rect(center=rect_conti.center)
                screen.blit(current_anim["btn_continuar_hover"], r.topleft)
            else:
                screen.blit(current_anim["btn_continuar_orig"], rect_conti.topleft)

            # BOTON CONFIGURACION
            if rect_config.collidepoint(mouse_pos):
                    r = current_anim["btn_config_hover"].get_rect(center=rect_config.center)
                    screen.blit(current_anim["btn_config_hover"], r.topleft)
            else:
                screen.blit(current_anim["btn_config_orig"], rect_config.topleft)

            # BOTON SALIR
            if rect_salir.collidepoint(mouse_pos):
                r = current_anim["btn_salir_hover"].get_rect(center=rect_salir.center)
                screen.blit(current_anim["btn_salir_hover"], r.topleft)
            else:
                screen.blit(current_anim["btn_salir_orig"], rect_salir.topleft)
            
        elif game_state == "config":
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

        # === Condiciones de fin de juego ===
        if time_left <= 0 or player.energy <= 0:
            screen.blit(pantalla_perdedor, (0,0))
            pygame.display.flip()
            pygame.time.delay(3000)
            # Solicita música de menú niveles al volver
            set_next_music("musica_menu_niveles.mp3")
            return "niveles"
        
        elif all(not obj.encendido for obj in objetos):
            screen.blit(pantalla_ganador, (0,0))
            pygame.display.flip()
            pygame.time.delay(3000)
            # Solicita música de menú niveles al volver
            set_next_music("musica_menu_niveles.mp3")
            return "niveles"