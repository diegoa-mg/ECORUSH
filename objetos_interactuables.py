import pygame
from pathlib import Path

# --- 1. FUNCIÓN DE AYUDA SIMPLIFICADA ---
# (Ahora solo necesita la imagen de 'encendido')
def _crear_objeto(pos, size, img_on, hitbox=None):
    """
    Función de ayuda para crear la configuración de un objeto.
    Genera un hitbox por defecto (basado en pos y size) si no se proporciona uno.
    """
    if hitbox is None:
        hitbox_config = (pos[0], pos[1], size[0], size[1])
    else:
        hitbox_config = hitbox
        
    return {
        "pos": pos,
        "size": size,
        "hitbox": hitbox_config,
        "img_on": img_on, # 'img_off' ya no es necesario
    }

# --- 2. CONFIGURACIÓN CENTRALIZADA ---
# ¡Ahora es incluso más limpia!
"""
    Ejemplo:
    pos=(1200, 614), size=(80, 80), 
    img_on="lamparaencendida.png
"""
CONFIG_OBJETOS = {
    "entrada_nivel1.png": [],
    "sala_nivel1.png": [
        _crear_objeto(
            pos=(383, 81), size=(238, 126),
            img_on="TVprendida_sala.png"
        ),
        _crear_objeto(
            pos=(1744, 164), size=(119, 154),
            img_on="Lavabo.png"
        )
    ],
    "cocina_nivel1.png": [],
    "garaje_nivel1.png": [],
    "cuarto1_nivel1.png": [
        _crear_objeto(
            pos=(674, 161), size=(548, 239),
            img_on="TVprendida_cuarto1.png"
        ),
        _crear_objeto(
            pos=(1424, 162), size=(119, 153),
            img_on="Lavabo.png"
        ),
        _crear_objeto(
            pos=(32, 761), size=(149, 283),
            img_on="PC_cuarto1.png"
        )
    ],
    "cuarto2_nivel1.png": []
}


# --- 3. CLASE DE OBJETO SIMPLIFICADA ---
class ObjetoInteractuable:
    # --- MODIFICADO: 'img_off_path' eliminado ---
    def __init__(self, habitacion, pos, size, hitbox_rect, img_on_data):
        self.habitacion = habitacion
        self.encendido = True
        
        self.frames_encendido = []
        self.imagen_encendida = None
        self._frame_idx = 0
        self._last_frame_ts = 0
        self._frame_interval = 150 

        try:
            # --- Carga de Imagen/Animación de ENCENDIDO ---
            if isinstance(img_on_data, list):
                # Es una animación (lista de paths)
                for path in img_on_data:
                    img = pygame.image.load(path).convert_alpha()
                    self.frames_encendido.append(pygame.transform.scale(img, size))
                self.imagen_encendida = self.frames_encendido[0]
            else:
                # Es una imagen estática (un solo path)
                img = pygame.image.load(img_on_data).convert_alpha()
                self.imagen_encendida = pygame.transform.scale(img, size)
        except Exception as e:
            print(f"Error al cargar imagen ENCENDIDA '{img_on_data}': {e}")
            self.imagen_encendida = None 

        # --- Carga de Imagen de APAGADO (ELIMINADA) ---
        # Ya no necesitamos 'self.imagen_apagada'

        # --- Rects ---
        if self.imagen_encendida:
             self.image_rect = self.imagen_encendida.get_rect(topleft=pos)
        else:
             self.image_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
             
        self.rect_bloqueo = pygame.Rect(hitbox_rect)
        self.rect_interaccion = self.rect_bloqueo.inflate(8, 8)

    def draw(self, surface):
        # --- MODIFICADO: Lógica de dibujo simplificada ---
        if self.encendido:
            img_to_draw = None
            if self.frames_encendido:
                # Lógica de animación
                now = pygame.time.get_ticks()
                if self._last_frame_ts == 0: self._last_frame_ts = now
                elif now - self._last_frame_ts >= self._frame_interval:
                    self._frame_idx = (self._frame_idx + 1) % len(self.frames_encendido)
                    self._last_frame_ts = now
                img_to_draw = self.frames_encendido[self._frame_idx]
            else:
                img_to_draw = self.imagen_encendida
            
            # Dibuja la imagen de encendido
            if img_to_draw:
                surface.blit(img_to_draw, self.image_rect)
            else:
                # Dibuja un cuadrado fucsia si las imágenes fallaron
                pygame.draw.rect(surface, (255, 0, 255), self.image_rect)
        
        else:
            # Si está apagado, no dibuja NADA.
            pass

    def apagar(self):
        self.encendido = False


