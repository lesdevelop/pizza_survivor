import pygame
from pathlib import Path
import random
from perro import Perro
from gato import Gato
from caja_pizza import CajaPizza
from pizza import Pizza
from repartidor import Repartidor
from interfaz import Interfaz


pygame.init()
pygame.mixer.init()

# Crear la pantalla del juegosss
pantalla = pygame.display.set_mode((800, 600)) #pixels
pygame.display.set_caption("Pizza Survivor") #titulo del juego en ventana
carpeta_proyecto = Path(__file__).resolve().parent
pantalla = pygame.display.get_surface()
icono = pygame.image.load(str(carpeta_proyecto / "pizza.png")) #cargar imagen icono
pygame.display.set_icon(icono)
interfaz = Interfaz(pantalla)

# Sonidos
pygame.mixer.music.load(str(carpeta_proyecto / "MusicaFondo.mp3"))
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
sonido_disparo = pygame.mixer.Sound(str(carpeta_proyecto / "disparo.mp3"))
sonido_golpe = pygame.mixer.Sound(str(carpeta_proyecto / "golpe.mp3"))
sonido_vida_perdida = pygame.mixer.Sound(str(carpeta_proyecto / "vida_perdida.mp3"))
sonido_disparo.set_volume(1.0)
sonido_golpe.set_volume(1.0)
sonido_vida_perdida.set_volume(1.0)

# Fondo
fondo = pygame.image.load(str(carpeta_proyecto / "fondo.png")) #cargar imagen fondo
fondo = pygame.transform.scale(fondo, (800, 600)) #redimensionar

# Vidas e invulnerabilidad
repartidor = Repartidor(368, 440)

# Puntuación y tiempo
puntuacion = 0
tiempo_inicio = pygame.time.get_ticks()

def crear_enemigo():
    tipo_enemigo = random.choice((Perro, Gato))
    borde = random.choice(("arriba", "abajo", "izquierda", "derecha"))
    ancho = tipo_enemigo.imagen.get_width()
    alto = tipo_enemigo.imagen.get_height()
    if borde == "arriba":
        return tipo_enemigo(random.randint(0, 800 - ancho), 0)
    if borde == "abajo":
        return tipo_enemigo(random.randint(0, 800 - ancho), 600 - alto)
    if borde == "izquierda":
        return tipo_enemigo(0, random.randint(0, 600 - alto))
    return tipo_enemigo(800 - ancho, random.randint(0, 600 - alto))

enemigos = [crear_enemigo()]
ultimo_enemigo = pygame.time.get_ticks()
caja_pizza = None
proxima_caja_pizza = pygame.time.get_ticks() + random.randint(15000, 20000)

def intervalo_spawn_enemigos(segundos_transcurridos):
    minutos_sobrevividos = segundos_transcurridos // 60
    ratio_spawn = 1 + 0.1 * minutos_sobrevividos
    return 1650 / ratio_spawn

def mover_enemigos(enemigos, repartidor_x, repartidor_y):
    for enemigo in enemigos:
        enemigo.mover(repartidor_x, repartidor_y)

def crear_caja_pizza(ahora):
    ancho = CajaPizza.imagen.get_width()
    alto = CajaPizza.imagen.get_height()
    x = random.randint(0, 800 - ancho)
    y = random.randint(0, 600 - alto)
    return CajaPizza(x, y, ahora)

# Pizzas
pizzas = []
ultimo_lanzamiento = pygame.time.get_ticks()
reloj = pygame.time.Clock()

def mover_pizzas(pizzas):
    for pizza in pizzas:
        pizza.mover()

    return [
        pizza for pizza in pizzas
        if -Pizza.imagen.get_width() < pizza.x < 800
        and -Pizza.imagen.get_height() < pizza.y < 600
    ]

def lanzar_pizza(enemigos, pizzas, repartidor, ahora, ultimo_lanzamiento):
    if enemigos and ahora - ultimo_lanzamiento >= 1800:
        enemigo_cercano = min(
            enemigos,
            key=lambda enemigo: (enemigo.centro_x - repartidor.centro_x) ** 2
            + (enemigo.centro_y - repartidor.centro_y) ** 2,
        )
        dx = enemigo_cercano.centro_x - repartidor.centro_x
        dy = enemigo_cercano.centro_y - repartidor.centro_y
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        if distancia > 0:
            pizzas.append(Pizza(repartidor.x + 16, repartidor.y + 34, dx, dy))
            sonido_disparo.play()
        return ahora
    return ultimo_lanzamiento

