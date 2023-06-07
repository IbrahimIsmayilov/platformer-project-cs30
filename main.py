# Platformer Game Portfolio Project by Ibrahim Ismayilov

# IMPORTING MODULES 
# Import pygame
import pygame

# INTIALIZE MODULES OR DIRECTORIES
# Intialize pygame module
pygame.init()

# SET UP PYGAME WINDOW FOR DISPLAY 
# Change pygame window title
pygame.display.set_caption("Platformer Game by Ibrahim Ismayilov")

# Width and height of pygame window stored in variables
WIDTH, HEIGHT = 1500, 1200

# Intialize the pygame window for display
window = pygame.display.set_mode((WIDTH, HEIGHT))

# GLOBAL VARIABLES TO BE ACCESSED LATER
# Create FPS variable to set max FPS of the game to be 60 when run
FPS = 60

# FUNCTIONS
# Main function to contain event handlers and run non-stop while program is open
def main(window):
    # A new clock variable that will be used to track the time and set a framerate
    clock = pygame.time.Clock() 

    # Constant, infinitely running loop
    run = True


