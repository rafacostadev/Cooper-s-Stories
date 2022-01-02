from os import walk
import pygame


def importar_arquivo(caminho):
    '''Importa as imagens para serem usadas na animação do personagem'''
    lista_animacao = []
    for n, m, imagens_animacao in walk(caminho):
        for imagens in imagens_animacao:
            diretorio = caminho + '/' + imagens
            imagem = pygame.image.load(diretorio).convert_alpha()
            lista_animacao.append(imagem)

    return lista_animacao
