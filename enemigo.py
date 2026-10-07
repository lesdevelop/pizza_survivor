import pygame
import random
from pathlib import Path

class Enemigo:
    duracion_proteccion_inicial = 2000

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imagen = type(self).imagen
        self.velocidad = type(self).velocidad
        self.puede_hacer_dano_desde = (
            pygame.time.get_ticks() + self.duracion_proteccion_inicial
        )

    @property
    def rect(self):
        rect = self.imagen.get_rect(topleft=(self.x, self.y))
        return rect.inflate(
            -int(rect.width * 0.2),
            -int(rect.height * 0.2),
        )

    @property
    def centro_x(self):
        return self.x + self.imagen.get_width() / 2

    @property
    def centro_y(self):
        return self.y + self.imagen.get_height() / 2

    def mover(self, objetivo_x, objetivo_y):
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        if distancia > 0:
            self.x += (dx / distancia) * self.velocidad
            self.y += (dy / distancia) * self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