# --- 4. CLASE GESTOR SIMPLIFICADA ---
class GestorObjetosInteractuables:
    def __init__(self, assets_path):
        self.assets_path = Path(assets_path)
        self.objetos_activos = []
        
        # Cargar el icono de advertencia
        self.icono_advertencia = None
        try:
            icon_path = self.assets_path / "img" / "advertencia_objetos.png"
            icon = pygame.image.load(str(icon_path)).convert_alpha()
            self.icono_advertencia = pygame.transform.scale(icon, (35, 35))
        except Exception as e:
            print(f"[Advertencia] No se pudo cargar 'advertencia_objetos.png': {e}")

    def cargar_objetos_de_config(self, config_data):
        """
        Lee el diccionario de configuración, crea todos los objetos
        y los añade a la lista de 'objetos_activos'.
        """
        base_path = self.assets_path / "objetos_interactuables"
        
        for habitacion, lista_objetos in config_data.items():
            for obj_data in lista_objetos:
                try:
                    # --- Construir rutas de imágenes ---
                    img_on_data = obj_data["img_on"]
                    img_on_path = ""
                    
                    if isinstance(img_on_data, list):
                        img_on_path = [base_path / path for path in img_on_data]
                    else:
                        img_on_path = base_path / img_on_data
                    
                    # --- Lógica de 'img_off' ELIMINADA ---

                    # --- Crear el objeto ---
                    obj = ObjetoInteractuable(
                        habitacion = habitacion,
                        pos = obj_data["pos"],
                        size = obj_data["size"],
                        hitbox_rect = obj_data["hitbox"],
                        img_on_data = img_on_path,
                    )
                    self.objetos_activos.append(obj)
                
                except Exception as e:
                    print(f"Error al crear objeto {obj_data} en {habitacion}: {e}")

    # === Métodos de compatibilidad usados por nivel1 ===
    def crear_objetos_por_defecto(self):
        """Carga los objetos definidos en CONFIG_OBJETOS a objetos_activos y devuelve la lista."""
        try:
            # Vaciar cualquier lista previa para evitar duplicados
            self.objetos_activos = []
            self.cargar_objetos_de_config(CONFIG_OBJETOS)
        except Exception as e:
            print(f"[Objetos] No se pudieron crear por defecto: {e}")
        return self.objetos_activos

    def listar_objetos_disponibles(self):
        """Imprime un resumen simple de los objetos cargados por habitación."""
        try:
            resumen = {}
            for obj in self.objetos_activos:
                resumen.setdefault(obj.habitacion, 0)
                resumen[obj.habitacion] += 1
            for hab, count in resumen.items():
                print(f"[Objetos] {hab}: {count} objeto(s)")
        except Exception:
            pass

    # --- Funciones de filtrado (Estas no cambian) ---
    
    def dibujar_todos(self, surface, nombre_habitacion_actual: str):
        """Dibuja todos los objetos activos en la habitación actual"""
        for objeto in self.objetos_activos:
            if objeto.habitacion == nombre_habitacion_actual:
                objeto.draw(surface)
                # Dibuja la advertencia SÓLO si está encendido
                if self.icono_advertencia and objeto.encendido:
                    icon_w, icon_h = self.icono_advertencia.get_size()
                    x = objeto.image_rect.centerx - icon_w // 2
                    y = objeto.image_rect.top - icon_h - 4
                    surface.blit(self.icono_advertencia, (x, y))

    def verificar_colision(self, rect_jugador, nombre_habitacion_actual: str):
        """
        Verifica si el jugador colisiona con algún objeto
        EN LA HABITACIÓN ACTUAL.
        """
        for objeto in self.objetos_activos:
            if objeto.habitacion == nombre_habitacion_actual:
                # Solo se puede interactuar si está encendido
                if rect_jugador.colliderect(objeto.rect_interaccion) and objeto.encendido:
                    return True, objeto
        return False, None

    def obtener_rects_bloqueo(self, nombre_habitacion_actual: str):
        """Devuelve rectángulos que bloquean el movimiento
        SOLO de la habitación actual."""
        return [obj.rect_bloqueo for obj in self.objetos_activos if obj.habitacion == nombre_habitacion_actual]
    
    def obtener_objetos_encendidos(self):
        """Retorna lista de objetos que están encendidos (en TODAS las habitaciones)"""
        return [obj for obj in self.objetos_activos if obj.encendido]