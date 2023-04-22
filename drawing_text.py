import pygame

key_conversion = {
    pygame.K_LEFT: "Left",
    pygame.K_RIGHT: "Right",
    pygame.K_UP: "Up",
    pygame.K_DOWN: "Down",
}


def display_travel_directions(next_direction, surface, width, height):
    """
    Determines what direction the player can move at
    each decision point in the came

    Args:
        next_direction: tuple of four integers or None
        surface: pygame surface that the game is being displayed on
        width: integer representing the width in pixels of the pygame surface
        height: integer representing the height in pixels of the pygame surface
    """
    next_direction[0] = pygame.K_LEFT
    next_direction[1] = pygame.K_RIGHT
    next_direction[2] = pygame.K_UP
    next_direction[3] = pygame.K_DOWN
    directions = []

    # Determining what directions are possible at a point
    for direction, index in enumerate(next_direction):
        if next_direction[index] != None:
            directions.append(key_conversion[direction])
    directions_str = "or".join(directions)

    # Display options within game window
    font = pygame.font.Font("freesansbold.ttf", 20)
    text = font.render(f"Choose {directions_str}", True)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 5)
    surface.blit(text, textRect)
    return directions
