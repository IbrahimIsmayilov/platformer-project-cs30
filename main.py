# Platformer Game Portfolio Project by Ibrahim Ismayilov

# IMPORTING MODULES 
# Import pygame
import pygame

# Import "join" method from os to help with saving images in variables
from os.path import join, isfile
from pygame._sdl2 import Window


# INTIALIZE MODULES OR DIRECTORIES
# Intialize pygame module
pygame.init()


# SET UP PYGAME WINDOW FOR DISPLAY 
# Change pygame window title
pygame.display.set_caption("Platformer Game by Ibrahim Ismayilov")

# Width and height of pygame window stored in variables
WIDTH, HEIGHT = 1200, 600

# Intialize the pygame window for display
window = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas_rect = pygame.Rect(0, 0, canvas.get_width(), canvas.get_height())

# Create FPS variable to set max FPS of the game to be 60 when run
FPS = 60


# CLASSES
# A parent class for to serve as a base class when drawing all objects in the game, including characters, terrain blocks, the background tiles and etc
class Objects():
    # Constructor
    def __init__(self, image_folder, image_name, object_name):
        self.image = pygame.image.load(join("Assets", image_folder, image_name)).convert()
        self.width = self.image.get_width()
        self.height = self.image.get_width()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.coordinates = []
        self.object_name = object_name
        self.level = 1


    # Methods
    # Function to draw the object's image with the correct coordinates on the screen
    def draw(self, win, canvas, offset_x):
        for coordinate in self.coordinates:
            canvas.blit(self.image, (coordinate[0], coordinate[1]))
            win.blit(canvas, (0 - offset_x, 0))

