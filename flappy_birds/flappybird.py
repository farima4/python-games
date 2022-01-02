from pygame import *
from random import *
from sys import exit

width, height = 480, 720
range = 100, 640
h = randrange(100, 720)
path = 'flappy_birds\\files\\'
animation = [path + 'bird1.png', path + 'bird2.png', path + 'bird3.png']

init()
screen = display.set_mode((width, height))
display.set_caption('flappy birds')
clock = time.Clock()

x = 0
bg = image.load('flappy_birds\\files\\background.png').convert_alpha()
bg_rect = bg.get_rect(center = (x, height / 2))
# ~~~~~~~~
end = font.Font(None, 100) 
endSurf = end.render("You died", True, 'white')
endRect = endSurf.get_rect(center = (width / 2, height / 4))

again = font.Font(None, 45)
againSurf = again.render('press spacebar to play again!', True, 'white')
againRect = againSurf.get_rect(center = (width /2, height /3))

num = 0
score = font.Font(None, 100)
scoreSurf = score.render(f'score: {num}', True, 'white')
scoreRect = scoreSurf.get_rect(center = (width /2, height /2))
# ~~~~~~~~

def background():
    global x
    screen.blit(bg, bg_rect)
    x -= 2
    
    if bg_rect.center[0] < -520:
        x = 0
    bg_rect.center = (x, height / 2)
    
    
counter = 0
gravity = 3

class Bird(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load(animation[1]).convert_alpha()
        self.rect = self.image.get_rect(center = (width / 4, height / 2))
        self.mask = mask.from_surface(self.image)
        self.x, self.y = self.rect.center[0], self.rect.center[1]
        
    def move(self):
        global counter
        global gravity
        global old 
        old = self.y
        for e in event.get():
            if e.type == QUIT:
                exit()
            if e.type == MOUSEBUTTONDOWN:
                counter = 0.1
                
        if counter > 0:
            gravity = -3
            self.y -= 5
            counter -= 0.01
            
        
            


        gravity += 0.5
        self.y += gravity
        
        self.rect.center = (self.x, self.y)
        
        if self.y < old+5:
            self.image = image.load(animation[0]).convert_alpha()
        elif self.y > old-5:
            self.image = image.load(animation[2]).convert_alpha()
        else:
            self.image = image.load(animation[1]).convert_alpha()
            
        
bird = Bird()        
birbs = sprite.Group()
birbs.add(bird)


class Pipe(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load(path + 'pipe.png')
        self.rect = self.image.get_rect(center = (550, h))
        self.mask = mask.from_surface(self.image)
        self.x, self.y = self.rect.center[0], self.rect.center[1]
        self.score = True

    def move(self):
        global num
        global scoreSurf
        global scoreRect
        self.x -= 3
        if self.x < -100:
            self.kill()
            
        if self.x < bird.rect.center[0] and self.score:
            self.score = False
            num += 1
            scoreSurf = score.render(f'score: {num}', True, 'white')
            scoreRect = scoreSurf.get_rect(center = (width /2, height /2))
        
        self.rect.center = (self.x, self.y)
        
        

pipes = sprite.Group()
pipes_group = []

pipeC = 0
def new_pipe():
    return Pipe()

while True:
    

    background()
    
    birbs.draw(screen)
    bird.move()
        
    if pipeC <= 0:
        h = randrange(150, 620)
        pip = new_pipe()
        pipes.add(pip)
        pipes_group.append(pip)
        pipeC = 6
        
    pipeC -= 0.05
    
    
    
    for p in pipes_group:
        p.move()
        
        

        offset = (int(bird.rect.topleft[0]-p.rect.topleft[0]),
                  int(bird.rect.topleft[1]-p.rect.topleft[1]))
        bird.mask = mask.from_surface(bird.image)
        if p.mask.overlap(bird.mask, offset) or bird.rect.top > height or bird.rect.bottom < 0:
            pipes_group.remove(p)
            p.kill()
            go, gravity = 0, -1
            
            bird.y = height / 2 
            bird.move()
            
            timer = 1

            while go != 1:
                for n in event.get():
                    if n.type == QUIT:
                        exit()

                keys = key.get_pressed()
                if keys[K_SPACE]:
                    go = 1
                
                scoreSurf = score.render(f'score: {num}', True, 'white')
                num = 0
                
                screen.blit(endSurf, endRect)
                screen.blit(againSurf, againRect)
                screen.blit(scoreSurf, scoreRect)
                if timer == 1:
                    display.update()
                    timer = 0
                clock.tick(30)
                    
    pipes.draw(screen)
       
    display.update()
    
    clock.tick(60)

