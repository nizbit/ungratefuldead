Use Case Descriptions:
  * interacts with friendly NPC
> > Brief Description:
> > > The interacts with friendly NPC use case is an action in the game where the player
> > > approaches and converses with a friendly NPC

> > Step-by-Step Description:
      1. The player approaches the NPC
      1. Dialog between the player and the NPC will occur, if the player chooses to invoke a conversation

  * interacts with enemy NPC
> > Brief Description:
> > > The interacts with enemy NPC use case is an action in the game where the player
> > > controls a character to attack an AI controlled enemy character.

> > Step-by-Step Description:
      1. The player character at minimum has a melee weapon.
      1. An enemy is spotted and the player character is moved to the approximate location of the enemy.
      1. Using the weapon key on the keyboard the player controls the player character to attack the enemy.
      1. If the attack is successful, damage is inflicted to the enemy and the enemy’s hit points are decreased.
      1. If the attack is unsuccessful, no damage is inflicted to the enemy
      1. If the enemy attacks the player character successfully then the player character’s hit points are decreased.
      1. The attack scenario will continue until either the player character's or enemy's hit point values reaches zero. If the player character's hit points reach zero, then the player character dies and starts the level over at the beginning of the level or last checkpoint. If the enemy dies, then the player character kills the NPC and the NPC has the possibility of dropping an item.
  * collect item
> > Brief Description:
> > > The collect item use case is when a player character acquires an item in the game.

> > Step-by-Step Description:
      1. The player finds an item through exploration of the level or by defeating an enemy NPC
      1. The player controls the player character using the keyboard to collect the item.
      1. The item can then be saved for future use.
  * use item
> > Brief Description:
> > > The use item use case enables a player to use an item saved in the player controlled character's inventory or by being used automatically.

> > Step-by-Step Description:
      1. Using a key on the keyboard, the player selects an item, from a list of items, located in the player controlled character’s inventory for immediate use.
      1. When a player controlled character collides with a special item the character receives either a temporary or permanent, favorable or negative condition depending upon the nature of the special item.
  * completes level
> > Brief Description:
> > > The completes level use case is when the player successfully defeats the boss of a level.

> > Step-by-Step Description:
      1. The player kills the boss NPC within a specified time displayed on the screen.

  * fails to complete level
> > Brief Description:
> > > The fails to complete level use case is when the player dies before the completion of a level

> > Step-by-Step Description:
      1. The player runs out of time before killing the boss
      1. The player's hit points drop to zero at any point in the level
      1. The player, due to the environment's topography, falls out of the boundaries of the level

  * controls the character
> > Brief Description:
> > > The controls the character use case enables the player to control the main character on the screen or use an item with the keyboard.

> > Step-by-Step Description:
      1. By using keys, such as the directional keys, the player will cause the main character to jump, move, change direction, use an item, collect an item, attack an NPC, etc.
  * configure settings
> > Brief Description:
> > > The configure settings use case enables the player to change the settings of the game

> > Step-by-Step Description:
      1. The player can adjust the sound level

  * uses menu
> > Brief Description:
> > > The uses menu use case enables the player to access the various sub-menus in the game

> > Step-by-Step Description:
      1. The player can pause the game
      1. The player can access the inventory
      1. The player can exit the game
      1. The player can access the configure settings sub-menu

[Back](Requirements.md)