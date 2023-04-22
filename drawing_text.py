import pygame

key_conversion = {
    pygame.K_LEFT: "Left",
    pygame.K_RIGHT: "Right",
    pygame.K_UP: "Top",
    pygame.K_DOWN: "Down",
}


def display_travel_directions(next_directions, surface, width, height):
    """
    Determines what direction the player can move at
    each decision point in the came

    Args:
        next_direction: tuple of integers or None
        surface: pygame surface that the game is being displayed on
    """

    # Determining what directions are possible at a point
    directions = []
    if next_directions[0] != None:
        directions.append("Left")
    if next_directions[1] != None:
        directions.append("Right")
    if next_directions[2] != None:
        directions.append("Top")
    if next_directions[3] != None:
        directions.append("Down")
    directions_str = "or".join(directions)

    # Display options within game window
    font = pygame.font.Font("freesansbold.ttf", 20)
    text = font.render(f"Choose {directions_str}", True)
    textRect = text.get_rect()
    textRect.topleft = (width // 2, 4 * height // 5)
    surface.blit(text, textRect)
