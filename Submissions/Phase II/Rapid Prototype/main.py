import pygame
import morris
import phantom
import world
import viewport
import sys
from  pygame.locals import *

class Game(object):
    def __init__(self):
        """init pygame and the sound mixer"""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("Rapid Prototype")
        self.clock = pygame.time.Clock()
        
        """init the world and the characters"""
        self.level = world.World()
        self.vp = viewport.Viewport(pygame.Rect(0,0,640,480))
        #MAY BE OVERKILL
        self.tempvp = pygame.image.load("Images/bck.png")
        self.player = morris.Morris((10, 350), world)
        #self.prevPlayerRect = pygame.Rect()
        self.phantom = phantom.Phantom((604, 430), world)
        self.phantom2 = phantom.Phantom((804, 430), world)
        self.phantom3 = phantom.Phantom((1600, 377), world)
        self.phantom4 = phantom.Phantom((1750, 371), world)
        self.phantom5 = phantom.Phantom((3160, 430), world)
        self.phantom6 = phantom.Phantom((1004, 430), world)
        self.phantom7 = phantom.Phantom((604, 430), world)
        self.phantom8 = phantom.Phantom((804, 430), world)
        self.phantom9 = phantom.Phantom((1004, 430), world)
        self.phantom10 = phantom.Phantom((904, 430), world)
        self.phantom11 = phantom.Phantom((2204, 430), world)
        self.phantom12 = phantom.Phantom((2504, 430), world)
        """put the enemies in a group to check for collision later"""
        self.group = pygame.sprite.Group()
        self.group.add(self.phantom,
                       self.phantom2,
                       self.phantom3,
                       self.phantom4,
                       self.phantom5,
                       self.phantom6,
                       self.phantom7,
                       self.phantom8,
                       self.phantom9,
                       self.phantom10,
                       self.phantom11,
                       self.phantom12)
        self.enemies = [self.phantom,
                       self.phantom2,
                       self.phantom3,
                       self.phantom4,
                       self.phantom5,
                       self.phantom6,
                       self.phantom7,
                       self.phantom8,
                       self.phantom9,
                       self.phantom10,
                       self.phantom11,
                       self.phantom12]
        self.heartSound = pygame.mixer.Sound("Sounds/heart.wav")
        self.hurtSound = pygame.mixer.Sound("Sounds/hit.wav")
        self.killSound = pygame.mixer.Sound("Sounds/killSound.wav")
        self.killSound.set_volume(.25)
        self.bckMusic = pygame.mixer.music 
        self.bckMusic.load("Sounds/music.ogg")
        self.bckMusic.set_volume(.25)
        self.bckMusic.play()
    def handleEnemies(self, event):
        for enemy in self.enemies:
            enemy.handle_event(event)
            enemy.handle_animation()

    def update(self):

        #print "player velocity: ", self.player.x_velocity
        if self.player.rect.left >= self.vp.rect.right - 300:
            self.vp.rect.right = self.player.rect.left + 300
        if self.player.rect.right <= self.vp.rect.left + 300 and \
        self.player.rect.right - 300 >= 0:
            self.vp.rect.left = self.player.rect.right - 300
        if self.vp.rect.right > 3800:
            self.vp.rect.right = 3800
            
    def render(self):
        #print "vp: ", self.vp.getViewportSize()
        #print self.viewport
        self.level.image.blit(self.tempvp,self.vp.rect,self.vp.rect)
        self.level.image.blit(self.player.image,self.player.rect,self.player.area)
        for enemy in self.enemies:
            if enemy != None:
                self.level.image.blit(enemy.image, enemy.rect, enemy.area)
        
        self.screen.blit(self.level.image.subsurface(self.vp.rect),(0,0))        
        if self.enemies == []:
            self.font = pygame.font.Font(None, 100)
            self.text = self.font.render("YOU WIN!!!!!", 1, (255,255,255))
            self.textRect = self.text.get_rect()
            self.textRect.centerx = self.vp.rect.centerx
            self.screen.blit(self.text,(0,0))
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            """loop through the events"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            #print event
            """handle the events and animation"""
            self.player.handle_event(event)
            self.player.handle_animation()
            if self.phantom != None:
                for enemy in self.enemies:
                    if pygame.sprite.collide_rect(self.player, enemy) and \
                    self.player.state == self.player.attacking_state:
                        self.killSound.play()
                        self.enemies.remove(enemy)
                        enemy = None
                    elif pygame.sprite.collide_rect(self.player,enemy):
                        self.player.HP -= 1
                        print "player hp: ", self.player.HP
                else:
                    self.handleEnemies(event)
                    
            self.update()
            self.render()
            self.clock.tick(60)
            
if __name__ == "__main__":
    while True:
        game = Game()
        game.run()
            