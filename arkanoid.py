import pygame
import random


pygame.init()
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Breakout      Version 1.0.0")


NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
COLORES_BLOQUES = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 165, 0)
]

fuente = pygame.font.SysFont(None, 60)
fuente_peque = pygame.font.SysFont(None, 36)


def crear_bloques():
    bloques_nuevos = []
    for fila in range(5):
        for col in range(10):
            bloque = pygame.Rect(col * 80 + 5, fila * 30 + 40, 70, 20)
            color = random.choice(COLORES_BLOQUES)
            bloques_nuevos.append((bloque, color))
    return bloques_nuevos

def reiniciar_juego():
    global paleta, pelota, vel_pelota, bloques, pausado, perdio
    paleta = pygame.Rect(ANCHO // 2 - 60, ALTO - 20, 120, 10)
    pelota = pygame.Rect(ANCHO // 2 - 10, ALTO // 2, 20, 20)
    vel_pelota = [4, -4]
    bloques = crear_bloques()
    pausado = False
    perdio = False

reiniciar_juego()
reloj = pygame.time.Clock()
corriendo = True


while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p and not perdio:
                pausado = not pausado
            if evento.key == pygame.K_r and perdio:
                reiniciar_juego()

    if not pausado and not perdio:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and paleta.left > 0:
            paleta.move_ip(-6, 0)
        if teclas[pygame.K_RIGHT] and paleta.right < ANCHO:
            paleta.move_ip(6, 0)

        pelota.x += vel_pelota[0]
        pelota.y += vel_pelota[1]

        if pelota.left <= 0 or pelota.right >= ANCHO:
            vel_pelota[0] *= -1
        if pelota.top <= 0:
            vel_pelota[1] *= -1
        if pelota.bottom >= ALTO:
            perdio = True
            pausado = True

        if pelota.colliderect(paleta):
            vel_pelota[1] *= -1

        for bloque, color in bloques[:]:
            if pelota.colliderect(bloque):
                bloques.remove((bloque, color))
                vel_pelota[1] *= -1
                break

   
    ventana.fill(NEGRO)
    pygame.draw.rect(ventana, BLANCO, paleta)
    pygame.draw.ellipse(ventana, VERDE, pelota)
    for bloque, color in bloques:
        pygame.draw.rect(ventana, color, bloque)

    if pausado and not perdio:
        texto = fuente.render("PAUSA", True, BLANCO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - texto.get_height() // 2))

    if perdio:
        texto = fuente.render("¡PERDISTE!", True, (255, 50, 50))
        texto2 = fuente_peque.render("Presiona 'R' para reiniciar", True, BLANCO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 40))
        ventana.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 + 20))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
