"""
Fairy Hunter - Game
Fairy hunter is a shooter game

music by Alexander Ehlers
"""

import random
import sys
import time

import pygame
from game_constants import *

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
        pygame.display.set_caption('Fairy Hunter')
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('res/background.png')
        self.fairys = [Fairy(self) for _ in range(INITIAL_FAIRY_COUNT)]
        self.hearts = [Live(self) for _ in range(INITIAL_LIVES)]
        self.starship = Starship(self)
        self.lasers = []
        self.lives = 3
        self.score = 0
        self.score_image = pygame.image.load('res/score.png').convert_alpha()

    def _compute_score(self):
        self.score += 5

    def _show_score(self):
        if pygame.font.get_init():
            text_font1 = pygame.font.Font('res/fonts/prstart.ttf', 28)
            text_font2 = pygame.font.Font('res/fonts/prstart.ttf', 36)
            text_suface1 = text_font1.render('{}'.format(self.score), True, (255, 174, 66))
            text_suface2 = text_font2.render('{}'.format(self.score), True, (0, 0, 0))
            self.display_surface.blit(
                text_suface2, (DISPLAY_WIDTH - text_font2.size(str(self.score))[0] - 10, 25))
            self.display_surface.blit(
                text_suface1, (DISPLAY_WIDTH - text_font1.size(str(self.score))[0] - 10, 25))
            self.display_surface.blit(self.score_image, (DISPLAY_WIDTH - 333, 0))

    def _check_for_lasercollision(self):
        result = False
        for f, fairy in enumerate(self.fairys):
            for l, laser in enumerate(self.lasers):
                if laser.rect().colliderect(fairy.rect()):
                    Fairy.play_sound()
                    self.fairys.pop(f)
                    self.lasers.pop(l)
                    result = True
                    self._compute_score()
                    break
        return result

    def menu_game(self):
        running = True
        self.display_background()
        title = pygame.image.load('res/Title2.png').convert_alpha()
        novo_jogo = pygame.image.load('res/novojogo.png').convert_alpha()
        recordes = pygame.image.load('res/recordes.png').convert_alpha()
        sobre = pygame.image.load('res/sobre.png').convert_alpha()
        ajustes = pygame.image.load('res/ajustes.png').convert_alpha()
        sair = pygame.image.load('res/sair.png').convert_alpha()

        self.display_surface.blit(title, (60, 50))
        self.display_surface.blit(novo_jogo, (DISPLAY_WIDTH / 2 - 60 * 2, 180))
        self.display_surface.blit(recordes, (DISPLAY_WIDTH / 2 - 60 * 2, 240))
        self.display_surface.blit(ajustes, (DISPLAY_WIDTH / 2 - 60 * 2, 300))
        self.display_surface.blit(sobre, (DISPLAY_WIDTH / 2 - 60 * 2, 365))
        self.display_surface.blit(sair, (DISPLAY_WIDTH / 2 - 60 * 2, 425))
        btn_newgame = Button(self, 'blue', DISPLAY_WIDTH / 2 - 60 * 3, 180, action=self.play)
        btn_hiscore = Button(self, 'yellow', DISPLAY_WIDTH / 2 - 60 * 3, 240)
        btn_credits = Button(self, 'purple', DISPLAY_WIDTH / 2 - 60 * 3, 300)
        btn_config = Button(self, 'green', DISPLAY_WIDTH / 2 - 60 * 3, 360)
        btn_quit = Button(self, 'red', DISPLAY_WIDTH / 2 - 60 * 3, 420, action=_quit_game)
        btn_newgame.draw()
        btn_hiscore.draw()
        btn_credits.draw()
        btn_config.draw()
        btn_quit.draw()
        buttons = [btn_newgame, btn_hiscore, btn_credits, btn_config, btn_quit]

        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    for button in buttons:
                        button.mouse_over(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.mouse_click(event):
                            button.action()
                            running = False
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
        pygame.quit()

    def _check_for_shipcollison(self):
        result = False
        for f, fairy in enumerate(self.fairys):
            if self.starship.rect().colliderect(fairy.rect()):
                self.fairys.pop(f)
                result = True
                break
        return result

    def _pause(self):
        game_paused = True
        pygame.mixer.music.pause()
        while game_paused:
            self._game_msg('Pause', BLUE, WHITE)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_paused = False
                        pygame.mixer.music.play()
                        break
                if event.type == pygame.QUIT:
                    _quit_game()
            pygame.display.update()

    def display_background(self):
        self.display_surface.blit(self.background, (0, 0))

    def play(self):
        fase1_mus = 'res/sounds/Twists.mp3'
        running = True
        self.game_music_player.load(fase1_mus)
        self.game_music_player.play(-1)
        while running and self.lives >= 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
                        self._pause()
                    elif event.key == pygame.K_q:
                        _quit_game()
            self.display_background()
            self._show_score()
            self.starship.draw()
            self.starship.rect()
            for heart in self.hearts:
                heart.draw()
                if Live.num == len(self.hearts):
                    Live.num = 0
            for laser in self.lasers:
                laser.draw()
                laser.move_up()
            for fada in self.fairys:
                fada.draw()
                fada.move_down()
            if self._check_for_shipcollison():
                Starship.play_sound()
                self.display_background()
                if len(self.hearts):
                    self.hearts.pop()
                else:
                    self._game_msg('GAME OVER', RED, GREEN)
                pygame.display.update()
                self.lives -= 1
            if self._check_for_lasercollision():
                pygame.display.update()
            pygame.display.update()
            if len(self.fairys) == 0:
                self.fairys = [Fairy(self) for _ in range(INITIAL_FAIRY_COUNT + 3)]
            self.clock.tick(FRAME_RATE)

        pygame.display.update()
        time.sleep(3)
        self.clock.tick(FRAME_RATE)

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


class GameObject:
    """
    Classe pai de todos os objetos do jogo
    """

    def load_image(self, filename):
        self.image = pygame.image.load(filename).convert_alpha()
        self.width = self.image.get_width()
        self.heigth = self.image.get_height()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.heigth)

    def draw(self):
        self.game.display_surface.blit(self.image, (self.x, self.y))


