import os
import sys
import pygame
from pygame.locals import *

class Viewport(object):
    def __init__(self, rect, character):
        self.rect = rect
        self.character = character
    def update(self):
        if self.character.getRect().left >= self.rect.right - 300 and \
        self.character.getRect().left + 300 <= 3800:
            self.rect.right = self.character.getRect().left + 300
        if self.character.getRect().left <= self.rect.left + 300 and \
        self.character.getRect().left - 300 >= 0:
            self.rect.left = self.character.getRect().left - 300
        if self.rect.right > 3800:
            self.rect.right = 3800
        if self.rect.left < 0:
            self.rect.left = 0