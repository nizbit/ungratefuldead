import pygame
"""from states import walking, running, jumping, falling, standing"""
import running
import standing
import attacking
import jumping
import falling
 
class Morris(pygame.sprite.Sprite):
    def __init__(self, position, world):
        """call base"""
        pygame.sprite.Sprite.__init__(self)
        self.world = world
 
        """load John Morris' sprite sheet"""
        self.image = pygame.image.load('johnmorris.png')
        self.spriterect = self.image.get_rect()
        
        """set max velocities for x and y directions"""
        self.y_velocity = 0
        self.max_y_velocity = -13
        self.x_velocity = 0
        self.max_x_velocity = 6    
            
        """rectangle to be used in collision detection"""
        self.rect = self.spriterect
        
        """get jump sound mixer object"""
        self.jump_sound = pygame.mixer.Sound("jump.wav")
        
        """get attack sound mixer object"""
        self.attack_sound = pygame.mixer.Sound("attack.wav")
        
        """areas on sprite sheet"""
        self.actions = {"right": (15, 15, 35, 45),
                        "left": (265, 20, 35, 45),
                        "right-run1": (15, 70, 35, 45),
                        "right-run2": (60, 70, 35, 45),
                        "right-run3": (100, 70, 35, 45),
                        "right-run4": (135, 70, 35, 45),
                        "right-run5": (175, 70, 35, 45),
                        "right-run6": (225, 70, 35, 45),
                        "left-run1": (265, 70, 26, 45),
                        "left-run2": (298, 70, 26, 45),
                        "left-run3": (330, 70, 26, 45),
                        "left-run4": (360, 70, 26, 45),
                        "left-run5": (395, 59, 26, 45),
                        "left-run6": (433, 59, 32, 45),
                        "right-attack1": (15, 130, 22, 45),
                        "right-attack2": (52, 130, 44, 45),
                        "right-attack3": (100, 130, 50, 45),
                        "right-attack4": (160, 130, 67, 45),
                        "right-attack5": (238, 130, 42, 45),
                        "right-attack6": (295, 130, 76, 45),
                        "left-attack1": (577, 73, 22, 45),
                        "left-attack2": (526, 62, 44, 45),
                        "left-attack3": (471, 62, 50, 45),
                        "left-attack4": (508, 121, 67, 45),
                        "left-attack5": (459, 120, 42, 45),
                        "left-attack6": (377, 127, 76, 45), }
        
        self.attack = False
 
        """first state will be standing, facing right"""
        self.action = "right"
        self.area = pygame.rect.Rect(self.actions[self.action])
        self.spriterect.topleft = position
        self.rect.topleft = self.spriterect.topleft
        self.rect.w = self.area.w
        self.rect.h = self.area.h
        
        """init. internal states"""
        self.running_state = running.Running(self)
        self.walking_state = running.Running(self)
        self.standing_state = standing.Standing(self)
        self.attacking_state = attacking.Attacking(self)
        self.jumping_state = jumping.Jumping(self)
        self.falling_state = falling.Falling(self)
        self.state = self.standing_state
 
        self.direction = "right"

        """how fast the char can attack"""
        self.attacking_speed = 1
 
    """just calls the states handel_event, otherwise no_event"""
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.action = self.state.handle_event(event)
        else:
            self.action = self.state.no_event()        
 
    """the height and width of the rect object were simply the height and
       width of the entire sprite sheet. Needed to change it to be the height
       and width of the sprite itself so we could utilize the sprite classes
       collide functions"""
    def handle_animation(self):
        self.check_bounds()
        self.area = pygame.rect.Rect(self.actions[self.action])
        self.rect.w = self.area.w
        self.rect.h = self.area.h
        
    """*Doug ===> this is probably apart of your class*"""
    def check_bounds(self):
        if self.spriterect.x < 12:
            self.spriterect.x = 12                  
 
        if self.spriterect.x > 575:
            self.spriterect.x = 575
 
        if self.spriterect.y > 504:
            self.spriterect.y = 0