class Button(GameObject):
    colors = {
        'blue': 'res/button_blue.png',
        'green': 'res/button_green.png',
        'grey': 'res/button_grey.png',
        'purple': 'res/button_purple.png',
        'red': 'res/button_red.png',
        'yellow': 'res/button_yellow.png'
    }

    def __init__(self, game, overcolor, x, y, defaultcolor='grey', action=None):
        self.game = game
        self.overcolor = overcolor
        self.defaultcolor = defaultcolor
        self.load_image(self.colors[defaultcolor])
        self.action = action
        self.x = x
        self.y = y

    def change_color(self, color):
        self.load_image(self.colors[color])
        self.draw()

    def mouse_over(self, pos):
        if self.rect().collidepoint(pos):
            self.change_color(self.overcolor)
        else:
            self.change_color(self.defaultcolor)

    def mouse_click(self, event):
        if self.rect().collidepoint(event.pos):
            if event.button.numerator == 1:
                return 1
            else:
                return 0


class Top(GameObject):
    ...


class Laser(GameObject):
    laser_sound = pygame.mixer.Sound('res/sounds/lasersound.wav')

    def __init__(self, game, x, y):
        self.game = game
        self.load_image('res/laserbeam.png')
        self.x = x
        self.y = y

    def move_up(self):
        self.y -= LASERSPEED
        if self.y < 0:
            self.game.lasers.pop(0)

    @classmethod
    def play_sound(cls):
        cls.laser_sound.set_volume(.6)
        cls.laser_sound.play(maxtime=700)


class Fairy(GameObject):
    pop_sound = pygame.mixer.Sound('res/sounds/pop.flac')
    images = ['res/fairy1.png', 'res/fairy2.png', 'res/fairy3.png']

    def __init__(self, game):
        self.game = game
        self.load_image('res/fairy1.png')
        self.x = random.randint(0, DISPLAY_WIDTH - self.width)
        self.y = FAIRY_LOC
        self.speed = random.randint(1, MAX_FAIRY_SPEED)
        self.frame = 0

    @classmethod
    def play_sound(cls):
        cls.pop_sound.set_volume(.5)
        cls.pop_sound.play(maxtime=500)

    def move_down(self):
        self.y += self.speed
        self.frame += 1
        if self.frame > 2:
            self.frame = 0
        self.load_image(self.images[self.frame])
        if self.y > DISPLAY_HEIGTH:
            self.game.fairys.pop(self.game.fairys.index(self))


class Starship(GameObject):
    ship_sound = pygame.mixer.Sound('res/sounds/shipimpact.wav')

    def __init__(self, game):
        self.game = game
        self.x = DISPLAY_WIDTH / 2 - 45
        self.y = DISPLAY_HEIGTH - 88
        self.load_image('res/spaceship.png')

    def move_rigth(self):
        self.x += STARSHIP_SPEED
        if self.x + self.width > DISPLAY_WIDTH:
            self.x = DISPLAY_WIDTH - self.width
        return True

    def move_left(self):
        self.x -= STARSHIP_SPEED
        if self.x < 0:
            self.x = 0
        return True

    def move_up(self):
        self.y -= STARSHIP_SPEED
        if self.y < 50:
            self.y = 50
        return True

    def move_down(self):
        self.y += STARSHIP_SPEED
        if self.y + self.heigth > DISPLAY_HEIGTH:
            self.y = DISPLAY_HEIGTH - self.heigth

    @classmethod
    def play_sound(cls):
        cls.ship_sound.set_volume(.8)
        cls.ship_sound.play(maxtime=700)


class Live(GameObject):
    num = 0

    def __init__(self, game):
        self.game = game
        self.load_image('res/Heart.png')
        self.x = self.width + 5
        self.y = 10

    def draw(self):
        self.x = self.x + Live.num * self.x
        super(Live, self).draw()
        # self.game.display_surface.blit(self.image, (self.x, self.y))
        self.x = self.width + 10
        Live.num += 1


if __name__ == '__main__':
    game = Game()
    game.menu_game()
