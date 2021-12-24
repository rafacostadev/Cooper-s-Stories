from os import walk
import pygame


def importar_arquivo(caminho):
    lista_animacao = []
    for _, __, imagens_animacao in walk(caminho):
        for imagens in imagens_animacao:
            diretorio = caminho + '/' + imagens
            imagem = pygame.image.load(diretorio).convert_alpha()
            lista_animacao.append(imagem)

    return lista_animacao
