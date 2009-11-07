import pygame
import state
 
class Running(state.State):
    def __init__(self, morris):
        super(Running, self).__init__(morris)
        self.right_running_frames = ["right-run1", "right-run2", "right-run3",
                                     "right-run4", "right-run5", "right-run6"]
        self.left_running_frames = ["left-run1", "left-run2", "left-run3",
                                     "left-run4", "left-run5", "left-run6"]
        self.frame = 0
 
    """events allowed in running state"""
    def handle_event(self, event):
        if event.key == pygame.K_a:
            if self.character.direction == "right":
                self.character.x_velocity = 0
                self.character.direction = "left"
            return self.run()
        elif event.key == pygame.K_d:
            if self.character.direction == "left":
                self.character.x_velocity = 0
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
 
    """set velocity back to 0 and stand"""
    def no_event(self):
        self.character.x_velocity = 0
        return self.stand()    
 
    """manipulate the velocity vars to give the appearance of sliding.
       cycle through the sprites"""
    def run(self):
        if self.character.direction == "left":
            if self.character.x_velocity > -self.character.max_x_velocity:
                self.character.x_velocity -= 1
            self.character.spriterect.move_ip(self.character.x_velocity, 0)
            return self.get_frame(self.left_running_frames)
        else:
            if self.character.x_velocity < self.character.max_x_velocity:
                self.character.x_velocity += 1
            self.character.spriterect.move_ip(self.character.x_velocity, 0)
            return self.get_frame(self.right_running_frames)
 
    def __str__(self):
        return "running"