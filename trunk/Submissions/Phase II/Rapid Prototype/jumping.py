
import pygame
import state
 
class Jumping(state.State):
    def __init__(self, morris):
        super(Jumping, self).__init__(morris)
        self.right_jumping_frames = ["right"]
        self.left_jumping_frames = ["left"]
        self.frame = 0
 
    """you can only jump in the jump state"""
    def handle_event(self, event):
        return self.jump()
 
    """finish jumping until the jump is over"""
    def no_event(self):
        return self.jump()    
 
    def jump(self):
        if self.character.y_velocity < 0:
            self.character.y_velocity = self.character.y_velocity + 1
            self.character.spriterect.move_ip(self.character.x_velocity, self.character.y_velocity)
        else:
            """once the y velocity reaches 0 ==> switch to falling state"""
            self.character.state = self.character.falling_state
        if self.character.direction == "right":
            return self.get_frame(self.right_jumping_frames)
        else:
            return self.get_frame(self.left_jumping_frames)
        
    def __str__(self):
        return "jumping"