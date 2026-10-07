import pygame
from pathlib import Path

carpeta_proyecto = Path(__file__).resolve().parent

class Repartidor:
    imagen = pygame.image.load(str(carpeta_proyecto / "repartidor.png"))
    imagen = pygame.transform.scale(imagen, (64, 100))
    velocidad = 6
    vidas_maximas = 5
    duracion_invulnerabilidad_inicial = 2000
    duracion_invulnerabilidad = 1000

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cambio_x = 0
        self.cambio_y = 0
        self.teclas_pulsadas = set()
        self.vidas = 3
        self.invulnerable_hasta = (
            pygame.time.get_ticks() + self.duracion_invulnerabilidad_inicial
        )

    def recuperar_vida(self):
        if self.vidas >= self.vidas_maximas:
            return False

        self.vidas += 1
        return True

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

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            self.teclas_pulsadas.add(evento.key)
        elif evento.type == pygame.KEYUP:
            self.teclas_pulsadas.discard(evento.key)
        elif evento.type == pygame.WINDOWFOCUSLOST:
            self.teclas_pulsadas.clear()

        izquierda = any(
            tecla in self.teclas_pulsadas
            for tecla in (pygame.K_LEFT, pygame.K_a)
        )
        derecha = any(
            tecla in self.teclas_pulsadas
            for tecla in (pygame.K_RIGHT, pygame.K_d)
        )
        arriba = any(
            tecla in self.teclas_pulsadas
            for tecla in (pygame.K_UP, pygame.K_w)
        )
        abajo = any(
            tecla in self.teclas_pulsadas
            for tecla in (pygame.K_DOWN, pygame.K_s)
        )
        self.cambio_x = (derecha - izquierda) * self.velocidad
        self.cambio_y = (abajo - arriba) * self.velocidad

    def mover(self, ancho_pantalla, alto_pantalla):
        self.x += self.cambio_x
        self.y += self.cambio_y
        self.x = max(0, min(self.x, ancho_pantalla - self.imagen.get_width()))
        self.y = max(0, min(self.y, alto_pantalla - self.imagen.get_height()))

    def recibir_golpe(self, ahora, sonido_vida_perdida):
        if ahora < self.invulnerable_hasta:
            return False

        self.vidas -= 1
        self.invulnerable_hasta = ahora + self.duracion_invulnerabilidad
        sonido_vida_perdida.play()
        return True

    def dibujar(self, pantalla, ahora):
        if ahora >= self.invulnerable_hasta or (ahora // 100) % 2 == 0:
            pantalla.blit(self.imagen, (self.x, self.y))
