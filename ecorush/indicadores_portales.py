import pygame
from pathlib import Path


class IndicadorPortales:
    """
    Dibuja flechas junto a los rectángulos de portal que
    teletransportan a otra habitación, SOLO cuando existen
    objetos encendidos en la habitación destino.
    """

    def __init__(self, assets_path: Path, size=(72, 72)):
        self.assets_path = Path(assets_path)
        self.size = size
        # Cargar flechas desde assets/img
        img_dir = self.assets_path / "img"
        def load(name):
            try:
                surf = pygame.image.load(str(img_dir / name)).convert_alpha()
                return pygame.transform.scale(surf, self.size)
            except Exception as e:
                print(f"[Indicadores] No se pudo cargar {name}: {e}")
                # placeholder
                ph = pygame.Surface(self.size, pygame.SRCALPHA)
                ph.fill((255, 0, 0, 160))
                return ph

        self.flecha_arriba = load("flecha_arriba.png")
        self.flecha_abajo = load("flecha_abajo.png")
        self.flecha_izquierda = load("flecha_izquierda.png")
        self.flecha_derecha = load("flecha_derecha.png")

    def _orientacion_por_rect(self, rect: pygame.Rect, screen_size: tuple[int, int]):
        W, H = screen_size
        margen = 40
        if rect.top <= margen:
            return "arriba"
        if rect.bottom >= H - margen:
            return "abajo"
        if rect.left <= margen:
            return "izquierda"
        if rect.right >= W - margen:
            return "derecha"
        # Por defecto, mostrar hacia arriba
        return "arriba"

    def _posicion_flecha(self, orient: str, rect: pygame.Rect):
        w, h = self.size
        if orient == "arriba":
            return rect.centerx - w // 2, rect.top + 8
        if orient == "abajo":
            return rect.centerx - w // 2, rect.bottom - h - 8
        if orient == "izquierda":
            return rect.left + 8, rect.centery - h // 2
        if orient == "derecha":
            return rect.right - w - 8, rect.centery - h // 2
        return rect.centerx - w // 2, rect.top + 8

    def _hay_objetos_encendidos_en(self, gestor_objetos, habitacion_destino: str) -> bool:
        try:
            for obj in getattr(gestor_objetos, "objetos_activos", []):
                if obj.habitacion == habitacion_destino and obj.encendido:
                    return True
        except Exception:
            pass
        return False

    def draw(self, screen: pygame.Surface, current_room: str, room_portals: dict[str, list[dict]], gestor_objetos, custom_arrows: dict[str, list[dict]] | None = None):
        """
        Dibuja flechas que apuntan a portales de la habitación actual
        SOLO si en la habitación destino hay objetos encendidos.

        Modo por defecto: se posicionan automáticamente junto al rect del portal.
        Modo coordenadas: si se pasa "custom_arrows" (por nivel), usa posiciones
        y orientación definidas manualmente: [{"to": room, "pos": (x,y), "orient": str}].
        """

        # Preferir coordenadas personalizadas si fueron definidas para la habitación
        if custom_arrows and current_room in custom_arrows:
            for ar in custom_arrows[current_room]:
                destino = ar.get("to")
                pos = ar.get("pos")
                orient = ar.get("orient", "arriba")
                if not destino or not pos:
                    continue
                if not self._hay_objetos_encendidos_en(gestor_objetos, destino):
                    continue
                if orient == "arriba":
                    img = self.flecha_arriba
                elif orient == "abajo":
                    img = self.flecha_abajo
                elif orient == "izquierda":
                    img = self.flecha_izquierda
                else:
                    img = self.flecha_derecha
                screen.blit(img, pos)
            return

        # Fallback: flechas automáticas junto al rect del portal
        portals = room_portals.get(current_room, [])
        for p in portals:
            destino = p.get("to")
            rect = p.get("rect")
            if not destino or not isinstance(rect, pygame.Rect):
                continue
            if not self._hay_objetos_encendidos_en(gestor_objetos, destino):
                continue
            orient = self._orientacion_por_rect(rect, screen.get_size())
            if orient == "arriba":
                img = self.flecha_arriba
            elif orient == "abajo":
                img = self.flecha_abajo
            elif orient == "izquierda":
                img = self.flecha_izquierda
            else:
                img = self.flecha_derecha
            pos = self._posicion_flecha(orient, rect)
            screen.blit(img, pos)