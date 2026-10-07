import pygame
from pathlib import Path
from enemigo import Enemigo

carpeta_proyecto = Path(__file__).resolve().parent

class Perro(Enemigo):
    imagen = pygame.image.load(str(carpeta_proyecto / "perro.png"))
    imagen = pygame.transform.scale(imagen, (54, 64))
    velocidad = 2.5