import os
import sys
import pygame
from pygame.locals import *

class Viewport(object):
    def __init__(self, rect, character, sections, offsetx=300, offsety=150, \
                 boundsx=640, boundsy=480):
        self.rect = rect
        self.startingRect = rect
        self.character = character
        self.offsetx = offsetx
        self.offsety = offsety
        self.xbounds = boundsx
        self.ybounds = boundsy
        temp = pygame.Rect(0, 0, 0, 0)
        self.sections = sections[:]
        self.section = sections[0]
    def update(self):
        
        
        if self.character.rect.left >= self.rect.right - self.offsetx:
            self.rect.right = self.character.rect.left + self.offsetx

        elif self.character.rect.left <= self.rect.left + self.offsetx:
            self.rect.left = self.character.rect.left - self.offsetx
        
        if self.character.rect.top <= self.rect.top + self.offsety:
            self.rect.top = self.character.rect.top - self.offsety
            
        elif self.character.rect.bottom >= self.rect.bottom - self.offsety:
            self.rect.bottom = self.character.rect.bottom + self.offsety
     
            
        if self.rect.right > self.xbounds:
            self.rect.right = self.xbounds
        elif self.rect.left < 0:
            self.rect.left = 0
        
        section = self.determineSection()
        
        if section is not None:
            self.section = section
        
        if self.rect.right > self.section.right:
            self.rect.right = self.section.right
        if self.rect.left < self.section.left:
            self.rect.left = self.section.left
        if self.rect.top < self.section.top:
            self.rect.top = self.section.top
        if self.rect.bottom > self.section.bottom:
            self.rect.bottom = self.section.bottom
        
        if self.rect.bottom > self.ybounds:
            self.rect.bottom = self.ybounds
        elif self.rect.top < 0:
            self.rect.top = 0
        
        
    def determineSection(self):
        cRect = self.character.rect
        for x in range(len(self.sections)):
            if self.sections[x].collidepoint(cRect.centerx, cRect.centery):
                return self.sections[x]
        return None