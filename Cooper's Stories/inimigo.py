import pygame
from blocos import BlocosAnimados


class Inimigo(BlocosAnimados):
    '''
    Adiciona os inimigos no mapa, carregando o tamanho do mesmo
    posx e posy que vão ser setados, a localização em que vai 
    ser setado e baseado nos valores do arquivo CSV.
    '''

    def __init__(self, tamanho, posx, posy):
        super().__init__(tamanho, posx, posy, "./assets/characters/inimigo")
        self.rect.y -= 6
        self.velocidade = 1

    def movimento(self):
        '''
        Método que adiciona o movimento dos inimigos.
        '''
        self.rect.x += self.velocidade

    def inverter_sprite(self):
        '''
        Método que inverte a imagem do inimigo baseada
        em sua direção de movimento.
        '''
        if self.velocidade < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def inverter_movimento(self):
        '''
        Método que inverte a direção de movimento do inimigo
        ao detectar colisão com os blocos invisíveis de limite.
        '''
        self.velocidade *= -1

    def update(self, movimento):
        '''
        Método para facilitar e diminuir código.
        '''
        self.rect.x += movimento
        self.animar()
        self.movimento()
        self.inverter_sprite()