def detectar_colisiones():
    global pizzas, enemigos, puntuacion # Para que no se creen variables locales dentro de la función

    pizzas_sobrevivientes = []
    enemigos_sobrevivientes = list(enemigos) #Copia de los enemigos existentes

    for pizza_actual in pizzas:
        pizza_choco = False

        for enemigo_actual in enemigos_sobrevivientes[:]:
            dx = pizza_actual.centro_x - enemigo_actual.centro_x
            dy = pizza_actual.centro_y - enemigo_actual.centro_y
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            if distancia < 30:
                enemigos_sobrevivientes.remove(enemigo_actual)
                pizza_choco = True
                puntuacion += 1
                sonido_golpe.play()
                break
        if not pizza_choco:
            pizzas_sobrevivientes.append(pizza_actual)

    pizzas = pizzas_sobrevivientes
    enemigos = enemigos_sobrevivientes

# Detectar el contacto del repartidor con los enemigos
def detectar_colision_repartidor(enemigos, repartidor, ahora):
    enemigos_sin_colision = []
    hubo_contacto = False
    puede_recibir_golpe = ahora >= repartidor.invulnerable_hasta

    for enemigo in enemigos:
        puede_hacer_dano = ahora >= enemigo.puede_hacer_dano_desde
        if (
            repartidor.rect.colliderect(enemigo.rect)
            and puede_hacer_dano
            and puede_recibir_golpe
        ):
            hubo_contacto = True
        else:
            enemigos_sin_colision.append(enemigo)

    if hubo_contacto:
        repartidor.recibir_golpe(ahora, sonido_vida_perdida)

    return enemigos_sin_colision

def dibujar_pantalla_juego(ahora):
    pantalla.blit(fondo, (0, 0))
    repartidor.dibujar(pantalla, ahora)
    interfaz.dibujar_vidas(repartidor.vidas)
    interfaz.dibujar_puntuacion(puntuacion)
    segundos_transcurridos = (ahora - tiempo_inicio) // 1000
    interfaz.dibujar_cronometro(segundos_transcurridos)
    for enemigo in enemigos:
        enemigo.dibujar(pantalla)
    if caja_pizza is not None:
        caja_pizza.dibujar(pantalla)
    for pizza in pizzas:
        pizza.dibujar(pantalla)

# Loop del juego
estado = "jugando"
tiempo_sobrevivido = 0
se_ejecuta = True
while se_ejecuta:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        elif estado == "jugando" and evento.type == pygame.KEYDOWN:
            repartidor.manejar_evento(evento)
        elif estado == "jugando" and evento.type == pygame.KEYUP:
            repartidor.manejar_evento(evento)
        elif evento.type == pygame.WINDOWFOCUSLOST:
            repartidor.manejar_evento(evento)

    if estado == "jugando":
        ahora = pygame.time.get_ticks()
        repartidor.mover(800, 600)
        mover_enemigos(enemigos, repartidor.x, repartidor.y)

        # Aumentar el ratio de aparición un 10% por cada minuto sobrevivido.
        segundos_transcurridos = (ahora - tiempo_inicio) // 1000
        if ahora - ultimo_enemigo >= intervalo_spawn_enemigos(segundos_transcurridos):
            enemigos.append(crear_enemigo())
            ultimo_enemigo = ahora

        if caja_pizza is None and ahora >= proxima_caja_pizza:
            caja_pizza = crear_caja_pizza(ahora)
            proxima_caja_pizza = ahora + random.randint(15000, 20000)
        elif caja_pizza is not None:
            if ahora >= caja_pizza.expira_en:
                caja_pizza = None
            elif repartidor.rect.colliderect(caja_pizza.rect):
                repartidor.recuperar_vida()
                caja_pizza = None

        # Lanzar una pizza cada 1,8 segundos hacia el enemigo más cercano
        ultimo_lanzamiento = lanzar_pizza(
            enemigos, pizzas, repartidor, ahora, ultimo_lanzamiento
        )

        # Mover las pizzas y quitar las que salieron de la pantalla
        pizzas = mover_pizzas(pizzas)

        detectar_colisiones()

        # Detectar el contacto con un enemigo y actualizar las vidas
        enemigos = detectar_colision_repartidor(enemigos, repartidor, ahora)

        if repartidor.vidas == 0:
            estado = "terminado"
            tiempo_sobrevivido = (ahora - tiempo_inicio) // 1000
            pygame.mixer.music.stop()

    if estado == "jugando":
        dibujar_pantalla_juego(ahora)
    else:
        interfaz.dibujar_pantalla_fin(fondo, puntuacion, tiempo_sobrevivido)

    pygame.display.update()
    reloj.tick(60)
    

pygame.quit()
