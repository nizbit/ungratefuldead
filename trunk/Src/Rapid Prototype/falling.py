
import pygame
import state
 
class Falling(state.State):
    def __init__(self, morris):
        super(Falling, self).__init__(morris)
        self.right_falling_frames = ["right"]
        self.left_falling_frames = ["left"]
        self.frame = 0
 
    """keep falling while you're in the falling state"""
    def handle_event(self, event):
        return self.fall()
 
    """fall until you are done falling"""
    def no_event(self):
        return self.fall()    
 
    def fall(self):
        if self.character.y_velocity > self.character.max_y_velocity + 1:
            self.character.y_velocity = self.character.y_velocity - 1
        self.character.spriterect.move_ip(self.character.x_velocity , -self.character.y_velocity)
            
        if self.character.direction == "right":
            return self.get_frame(self.right_falling_frames)
        else:
            return self.get_frame(self.left_falling_frames)

        
    def __str__(self):
        return "falling"