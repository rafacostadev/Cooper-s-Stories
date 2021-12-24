import pygame
from suporte import importar_arquivo


class Jogador(pygame.sprite.Sprite):
    '''
    Classe que cria tudo relacionado ao jogador.
    pos = Posição no mapa em que o jogador vai ser posicionado, no caso, é baseada na lista
    '''

    def __init__(self, pos):
        super().__init__()
        self.importar_animacoes()
        self.estado_animacao = 0
        self.velocidade_animacao = 0.15
        self.image = self.estados["idle"][self.estado_animacao]
        self.rect = self.image.get_rect(midbottom=pos)
        self.direcao = pygame.math.Vector2(0, 0)
        self.velocidade = 4
        self.peso = 1
        self.pulo = -15

    def importar_animacoes(self):
        nome_diretorio = "./assets/characters/main/"
        self.estados = {"idle": [], "jump_left": [],
                        "jump_right": [], "running_left": [], "running_right": [], "attack_left": [], "attack_right": []}

        for animacoes in self.estados.keys():
            diretorio = nome_diretorio + animacoes
            self.estados[animacoes] = importar_arquivo(diretorio)

    def animar(self):
        animacao = self.estados["running_right"]
        self.estado_animacao += self.velocidade_animacao
        if self.estado_animacao >= len(animacao):
            self.estado_animacao = 0
        self.image = animacao[int(self.estado_animacao)]

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

        if tecla[pygame.K_SPACE] and self.direcao.y == 0:
            self.pular()

    def gravidade(self):
        '''
        Método que aplica a gravidade do jogador.
        '''
        self.direcao.y += self.peso
        self.rect.y += self.direcao.y

    def pular(self):
        '''
        Método que faz o jogador pular.
        '''
        self.direcao.y = self.pulo

    def update(self):
        '''
        Método que aplica a movimentação.
        '''
        self.movimento()
        self.animar()
