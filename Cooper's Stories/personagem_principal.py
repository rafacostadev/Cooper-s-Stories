import pygame


class Jogador(pygame.sprite.Sprite):
    '''
    Classe que cria tudo relacionado ao jogador.
    pos = Posição no mapa em que o jogador vai ser posicionado, no caso, é baseada na lista
    '''

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(
            "./assets/characters/main/idle/1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.direcao = pygame.math.Vector2(0, 0)
        self.velocidade = 8

    def movimento(self):
        '''
        Método que movimenta o jogador.
        Recebe os inputs do teclado o movimenta baseado nisso.
        Usado Vetor para facilitar e também para deixar o movimento suave.
        '''
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_RIGHT]:
            self.direcao.x = 1
        elif tecla[pygame.K_LEFT]:
            self.direcao.x = -1
        else:
            self.direcao.x = 0

    def update(self):
        '''
        Método que aplica a movimentação.
        '''
        self.movimento()
        self.rect.x += self.direcao.x * self.velocidade
