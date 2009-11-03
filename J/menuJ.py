import pygame

class menuJ(object):
    def __init__(self):
        pygame.init()
        self.image = pygame.image.load('Images/currentSelection.png')
        self.spriterect = self.image.get_rect()
        self.rect = self.spriterect
        screen = pygame.display.set_mode((640,480))
        
    def handleEvent():
        self.y = 10
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.y =+ 10 
                if event.type == pygame.KEYUP:
                    self.y =+ 10
 
    def update(self):
        self.screen.blit(self.image, (50, y), self.rect)
    
    def render(self):
        pygame.display.flip()
    
    
    def run(self):
        pass
    
    
        
if __name__ == "__main__":
    while True:
        menu = menuJ()
        menu.handleEvent()
    