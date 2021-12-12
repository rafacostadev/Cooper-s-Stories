import pygame
from sys import exit
from configs import *
from mapa import MostrarBlocos

pygame.init()
pygame.display.set_caption("Cooper's Stories")
tela = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock()
level = MostrarBlocos(mapa, tela)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    tela.fill("black")
    level.mostrar_mapa()

    # Adicionar antes
    pygame.display.update()
    clock.tick(60)
