import pygame


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


class BlocosPisos(Bloco):
    def __init__(self, tam, posx, posy, superficie):
        super().__init__(tam, posx, posy)
        self.image = superficie
