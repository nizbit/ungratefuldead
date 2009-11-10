******************************************************************************
*   README - PHASE III
******************************************************************************
*
*   The Ungrateful Dead
*   by
*   Kernel Panic
*
******************************************************************************

Objective:
    
    Get the coin at the end of the level with the most points possible. Points
    are gained by killing enemies. Point values are determined by number of
    lives left, as well as the current HP
    
    ***
       EACH LEVEL IS BEATABLE. (Jumps can be tricky, but are possible. They
       actually are very easy, once you know the trick) 
    ***
    
Controls:
    
    1. Left directional key is the left movement key
    2. Right directional key is the right movement key
    3. Left-shift is the attack key
    4. Spacebar is the jump key
    5. Escape will pause the game, bringing up the pause menu
    6. Enter will be the selector button for the menu

Requirements:
    
    1. Refine:
        a. Controls - Changed keystroke detection
        b. Collisions - Implemented a more sophisticated detection algorithm
        c. Camera - No change necessary
    
    2. Menu System
        a. Choose level - Level 1 and 2 options in menu
        b. Can quit the game
        c. Pause menu implemented with ability to quit level
    
    3. Level transitions
        a. Are done through main menu and pause menu
    
    4. Implement Vector2D class
        a. Implemented
        b. Unit testing - complete
        
    5. Previous Requirements still stand
    
        Previous Requirements:

            Three sound effects:
        
                1. Jump sound
                2. Attack sound
                3. Enemy death sound
                4 (extra). Coin sound
    
        One song:
        
            Game background music
            (extra) Main Menu background music
            (extra) Game over music
    
        Reset Level:
        
            Via pause menu, go back to the original menu screen, where you can
            select a level to play
    
        At least one power up:
        
            Coin collected at end will cause the player to beat the level
        
        At least one NPC:
            
            2 different types of enemies.
        
        A way to see how the player is doing:
            
            Score, HP value, and lives are blit to the screen
        
All images and music are the works of others and Kernel Panic does not claim
credit for their work
