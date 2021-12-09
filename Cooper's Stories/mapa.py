import pygame
from configs import *
from blocos import Bloco


class MostrarBlocos():
    '''
    Classe que recebe os atributos para mostrar os blocos.
    level = "mapa" que vai ser usado para mostrar os blocos na tela. 
    superficie = a tela em que vai ser mostrada o mapa.
    '''

    def __init__(self, level, superficie):
        self.superficie = superficie
        self.setarblocos(level)

    def setarblocos(self, mapa):
        '''
        Recebe o mapa como atributo para identificar onde colocar cada bloco e
        os adiciona no grupo de sprites de blocos.
        '''
        self.blocos = pygame.sprite.Group()
        for index_linha, linhas in enumerate(mapa):
            for index_coluna, coluna in enumerate(linhas):
                PosX = index_coluna * tamanhoBloco
                PosY = index_linha * tamanhoBloco
                if coluna == "X":
                    bloco = Bloco((PosX, PosY), tamanhoBloco)
                    self.blocos.add(bloco)

    def mostrarblocos(self):
        '''
        Usado para facilitar e diminuir o código ao mostrar
        Os blocos na tela.
        '''
        self.blocos.draw(self.superficie)
