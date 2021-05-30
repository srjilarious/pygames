# Simple pygame program
import pygame
import math

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

ScreenWidth = 800
ScreenHeight = 600

running = True
player_x = 250 
player_y = 250

def update_game():
    global player_x, player_y, running
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_UP]:
        player_y = max(-2*ScreenHeight, player_y - 1)
    if pressed_keys[K_DOWN]:
        player_y = min(player_y + 1,  2*ScreenHeight)
    if pressed_keys[K_LEFT]:
        player_x = max(-2*ScreenHeight, player_x - 1)
    if pressed_keys[K_RIGHT]:
        player_x = min(player_x + 1, 2*ScreenHeight)
    if pressed_keys[K_RETURN]:
        player_x = 250
        player_y = 250
    if pressed_keys[K_ESCAPE]:
        running = False

def render(screen):
    # Fill the background with white
    screen.fill((0,0,0))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (player_x, player_y), 50)

    # Flip the display
    pygame.display.flip()

if __name__ == "__main__":
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([ScreenWidth, ScreenHeight])

    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_game()
        render(screen)

    # Done! Time to quit.
    pygame.quit()