import pygame
from pathlib import Path
from enemigo import Enemigo

carpeta_proyecto = Path(__file__).resolve().parent

class Gato(Enemigo):
    imagen = pygame.image.load(str(carpeta_proyecto / "gato.png"))
    imagen = pygame.transform.scale(imagen, (44, 54))
    velocidad = 3.5