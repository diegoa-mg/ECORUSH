import pygame
from pathlib import Path

# === Configuración editable de posiciones ===
# Puedes ajustar aquí las coordenadas (x, y) de cada objeto por nombre.
POSICIONES_OBJETOS = {
    "entrada_nivel1.png": [
        {"nombre": "lamparaencendida", "pos": (1200, 614)}
    ],
    "sala_nivel1.png": [
    ],
    "cocina_nivel1.png": [
        {"nombre": "refrigerador encendido", "pos": (865, 25)}
    ],
    "garaje_nivel1.png": [
    ],
    "cuarto1_nivel1.png": [
        {"nombre": "airedeventanaencendido", "pos": (1200, 475)}
    ],
    "cuarto2_nivel1.png": [
    ]
}

class ObjetoInteractuable:
    def __init__(self, x, y, imagen_encendida_path, nombre="objeto", imagen_apagada_path=None, hitbox_size=None, hitbox_top_left=None, hitbox_offset=None, hitbox_mode: str = "base", frames_encendido=None, frame_interval_ms: int = 180, habitacion: str = "default"):
        self.nombre = nombre
        self.encendido = True
        self.habitacion = habitacion # <-- ATRIBUTO AÑADIDO
        
        # Tamaños
        self.display_size = 80  # solicitado: imágenes de 40x40
        if isinstance(hitbox_size, (list, tuple)) and len(hitbox_size) == 2:
            lado_w, lado_h = int(hitbox_size[0]), int(hitbox_size[1])
        elif isinstance(hitbox_size, (int, float)):
            lado_w = lado_h = int(hitbox_size)
        else:
            lado_w = lado_h = 37

        # Cargar y redimensionar imagen encendida si está disponible
        self.imagen_encendida = None
        try:
            if imagen_encendida_path:
                encendida = pygame.image.load(imagen_encendida_path).convert_alpha()
                self.imagen_encendida = pygame.transform.scale(encendida, (self.display_size, self.display_size))
        except Exception:
            self.imagen_encendida = None

        # Animación de encendido (opcional)
        self.frames_encendido = []
        if frames_encendido:
            for ruta in frames_encendido:
                try:
                    surf = pygame.image.load(str(ruta)).convert_alpha()
                    surf = pygame.transform.scale(surf, (self.display_size, self.display_size))
                    self.frames_encendido.append(surf)
                except Exception:
                    pass
        self._frame_idx = 0
        self._last_frame_ts = 0
        self._frame_interval = max(60, int(frame_interval_ms))
        if self.imagen_encendida is None and self.frames_encendido:
            self.imagen_encendida = self.frames_encendido[0]

        # Cargar y redimensionar imagen apagada si existe
        self.imagen_apagada = None
        if imagen_apagada_path:
            try:
                apagada = pygame.image.load(imagen_apagada_path).convert_alpha()
                self.imagen_apagada = pygame.transform.scale(apagada, (self.display_size, self.display_size))
            except FileNotFoundError:
                self.imagen_apagada = None

        # Rect de imagen (posición de dibujo)
        self.image_rect = pygame.Rect(x, y, self.display_size, self.display_size)

        # Hitbox: modo de colocación
        if hitbox_mode == "coords" and hitbox_top_left is not None:
            self.rect_bloqueo = pygame.Rect(int(hitbox_top_left[0]), int(hitbox_top_left[1]), lado_w, lado_h)
        elif hitbox_mode == "centro":
            bloque_x = self.image_rect.centerx - lado_w // 2
            bloque_y = self.image_rect.centery - lado_h // 2
            self.rect_bloqueo = pygame.Rect(bloque_x, bloque_y, lado_w, lado_h)
        else:  # "base"
            bloque_x = self.image_rect.centerx - lado_w // 2
            bloque_y = self.image_rect.bottom - lado_h
            self.rect_bloqueo = pygame.Rect(bloque_x, bloque_y, lado_w, lado_h)
        
        if hitbox_offset is not None:
            try:
                dx, dy = int(hitbox_offset[0]), int(hitbox_offset[1])
                self.rect_bloqueo.move_ip(dx, dy)
            except Exception:
                pass
        self.rect_interaccion = self.rect_bloqueo.inflate(8, 8)

    def draw(self, surface):
        if self.encendido:
            if self.frames_encendido:
                now = pygame.time.get_ticks()
                if self._last_frame_ts == 0:
                    self._last_frame_ts = now
                elif now - self._last_frame_ts >= self._frame_interval:
                    self._frame_idx = (self._frame_idx + 1) % len(self.frames_encendido)
                    self._last_frame_ts = now
                frame = self.frames_encendido[self._frame_idx]
                surface.blit(frame, self.image_rect.topleft)
            else:
                if self.imagen_encendida is not None:
                    surface.blit(self.imagen_encendida, self.image_rect.topleft)
                else:
                    ph = pygame.Surface((self.display_size, self.display_size), pygame.SRCALPHA)
                    ph.fill((255, 0, 255, 150))
                    surface.blit(ph, self.image_rect.topleft)
        else:
            if self.imagen_apagada:
                surface.blit(self.imagen_apagada, self.image_rect.topleft)
            else:
                if self.imagen_encendida is not None:
                    imagen_roja = self.imagen_encendida.copy()
                    imagen_roja.fill((255, 0, 0, 180), None, pygame.BLEND_RGBA_MULT)
                    surface.blit(imagen_roja, self.image_rect.topleft)
                elif self.frames_encendido:
                    frame = self.frames_encendido[self._frame_idx]
                    imagen_roja = frame.copy()
                    imagen_roja.fill((255, 0, 0, 180), None, pygame.BLEND_RGBA_MULT)
                    surface.blit(imagen_roja, self.image_rect.topleft)
                else:
                    ph = pygame.Surface((self.display_size, self.display_size), pygame.SRCALPHA)
                    ph.fill((255, 0, 255, 150))
                    surface.blit(ph, self.image_rect.topleft)

    def apagar(self):
        self.encendido = False

    def encender(self):
        self.encendido = True


