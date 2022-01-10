import pygame
from configs import *


class background:
    '''
    Carrega a imagem de background do jogo.
    '''

    def __init__(self):
        self.background_image = pygame.image.load(
            "./assets/level/background_image/Background.png").convert_alpha()
        self.background_image = pygame.transform.scale(
            self.background_image, (largura, altura))

    def draw(self, superficie):
        '''
        Método que desenha o background do jogo.
        '''
        superficie.blit(self.background_image, (0, 0))
