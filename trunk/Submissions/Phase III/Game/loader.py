import sys
import pygame
from pygame import *

import vector2d

class Loader(object):
    def __init__(self):
        self.platforms = []
        self.enemyBounds = [] 
    
    def loadLevel(self, fileName):
        try:
            levelFile = open(fileName, 'r')
        except IOError:
            print "Can't find file"
            sys.exit()
            
        fileInfo = levelFile.read()
        levelFile.close()
        p = fileInfo.find("Platforms")
        e = fileInfo.find("EnemyBounds")
        i = fileInfo.find("Image")
        
        temp = fileInfo[p:e].splitlines()
        temp.pop(0)
        self.loadPlatforms(temp)
        
        temp = fileInfo[e:i].splitlines()
        temp.pop(0)
        self.loadEnemyBounds(temp)
        
        temp = fileInfo[i:].splitlines()
        temp.pop(0)
        
        return [self.platforms,self.enemyBounds,self.loadImage(temp)]
        
    
    def loadPlatforms(self, platList):

        for y in platList:
            if y == "":
                continue
            x = y.split()
            self.platforms.append(pygame.Rect(int(x[0]), int(x[1]), \
                                              int(x[2]), int(x[3])))
            
    def loadEnemyBounds(self, bounds):
                    
        for y in bounds:
            if y == "":
                continue
            x = y.split()
            self.enemyBounds.append(pygame.Rect(int(x[0]), int(x[1]), \
                                                int(x[2]), int(x[3])))
    
    def loadImage(self, name):
        for x in name:
            if x == "":
                continue
            return x
    
    def loadPlayer(self, fileName):
        try:
            levelFile = open(fileName, 'r')
        except IOError:
            print "Can't find file"
            sys.exit()
            
        fileInfo = levelFile.read()
        
        a = fileInfo.find("Actions")
        v = fileInfo.find("Velocity")
        ss = fileInfo.find("SpriteSheet")
        p = fileInfo.find("Position")
        
        temp = fileInfo[a:v].splitlines()
        temp.pop(0)
        actions = self.loadPlayerActions(temp)
        
        temp = fileInfo[v:ss].splitlines()
        temp.pop(0)
        velocity = self.loadPlayerVelocity(temp[0].split())
        
        temp = fileInfo[ss:p].splitlines()
        spriteSheet = temp[1]
        
        temp = fileInfo[ss:].splitlines()
        temp.pop(0)
        temp = temp[0].split()
        position = [temp[0], temp[1]]
        return [actions, velocity, spriteSheet, position]
        
    def loadPlayerActions(self, alist):
        actions = {}
        while alist != []:
            key = alist.pop(0)
            temp = {}
            while alist[0] != ";":
                l = alist.pop(0).split()
                t = [l[0]]
                for x in l[1:]:
                    t.append(int(x))
                print t
                temp[t[0]] = pygame.Rect(t[1],t[2],t[3],t[4])
            actions[key] = temp
            alist.pop(0)
        return actions
    def loadPlayerVelocity(self, alist):
        return vector2d.Vector2D(int(alist[0]), int(alist[1]))
 
if __name__ == "__main__":
    
    test = Loader()
    print test.loadPlayer("Files/player.plr")
    