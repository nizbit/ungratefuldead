import pygame
import state
 
class Standing(state.State):
    def __init__(self, morris):
        super(Standing, self).__init__(morris)
        self.left_stand = "left"
        self.right_stand = "right"
 
    """events allowed in he standing state"""
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.character.direction = "left"
                return self.run()
            elif event.key == pygame.K_RIGHT:
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
        else:
            return self.no_event()  
     
    """set velocity back to 0 just in case"""
    def no_event(self):
        self.character.x_velocity = 0
        return self.stand()
 
    """delineate between left and right stances"""
    def stand(self):
        if self.character.direction == "left":
            return self.left_stand
        else:
            return self.right_stand
 
    def __str__(self):
        return "standing"