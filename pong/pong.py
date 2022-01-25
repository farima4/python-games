from pygame import *
from sys import exit
from random import randint, choice
from pong_path import path, audio_path

from pygame.sprite import RenderUpdates
init()

MAINLOOP = True
side = choice(('left', 'right'))
ver = choice(('up', 'down'))
Vspeed = randint(3, 10)
Hspeed = randint(8, 12)
# ~~~~~~~~~~~~  SCORE
score1, score2 = 0, 0
scoreB = font.Font(None, 80)
scoreR = font.Font(None, 80)
scoreBsurf = scoreB.render(str('0'), True, 'Blue')
scoreRsurf = scoreR.render(str('0'), True, 'Red')

line = Surface((30, 10))
line.fill('purple')

# ~~~~~~~~~~~~~~~~~~~~ AUDIO
mixer.music.load(audio_path + 'background.mp3')
mixer.music.play(-1)
hit_audio = mixer.Sound(audio_path + 'hit.wav')
score_audio = mixer.Sound(audio_path + 'score.wav')

def hit():
    hit_audio.play()

def blueScore():
    global score1
    global scoreBsurf
    score1 += 1
    scoreBsurf = scoreB.render(str(score1), True, 'Blue')


def redScore():
    global score2
    global scoreRsurf
    score2 += 1
    scoreRsurf = scoreR.render(str(score2), True, 'Red')
###########


width = 1100
height = 600

screen = display.set_mode((width, height))
display.set_caption('PONG!')

wall1 = Surface((width, 20))
wall1.fill('purple')
wall1_rect = wall1.get_rect(center=(550, 10))

wall2 = Surface((width, 20))
wall2.fill('purple')
wall2_rect = wall2.get_rect(center=(550, 590))


clock = time.Clock()


class Player(sprite.Sprite):
    def __init__(self, up, down, x, y, sprite):
        super().__init__()
        self.image = image.load(sprite).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

        self.up = up
        self.down = down

    def move(self):
        keys = key.get_pressed()

        if keys[self.up]:
            self.y -= 3
        if keys[self.down]:
            self.y += 3

        self.rect.center = (self.x, self.y)

        if self.rect.bottom > wall2_rect.top:
            self.rect.bottom = wall2_rect.top-1
        if self.rect.top < wall1_rect.bottom:
            self.rect.top = wall1_rect.bottom+1

        self.x = self.rect.center[0]
        self.y = self.rect.center[1]


blue = Player(K_w, K_s, 40, 300, path + 'blue.png')
red = Player(K_UP, K_DOWN, 1060, 300, path + 'red.png')

plyers = sprite.Group()
plyers.add(blue)
plyers.add(red)


class Ball(sprite.Sprite):
    def __init__(self, side, ver, Hspeed, Vspeed):
        super().__init__()
        self.image = image.load(
            path + 'ball.png').convert_alpha()
        self.rect = self.image.get_rect(center=(width / 2, height / 2))
        self.side = side
        self.ver = ver
        self.Hspeed, self.Vspeed = Hspeed, Vspeed

        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

    def move(self):
        # ~~~~~~~~~~~~~~~~~~~~ MOVEMENT
        if self.side == 'right':
            self.x += self.Hspeed
        if self.side == 'left':
            self.x -= self.Hspeed

        if self.ver == 'up':
            self.y -= self.Vspeed
        if self.ver == 'down':
            self.y += self.Vspeed
        # ~~~~~~~~~~~~~~~~~~~~ RESTRICTIONS
        if self.rect.left > width + 200:
            score_audio.play()
            self.image = image.load(path + 'ball.png')
            self.side = choice(('left', 'right'))
            self.ver = choice(('up', 'down'))
            self.Hspeed = randint(3, 10)
            self.Vspeed = randint(3, 10)
            self.x = width / 2
            self.y = height / 2
            blueScore()

        if self.rect.right < -200:
            score_audio.play()
            self.image = image.load(path + 'ball.png')
            self.side = choice(('left', 'right'))
            self.ver = choice(('up', 'down'))
            self.Hspeed = randint(2, 6)
            self.Vspeed = randint(3, 10)
            self.x = width / 2
            self.y = height / 2
            redScore()

        # ~~~~~~~~~~~~~~~~~~~~~~~ COLLISION
        if self.rect.colliderect(wall1_rect):
            hit()
            self.ver = 'down'
        if self.rect.colliderect(wall2_rect):
            hit()
            self.ver = 'up'

        if self.rect.colliderect(blue.rect):
            hit()
            self.side = 'right'
            self.Hspeed = randint(8, 12)
            self.Vspeed = randint(4, 12)
            self.image = image.load(path + 'blueball.png')

        if self.rect.colliderect(red.rect):
            hit()
            self.side = 'left'
            self.Hspeed = randint(8, 12)
            self.Vspeed = randint(4, 12)
            self.image = image.load(path + 'redball.png')

        self.rect.center = (self.x, self.y)


ball = Ball(side, ver, Hspeed, Vspeed)
balls = sprite.Group()
balls.add(ball)

bg = Surface((width, height))


# ~~~~~~~~~~~~~~~~~~~~ MAINLOOP
while MAINLOOP:
    for e in event.get():
        if e.type == QUIT:
            exit()
    screen.blit(bg, (0, 0))

    screen.blit(wall1, wall1_rect)
    screen.blit(wall2, wall2_rect)

    screen.blit(scoreBsurf, (width / 2 - 60, 40))
    screen.blit(scoreRsurf, (width / 2 + 60, 40))
    screen.blit(line, (width / 2, 60))
    # ~~~~~~~~~~~~ PLAYERS
    plyers.draw(screen)
    plyers.update()

    blue.move()
    red.move()

    balls.draw(screen)
    balls.update()

    ball.move()
    # ~~~~~~~~~~~~ PLAYERS

    display.update()
    clock.tick(60)
