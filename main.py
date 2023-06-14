# Platformer Game Portfolio Project by Ibrahim Ismayilov

# IMPORTING MODULES 
# Import pygame
import pygame

# Import "join" method from os to help with saving images in variables
from os.path import join, isfile


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
canvas = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
canvas = canvas.convert_alpha()
canvas_rect = pygame.Rect(0, 0, canvas.get_width(), canvas.get_height())

# Create FPS variable to set max FPS of the game to be 60 when run
FPS = 60


# CLASSES
# A parent class for to serve as a base class when drawing all objects in the game, including characters, terrain blocks, the background tiles and etc
class Objects():
    # Constructor
    def __init__(self, image_folder, image_name, object_name):
        self.image = pygame.image.load(join("Assets", image_folder, image_name)).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.object_name = object_name
        self.level = 1
        

    # Methods
    # Function to draw the object's image with the correct coordinates on the screen
    def draw_and_create_surface(self, win, canvas, offset_x, canvas_rect):
        for coordinate in self.coordinates:

            canvas.blit(self.image, (coordinate[0], coordinate[1]))

# Child class to get acquire all of the intialized attributes from the "Objects" Parent class but add its additional methods for drawing the background
class Background(Objects):
    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)

    # Methods
    def get_background_block_array(self):
        for i in range(-WIDTH // self.width + 1, WIDTH // self.width + 1):
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
        for i in range (-30, 40):
            self.rect.x, self.rect.y = i * self.width, HEIGHT - self.height
            self.coordinates.append((self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        
        
class Coins(Objects):
    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)
        self.hit = False

    def disappear(self):
        collided_obj, collided_rect  = handle_collision()
        if collided_obj != "":
            self.hit = True
            collided_obj.pop(collided_rect)



    def get_level_1_coins(self, terrain):
        self.level_1_map = [(350, HEIGHT - terrain.height * 3 - self.height, self.width, self.height), (700 + terrain.width + 30, HEIGHT - terrain.height * 3 - self.height, self.wdith, self.height), (1800 + terrain.width * 3, HEIGHT - terrain.height * 5 - self.height)]

        self.coordinates.extend(self.level_1_map)

class Enemies(Objects):
    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)
        self.return_lap = False
        self.moving = True

    def enemy_movement(self):
        for coordinate in self.coordinates:
            if (coordinate.x < coordinate.x + 40) and (self.return_lap == False):
                coordinate.x += 3
            elif (coordinate.x > coordinate.x - 40):
                self.return_lap = True
                coordinate.x += -3




# Class to draw the player
class Player(Objects):
    GRAVITY = 1   

    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)
        self.xVel = 0
        self.yVel = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(500, 50, self.width, self.height)
        self.direction = "Right"
        self.jump_count = 0
        self.fall_count = 0
        self.collided_objects = []

    # Methods
    def move(self, vel):
        self.xVel = vel
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
    

    def handle_movement(self, player, terrain, coins):
        # handle_collision(player, terrain, coins)
        # self.gravity()

        keys = pygame.key.get_pressed()
        self.xVel = 0
        if keys[pygame.K_LEFT]:
            self.move(-3)
        if keys[pygame.K_RIGHT]:
            self.move(3)
        
        self.coordinates = [(self.rect.x, self.rect.y, self.rect.width, self.rect.height)]


# FUNCTIONS
# THe main draw function to draw everything for the program or run other smaller drawing functions
def handle_collision(player, terrain, coins):
    # for coordinate in terrain.coordinates:
    #     x_offset = coordinate[0] - player.rect.left
    #     y_offset = coordinate[1] - player.rect.top
    #     if player.mask.overlap(terrain.mask, (x_offset, y_offset)):
    #         print("i")
    pass


                
                

def draw(window, background, terrain, player, canvas, offset_x, canvas_rect, coins):


    background.draw(window, canvas, offset_x, canvas_rect)

    terrain.draw(window, canvas, offset_x, canvas_rect)

    player.handle_movement(player, terrain, coins)
    player.draw(window, canvas, offset_x, canvas_rect)


    window.blit(canvas, (canvas_rect.x - offset_x, canvas_rect.y))

    # Update the display
    pygame.display.update()

    

# Main function to contain event handlers and run non-stop while program is open
# Why pass the window parameter?
def main(window, canvas, canvas_rect):

    offset_x = 0
    scroll_area_width = 200

    # A new clock variable that will be used to track the time and set a framerate
    clock = pygame.time.Clock() 

    # Array to store all the terrain block coordinates to fill the screen
    background = Background("Backgrounds", "Sky.jpg", "The Background")
    background.get_background_block_array()

    # Store terrain object in this variable
    terrain = Terrain_Blocks("Terrains", "DirtTerrain.png", "The Terrain")
    terrain.get_terrain_floor_array()
    terrain.get_level()

    # Store player object in this variable
    player = Player("Characters", "RunningGuy.png", "The Player's Chosen Character")

    coins = Coins("Coins", "Coins.png", "Level 1 Coins")


    # Constant, infinitely running loop
    run = True
    while run:
        # A method to run every frame and make the game run at max 60 FPS on all machines
        clock.tick(60)
        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user closes the program, exit the while loop and quit pygame
                run = False
                break
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()


        # Call the draw function every frame to update the screen
        draw(window, background, terrain, player, canvas, offset_x, canvas_rect, coins)

        if (player.rect.left < canvas_rect.x + 200 and player.xVel < 0):
            offset_x += player.xVel


    # Quit pygame if the while loop has been broken
    pygame.quit()
    quit()


# Call main function to start the game
main(window, canvas, canvas_rect)
