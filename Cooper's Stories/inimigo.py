import pygame
from blocos import BlocosAnimados
from random import randint


class Inimigo(BlocosAnimados):
    def __init__(self, tamanho, posx, posy):
        super().__init__(tamanho, posx, posy, "./assets/characters/inimigo")
        self.rect.y -= 6
        self.velocidade = randint(1, 2)

    def movimento(self):
        self.rect.x += self.velocidade

    def inverter_sprite(self):
        if self.velocidade < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def inverter_movimento(self):
        self.velocidade *= -1

    def update(self, movimento):
        self.rect.x += movimento
        self.animar()
        self.movimento()
        self.inverter_sprite()
