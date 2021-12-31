from pygame import *
from random import *
from sys import exit

init()

width, height = 1320, 700

screen = display.set_mode((width, height))
display.set_caption('DVD screensaver :)')

clock = time.Clock()

colors = ['DVD\\files\\blue.png', 'DVD\\files\\cyan.png',
          'DVD\\files\\darkblue.png', 'DVD\\files\\green.png',
          'DVD\\files\\lime.png', 'DVD\\files\\orange.png',
          'DVD\\files\\pink.png', 'DVD\\files\\purple.png',
          'DVD\\files\\red.png', 'DVD\\files\\yellow.png']



class DVD(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image.load(choice(colors)).convert_alpha()
        self.rect = self.image.get_rect(center = (width / 2, height / 2))
        self.x, self.y = self.rect.center[0], self.rect.center[1]
        self.ver = choice(('up', 'down'))
        self.hor = choice(('left', 'right'))
        
    def move(self):
        if self.hor =='left':
            self.x -= 3
        if self.hor =='right':
            self.x += 3
                 
        if self.ver =='up':
            self.y -= 3
        if self.ver =='down':
            self.y += 3
            
        self.rect.center = (self.x, self.y)
        
        # ~~~~~~~~~~ RESTRICTIONS
        
        if self.rect.top < 0:
            old = self.image
            while self.image == old:
                self.image = image.load(choice(colors))
            self.ver = 'down'
        if self.rect.bottom > height:
            old = self.image
            while self.image == old:
                self.image = image.load(choice(colors))
            self.ver = 'up'
            
        if self.rect.left < 0:
            old = self.image
            while self.image == old:
                self.image = image.load(choice(colors))
            self.hor = 'right'
        if self.rect.right > width:
            old = self.image
            while self.image == old:
                self.image = image.load(choice(colors))
            self.hor = 'left'
        
logo = DVD()    
dvdg = sprite.Group()
dvdg.add(logo)

bg = Surface((width, height))
bg.fill('black')
     
 
     
       
while True:
    for e in event.get():
        if e.type == QUIT:
            exit()
            
    screen.blit(bg, (0, 0))
            
    dvdg.draw(screen)
    logo.move()
        
    display.update()
    clock.tick(60)
            
        
        