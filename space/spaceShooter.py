# ~~~~~~~~~~~~~~ IMPORTS
from time import *
from random import randint
from sys import exit
from space_path import path, audio_path
from pygame import *
from pygame import mixer

# ~~~~~~~~~~~~~~ PYGAME INIT
init()
SW = 600
SH = 750
screen = display.set_mode((SW, SH))
mouse.set_visible(False)

# ~~~~~~~~~~~~~~ OBJECTS
clock = time.Clock()
score = font.Font(None, 40)
Hp = font.Font(None, 40)

# ~~~~~~~~~~~~~~~~~~~~ AUDIO    
mixer.music.load(audio_path + 'background.mp3')
mixer.music.play(-1)
shoot_audio = mixer.Sound(audio_path + 'shoot.wav')
explosion_audio = mixer.Sound(audio_path + 'explosion.wav')
damage_audio = mixer.Sound(audio_path + 'damage.wav')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PLAYER


class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load(
            path + 'spaceShip.png').convert_alpha()
        self.rect = self.image.get_rect(center=(300, 650))
        self.mask = mask.from_surface(self.image)
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

    def move(self):
        self.x = mouse.get_pos()[0]
        self.y = mouse.get_pos()[1]

        if self.x <= 0:
            self.x = 600
        if self.x >= 601:
            self.x = -1

        if self.y > 760:
            self.y = 760
        if self.y < -10:
            self.y = -10

        self.rect.center = (self.x, self.y)

    def shoot(self):
        
        shoot_audio.play()
        return Bullet(self.x, self.y)


ship = Player()
PLgroup = sprite.Group()
PLgroup.add(ship)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ASTEROID


class Asteroid(sprite.Sprite):
    def __init__(self, x1):
        super().__init__()
        self.image = image.load(
            path + 'asteroid.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x1, 5))
        self.mask = mask.from_surface(self.image)
        self.x = self.rect.center[0]
        self.y = self.rect.center[1]

    def update(self):
        self.y += 4
        if self.y > 800:
            self.x = randint(0, SW)
            self.y = -20
        self.rect.center = (self.x, self.y)

    def spawn(self):
        return Asteroid(randint(0, SW))


asteroid = Asteroid(randint(0, SW))
ASgroup = sprite.Group()
ASgroup.add(asteroid)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BULLET


class Bullet(sprite.Sprite):
    def __init__(self, x_, y_):
        super().__init__()
        self.image = Surface((4, 20))
        self.image.fill('yellow')
        self.mask = mask.from_surface(self.image)
        self.x = x_
        self.y = y_
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.rect.y -= 8
        if self.rect.y < -20:
            self.kill()


bullets = sprite.Group()

BUgroup = sprite.Group()

scoreNUM = 0
cd = 1
asteroidHP = 1
playerHP = 5
asteroids = list()
asteroids.append(asteroid)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SURFACES

scoreSurface = score.render('score', True, 'white')
spaceSurface = image.load(path + 'background.png').convert_alpha()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN LOOP
display.set_caption('space man jaximus')
while True:
    # ~~~~~~~~~~~~~~ EVENTS
    for e in event.get():
        if e.type == QUIT:
            exit()
        if e.type == MOUSEBUTTONDOWN and cd < 0:
            cd = 1
            BUgroup.add(ship.shoot())

    # ~~~~~~~~~~~~~~ RENDERING
    screen.blit(spaceSurface, (0, 0))

    ASgroup.draw(screen)
    BUgroup.draw(screen)
    PLgroup.draw(screen)

    # ~~~~~~~~~~~~~~ COLLISIONS
    #offset2 = (int(), int())
    for i in asteroids:
        kills = sprite.spritecollide(i, BUgroup, True)
        for b in kills:
            explosion_audio.play()
            asteroidHP -= 1
            scoreNUM += 1
        if asteroidHP < 1:
            # ASgroup.remove(asteroid)
            # asteroid.kill()
            randAsteroid = i.spawn()
            ASgroup.add(randAsteroid)
            asteroids.append(randAsteroid)
            asteroidHP = 1
    for i in asteroids:
        offset = (int(ship.rect.topleft[0]-i.rect.topleft[0]),
                  int(ship.rect.topleft[1]-i.rect.topleft[1]))
        if asteroid.mask.overlap(ship.mask, offset) and asteroidHP > 0:
            damage_audio.play()
            if len(asteroids) == 1:
                randAsteroid = i.spawn()
                asteroids.remove(i)
                i.kill()
                ASgroup.add(randAsteroid)
                asteroids.append(randAsteroid)
            else:
                asteroids.remove(i)
                i.kill()
            playerHP -= 1
        elif playerHP < 1:
            for i in asteroids:
                ASgroup.remove(i)
                i.kill()
            mouse.set_visible(True)
            while True:
                for e in event.get():
                    if e.type == QUIT:
                        exit()
                screen.fill("black")
                score = font.Font(None, 100)
                screen.blit(spaceSurface, (0, 0))
                scoreSurface = score.render(f'SCORE:{scoreNUM*10}', True, 'white')
                scoreRect.center = (SW / 2 - 100, SH / 2)
                screen.blit(scoreSurface, scoreRect.topleft)
                display.update()
                clock.tick(20)
                

    scoreSurface = score.render(f'SCORE:{scoreNUM*10}', True, 'white')
    screen.blit(scoreSurface, (10, 720))
    scoreRect = scoreSurface.get_rect()
    hpSurface = Hp.render(f'HP:{playerHP}', True, 'white')
    screen.blit(hpSurface, (10, 690))
    ASgroup.update()
    ship.move()
    BUgroup.update()
    cd -= 0.04
    display.update()
    clock.tick(60)
