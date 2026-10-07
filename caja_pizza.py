import pygame
from pathlib import Path

carpeta_proyecto = Path(__file__).resolve().parent


class CajaPizza:
    imagen = pygame.image.load(str(carpeta_proyecto / "caja_pizza.png"))
    imagen = pygame.transform.scale(imagen, (80, 80))
    duracion = 5000

    def __init__(self, x, y, ahora):
        self.x = x
        self.y = y
        self.expira_en = ahora + self.duracion

    @property
    def rect(self):
        return self.imagen.get_rect(topleft=(self.x, self.y))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))
