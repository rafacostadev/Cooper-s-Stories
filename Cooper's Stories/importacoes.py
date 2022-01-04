import pygame
from os import walk
from csv import reader
from configs import tamanhoBloco


def importar_arquivo(caminho):
    '''
    Importa as imagens para serem usadas na animação do personagem.
    '''
    lista_animacao = []
    for n, m, imagens_animacao in walk(caminho):
        for imagens in imagens_animacao:
            diretorio = caminho + '/' + imagens
            imagem = pygame.image.load(diretorio).convert_alpha()
            lista_animacao.append(imagem)

    return lista_animacao


def importar_arquivo_csv(caminho):
    '''
    Importa os arquivos CSV para serem usados como base dos blocos.
    '''
    pisos_mapa = []
    with open(caminho) as map:
        level = reader(map, delimiter=",")
        for row in level:
            pisos_mapa.append(list(row))
        return pisos_mapa


def importar_blocos_recortados(caminho):
    '''
    Importa e recorta os blocos para serem desenhados
    baseado no seu código.
    '''
    superficie = pygame.image.load(caminho).convert_alpha()
    bloco_x = int(superficie.get_size()[0]/tamanhoBloco)
    bloco_y = int(superficie.get_size()[1]/tamanhoBloco)

    blocos_recortados = []
    for linha in range(bloco_y):
        for coluna in range(bloco_x):
            x = coluna * tamanhoBloco
            y = linha * tamanhoBloco
            nova_superficie = pygame.Surface((tamanhoBloco, tamanhoBloco))
            nova_superficie.blit(superficie, (0, 0), pygame.Rect(
                x, y, tamanhoBloco, tamanhoBloco))
            blocos_recortados.append(nova_superficie)

    return blocos_recortados
