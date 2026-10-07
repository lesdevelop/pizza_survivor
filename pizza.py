import pygame
from pathlib import Path

carpeta_proyecto = Path(__file__).resolve().parent

class Pizza:
    imagen = pygame.image.load(str(carpeta_proyecto / "pizza.png"))
    imagen = pygame.transform.scale(imagen, (32, 32))
    velocidad = 6

    def __init__(self, x, y, objetivo_x, objetivo_y):
        self.x = x
        self.y = y
        distancia = (objetivo_x ** 2 + objetivo_y ** 2) ** 0.5
        self.cambio_x = (objetivo_x / distancia) * self.velocidad
        self.cambio_y = (objetivo_y / distancia) * self.velocidad

    @property
    def centro_x(self):
        return self.x + self.imagen.get_width() / 2

    @property
    def centro_y(self):
        return self.y + self.imagen.get_height() / 2

    def mover(self):
        self.x += self.cambio_x
        self.y += self.cambio_y

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
