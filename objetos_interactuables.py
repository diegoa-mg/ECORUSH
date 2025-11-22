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
OBJETOS_NIVEL1 = {
    # --- Nivel 1 (plano_mapa1) ---
    "sala_nivel1.png": [
        _crear_objeto(
            pos=(383, 81), size=(238, 126),
            img_on="TV_sala.png"
        ),
        _crear_objeto(
            pos=(1744, 164), size=(119, 154),
            img_on="Lavamanos.png"
        )
    ],
    "cocina_nivel1.png": [
        _crear_objeto(
            pos=(37, 80), size=(161, 362),
            img_on="Refrigerador.png"
        ),
        _crear_objeto(
            pos=(1232, 191), size=(249, 259),
            img_on="Estufa.png"
        )
    ],
    "garaje_nivel1.png": [
        _crear_objeto(
            pos=(108, 170), size=(105, 120),
            img_on="Grifo.png"
        )
    ],
    "cuarto1_nivel1.png": [
        _crear_objeto(
            pos=(674, 161), size=(548, 239),
            img_on="TV_cuarto1.png"
        ),
        _crear_objeto(
            pos=(1424, 162), size=(119, 153),
            img_on="Lavamanos.png"
        ),
        _crear_objeto(
            pos=(30, 761), size=(149, 283),
            img_on="PC_cuarto1.png"
        )
    ],
    "cuarto2_nivel1.png": [
        _crear_objeto(
            pos=(34, 138), size=(228, 464),
            img_on="Bañera_cuarto2.png"
        ),
        _crear_objeto(
            pos=(484, 162), size=(215, 258),
            img_on="Lavamanos_cuarto2.png"
        ),
        _crear_objeto(
            pos=(742, 576), size=(144, 305),
            img_on="TV_cuarto2.png"
        ),
        _crear_objeto(
            pos=(1210, 162), size=(212, 143),
            img_on="PC_cuarto2.png"
        ),
    ],
}
OBJETOS_NIVEL2 = {
    # --- Nivel 2 (plano_mapa2) ---
    "entrada_nivel2.png": [
         _crear_objeto(
            pos=(1491, 120), size=(300, 228),
            img_on="lamparaencendida.png"
         ),
    ],
    "sala nivel 2.png": [],
    "cuarto__nivel2.png": [],
    "baño_nivel2.png": [],
    "cocina_nivel2.png": [],
}
OBJETOS_NIVEL3 = {
    # --- Nivel 3 (plano_mapa3) ---
    "cuarto_nivel3.png": [],
    "cuarto2_nivel3.png": [
        _crear_objeto(
            pos=(34, 138), size=(228, 464),
            img_on="Bañera_cuarto2.png"
        ),
        _crear_objeto(
            pos=(484, 162), size=(215, 258),
            img_on="Lavamanos_cuarto2.png"
        ),
        _crear_objeto(
            pos=(742, 576), size=(144, 305),
            img_on="TV_cuarto2.png"
        ),
        _crear_objeto(
            pos=(1210, 162), size=(212, 143),
            img_on="PC_cuarto2.png"
        ),
    ],
}

# --- 3. CLASE DE OBJETO ---
class ObjetoInteractuable:
    def __init__(self, habitacion, pos, size, hitbox_rect, img_on_data):
        self.habitacion = habitacion
        self.encendido = True
        
        self.frames_encendido = []
        self.imagen_encendida = None
        self._frame_idx = 0
        self._last_frame_ts = 0
        self._frame_interval = 150 

        try:
            if isinstance(img_on_data, list):
                for path in img_on_data:
                    img = pygame.image.load(path).convert_alpha()
                    self.frames_encendido.append(pygame.transform.scale(img, size))
                self.imagen_encendida = self.frames_encendido[0]
            else:
                img = pygame.image.load(img_on_data).convert_alpha()
                self.imagen_encendida = pygame.transform.scale(img, size)
        except Exception as e:
            print(f"Error al cargar imagen '{img_on_data}': {e}")
            self.imagen_encendida = None 

        if self.imagen_encendida:
             self.image_rect = self.imagen_encendida.get_rect(topleft=pos)
        else:
             self.image_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
             
        self.rect_bloqueo = pygame.Rect(hitbox_rect)
        self.rect_interaccion = self.rect_bloqueo.inflate(8, 8)

    def draw(self, surface):
        if self.encendido:
            img_to_draw = None
            if self.frames_encendido:
                now = pygame.time.get_ticks()
                if self._last_frame_ts == 0: self._last_frame_ts = now
                elif now - self._last_frame_ts >= self._frame_interval:
                    self._frame_idx = (self._frame_idx + 1) % len(self.frames_encendido)
                    self._last_frame_ts = now
                img_to_draw = self.frames_encendido[self._frame_idx]
            else:
                img_to_draw = self.imagen_encendida
            
            if img_to_draw:
                surface.blit(img_to_draw, self.image_rect)
            else:
                pygame.draw.rect(surface, (255, 0, 255), self.image_rect)

    def apagar(self):
        self.encendido = False

# --- 4. CLASE GESTOR ---
class GestorObjetosInteractuables:
    def __init__(self, assets_path):
        self.assets_path = Path(assets_path)
        self.objetos_activos = []
        
        self.icono_advertencia = None
        try:
            icon_path = self.assets_path / "img" / "advertencia_objetos.png"
            icon = pygame.image.load(str(icon_path)).convert_alpha()
            self.icono_advertencia = pygame.transform.scale(icon, (35, 35))
        except Exception as e:
            pass

    def cargar_objetos_de_config(self, config_data):
        """Lee el diccionario y crea los objetos."""
        base_path = self.assets_path / "objetos_interactuables"
        
        for habitacion, lista_objetos in config_data.items():
            for obj_data in lista_objetos:
                try:
                    img_on_data = obj_data["img_on"]
                    img_on_path = ""
                    
                    if isinstance(img_on_data, list):
                        img_on_path = [base_path / path for path in img_on_data]
                    else:
                        img_on_path = base_path / img_on_data
                    
                    obj = ObjetoInteractuable(
                        habitacion = habitacion,
                        pos = obj_data["pos"],
                        size = obj_data["size"],
                        hitbox_rect = obj_data["hitbox"],
                        img_on_data = img_on_path,
                    )
                    self.objetos_activos.append(obj)
                
                except Exception as e:
                    print(f"Error al crear objeto en {habitacion}: {e}")

    def dibujar_todos(self, surface, nombre_habitacion_actual: str):
        for objeto in self.objetos_activos:
            if objeto.habitacion == nombre_habitacion_actual:
                objeto.draw(surface)
                if self.icono_advertencia and objeto.encendido:
                    icon_w, icon_h = self.icono_advertencia.get_size()
                    x = objeto.image_rect.centerx - icon_w // 2
                    y = objeto.image_rect.top - icon_h - 4
                    surface.blit(self.icono_advertencia, (x, y))

    def verificar_colision(self, rect_jugador, nombre_habitacion_actual: str):
        for objeto in self.objetos_activos:
            if objeto.habitacion == nombre_habitacion_actual:
                if rect_jugador.colliderect(objeto.rect_interaccion) and objeto.encendido:
                    return True, objeto
        return False, None

    def obtener_rects_bloqueo(self, nombre_habitacion_actual: str):
        return [obj.rect_bloqueo for obj in self.objetos_activos if obj.habitacion == nombre_habitacion_actual]
    
    def obtener_objetos_encendidos(self):
        return [obj for obj in self.objetos_activos if obj.encendido]