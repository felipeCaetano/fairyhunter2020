"""
Fairy Hunter - Game
Fairy hunter is a shooter game

music by Alexander Ehlers
"""

import sys
import time

import pygame

from game_constants import *
from gameobject import Fairy, Live, Starship, Button, Laser
from images import title, novo_jogo, recordes, ajustes, sobre, sair


pygame.mixer.pre_init()
pygame.init()
pygame.font.init()
pygame.mixer.init()


def _quit_game():
    pygame.quit()
    sys.exit()


class Game:
    """
    Classe que contem o motor do jogo. Dinamicas como criação dos objetos do jogo, inicio do jogo,
    fim do jogo, pausa...
    """
    game_music_player = pygame.mixer.music

    def __init__(self):
        self.display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGTH))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('res/background.png')
        self.fairys = [Fairy(self) for _ in range(INITIAL_FAIRY_COUNT)]
        self.hearts = [Live(self) for _ in range(INITIAL_LIVES)]
        self.starship = Starship(self)
        self.lasers = []
        self.lives = 3
        self.score = 0
        self.score_image = pygame.image.load('res/score.png').convert_alpha()

    def menu_game(self):
        running = True
        self._display_background()
        self._menu_game_blits()
        buttons = self._create_buttons()
        self._menu_game_draw_buttons(buttons)
        while running:
            running = self._menu_handle(buttons, running)
            pygame.display.flip()
        pygame.quit()

    def _menu_game_blits(self):
        self.display_surface.blit(title, (60, 50))
        self.display_surface.blit(novo_jogo, (DISPLAY_WIDTH / 2 - 60 * 2, 180))
        self.display_surface.blit(recordes, (DISPLAY_WIDTH / 2 - 60 * 2, 240))
        self.display_surface.blit(ajustes, (DISPLAY_WIDTH / 2 - 60 * 2, 300))
        self.display_surface.blit(sobre, (DISPLAY_WIDTH / 2 - 60 * 2, 365))
        self.display_surface.blit(sair, (DISPLAY_WIDTH / 2 - 60 * 2, 425))

    def _menu_game_draw_buttons(self, buttons):
        for button in buttons:
            button.draw()

    def _create_buttons(self):
        btn_newgame = Button(self, 'blue', DISPLAY_X_POS, 180, action=self.play)
        btn_hiscore = Button(self, 'yellow', DISPLAY_X_POS, 240)
        btn_credits = Button(self, 'purple', DISPLAY_X_POS, 300)
        btn_config = Button(self, 'green', DISPLAY_X_POS, 360)
        btn_quit = Button(self, 'red', DISPLAY_X_POS, 420, action=_quit_game)
        buttons = [btn_newgame, btn_hiscore, btn_credits, btn_config, btn_quit]
        return buttons

    def _menu_handle(self, buttons, running):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self._get_mouse_over(buttons, event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = self._get_mouse_click(buttons, event, running)
            if event.type == pygame.QUIT:
                running = False
        return running

    def _get_mouse_click(self, buttons, event, running):
        for button in buttons:
            if button.mouse_click(event):
                button.action()
                running = False
        return running

    def _get_mouse_over(self, buttons, event):
        for button in buttons:
            button.mouse_over(event.pos)

    def _check_for_lasercollision(self):
        result = False
        laser_index = None
        fairy_index = None
        for fairy_index, fairy in enumerate(self.fairys):
            for index, laser in enumerate(self.lasers):
                if laser.rect().colliderect(fairy.rect()):
                    result = True
                    break
            if result:
                laser_index = index
                break
        return result, fairy_index, laser_index

    def _check_for_shipcollison(self):
        result = False
        fairy_index = None
        for fairy_index, fairy in enumerate(self.fairys):
            if self.starship.rect().colliderect(fairy.rect()):
                result = True
                break
        return result, fairy_index

    def _pause(self, pause=False):
        game_paused = pause
        pygame.mixer.music.pause()
        while game_paused:
            self._game_msg(PAUSE, BLUE, WHITE)
            game_paused = self._check_pause_state(game_paused)
            pygame.display.update()
        pygame.mixer.music.play()

    def _change_pause_state(self, game_paused):
        if game_paused:
            return False
        return True

    def _check_pause_state(self, game_paused):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_paused = self._change_pause_state(game_paused)
                    break
            if event.type == pygame.QUIT:
                _quit_game()
        return game_paused

    def _display_background(self):
        self._place_lives()
        self._show_score()
        pygame.display.update()
        self.display_surface.blit(self.background, (0, 0))

    def play(self):
        fase1_mus = FASE1_MUSIC
        running = True
        self.game_music_player.load(fase1_mus)
        self.game_music_player.play(-1)
        while running and self.lives >= 0:
            self._display_background()
            self._game_handle()
            self._first_plane_move()
            collision, fairy = self._check_for_shipcollison()
            if collision:
                self._ship_collided(fairy)
            collision, fairy, laser = self._check_for_lasercollision()
            if collision:
                self._fairy_hunted(fairy, laser)
            if len(self.fairys) == 0:
                self.fairys = [Fairy(self) for _ in range(INITIAL_FAIRY_COUNT + 3)]
            self.clock.tick(FRAME_RATE)
        time.sleep(3)

    def _game_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.starship.move_rigth()
                elif event.key == pygame.K_LEFT:
                    self.starship.move_left()
                elif event.key == pygame.K_UP:
                    self.starship.move_up()
                elif event.key == pygame.K_DOWN:
                    self.starship.move_down()
                elif event.key == pygame.K_SPACE:
                    Laser.play_sound()
                    self.lasers.append(
                        Laser(game, self.starship.x - 2 + self.starship.width / 2,
                              self.starship.y))
                elif event.key == pygame.K_p:
                    self._pause(True)
                elif event.key == pygame.K_q:
                    _quit_game()

    def _compute_score(self):
        self.score += 5

    def _show_score(self):
        if pygame.font.get_init():
            text_font1 = pygame.font.Font('res/fonts/prstart.ttf', 28)
            text_font2 = pygame.font.Font('res/fonts/prstart.ttf', 36)
            text_suface1 = text_font1.render('{}'.format(self.score), True, REAL_ORANGE)
            text_suface2 = text_font2.render('{}'.format(self.score), True, (0, 0, 0))
            self.display_surface.blit(
                text_suface2, (DISPLAY_WIDTH - text_font2.size(str(self.score))[0] - 10, 25))
            self.display_surface.blit(
                text_suface1, (DISPLAY_WIDTH - text_font1.size(str(self.score))[0] - 10, 25))
            self.display_surface.blit(self.score_image, (DISPLAY_WIDTH - 333, 0))

    def _fairy_hunted(self, fairy_index, laser_index):
        self.fairys.pop(fairy_index)
        Fairy.play_sound()
        self.lasers.pop(laser_index)
        self._compute_score()

    def _ship_collided(self, fairy_index):
        Starship.play_sound()
        self.fairys.pop(fairy_index)
        self._display_background()  # é chamado aqui para fazer a tela piscar
        if len(self.hearts):
            self.hearts.pop()
        else:
            self._game_msg(GAME_OVER, RED, GREEN)
        pygame.display.update()
        self.lives -= 1

    def _first_plane_move(self):
        self.starship.draw()
        for laser in self.lasers:
            laser.draw()
            laser.move_up()
            if self._check_game_object_in_the_screen(laser):
                self._remove_laser(laser)
        for fada in self.fairys:
            fada.draw()
            fada.move_down()
            if self._check_game_object_in_the_screen(fada):
                self._remove_fairy(fada)

    def _place_lives(self):
        for heart in self.hearts:
            heart.draw()
            if Live.num == len(self.hearts):
                Live.num = 0

    def _game_msg(self, msg, color, bgcolor):
        """
        printa na tela do jogo a mensagem de game paused
        :return: None
        """
        if pygame.font.get_init():
            text_font = pygame.font.Font('res/fonts/Inkfree.ttf', 48)
            text_suface = text_font.render(msg, True, color, bgcolor)
            text_retangle = text_suface.get_rect()
            text_retangle.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGTH / 2)
            self.display_surface.blit(text_suface, text_retangle)

    def _check_game_object_in_the_screen(self, gameobject):
        """
        Check If Fairys On the Screen
        Verifica se ainda há fadas na tela
        :fada: Fairy : Fada a ser verificada
        :return: Boolean
        """
        return gameobject.y > DISPLAY_HEIGTH or gameobject.y < 0

    def _remove_fairy(self, fada):
        self.fairys.pop(self.fairys.index(fada))

    def _remove_laser(self, laser):
        self.lasers.pop(self.lasers.index(laser))


if __name__ == '__main__':
    game = Game()
    game.menu_game()
