import pygame
import state
 
class Attacking(state.State):
    def __init__(self, morris):
        super(Attacking, self).__init__(morris)
        
        """these are probably the only thing preventing us from combining all of the 
           characters' states into one class, which would be proper. They will be abstracted 
           out later through some type of dependency injection (inversion of control)"""
        self.right_attacking_frames = ["right-attack1", "right-attack2", "right-attack3",
                                     "right-attack4", "right-attack5", "right-attack6",
                                     "right-attack6", "right-attack6", "right-attack6"]
        self.left_attacking_frames = ["left-attack1", "left-attack2", "left-attack3",
                                     "left-attack4", "left-attack5", "left-attack6",
                                     "left-attack6", "left-attack6", "left-attack6"]
        self.frame = 0
 
    """only check conditions for which the character can perform in the current state"""
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.character.direction = "left"
                return self.run()
            elif event.key == pygame.K_d:
                self.character.direction = "right"
                return self.run()
            elif event.key == pygame.K_SPACE:
                return self.jump()
            elif event.key == pygame.K_j:
                return self.run()
            elif event.key == pygame.K_LSHIFT:
                return self.attack()
            else:
                return self.no_event()
        elif event.type == pygame.KEYUP:
            return self.no_event()
 
    def no_event(self):
        self.character.attack = False
        return self.stand()    
 
    """cycle through attack sprites and utilize the attacking speed"""
    def attack(self):
        #self.character.attack_sound.play()
        if self.character.direction == "left":
            self.character.spriterect.move_ip(-self.character.attacking_speed, 0)
            self.character.rect.topleft = self.character.spriterect.topleft
            return self.get_frame(self.left_attacking_frames)
        else:
            self.character.spriterect.move_ip(self.character.attacking_speed, 0)
            self.character.rect.topleft = self.character.spriterect.topleft
            return self.get_frame(self.right_attacking_frames)
    
    def get_current_frame(self, frame_set):
        return frame_set[self.frame]
 
    def __str__(self):
        return "attacking"