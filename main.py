# Platformer Game Portfolio Project by Ibrahim Ismayilov

# IMPORTING MODULES 
# Import pygame
import pygame

# Import "join" and "isfile" methods from os to help with managing files without having to meddle with directories
from os.path import join, isfile


# INTIALIZE MODULES OR DIRECTORIES
# Intialize pygame module
pygame.init()


# SET UP PYGAME WINDOW FOR DISPLAY 
# Change pygame window title
pygame.display.set_caption("Platformer Game by Ibrahim Ismayilov")

# Width and height of pygame window stored in variables
WIDTH, HEIGHT = 1100, 800

# Intialize the pygame window for display
window = pygame.display.set_mode((WIDTH, HEIGHT))


# GLOBAL VARIABLES TO BE ACCESSED LATER
# Create FPS variable to set max FPS of the game to be 60 when run
FPS = 60


# FUNCTIONS
# Function to get a background image and the coordinates to fill the entire screen
def get_background(bg_name):
    # Load background image
    background = pygame.image.load(join("Assets", "Backgrounds", bg_name))
    # Get the background image's width and height
    width = background.get_width()
    height = background.get_height()

    # Array to store coordinates for the position of the background images to fill the entire screen
    bg_tiles = []

    # Get all the coordinates to fill the entire screen with tiles of the background image through for loops that attain that get the value column by column. 
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            # Put the data in a tuple to have its x and y coordinates be more accessible when appended to the "bg_tiles" array. Put it in a format that can access the x and y values. 
            bg_pos = (i * width, j * height)
            # Append it in a format that can access the x and y values 
            bg_tiles.append(bg_pos)

    # Return the array and the loaded background jpg image to be used later
    return bg_tiles, background

# THe main draw function to draw everything for the program or run other smaller drawing functions
def draw(window, bg_array, bg_image):
    # For every coordinate tuple in the array
    for bg_tile in bg_array:
        # Draw it onto the screen and fill the entire screen with it
        window.blit(bg_image, bg_tile)

    # Update the display
    pygame.display.update()

# Main function to contain event handlers and run non-stop while program is open
# Why pass the window parameter?
def main(window):
    # A new clock variable that will be used to track the time and set a framerate
    clock = pygame.time.Clock() 

    # Call the "get_background" function and get the returned values with the coordinates to draw tiles of the background to fill the whole screen
    bg_array, bg_image = get_background("Sky.jpg") 

    # Constant, infinitely running loop
    run = True
    while run:
        # A method to run every frame and make the game run at max 60 FPS on all machines
        clock.tick(FPS)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user closes the program, exit the while loop and quit pygame
                run = False
                break
        
        # Call the draw function every frame to update the screen
        draw(window, bg_array, bg_image)

    # Quit pygame if the while loop has been broken
    pygame.quit()
    quit()


# Call main function to start the game
main(window)


