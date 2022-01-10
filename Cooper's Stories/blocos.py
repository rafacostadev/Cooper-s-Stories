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
    '''
    Blocos que não se movem, só recebe imagem e o padrão da classe bloco.
    '''

    def __init__(self, tam, posx, posy, superficie):
        super().__init__(tam, posx, posy)
        self.image = superficie


class BlocosAnimados(Bloco):
    '''
    Blocos que são animados, recebem além da imagem, os arquivos de sprite
    para animação.
    '''

    def __init__(self, tam, posx, posy, caminho):
        super().__init__(tam, posx, posy)
        self.sprites = importar_arquivo(caminho)
        self.sprite_atual = 0
        self.image = self.sprites[self.sprite_atual]

    def animar(self):
        '''
        Método para animação dos sprites de blocos animados.
        '''
        self.sprite_atual += 0.15
        if self.sprite_atual >= len(self.sprites):
            self.sprite_atual = 0
        self.image = self.sprites[int(self.sprite_atual)]

    def update(self, movimento_x):
        '''
        Método para simplificar e diminuir código, anima e 
        atualiza a posição dos blocos com base na "câmera" do jogo.
        '''
        self.rect.x += movimento_x
        self.animar()