class GestorObjetosInteractuables:
    def __init__(self, assets_path):
        self.assets_path = Path(assets_path)
        self.objetos_disponibles = {}
        self.objetos_activos = []
        self.config_posiciones = None
        self.mostrar_hitbox = True
        self.tamanos_hitbox = {
            "airedeventanaencendido": (45, 37),
            "tarjallenadeagua": (43, 37),
        }
        self.offsets_hitbox = {}
        self.modo_hitbox = "coords"
        self.icono_advertencia = None
        try:
            icon_path = self.assets_path / "img" / "advertencia_objetos.png"
            icon = pygame.image.load(str(icon_path)).convert_alpha()
            self.icono_advertencia = pygame.transform.scale(icon, (35, 35))
        except Exception as e:
            print(f"[Advertencia] No se pudo cargar 'advertencia_objetos.png': {e}")
        self.mapeo_apagado_especial = {
            "lamparaencendida": "lampaapagada",
            "airedeventanaencendido": "airedeventana1apagado",
            "refrigerador encendido": "refrigeradorapagado",
            "tarjallenadeagua": "tarja",
            "pcencendida": "pc",
            "grifoprendido": "grifoapagado",
            "ventiladorencendido": "aireapagado",
        }
        self.mapeo_animacion_especial = {
            "ventiladorencendido": {"prefix": "aireprendidoenmovimiento", "cantidad": 14}
        }
        self._cargar_objetos_interactuables()

    def configurar_posiciones(self, posiciones: dict):
        self.config_posiciones = posiciones
    
    def _cargar_objetos_interactuables(self):
        objetos_path = self.assets_path / "objetos_interactuables"
        if not objetos_path.exists():
            print("Error: Carpeta 'objetos_interactuables' no encontrada")
            return
        for archivo in objetos_path.rglob("*.png"):
            nombre = archivo.stem
            self.objetos_disponibles[nombre] = str(archivo)
            try:
                print(f"Objeto cargado: {nombre} ({archivo.parent.name})")
            except Exception:
                print(f"Objeto cargado: {nombre}")

    def crear_objeto(self, x, y, nombre_imagen, habitacion="default"):
        """
        Crea un nuevo objeto interactuable
        x, y: posición
        nombre_imagen: nombre de la imagen (sin .png)
        habitacion: nombre de la habitación a la que pertenece
        """
        imagen_encendida_path = self.objetos_disponibles.get(nombre_imagen)

        base_candidatos = [
            self.mapeo_apagado_especial.get(nombre_imagen, ""),
            nombre_imagen.replace("encendida", "apagada"),
            nombre_imagen.replace("encendido", "apagado"),
            nombre_imagen.replace("encendida", ""),
            nombre_imagen.replace("encendido", ""),
        ]
        posibles_apagados = base_candidatos + [c.replace(" ", "") for c in base_candidatos if c]
        imagen_apagada_path = None
        for candidato in posibles_apagados:
            if candidato in self.objetos_disponibles:
                imagen_apagada_path = self.objetos_disponibles[candidato]
                break

        tam_hitbox = self.tamanos_hitbox.get(nombre_imagen)
        hitbox_top_left = (x, y) if self.modo_hitbox == "coords" else None
        hitbox_offset = self.offsets_hitbox.get(nombre_imagen)

        frames_anim = None
        if nombre_imagen in self.mapeo_animacion_especial:
            info = self.mapeo_animacion_especial[nombre_imagen]
            prefix = info.get("prefix")
            cantidad = int(info.get("cantidad", 0))
            if prefix and cantidad > 0:
                objetos_path = self.assets_path / "objetos_interactuables"
                frames = []
                for i in range(1, cantidad + 1):
                    coincidencias = list(objetos_path.rglob(f"{prefix}{i}.png"))
                    if coincidencias:
                        frames.append(coincidencias[0])
                if frames:
                    frames_anim = frames

        if imagen_encendida_path is None and not frames_anim:
            print(f"Error: Imagen '{nombre_imagen}' no encontrada y sin frames de animación")
            return None

        objeto = ObjetoInteractuable(
            x, y,
            imagen_encendida_path,
            nombre_imagen,
            imagen_apagada_path,
            hitbox_size=tam_hitbox,
            hitbox_top_left=hitbox_top_left,
            hitbox_offset=hitbox_offset,
            hitbox_mode=self.modo_hitbox,
            frames_encendido=frames_anim,
            frame_interval_ms=150,
            habitacion=habitacion
        )
        self.objetos_activos.append(objeto)
        return objeto
    
    def crear_objetos_por_defecto(self):
        """Crea objetos según POSICIONES_OBJETOS o self.config_posiciones."""
        objetos_creados = []
        posiciones = self.config_posiciones if self.config_posiciones else POSICIONES_OBJETOS

        for nombre_habitacion, lista_objetos in posiciones.items():
            for obj_info in lista_objetos:
                try:
                    nombre = obj_info["nombre"]
                    x, y = obj_info["pos"]
                    # Pasa el nombre de la habitación al crear el objeto
                    objeto = self.crear_objeto(x, y, nombre, habitacion=nombre_habitacion)
                    if objeto:
                        objetos_creados.append(objeto)
                except Exception as e:
                    print(f"Error al crear objeto {obj_info} en {nombre_habitacion}: {e}")
             
        return objetos_creados

    def configurar_hitbox_por_objeto(self, tamanos: dict):
        self.tamanos_hitbox = dict(tamanos)

    def configurar_offset_hitbox_por_objeto(self, offsets: dict):
        self.offsets_hitbox = dict(offsets)

    def configurar_modo_hitbox(self, modo: str):
        if modo in ("coords", "centro", "base"):
            self.modo_hitbox = modo
    
    def crear_todos_los_objetos(self):
        """Crea un objeto de cada tipo disponible en posiciones distribuidas"""
        objetos_creados = []
        x_inicial = 100
        y_inicial = 100
        separacion = 150
        
        x, y = x_inicial, y_inicial
        for nombre in self.objetos_disponibles.keys():
            objeto = self.crear_objeto(x, y, nombre)
            if objeto:
                objetos_creados.append(objeto)
            
            # Mover a la siguiente posición
            x += separacion
            if x > 1200:  # Si se sale del ancho, bajar fila
                x = x_inicial
                y += separacion
        
        return objetos_creados
    
    def dibujar_todos(self, surface, nombre_habitacion_actual: str):
        """Dibuja todos los objetos activos en la habitación actual"""
        for objeto in self.objetos_activos:
            if objeto.habitacion == nombre_habitacion_actual:
                objeto.draw(surface)
                # Dibujar advertencia sobre objetos encendidos
                if self.icono_advertencia and objeto.encendido:
                    icon_w, icon_h = self.icono_advertencia.get_size()
                    x = objeto.image_rect.centerx - icon_w // 2
                    y = objeto.image_rect.top - icon_h - 4
                    surface.blit(self.icono_advertencia, (x, y))

    def verificar_colision(self, rect_jugador, nombre_habitacion_actual: str):
        """
        Verifica si el jugador colisiona con algún objeto
        EN LA HABITACIÓN ACTUAL.
        Retorna: (hay_colision, objeto_colisionado)
        """
        for objeto in self.objetos_activos:
            if objeto.habitacion == nombre_habitacion_actual:
                if rect_jugador.colliderect(objeto.rect_interaccion) and objeto.encendido:
                    return True, objeto
        return False, None

    def obtener_rects_bloqueo(self, nombre_habitacion_actual: str):
        """Devuelve rectángulos que bloquean el movimiento
        SOLO de la habitación actual."""
        return [obj.rect_bloqueo for obj in self.objetos_activos if obj.habitacion == nombre_habitacion_actual]
    
    def apagar_objeto(self, objeto):
        objeto.apagar()
    
    def obtener_objetos_encendidos(self):
        return [obj for obj in self.objetos_activos if obj.encendido]
    
    def obtener_objetos_apagados(self):
        return [obj for obj in self.objetos_activos if not obj.encendido]
    
    def listar_objetos_disponibles(self):
        print("Objetos disponibles:")
        for nombre in self.objetos_disponibles.keys():
            print(f"  - {nombre}")