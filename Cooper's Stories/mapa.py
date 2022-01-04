import pygame
from configs import *
from blocos import Bloco, BlocosPisos
from personagem_principal import Jogador
from level_config import *
from importacoes import importar_arquivo_csv, importar_blocos_recortados


class MostrarBlocos():
    '''
    Classe que recebe os atributos para iniciar o mapa completo.
    level = arquivo CSV que vai ser utilizado para mostrar os blocos na tela.
    superficie = a tela em que vai ser mostrada o mapa.
    '''

    def __init__(self, level, superficie):
        self.superficie = superficie
        layout = importar_arquivo_csv(level["pisos"])
        self.terreno_mapa = self.gerar_blocos(layout, "pisos")

        # Movimento da câmera
        self.movimento = 0

    def gerar_blocos(self, layout, tipo):
        '''
        Recebe o layout como atributo para identificar onde posicionar
        cada bloco no jogo. Recebe o tipo para identificar que tipo de
        bloco está sendo posicionado.
        '''
        blocos = pygame.sprite.Group()
        for index_linha, linhas in enumerate(layout):
            for index_coluna, coluna in enumerate(linhas):
                if coluna != "-1":
                    PosX = index_coluna * tamanhoBloco
                    PosY = index_linha * tamanhoBloco
                    if tipo == "pisos":
                        lista_blocos_pisos = importar_blocos_recortados(
                            "./assets/level/tile_set/Tiles.png")
                        bloco_superficie = lista_blocos_pisos[int(coluna)]
                        sprite = BlocosPisos(
                            tamanhoBloco, PosX, PosY, bloco_superficie)
                        blocos.add(sprite)
        return blocos

    def movimento_camera(self):
        '''
        Adiciona o truque do movimento da câmera, movendo os 
        blocos no background se o jogador chegar a certa parte do mapa.
        '''
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
            jogador.velocidade = 4

    def colisao_horizontal(self):
        '''
        Adiciona a colisão horizontal entre o 
        personagem e os blocos do mapa.
        '''
        jogador = self.jogador.sprite
        jogador.rect.x += jogador.direcao.x * jogador.velocidade
        for sprite in self.blocos.sprites():
            if sprite.rect.colliderect(jogador.rect):
                if jogador.direcao.x < 0:
                    jogador.rect.left = sprite.rect.right
                elif jogador.direcao.x > 0:
                    jogador.rect.right = sprite.rect.left

    def colisao_vertical(self):
        '''
        Adiciona a colisão vertical entre o
        o personagem e os blocos do mapa e verifica
        se o jogador está no solo para poder pular.
        '''
        jogador = self.jogador.sprite
        jogador.gravidade()
        for sprite in self.blocos.sprites():
            if sprite.rect.colliderect(jogador.rect):
                if jogador.direcao.y > 0:
                    jogador.rect.bottom = sprite.rect.top
                    jogador.direcao.y = 0
                    jogador.no_chao = True
                elif jogador.direcao.y < 0:
                    jogador.rect.top = sprite.rect.bottom
                    jogador.direcao.y = 0

        if jogador.no_chao and jogador.direcao.y < 0 or jogador.direcao.y > 1:
            jogador.no_chao = False

    def mostrar_mapa(self):
        '''
        Usado para facilitar e diminuir o código ao mostrar
        os blocos e jogador na tela e executar todos os métodos restantes.
        '''
        # Mapa
        self.terreno_mapa.draw(self.superficie)
        self.terreno_mapa.update(-2)
        # self.terreno_mapa.update(self.movimento)
        # self.movimento_camera()
        # self.colisao_horizontal()
        # self.colisao_vertical()
        # # Jogador
        # self.jogador.update()
        # self.jogador.draw(self.superficie)
