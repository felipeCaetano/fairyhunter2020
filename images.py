import pygame

from game_constants import DISPLAY_WIDTH, DISPLAY_HEIGTH

pygame.init()

pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGTH))

title = pygame.image.load('res/Title2.png').convert_alpha()
novo_jogo = pygame.image.load('res/novojogo.png').convert_alpha()
recordes = pygame.image.load('res/recordes.png').convert_alpha()
sobre = pygame.image.load('res/sobre.png').convert_alpha()
ajustes = pygame.image.load('res/ajustes.png').convert_alpha()
sair = pygame.image.load('res/sair.png').convert_alpha()
