"""
Modulo dos objetos do jogo
Todos os objetos são derivados da classe GameObject para comportamentos comuns

"""
import random

import pygame

from game_constants import STARSHIP_SPEED, DISPLAY_WIDTH, DISPLAY_HEIGTH, FAIRY_LOC, \
    MAX_FAIRY_SPEED, LASERSPEED, MIN_FAIRY_SPEED

pygame.init()


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
        self.load_image(Button.colors[defaultcolor])
        self.action = action
        self.x = x
        self.y = y

    def change_color(self, color):
        self.load_image(Button.colors[color])
        self.draw()

    def mouse_over(self, pos):
        if self.rect().collidepoint(pos):
            self.change_color(self.overcolor)
        else:
            self.change_color(self.defaultcolor)

    def mouse_click(self, event):
        if self.rect().collidepoint(event.pos):
            if event.button.numerator == 1:
                return True
            else:
                return False


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

    @classmethod
    def play_sound(cls):
        cls.laser_sound.set_volume(.7)
        cls.laser_sound.play(maxtime=700)


class Fairy(GameObject):
    pop_sound = pygame.mixer.Sound('res/sounds/pop.flac')
    images = ['res/fairy1.png', 'res/fairy2.png', 'res/fairy3.png']

    def __init__(self, game):
        self.game = game
        self.load_image('res/fairy1.png')
        self.x = random.randint(0, DISPLAY_WIDTH - self.width)
        self.y = FAIRY_LOC
        self.speed = random.randint(MIN_FAIRY_SPEED, MAX_FAIRY_SPEED)
        self.frame = 0

    @classmethod
    def play_sound(cls):
        cls.pop_sound.set_volume(.3)
        cls.pop_sound.play()

    def move_down(self):
        self.y += self.speed
        self.frame += 1
        if self.frame > 2:
            self.frame = 0
        self.load_image(self.images[self.frame])


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
        self.x = self.width + 10
        Live.num += 1

