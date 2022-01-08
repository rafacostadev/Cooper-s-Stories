import pygame
from importacoes import importar_arquivo
from configs import altura


class Jogador(pygame.sprite.Sprite):
    '''
    Classe que cria tudo relacionado ao jogador.
    pos = Posição no mapa em que o jogador vai ser posicionado
    baseado no arquivo CSV do jogador.
    '''

    def __init__(self, pos):
        super().__init__()

        # Importa as animações do personagem
        self.importar_animacoes()

        # Importa o som do pulo
        self.som_pulando = pygame.mixer.Sound("./assets/level/audio/jump.wav")

        # Configurações de animação
        self.estado_animacao = 0
        self.velocidade_animacao = 0.05

        # Configurações de personagem
        self.image = self.estados["idle"][self.estado_animacao]
        self.rect = self.image.get_rect(topleft=pos)
        self.direcao = pygame.math.Vector2(0, 0)

        # Configurações de movimento e animação
        self.velocidade = 2
        self.peso = 1
        self.pulo = -15
        self.lado_direito = True
        self.estado = "idle"
        self.no_chao = False

    def importar_animacoes(self):
        '''
        Método que importa as imagens para serem 
        colocadas dentro das suas respectivas listas de animação.
        '''
        nome_diretorio = "./assets/characters/main/"
        self.estados = {"idle": [],
                        "jump": [], "running": [], "attack": []}
        for animacoes in self.estados.keys():
            diretorio = nome_diretorio + animacoes
            self.estados[animacoes] = importar_arquivo(diretorio)

    def animar(self):
        '''
        Método que anima os movimentos do jogador.
        '''
        animacao = self.estados[self.estado]
        self.estado_animacao += self.velocidade_animacao
        if self.estado_animacao >= len(animacao):
            self.estado_animacao = 0
        imagem = animacao[int(self.estado_animacao)]
        if self.lado_direito:
            self.image = imagem
        else:
            imagem_invertida = pygame.transform.flip(imagem, True, False)
            self.image = imagem_invertida

    def movimento(self):
        '''
        Método que movimenta o jogador.
        Recebe os inputs do teclado o movimenta baseado nisso.
        Usado Vetor para facilitar e também para deixar o movimento suave.
        '''
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_RIGHT]:
            self.direcao.x = 1
            self.lado_direito = True

        elif tecla[pygame.K_LEFT]:
            self.direcao.x = -1
            self.lado_direito = False

        else:
            self.direcao.x = 0

        if tecla[pygame.K_SPACE] and self.no_chao:
            self.som_pulando.play()
            self.som_pulando.set_volume(0.2)
            self.pular()

    def estadoAnimacao(self):
        '''
        Método que identifica o ato do jogador e define seu
        estado para animar corretamente seus movimentos.
        '''
        if self.direcao.y < 0:
            self.estado = "jump"
            self.velocidade_animacao = 0.06
        elif self.direcao.y == 0 and self.direcao.x != 0:
            self.estado = "running"
            self.velocidade_animacao = 0.3
        else:
            self.estado = "idle"
            self.velocidade_animacao = 0.05

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
        Método que atualiza o personagem na tela.
        '''
        self.movimento()
        self.estadoAnimacao()
        self.animar()
