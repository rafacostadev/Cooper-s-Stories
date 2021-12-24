import pygame


class Bloco(pygame.sprite.Sprite):
    ''' Classe que recebe os atributos para criação do bloco e movimento da câmera.
        pos(Posição do bloco) = uma tupla com a posição X e Y.
        tam(Tamanho do bloco) = um número(pois o bloco é quadrado).
        movimento_x = velocidade da movimentação da câmera.
    '''

    def __init__(self, pos, tam):
        super().__init__()
        self.image = pygame.image.load(
            "./assets/background/blocks/IndustrialTile_73.png")
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self, movimento_x):
        '''
        Método que cria um truque de movimento para a câmera.
        '''
        self.rect.x += movimento_x
