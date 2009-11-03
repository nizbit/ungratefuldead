import pygame
from pygame.locals import *

class menu():
    def __init__(self, name):
        self.image = pygame.image.load(name).convert_alpha()
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font("Images/murder.ttf", 30)
        
    def displayText(self):
        self.title = self.font.render("Ungreatful Dead", 1, (123,30,30))
        self.start = self.font.render("Start game", 1, (123,30,30))
        self.level1 = self.font.render("Level 1", 1, (123,30,30))
        self.level2 = self.font.render("Level 2", 1, (123,30,30))
        self.quit = self.font.render("Quit", 1, (123,30,30))
        self.screen.blit(self.image, (640,480))
        self.screen.blit(self.title, (300,35))
        self.screen.blit(self.start, (25,135))