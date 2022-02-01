from pygame import *
from sys import exit
import os
from cheeseball_path import path, save_path
init()

width, height = 1100, 750
clock = time.Clock()

screen = display.set_mode((width, height))
display.set_caption('cheeseballs lol')

background = image.load(path + 'background.jpg').convert()

cheeseball_surf = image.load(path + 'cheeseballs.png').convert_alpha()
cheeseball_rect = cheeseball_surf.get_rect(center = (width / 2 + 280, height / 2 + 100))

num = 0
score = font.Font(None, 100)
scoreSurf = score.render(f'{num}', True, 'white')
scoreRect = scoreSurf.get_rect(center = (width / 2 + 200, height / 2 - 200))

Upgrades = sprite.Group()
upgrade_list = []

class Upgrade(sprite.Sprite):
    
    def __init__(self,image_name, cost, worth, pos):
        super().__init__()
        self.image = image.load(path + image_name).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.cost = cost
        self.worth = worth
        self.count = 0
        self.text = font.Font(None, 40)
        Upgrades.add(self)
        upgrade_list.append(self)
        
    def show_text(self):
        self.textSurf = self.text.render(f'cost: {self.cost}, {self.worth}/sec, you have: {self.count}', True, 'white')
        self.textRect = self.textSurf.get_rect(left = self.rect.right + 10, bottom = self.rect.center[1] + 10)
        screen.blit(self.textSurf, self.textRect)
        
    def work(self):
        global num
        num = int((self.worth * self.count) + num)
        
        
make_cheeseballs = USEREVENT + 0
time.set_timer(make_cheeseballs, 1000)        

cursor = Upgrade(image_name = 'cursor.png', cost= 10, worth = 1, pos = (50, 50))
farm = Upgrade(image_name = 'farm.png', cost = 100, worth = 3, pos = (50, 140))
walmart = Upgrade(image_name = 'walmart.jpg', cost = 1000, worth = 8, pos = (50, 230))
factory = Upgrade(image_name = 'factory.jpg', cost = 10000, worth = 20, pos = (50, 320))
spaceship = Upgrade(image_name = 'spaceship.jpg', cost = 50000, worth = 30, pos = (50, 410))
netherportal = Upgrade(image_name = 'nether portal.png', cost = 200000, worth = 50, pos = (50, 500))
prism = Upgrade(image_name = 'prism.jpg', cost = 1000000, worth = 100, pos = (50, 590))

line_num = 0
if os.path.isfile(save_path):
    print('works')
    with open(save_path, 'r') as save:
        for line in save:
            
            if line_num == 1:
                cursor.count = int(line)
            elif line_num == 2:
                farm.count = int(line)
            elif line_num == 3:
                walmart.count = int(line)
            elif line_num == 4:
                factory.count = int(line)
            elif line_num == 5:
                spaceship.count = int(line)
            elif line_num == 6:
                netherportal.count = int(line)
            elif line_num == 7:
                prism.count = int(line)
            elif line_num == 8:
                num = int(line)
                
            elif line_num == 9:
                cursor.cost = int(line)
            elif line_num == 10:
                farm.cost = int(line)
            elif line_num == 11:
                walmart.cost = int(line)
            elif line_num == 12:
                factory.cost = int(line)
            elif line_num == 13:
                spaceship.cost = int(line)
            elif line_num == 14:
                netherportal.cost = int(line)
            elif line_num == 15:
                prism.cost = int(line)
            line_num += 1
        line_num = 0
else:
    with open(save_path, 'w') as opening:
        opening.write(' \n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0')


while True:
    for e in event.get():
        if e.type == QUIT:
            with open(save_path, 'w') as saving:
                saving.write(f' \n{cursor.count}\n{farm.count}\n{walmart.count}\n{factory.count}\n{spaceship.count}\n{netherportal.count}\n{prism.count}\n{num}\n{cursor.cost}\n{farm.cost}\n{walmart.cost}\n{factory.cost}\n{spaceship.cost}\n{netherportal.cost}\n{prism.cost}')
            exit()
        if e.type == make_cheeseballs:
            for upgrade in upgrade_list:
                upgrade.work()
        if e.type == MOUSEBUTTONDOWN:
            mouse_pos = mouse.get_pos()
            if cheeseball_rect.collidepoint(mouse_pos):
                num += 1

            else:
                for upgrade in upgrade_list:
                    if upgrade.rect.collidepoint(mouse_pos) and num >= upgrade.cost:
                        upgrade.count += 1
                        num -= upgrade.cost
                        upgrade.cost += upgrade.cost * 0.4
                        upgrade.cost = int(round(upgrade.cost, 0))
           
    screen.blit(background, (0, 0)) 
    screen.blit(cheeseball_surf, cheeseball_rect)
    scoreSurf = score.render(f'{num}', True, 'white')
    scoreRect = scoreSurf.get_rect(center = (width / 2 + 280, height / 2 - 200))
    screen.blit(scoreSurf, scoreRect)
    Upgrades.draw(screen)
    
    for upgrade in upgrade_list:
        upgrade.show_text()

            
    display.update()
    clock.tick(60)
            