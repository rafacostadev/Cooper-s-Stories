import pygame
from sys import exit
from pygame.constants import K_ESCAPE
from configs import *
from blocos import Bloco, BlocosEstaticos, BlocosAnimados
from personagem_principal import Jogador
from inimigo import Inimigo
from level_config import *
from importacoes import importar_arquivo_csv, importar_blocos_recortados
from background_image import background


class MostrarBlocos():
    '''
    Classe que recebe os atributos para iniciar o mapa completo.
    level = arquivo CSV que vai ser utilizado para mostrar os blocos na tela.
    superficie = a tela em que vai ser mostrada o mapa.
    '''

    def __init__(self, superficie):

        # Importações sons jogo
        self.som_jogo = pygame.mixer.Sound("./assets/level/audio/ingame.wav")
        self.som_jogo.play(loops=-1)
        self.som_jogo.set_volume(0.2)
        self.som_dinheiro = pygame.mixer.Sound(
            "./assets/level/audio/money_collect.mp3")
        self.som_eliminando_inimigo = pygame.mixer.Sound(
            "./assets/level/audio/stomp.wav")
        self.som_game_over = pygame.mixer.Sound(
            "./assets/level/audio/game_over.mp3")
        self.som_vitoria = pygame.mixer.Sound(
            "./assets/level/audio/victory.wav")
        self.som_grito_morte = pygame.mixer.Sound(
            "./assets/level/audio/scream_dead.flac")
        self.som_grito_dano = pygame.mixer.Sound(
            "./assets/level/audio/scream_hurt.flac")

        # Superfície em que vai ser mostrado o jogo
        self.superficie = superficie

        # Movimento da câmera
        self.movimento = 0

        # Status mapa
        self.mapa_atual = level_1
        self.objetivo_do_jogo = False

        # Status jogador
        self.vivo = True
        self.vida_atual = 4
        self.invencivel = False
        self.duracao_invencibilidade = 1200
        self.tempo_dano = 0

        # Jogador
        jogador_layout = importar_arquivo_csv(self.mapa_atual["jogador"])
        self.jogador = pygame.sprite.GroupSingle()
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
        Posiciona o jogador no mapa baseado no arquivo CSV.
        '''
        for index_linha, linhas in enumerate(layout):
            for index_coluna, coluna in enumerate(linhas):
                PosX = index_coluna * tamanhoBloco
                PosY = index_linha * tamanhoBloco
                if coluna == "0":
                    sprite = Jogador((PosX, PosY))
                    self.jogador.add(sprite)

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
        if jogador_x < (largura/3) and direcao_x < 0:
            self.movimento = 6
            jogador.velocidade = 0
        elif jogador_x > largura - (largura/3) and direcao_x > 0:
            self.movimento = -6
            jogador.velocidade = 0
        else:
            self.movimento = 0
            jogador.velocidade = 4

    def colisao_horizontal(self):
        '''
        Adiciona a colisão horizontal entre o
        personagem e os blocos do mapa e adiciona
        os valores de movimento ao personagem ao
        pressionar alguma tecla.
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
        se o jogador está no solo para poder pular e
        adiciona esse de movimento ao personagem.
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
        '''
        Adiciona colisão para pegar moedas
        e faze-las desaparecer do mapa.
        '''
        jogador = self.jogador.sprite
        moedas = self.moedas.sprites()
        for moeda in moedas:
            if moeda.rect.colliderect(jogador.rect):
                self.som_dinheiro.play()
                moeda.kill()

    def colisao_inimigos(self):
        '''
        Adiciona a colisão com os inimigos do jogo 
        para eliminar ou levar dano.
        '''
        jogador = self.jogador.sprite
        inimigos = self.inimigos.sprites()
        for inimigo in inimigos:
            if inimigo.rect.colliderect(jogador.rect) and jogador.direcao.y > 0:
                self.som_eliminando_inimigo.play()
                inimigo.kill()
                jogador.direcao.y = -10
            elif inimigo.rect.colliderect(jogador.rect):
                self.dano()

    def queda(self):
        '''
        Adiciona a morte do jogador ao cair do mapa.
        '''
        jogador = self.jogador.sprite.rect.top
        if jogador >= altura:
            self.vida_atual = 0

    def dano(self):
        '''
        Adiciona o dano ao personagem se
        ele não estiver com frame de invencibilidade.
        '''
        if not self.invencivel:
            self.som_grito_dano.play()
            self.som_grito_dano.set_volume(0.3)
            self.invencivel = True
            self.vida_atual -= 1
            self.tempo_dano = pygame.time.get_ticks()

    def invencibilidade(self):
        '''
        Adiciona o frame de invulnerabilidade
        ao levar dano de inimigos.
        '''
        if self.invencivel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_dano >= self.duracao_invencibilidade:
                self.invencivel = False

    def objetivos_jogo(self):
        '''
        Adiciona o objetivo do jogo que é
        coletar as moedas.
        '''
        if len(self.moedas) == 0:
            self.objetivo_do_jogo = True
            self.som_jogo.set_volume(0)
            self.som_vitoria.play()

    def tela_vitoria(self):
        '''
        Método que mostra a tela de vitória
        e permite o jogador apertar ESC para
        sair do jogo.
        '''
        imagem = pygame.image.load(
            "./assets/level/win/win_image.jpg").convert_alpha()
        imagem = pygame.transform.scale(imagem, (largura, altura))
        self.superficie.blit(imagem, (0, 0))

        if self.objetivo_do_jogo:
            input = pygame.key.get_pressed()
            if input[K_ESCAPE]:
                pygame.quit()
                exit()

    def morte(self):
        '''
        Verifica a vida do personagem para atualizar
        o status de vivo ou morto e adicionar a música
        de game over e o grito de morte.
        '''
        if self.vida_atual <= 0:
            self.vivo = False
            self.som_game_over.play()
            self.som_jogo.set_volume(0)
            self.som_grito_morte.play()

    def tela_morte(self):
        '''
        Método que mostra a tela de morte
        se o status for esse.
        '''
        imagem_game_over = pygame.image.load(
            "./assets/level/gameover/game_over_screen.jpg")
        imagem_game_over = pygame.transform.scale(
            imagem_game_over, (largura, altura))

        if not self.vivo:
            self.superficie.blit(imagem_game_over, (0, 0))
            input = pygame.key.get_pressed()
            if input[K_ESCAPE]:
                pygame.quit()
                exit()

    def UI(self):
        '''
        Carrega as imagens de vida do personagem
        e atualiza elas em relação a quantidade
        de vida do mesmo.
        '''
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

        if self.vivo:
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
            self.jogador.update()
            self.colisao_horizontal()
            self.colisao_vertical()
            self.movimento_camera()
            self.jogador.draw(self.superficie)
            self.colisao_inimigos()
            self.pegar_moedas()
            self.invencibilidade()

            # Desenhando a interface
            self.UI()

            # Checando estados do jogo
            self.queda()
            self.morte()
            self.objetivos_jogo()

        if self.objetivo_do_jogo:
            self.tela_vitoria()

        # Desenhando a tela de morte
        else:
            self.tela_morte()
