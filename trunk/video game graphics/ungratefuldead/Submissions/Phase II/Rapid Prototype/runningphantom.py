import pygame
import state
 
class Runningphantom(state.State):
    def __init__(self, phantom):
        super(Runningphantom, self).__init__(phantom)
        
        """running phantom sprites"""
        self.left_running_frames = ["left-run1", "left-run2", "left-run3", "left-run4",
                                     "left-run5", "left-run6", "left-run7", "left-run8"]
        self.frame = 0
 
    """all the phantom does is run"""
    def handle_event(self, event):
        return self.run()
 
    """there will never be a no_event() with the phantom, but saved for later use"""
    def no_event(self):
        return self.stand()    
 
    def run(self):
        if self.character.direction == "left":
            if self.character.displaced < 20:
                self.character.spriterect.move_ip(-self.character.running_speed, 0)
                self.character.displaced += 1
            else:
                self.character.direction = "right"
                self.character.displaced = 0
                self.character.spriterect.move_ip(-self.character.running_speed, 0)
        else:
            if self.character.displaced < 20:
                self.character.spriterect.move_ip(self.character.running_speed, 0)
                self.character.displaced += 1
            else:
                self.character.direction = "left"
                self.character.displaced = 0
                self.character.spriterect.move_ip(self.character.running_speed, 0)
            
        self.character.rect.topleft = self.character.spriterect.topleft
        return self.get_frame(self.left_running_frames)
 
    def __str__(self):
        return "runningphantom"