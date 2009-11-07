class State(object):
    """ALL STATES SHOULD INHERIT FROM THIS CLASS"""
 
    def __init__(self, character):
        self.character = character
 
    def run(self):
        self.character.state = self.character.running_state
        return self.character.state.run()
 
    def stand(self):
        self.character.state = self.character.standing_state
        return self.character.state.stand()
    
    def jump(self):
        """add morris's jump sound"""
        self.character.jump_sound.play()
        self.character.y_velocity = self.character.max_y_velocity
        self.character.state = self.character.jumping_state
        return self.character.state.jump()
    
    def fall(self):
        self.character.state = self.character.falling_state
        return self.character.state.fall()
    
    def attack(self):
        """add morris's attack sound"""
        self.character.attack_sound.play()
        self.character.state = self.character.attacking_state
        self.character.attack = True
        return self.character.state.attack()
 
    """cycle through"""
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]            
 
    def __str__(self):
        return "Default state"