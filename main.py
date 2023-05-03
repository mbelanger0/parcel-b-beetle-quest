"""
Bring together model, view, and controller to implement Parcel B Beetle Quest.
"""
import sys
from ast import literal_eval
import pygame
from character import PlayerCharacter
import scene
import controller


pygame.init()
pygame.display.set_caption("Parcel B: Beetle Quest")

# Define constants related to pygame window
HEIGHT = 500
WIDTH = 800
FPS = 60

# Define player character & related constants
PLAYER_SPRITE_FILEPATH = "data/sprite_data/resting.png"
DEFAULT_PLAYER_HEALTH = 10
player = PlayerCharacter(PLAYER_SPRITE_FILEPATH, DEFAULT_PLAYER_HEALTH)

# Setup pygame clock
FramePerSec = pygame.time.Clock()

# Define surface to draw on and sprites
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
displaysurface.fill((0, 0, 0))

# Define map and scene objects to draw
#
# Additionally, load the scene data associated with these objects into this
# class so the appropriate control methods can be called and scene switches
# can occur.
event_scene = scene.EventScene(displaysurface, player)
event_data = event_scene.scene_data
map_scene = scene.MapScene(displaysurface, player)
map_data = map_scene.scene_data

controls = controller.TextController("data/event_data/events.json")

# Define map starting point
#
# PYLINT DISABLE: This is not a constant, but needs to be defined outside of the
# loop so it isn't reset on every iteration, and this makes pylint mad that it's
# not uppercase, so disabling.
current_map_scene = 0  # pylint: disable=invalid-name

while True:
    # Check if there is a valid event that occurs at this scene. If so, this
    # event should be drawn first.
    #
    # If there is no special event, trying to pull from the event datafile from
    # a blank index will result in an error, at which point the code will
    # continue on.
    #
    # Since events often lead to new events, this loop continues until an error
    # is thrown, representing that you have reached the end of the current event
    # tree.

    try:
        current_event = event_data[map_data[current_map_scene]["SpecialEvent"]][
            "ID"
        ]
        while True:
            event_scene.draw(current_event)
            pygame.display.update()

            # Get the player's input on which decision to make
            (
                new_event_id,
                health_change,
                inventory_change,
                end_message,
                item_check,
            ) = controls.find_result_event(current_event)

            # If a particular event is changed by a the presence of an item in
            # the inventory, then modify the health that is to be removed.
            #
            # This tuple is structured (str, int), where string is the item
            # being searched for in inventory and the int is the difference
            # in the amount of damage done (such that damage done is decreased)
            if item_check is not None:
                if player.in_inventory(item_check[0]):
                    health_change -= item_check[1]

            # Update player state based on event outcome
            if health_change != 0:
                # Update health returns a boolean representing if the character
                # is still alive. If the player has died, display a death
                # screen, potentially with a custom death message
                alive = player.update_health(health_change)
                if not alive:
                    if end_message is not None:
                        event_scene.draw_death_scene(end_message)
                    else:
                        event_scene.draw_death_scene()

                    pygame.display.update()
                    # If the player has died, display the death screen for 10
                    # seconds, then quit the game
                    pygame.time.wait(10000)
                    pygame.quit()
                    sys.exit()

            # If there is a game end message and the player hasn't already died,
            # it is assumed that they won.
            if health_change == 0 and end_message is not None:
                event_scene.draw_win_scene(end_message)
                pygame.display.update()
                # If the player has died, display the death screen for 10
                # seconds, then quit the game
                pygame.time.wait(6000)
                pygame.quit()
                sys.exit()

            # Add/remove items from the inventory
            if inventory_change is not None:
                player.update_inventory(inventory_change)

            # Loop will continue with the next result id
            current_event = new_event_id
            print(current_event)
            FramePerSec.tick(FPS)

    except (KeyError, ValueError, IndexError):
        # If this block is reached, there is no event at the given map point,
        # so the code continues on.

        # Print the map scene and then get the next map location
        map_scene.draw(current_map_scene)
        pygame.display.update()
        current_map_scene = controls.find_result_map(
            literal_eval(map_data[current_map_scene]["DirectionsToMove"])
        )
        current_event = current_map_scene
        print(current_event)
