import pygame
from pathlib import Path

carpeta_proyecto = Path(__file__).resolve().parent


class Interfaz:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_game_over = pygame.font.Font(None, 80)
        self.imagen_corazon = pygame.image.load(
            str(carpeta_proyecto / "corazon.png")
        )
        self.imagen_corazon = pygame.transform.scale(self.imagen_corazon, (32, 32))

    @staticmethod
    def formatear_tiempo(segundos):
        minutos, segundos_restantes = divmod(segundos, 60)
        return f"{minutos}:{segundos_restantes:02d}"

    def dibujar_vidas(self, vidas):
        for vida in range(vidas):
            self.pantalla.blit(self.imagen_corazon, (10 + vida * 40, 10))

    def dibujar_puntuacion(self, puntuacion):
        texto = self.fuente.render(
            f"Puntuación: {puntuacion}", True, (255, 255, 255)
        )
        self.pantalla.blit(texto, (600, 10))

    def dibujar_cronometro(self, segundos_transcurridos):
        texto = self.fuente.render(
            f"Tiempo: {self.formatear_tiempo(segundos_transcurridos)}",
            True,
            (255, 255, 255),
        )
        self.pantalla.blit(texto, texto.get_rect(midtop=(400, 10)))

    def dibujar_pantalla_fin(self, fondo, puntuacion, tiempo_sobrevivido):
        self.pantalla.blit(fondo, (0, 0))

        titulo = self.fuente_game_over.render(
            "GAME OVER", True, (255, 255, 255)
        )
        self.pantalla.blit(titulo, titulo.get_rect(center=(400, 230)))

        texto_puntuacion = self.fuente.render(
            f"Puntuación final: {puntuacion}", True, (255, 255, 255)
        )
        self.pantalla.blit(
            texto_puntuacion, texto_puntuacion.get_rect(center=(400, 310))
        )

        texto_tiempo = self.fuente.render(
            f"Tiempo sobrevivido: {self.formatear_tiempo(tiempo_sobrevivido)}",
            True,
            (255, 255, 255),
        )
        self.pantalla.blit(
            texto_tiempo, texto_tiempo.get_rect(center=(400, 360))
        )
