import pygame


class Bloco(pygame.sprite.Sprite):
    ''' Classe que recebe os atributos para criação do bloco.
        pos(Posição do bloco) = uma tupla com a posição X e Y.
        tam(Tamanho do bloco) = um número(pois o bloco é quadrado).
    '''

    def __init__(self, pos, tam):
        super().__init__()
        self.image = pygame.Surface((tam, tam))
        self.image.fill("green")
        self.rect = self.image.get_rect(midbottom=pos)
