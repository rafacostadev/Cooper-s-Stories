import pygame
from configs import *
from blocos import Bloco, BlocosEstaticos, BlocosAnimados
from personagem_principal import Jogador
from inimigo import Inimigo
from level_config import *
from importacoes import importar_arquivo_csv, importar_blocos_recortados
from background_image import background
from math import sin


class MostrarBlocos():
    '''
    Classe que recebe os atributos para iniciar o mapa completo.
    level = arquivo CSV que vai ser utilizado para mostrar os blocos na tela.
    superficie = a tela em que vai ser mostrada o mapa.
    '''

    def __init__(self, superficie):

        # Superfície em que vai ser mostrado o jogo
        self.superficie = superficie

        # Status mapa
        self.mapa_atual = level_1
        self.objetivos_1 = False
        self.objetivos_2 = False
        self.objetivos_3 = False

        # Status jogador
        self.vivo = True
        self.vida_atual = 4
        self.invencivel = False
        self.duracao_invencibilidade = 800
        self.tempo_dano = 0
        self.valor_piscar = 0

        # Jogador
        jogador_layout = importar_arquivo_csv(self.mapa_atual["jogador"])
        self.jogador = pygame.sprite.GroupSingle()
        self.objetivo = pygame.sprite.GroupSingle()
        self.setar_jogador(jogador_layout)

        # Imagem de fundo
        self.background = background()

        # Blocos de piso
        pisos_layout = importar_arquivo_csv(self.mapa_atual["pisos"])
        self.terreno_mapa = self.gerar_blocos(pisos_layout, "pisos")

        # Moedas
        moedas_layout = importar_arquivo_csv(self.mapa_atual["dinheiro"])
        self.moedas = self.gerar_blocos(moedas_layout, "dinheiro")

        # Inimigos
        inimigos_layout = importar_arquivo_csv(self.mapa_atual["inimigos"])
        self.inimigos = self.gerar_blocos(inimigos_layout, "inimigos")

        # Limites inimigos
        limites_inimigos_layout = importar_arquivo_csv(
            self.mapa_atual["limites_inimigos"])
        self.limites_inimigos = self.gerar_blocos(
            limites_inimigos_layout, "limites_inimigos")

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
                        sprite = BlocosEstaticos(
                            tamanhoBloco, PosX, PosY, bloco_superficie)

                    if tipo == "dinheiro":
                        sprite = BlocosAnimados(
                            tamanhoBloco, PosX, PosY, "./assets/level/tile_set/dinheiro_sprites")

                    if tipo == "inimigos":
                        sprite = Inimigo(tamanhoBloco, PosX, PosY)

                    if tipo == "limites_inimigos":
                        sprite = Bloco(
                            tamanhoBloco, PosX, PosY)

                    blocos.add(sprite)

        return blocos

    def setar_jogador(self, layout):
        '''
        Posiciona o jogador no mapa baseado no arquivo CSV e também
        adiciona o objetivo do jogador.
        '''
        for index_linha, linhas in enumerate(layout):
            for index_coluna, coluna in enumerate(linhas):
                PosX = index_coluna * tamanhoBloco
                PosY = index_linha * tamanhoBloco
                if coluna == "0":
                    sprite = Jogador((PosX, PosY))
                    self.jogador.add(sprite)
                if coluna == "1":
                    objetivo_imagem = pygame.image.load(
                        "./assets/level/tile_set/player_goal.png").convert_alpha()
                    sprite = BlocosEstaticos(
                        tamanhoBloco, PosX, PosY, objetivo_imagem)
                    self.objetivo.add(sprite)

    def colisao_movimentos_inimigo(self):
        '''
        Adiciona as colisões dos inimigos com os blocos invisíveis
        para colocar um limite nos seus movimentos e aciona o método
        para inverter o movimento.
        '''
        for inimigos in self.inimigos.sprites():
            if pygame.sprite.spritecollide(inimigos, self.limites_inimigos, False):
                inimigos.inverter_movimento()

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
        for sprite in self.terreno_mapa.sprites():
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
        for sprite in self.terreno_mapa.sprites():
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

    def pegar_moedas(self):
        jogador = self.jogador.sprite
        moedas = self.moedas.sprites()
        for moeda in moedas:
            if moeda.rect.colliderect(jogador.rect):
                moeda.kill()

    def objetivos(self):
        if self.mapa_atual == level_1 and len(self.moedas) == 0:
            self.objetivos_1 = True

        if self.mapa_atual == level_2 and len(self.moedas) == 0:
            pass

        if self.mapa_atual == level_3 and len(self.moedas) == 0:
            pass

    def selecionar_fase(self):
        if self.mapa_atual == level_1 and self.objetivos_1:
            print("passou")
        if self.mapa_atual == level_2 and self.objetivos_2:
            self.mapa_atual = level_3
        if self.mapa_atual == level_3 and self.objetivos_3:
            pass

    def checar_fase(self):
        print(self.mapa_atual)
        return self.mapa_atual

    def colisao_inimigos(self):
        '''
        Adiciona a colisão com os inimigos do jogo para eliminar
        ou levar dano.
        '''
        jogador = self.jogador.sprite
        inimigos = self.inimigos.sprites()
        for inimigo in inimigos:
            if inimigo.rect.colliderect(jogador.rect) and jogador.direcao.y > 0:
                inimigo.kill()
                jogador.direcao.y = -10
            elif inimigo.rect.colliderect(jogador.rect):
                self.dano()

    def queda(self):
        jogador = self.jogador.sprite.rect.top
        if jogador >= altura:
            self.vida_atual = 0

    def dano(self):
        if not self.invencivel:
            self.invencivel = True
            self.vida_atual -= 1
            self.tempo_dano = pygame.time.get_ticks()

    def valor_efeito_dano(self):
        self.valor_piscar = sin(pygame.time.get_ticks())
        if self.valor_piscar >= 0:
            return 255
        else:
            return 0

    def efeito_dano(self):
        if self.invencivel:
            self.jogador.sprite.image.set_alpha(self.valor_piscar)
        else:
            self.jogador.sprite.image.set_alpha(255)

    def invencibilidade(self):
        if self.invencivel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_dano >= self.duracao_invencibilidade:
                self.invencivel = False

    def morte(self):
        if self.vida_atual <= 0:
            self.vivo = False

    def tela_morte(self):
        if not self.vivo:
            imagem_game_over = pygame.image.load(
                "./assets/level/gameover/game_over_screen.jpg")
            self.superficie.blit(imagem_game_over, (altura/2, largura/2))

    def UI(self):
        if self.vida_atual == 4:
            vida = pygame.image.load(
                "./assets/level/UI/1.png").convert_alpha()
        elif self.vida_atual == 3:
            vida = pygame.image.load("./assets/level/UI/2.png").convert_alpha()
        elif self.vida_atual == 2:
            vida = pygame.image.load("./assets/level/UI/3.png").convert_alpha()
        elif self.vida_atual == 1:
            vida = pygame.image.load("./assets/level/UI/4.png").convert_alpha()
        else:
            vida = pygame.image.load("./assets/level/UI/5.png").convert_alpha()

        vida_tamanho = pygame.transform.scale(vida, (50, 50))
        self.superficie.blit(vida_tamanho, (5, 5))

    def mostrar_mapa(self):
        '''
        Usado para facilitar e diminuir o código ao mostrar
        os blocos e jogador na tela e executar todos os métodos restantes.
        '''

        # Desenhando o background
        self.background.draw(self.superficie)

        # Desenhando o terreno sólido do mapa e atualizando a posição
        self.terreno_mapa.update(self.movimento)
        self.terreno_mapa.draw(self.superficie)

        # Desenhando as moedas do jogo e atualizando a posição
        self.moedas.update(self.movimento)
        self.moedas.draw(self.superficie)

        # Desenhando os inimigos e atualizando a posição e os limites
        self.inimigos.update(self.movimento)
        self.limites_inimigos.update(self.movimento)
        self.colisao_movimentos_inimigo()
        self.inimigos.draw(self.superficie)

        # Jogador
        self.objetivo.update(self.movimento)
        self.jogador.update()
        self.colisao_horizontal()
        self.colisao_vertical()
        self.movimento_camera()
        self.jogador.draw(self.superficie)
        self.objetivo.draw(self.superficie)
        self.colisao_inimigos()
        self.pegar_moedas()
        self.invencibilidade()
        self.queda()
        self.morte()
        self.efeito_dano()
        self.tela_morte()

        # Objetivos e seleção de fases:
        self.objetivos()
        self.selecionar_fase()

        # Desenhando a interface
        self.UI()
