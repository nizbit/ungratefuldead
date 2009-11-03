import pygame
import runningphantom
 
"""essentially the same as the main character, morris, class. Except the handle_event is AI"""
class Phantom(pygame.sprite.Sprite):
    def __init__(self, position, world):
        pygame.sprite.Sprite.__init__(self)
        self.world = world
 
        self.image = pygame.image.load('Images/enemies1.png')
        self.spriterect = self.image.get_rect()
        self.rect = self.spriterect
        self.actions = {"left-run1": (362, 20, 30, 41),
                        "left-run2": (396, 20, 32, 41),
                        "left-run3": (430, 20, 30, 41),
                        "left-run4": (463, 20, 28, 41),
                        "left-run5": (507, 20, 30, 41),
                        "left-run6": (541, 20, 30, 41),
                        "left-run7": (575, 20, 30, 41),
                        "left-run8": (610, 20, 30, 41)}
 
        self.action = "left-run1"
        self.area = pygame.rect.Rect(self.actions[self.action])
        self.spriterect.topleft = position
        self.rect.topleft = self.spriterect.topleft
        self.rect.w = self.area.w
        self.rect.h = self.area.h
        
        self.attack = False
        self.running_state = runningphantom.Runningphantom(self)
        self.walking_state = runningphantom.Runningphantom(self)
        self.state = self.running_state
 
        self.direction = "left"
        self.displaced = 0
        self.running_speed = 4
 
    def handle_event(self, event):
        """AI: no condition"""
        self.action = self.state.handle_event(event)       
 
    def handle_animation(self):
        self.check_bounds()
        self.area = pygame.rect.Rect(self.actions[self.action])
        self.rect.w = self.area.w
        self.rect.h = self.area.h
 
    def check_bounds(self):
        if self.rect.x < -10:
            self.rect.x = 3790                  
 
        if self.rect.x > 3790:
            self.rect.x = -5
 
        if self.rect.y > 504:
            self.rect.y = 0