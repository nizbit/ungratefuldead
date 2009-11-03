import os
import sys
import pygame
from pygame.locals import *

class Viewport(object):
    def __init__(self, rect):
        self.rect = rect
        