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
        self.viewport = pygame.Surface((640,480))
        self.player = morris.Morris((10, 350), world)
        self.enemy = phantom.Phantom((604, 430), world)
        
        """put the enemies in a group to check for collision later"""
        self.group = pygame.sprite.Group()
        self.group.add(self.enemy)
        
        self.killSound = pygame.mixer.Sound("shoot.wav")
        self.hurtSound = pygame.mixer.Sound("explosion.wav")
        
        self.bckMusic = pygame.mixer.music 
        self.bckMusic.load("countingBodies.ogg")
        self.bckMusic.set_volume(.25)
        self.bckMusic.play()
        
    def update(self):

        #print "player velocity: ", self.player.x_velocity
        if self.player.rect.left >= self.vp.getViewportSize().right - 300:
            self.vp.viewportSize.right = self.player.rect.left + 300
        if self.player.rect.right <= self.vp.getViewportSize().left + 300 and \
        self.player.rect.right - 300 >= 0:
            self.vp.viewportSize.left = self.player.rect.right - 300
        if self.vp.viewportSize.right > 3800:
            self.vp.viewportSize.right = 3800
            
    def render(self):
        #print "vp: ", self.vp.getViewportSize()
        #print self.viewport
        
        self.level.image.blit(self.player.image, self.player.rect,self.player.area)
        self.viewport.blit(self.level.image.subsurface(self.vp.getViewportSize()),(0,0))
        #print "player: ", self.player.rect
        self.screen.blit(self.viewport,self.viewport.get_rect())
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
            
            self.update()
            self.render()
            self.clock.tick(60)
if __name__ == "__main__":
    while True:
        game = Game()
        game.run()
            