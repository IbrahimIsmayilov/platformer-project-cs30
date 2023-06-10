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


# CLASSES
# A parent class for creating all objects in the game, with shared attributes among with containing different values (terrain blocks, etc)
class Objects:
    # Constructor
    def __init__(self, image_folder, image_name, object_name):
        self.image = pygame.image.load(join("Assets", image_folder, image_name))
        self.width = self.image.get_width()
        self.height = self.image.get_width()
        self.coordinate = ()
        self.coordinates = []
        # self.rect = pygame.Rect(self.coordinate.x, self.coordinate.y, self.width, self.height)
        self.object_name = object_name


    # Methods
    def draw(self, win):
        for coordinate in self.coordinates:
            win.blit(self.image, (coordinate))


# Class to get background
class Background(Objects):
    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)

    # Method to get block
    def get_background_block_array(self):
        for i in range(WIDTH // self.width + 1):
            for j in range(HEIGHT // self.height + 1):
                # Put the data in a tuple to have its x and y coordinates be more accessible when appended to the "bg_tiles" array. Put it in a format that can access the x and y values. 
                self.coordinate = i * self.width, j * self.height
                # Append it in a format that can access the x and y values 
                self.coordinates.append(self.coordinate)

# Class to get terrain blocks
class Terrain_Blocks(Objects):
    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)


    # Method to get block coordinates
    def get_terrain_block_array(self):
        for i in range (WIDTH // self.width + 1):
            self.coordinate = i * self.width, HEIGHT - self.height
            self.coordinates.append(self.coordinate)

# Class to draw the player

# FUNCTIONS
# THe main draw function to draw everything for the program or run other smaller drawing functions
def draw(window, background, terrain):

    background.get_background_block_array()
    background.draw(window)

    terrain.get_terrain_block_array()
    terrain.draw(window)

    # Update the display
    pygame.display.update()

    

# Main function to contain event handlers and run non-stop while program is open
# Why pass the window parameter?
def main(window):
    # A new clock variable that will be used to track the time and set a framerate
    clock = pygame.time.Clock() 

    # Array to store all the terrain block coordinates to fill the screen
    background = Background("Backgrounds", "Sky.jpg", "The Background")

    # Store terrain object in this
    terrain = Terrain_Blocks("Terrains", "DirtTerrain.jpg", "The Terrain")

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
        draw(window, background, terrain)

    # Quit pygame if the while loop has been broken
    pygame.quit()
    quit()


# Call main function to start the game
main(window)


