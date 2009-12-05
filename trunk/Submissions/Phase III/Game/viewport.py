import os
import sys
import pygame
from pygame.locals import *

class Viewport(object):
    def __init__(self, rect, character, offsetx=300, offsety=150, \
                 boundsx=640, boundsy=480):
        self.rect = rect
        self.character = character
        self.offsetx = offsetx
        self.offsety = offsety
        self.xbounds = boundsx
        self.ybounds = boundsy
        
    def update(self):
        if self.character.getRect().left >= self.rect.right - self.offsetx:
            self.rect.right = self.character.getRect().left + self.offsetx
            
        elif self.character.getRect().left <= self.rect.left + self.offsetx:
            self.rect.left = self.character.getRect().left - self.offsetx
        
        if self.character.getRect().top <= self.rect.top + self.offsety:
            self.rect.top = self.character.getRect().top - self.offsety
            
        elif self.character.getRect().bottom >= self.rect.bottom - self.offsety:
            self.rect.bottom = self.character.getRect().bottom + self.offsety
            
        if self.rect.right > self.xbounds:
            self.rect.right = self.xbounds
        elif self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.bottom > self.ybounds:
            self.rect.bottom = self.ybounds
        elif self.rect.top < 0:
            self.rect.top = 0
        