# Child class to get acquire all of the intialized attributes from the "Objects" Parent class but add its additional methods for drawing the background
class Background(Objects):
    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)

    # Methods
    def get_background_block_array(self):
        for i in range(WIDTH // self.width + 1):
            for j in range(HEIGHT // self.height + 1):
                # Put the data in a tuple to have its x and y coordinates be more accessible when appended to the "bg_tiles" array. Put it in a format that can access the x and y values. 
                self.rect.x, self.rect.y = i * self.width, j * self.height
                # Append it in a format that can access the x and y values 
                # Why does the offset.x work here?  
                self.coordinates.append((self.rect.x, self.rect.y, self.rect.width, self.rect.height))

# # Child class to get acquire all of the intialized attributes from the "Objects" Parent class but add its additional methods for drawing the terrain blocks
class Terrain_Blocks(Objects):
    def __init__(self, image_folder, image_name, object_name): 
        super().__init__(image_folder, image_name, object_name)

    def get_level(self):
        if self.level == 1:
            self.get_level_1_terrain()
        elif self.level == 2:
            self.get_level_2_map()
        elif self.level == 3:
            self.get_level_3_map()

    def get_level_1_terrain(self):
        self.level_1_map = [(350, HEIGHT - self.height * 3, self.width, self.height), (350 + self.width, HEIGHT - self.height * 3, self.width, self.height), (700, HEIGHT - self.height * 2, self.width, self.height), (700, HEIGHT - self.height * 3, self.width, self.height), (700 + self.width, HEIGHT - self.height * 4, self.width, self.height), (700 + self.width * 2, HEIGHT - self.height * 4, self.width, self.height), (700 + self.width * 3, HEIGHT- self.height * 3, self.width, self.height), (700 + self.width * 3, HEIGHT - self.height * 2, self.width, self.height), (1800, HEIGHT - self.height * 2, self.width, self.height), (1800 + self.width, HEIGHT - self.height * 3, self.width, self.height), (1800 + self.width * 2, HEIGHT - self.height * 4, self.width, self.height), (1800 + self.width * 3, HEIGHT - self.height * 5, self.width, self.height)]
        self.coordinates.extend(self.level_1_map)

    # Method to get block coordinates
    def get_terrain_floor_array(self):
        for i in range (-WIDTH // self.width * 2, WIDTH // self.width * 2):
            self.rect.x, self.rect.y = i * self.width, HEIGHT - self.height
            self.coordinates.append((self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        
        
# Class to draw the player
class Player(Objects):
    GRAVITY = 1   

    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)
        self.xVel = 0
        self.yVel = 0
        self.rect = pygame.Rect(230, 50, self.width, self.height)
        self.direction = "Right"
        self.jump_count = 0
        self.fall_count = 0
        self.collided_objects = []

    # Methods
    def move(self, x_vel):
        self.xVel = x_vel
        self.rect.x += self.xVel

    def gravity(self):
        self.yVel += min(1, self.fall_count / FPS * 3)
        self.rect.y += self.yVel
        self.fall_count += 1

    def jump(self):
        self.yVel = -self.GRAVITY * 12
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def landed(self):
        self.jump_count = 0
        self.fall_count = 0
        self.yVel = 0
    
    def hit_head(self):
        self.count = 0
        self.yVel *= -1

    def handle_horizontal_collision(self, objects):
        for obj in objects:
            obj = pygame.Rect(obj)
            if self.xVel > 0:    
                if self.rect.topRight + self.xVel > obj.rect.topleft - 2:
                    self.xVel = 0
            if self.xVel < 0:
                if self.rect.topleft + self.xVel > obj.rect.TopRight + 2:
                    self.xVel = 0
                    
    def handle_vertical_collision(self, objects):
        for obj in objects:
            obj = pygame.Rect(obj)
            if self.rect.colliderect(obj):
                if self.yVel > 0:
                   self.rect.bottom = obj.top
                   self.landed()
                if self.yVel < 0:
                    self.rect.top = obj.bottom
                    self.hit_head()
                self.collided_objects.append(obj)


    def handle_movement(self, objects):
        # self.handle_horizontal_collision(objects)
        self.gravity()
        self.handle_vertical_collision(objects)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-3)
        if keys[pygame.K_RIGHT]:
            self.move(3)
        
        self.coordinates = [(self.rect.x, self.rect.y, self.rect.width, self.rect.height)]


# FUNCTIONS
# THe main draw function to draw everything for the program or run other smaller drawing functions
def draw(window, background, terrain, player, canvas, offset_x, objects):

    window.fill((255, 255, 255))

    if offset_x > WIDTH:
        background.get_background_block_array()

    
    background.draw(window, canvas, offset_x)

    terrain.draw(window, canvas, offset_x)

    player.handle_movement(objects)
    player.draw(window, canvas, offset_x)
    # Update the display
    pygame.display.update()

    

# Main function to contain event handlers and run non-stop while program is open
# Why pass the window parameter?
def main(window, canvas):

    offset_x = 0
    scroll_area_width = 200

    # A new clock variable that will be used to track the time and set a framerate
    clock = pygame.time.Clock() 

    # Array to store all the terrain block coordinates to fill the screen
    background = Background("Backgrounds", "Sky.png", "The Background")
    background.get_background_block_array()
    background.draw(window, canvas, offset_x)

    # Store terrain object in this variable
    terrain = Terrain_Blocks("Terrains", "DirtTerrain.png", "The Terrain")
    terrain.get_terrain_floor_array()
    terrain.get_level()
    objects = [*terrain.coordinates]
    print(objects)

    # Store player object in this variable
    player = Player("Characters", "RunningGuy.png", "The Player's Chosen Character")


    # Constant, infinitely running loop
    run = True
    while run:
        # A method to run every frame and make the game run at max 60 FPS on all machines
        clock.tick(60)
        print(clock.get_fps())
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user closes the program, exit the while loop and quit pygame
                run = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()


        # Call the draw function every frame to update the screen
        draw(window, background, terrain, player, canvas, offset_x, objects)

        if (player.rect.left - offset_x < 200):
            offset_x += player.xVel 

    # Quit pygame if the while loop has been broken
    pygame.quit()
    quit()


# Call main function to start the game
main(window, canvas)





# Thing sto ask
# animation feels off, how do i roate image in the x axis depending on the direction, why cant i just append rects to coordinates, how do surfaces work