import pygame
from pathlib import Path

# Tamaño uniforme para decorativos (igual que objetos interactuables)
DISPLAY_SIZE = 80

# Tamaños específicos por decorativo (opcional)
# Si un nombre aparece aquí, se usará este tamaño en lugar de DISPLAY_SIZE
TAMANOS_DECORATIVOS = {
    "alfombra1": (140, 140),  # alfombra más grande
}

# Tamaños de hitbox por decorativo (opcional). Por defecto 37x37 centrado.
TAMANOS_HITBOX_DECORATIVOS = {
    # Ejemplos si deseas personalizar:
    # "cajonera1": (40, 40),
}


POSICIONES_DECORATIVOS = {
    # Coordenadas por defecto (modifícalas a tu gusto)

}


class Decorativo:
    def __init__(self, x: int, y: int, imagen_path: str, nombre: str = "decorativo"):
        self.nombre = nombre
        img = pygame.image.load(imagen_path).convert_alpha()
        # Escalar al tamaño específico si existe, si no al tamaño uniforme
        w, h = TAMANOS_DECORATIVOS.get(nombre, (DISPLAY_SIZE, DISPLAY_SIZE))
        self.imagen = pygame.transform.scale(img, (w, h))
        self.rect = self.imagen.get_rect(topleft=(x, y))
        # Hitbox centrada (como objetos interactivos) sin interacción.
        # Excluir alfombras: no tendrán hitbox.
        self.rect_bloqueo = None
        # Excluir por nombre: alfombras y 'mesadefin' no tienen hitbox
        try:
            nombre_norm = str(nombre).lower().strip()
        except Exception:
            nombre_norm = ""
        exclusiones = ("alfombra", "mesadefin")
        es_excluido = any(token in nombre_norm for token in exclusiones)

        if not es_excluido:
            tam_hitbox = TAMANOS_HITBOX_DECORATIVOS.get(nombre)
            if isinstance(tam_hitbox, (list, tuple)) and len(tam_hitbox) == 2:
                hw, hh = int(tam_hitbox[0]), int(tam_hitbox[1])
            elif isinstance(tam_hitbox, (int, float)):
                hw = hh = int(tam_hitbox)
            else:
                hw = hh = 37

            bloque_x = self.rect.centerx - hw // 2
            bloque_y = self.rect.centery - hh // 2
            self.rect_bloqueo = pygame.Rect(bloque_x, bloque_y, hw, hh)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.imagen, self.rect.topleft)


class GestorObjetosDecorativos:
    def __init__(self, assets_path):
        self.assets_path = Path(assets_path)
        self.decorativos_disponibles = {}
        self.decorativos_activos = []
        self.config_posiciones = None  # opcional: sobreescribir posiciones desde nivel
        self._cargar_decorativos()
        # Depuración: dibujar contornos de hitbox de decorativos si se desea
        self.mostrar_hitbox = False

    def _cargar_decorativos(self):
        carpeta = self.assets_path / "objetos_decorativos"
        if carpeta.exists():
            for archivo in carpeta.glob("*.png"):
                nombre = archivo.stem
                self.decorativos_disponibles[nombre] = str(archivo)
                print(f"Decorativo cargado: {nombre}")
        else:
            print("Error: Carpeta 'objetos_decorativos' no encontrada")

    def configurar_posiciones(self, posiciones: dict):
        """Define un dict {nombre: (x, y)} para crear decorativos en esas coordenadas."""
        self.config_posiciones = posiciones

    def crear_decorativo(self, x: int, y: int, nombre_imagen: str):
        if nombre_imagen in self.decorativos_disponibles:
            deco = Decorativo(x, y, self.decorativos_disponibles[nombre_imagen], nombre_imagen)
            self.decorativos_activos.append(deco)
            return deco
        else:
            print(f"Error: Decorativo '{nombre_imagen}' no encontrado")
            return None

    def crear_decorativos_por_defecto(self):
        """Crea decorativos según POSICIONES_DECORATIVOS o configuración personalizada."""
        creados = []
        posiciones = self.config_posiciones if self.config_posiciones else POSICIONES_DECORATIVOS

        for nombre, (x, y) in posiciones.items():
            deco = self.crear_decorativo(x, y, nombre)
            if deco:
                creados.append(deco)
        return creados

    def dibujar_todos(self, surface: pygame.Surface):
        for deco in self.decorativos_activos:
            deco.draw(surface)
            if self.mostrar_hitbox and getattr(deco, "rect_bloqueo", None):
                try:
                    pygame.draw.rect(surface, (0, 128, 255), deco.rect_bloqueo, 2)
                except Exception:
                    pass

    def obtener_rects_bloqueo(self):
        """Devuelve rectángulos de bloqueo centrados de decorativos (excluye alfombras)."""
        rects = []
        for deco in self.decorativos_activos:
            rb = getattr(deco, "rect_bloqueo", None)
            if rb is not None:
                rects.append(rb)
        return rects