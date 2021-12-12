import pygame


class Npc(pygame.sprite.Sprite):
    '''
    Classe que cria tudo relacionado ao NPC(fumante) do primeiro mapa.
    '''

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(
            "./assets/characters/npcs/smoker/idle/Idle_1.png")
        self.rect = self.image.get_rect(midbottom=pos)
