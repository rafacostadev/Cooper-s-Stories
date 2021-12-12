import pygame
from configs import *
from blocos import Bloco
from personagem_principal import Jogador
from missao_1_npc import Npc


class MostrarBlocos():
    '''
    Classe que recebe os atributos para mostrar os blocos.
    level = "mapa" que vai ser usado para mostrar os blocos na tela. 
    superficie = a tela em que vai ser mostrada o mapa.
    '''

    def __init__(self, level, superficie):
        self.superficie = superficie
        self.setar_mapa(level)

        # Movimento da câmera
        self.movimento = 0

    def setar_mapa(self, mapa):
        '''
        Recebe o mapa como atributo para identificar onde colocar cada bloco e
        os adiciona no grupo de sprites de blocos.
        '''
        self.blocos = pygame.sprite.Group()
        self.jogador = pygame.sprite.GroupSingle()
        self.npc = pygame.sprite.GroupSingle()

        for index_linha, linhas in enumerate(mapa):
            for index_coluna, coluna in enumerate(linhas):
                PosX = index_coluna * tamanhoBloco
                PosY = index_linha * tamanhoBloco
                if coluna == "X":
                    bloco = Bloco((PosX, PosY), tamanhoBloco)
                    self.blocos.add(bloco)
                elif coluna == "P":
                    jogador = Jogador((PosX, PosY))
                    self.jogador.add(jogador)
                elif coluna == "N":
                    npc = Npc((PosX, PosY))
                    self.npc.add(npc)

    def movimento_camera(self):
        jogador = self.jogador.sprite
        jogador_x = jogador.rect.centerx
        direcao_x = jogador.direcao.x
        if jogador_x < (largura/6) and direcao_x < 0:
            self.movimento = 8
            jogador.velocidade = 0
        elif jogador_x > largura - (largura/6) and direcao_x > 0:
            self.movimento = -8
            jogador.velocidade = 0
        else:
            self.movimento = 0
            jogador.velocidade = 8

    def mostrar_mapa(self):
        '''
        Usado para facilitar e diminuir o código ao mostrar
        os blocos e jogador na tela e executar todos os métodos restantes.
        '''
        # Blocos
        self.blocos.draw(self.superficie)
        self.blocos.update(self.movimento)

        # Jogador
        self.jogador.update()
        self.jogador.draw(self.superficie)
        self.movimento_camera()
        # Npc
        self.npc.draw(self.superficie)
