import pygame
from importacoes import importar_arquivo


class Bloco(pygame.sprite.Sprite):
    ''' Classe que recebe os atributos para criação do bloco e movimento da câmera.
        tam(Tamanho do bloco) = um número, normalmente 32.
        pos(Posição do bloco) = uma tupla com a posição X e Y do bloco.
        movimento_x = velocidade da movimentação da câmera.
    '''

    def __init__(self, tam, posx, posy):
        super().__init__()
        self.image = pygame.Surface((tam, tam))
        self.rect = self.image.get_rect(topleft=(posx, posy))

    def update(self, movimento_x):
        '''
        Método que cria um truque de movimento para a câmera.
        '''
        self.rect.x += movimento_x


class BlocosEstaticos(Bloco):
    def __init__(self, tam, posx, posy, superficie):
        super().__init__(tam, posx, posy)
        self.image = superficie


class BlocosAnimados(Bloco):
    def __init__(self, tam, posx, posy, caminho):
        super().__init__(tam, posx, posy)
        self.sprites = importar_arquivo(caminho)
        self.sprite_atual = 0
        self.image = self.sprites[self.sprite_atual]

    def animar(self):
        self.sprite_atual += 0.15
        if self.sprite_atual >= len(self.sprites):
            self.sprite_atual = 0
        self.image = self.sprites[int(self.sprite_atual)]

    def update(self, movimento_x):
        self.rect.x += movimento_x
        self.animar()
