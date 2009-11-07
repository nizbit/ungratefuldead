import pygame
import morris
import phantom
import world
import sys
from  pygame.locals import *
 
"""init pygame and the sound mixer"""
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("John Morris Test Case")
clock = pygame.time.Clock()
 
"""init the world and the characters"""
world = world.World()
morris = morris.Morris((10, 430), world)
phantom = phantom.Phantom((604, 430), world)

"""put the enemies in a group to check for collision later"""
group = pygame.sprite.Group()
group.add(phantom)

music = pygame.mixer.Sound("music.ogg")
music.play()

vpposition = 0
MAX_X = 575
MIN_X = 545
 
running = True

#sys.setrecursionlimit(sys.getrecursionlimit()*2)
 
while running:
    """loop through the events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    """handle the events and animation"""
    morris.handle_event(event)
    morris.handle_animation()
    
    if ((morris.rect[0] <= MAX_X) and (morris.rect[0] > MIN_X)):
        vpposition += morris.x_velocity
        if vpposition < 0:
            vpposition = 3160
        elif vpposition > 3160:
            vpposition =  0
        
    print morris.rect
    print vpposition
    viewport = world.image.subsurface(abs(vpposition), 0, 640, 480)
    screen.blit(viewport, (0,0))
                  
    """collision detector ==> if the condition evals to true, don't display the phantom anymore"""  
    if phantom != None:
        if pygame.sprite.spritecollideany(morris, group) and morris.attack:
            group.empty()
            phantom = None
        else:
            phantom.handle_event(event)
            phantom.handle_animation()
            screen.blit(phantom.image, phantom.rect, phantom.area)
            
    screen.blit(morris.image, morris.spriterect, morris.area)
 
    pygame.display.flip()
    clock.tick(20)