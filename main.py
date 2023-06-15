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
canvas_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

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
        self.coordinates = []
        

    # Methods
    # Function to draw the object's image with the correct coordinates on the screen
    def draw(self, win, canvas_rect):
        for coordinate in self.coordinates:
            win.blit(self.image, (coordinate[0] - canvas_rect.x, coordinate[1]))


# Child class to get acquire all of the intialized attributes from the "Objects" Parent class but add its additional methods for drawing the background
class Background(Objects):
    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)

    # Methods
    # Function to append the coordinates for drawing the background tiles
    def get_background_block_array(self):
        for i in range(-30, 27):
            for j in range(8):
                # Put the data in a tuple to have its x and y coordinates be more accessible when appended to the coordinates array. Put it in a format that can access the x and y values. 
                self.rect.x, self.rect.y = i * self.width, j * self.height
                # Append it in a format that can access the x and y values 
                self.coordinates.append((self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.object_name))


# # Child class to get acquire all of the intialized attributes from the "Objects" Parent class but add its additional methods for drawing the terrain blocks
class Terrain_Blocks(Objects):
    def __init__(self, image_folder, image_name, object_name): 
        super().__init__(image_folder, image_name, object_name)

    # Method to draw terrain based on which level the user is on
    def get_level(self):
        if self.level == 1:
            self.get_level_1_terrain()
        elif self.level == 2:
            self.get_level_2_map()
        elif self.level == 3:
            self.get_level_3_map()

    # Method to append the coordinates for creating the level 1 map terrain
    def get_level_1_terrain(self):
        self.level_1_map = [(350, HEIGHT - self.height * 3, self.width, self.height, self.object_name), (350 + self.width, HEIGHT - self.height * 3, self.width, self.height, self.object_name), (700, HEIGHT - self.height * 2, self.width, self.height, self.object_name), (700, HEIGHT - self.height * 3, self.width, self.height, self.object_name), (700 + self.width, HEIGHT - self.height * 4, self.width, self.height, self.object_name), (700 + self.width * 2, HEIGHT - self.height * 4, self.width, self.height, self.object_name), (700 + self.width * 3, HEIGHT- self.height * 3, self.width, self.height, self.object_name), (700 + self.width * 3, HEIGHT - self.height * 2, self.width, self.height, self.object_name), (1800, HEIGHT - self.height * 2, self.width, self.height, self.object_name), (1800 + self.width, HEIGHT - self.height * 3, self.width, self.height, self.object_name), (1800 + self.width * 2, HEIGHT - self.height * 4, self.width, self.height, self.object_name), (1800 + self.width * 3, HEIGHT - self.height * 5, self.width, self.height, self.object_name)]
        self.coordinates.extend(self.level_1_map)

    # Method to get block coordinates
    def get_terrain_floor_array(self):
        for i in range (-30, 40):
            self.rect.x, self.rect.y = i * self.width, HEIGHT - self.height
            self.coordinates.append((self.rect.x, self.rect.y, self.rect.width, self.rect.height, self.object_name))

# Coins class that inherits attributes from Objects parents class and has methods from generating coins at set places on the map 
class Coins(Objects):
    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)
        self.collided_coins = []
        self.hit = False
        self.coins_collected = 0

    # Method to append specific coordinates based on the level to its coordinates array which will be drawn by the draw function
    def get_level_1_coins(self, terrain):
        self.level_1_map = [(350, HEIGHT - terrain.height * 3 - self.height, self.width, self.height, self.object_name), (700 + terrain.width + 30, HEIGHT - terrain.height * 5, self.width, self.height, self.object_name), (1800 + terrain.width * 3, HEIGHT - terrain.height * 5 - self.height, self.width, self.height, self.object_name), (1800 + terrain.width + 10, HEIGHT - terrain.height * 2 + 10, self.width, self.height, self.object_name)]

        self.coordinates.extend(self.level_1_map)


    def check_coins(self):
        if self.coins_collected == 4:
            print("YOU WIN!")
# class Enemies(Objects):
#     def __init__(self, image_folder, image_name, object_name):
#         super().__init__(image_folder, image_name, object_name)
#         self.return_lap = False
#         self.moving = True

#     def enemy_movement(self):
#         for coordinate in self.coordinates:
#             if (coordinate.x < coordinate.x + 40) and (self.return_lap == False):
#                 coordinate.x += 3
#             elif (coordinate.x > coordinate.x - 40):
#                 self.return_lap = True
#                 coordinate.x += -3


# Player class that inherits attributes from Objects parent class and handles almost everything related to the character drawn on the screen including speed, gravity, etc. 
class Player(Objects):
    GRAVITY = 1   

    def __init__(self, image_folder, image_name, object_name):
        super().__init__(image_folder, image_name, object_name)
        self.lvl_xVel = 3
        self.xVel = 0
        self.yVel = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(500, 50, self.width, self.height)
        self.moving_direction = "Right" 
        self.jump_count = 0
        self.fall_count = 0
        self.collided_objects = []

    # Method to move left when the user presses the left arrowkey
    def move_left(self):
        self.rect.x += self.xVel

    # Method to move right when the user presses the right arrow key
    def move_right(self):
        self.rect.x += self.xVel

    # Method to instill constant gravity when the user is in the air
    def gravity(self):
        self.yVel += min(1, self.fall_count / FPS * 3)
        self.rect.y += self.yVel
        self.fall_count += 1

    # Method to move the user up when the user presses the backspace key, allowing them to double jump too
    def jump(self):
        self.yVel = -self.GRAVITY * 12
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    # Method to move to have the user land on a surface and reset things like gravity, when they collided with an object whilst having a yVel greater than zero
    def landed(self):
        self.jump_count = 0
        self.fall_count = 0
        self.yVel = 0
    
    # Method to reverse the user's yVel and have them head down once they collided with an object while jumping
    def hit_head(self):
        self.fall_count = 0
        self.yVel *= -1
    
    # Method to move the player depending on which key is pressed and change their position on the screen
    def handle_player_movement(self):
        self.xVel = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.xVel = -3
            if self.moving_direction != "Left":
                self.moving_direction = "Left"
                self.image = pygame.transform.flip(self.image, True, False)
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.xVel = 3
            if self.moving_direction != "Right":
                self.moving_direction = "Right"
                self.image = pygame.transform.flip(self.image, True, False)
            self.move_right()

        
        self.coordinates = [(self.rect.x, self.rect.y, self.rect.width, self.rect.height)]


# FUNCTIONS

# Function to handle the vertical collisions involving the player
def handle_vertical_collision(player, terrain, coins):
    all_coordinates = (*terrain.coordinates, *coins.coordinates)
    for coordinate in all_coordinates:
        coordinate_rect = pygame.Rect((coordinate[0]), (coordinate[1]), (coordinate[2]), (coordinate[3]))
        if player.rect.colliderect(coordinate_rect):
            if coordinate[-1] == "The Terrain":
                if player.yVel > 0:
                    player.rect.bottom = coordinate_rect.top
                    player.landed()
                if player.yVel < 0:
                    player.rect.top = coordinate_rect.bottom
                    player.hit_head()
            elif coordinate[-1] == "Coins":
                index = coins.coordinates.index(coordinate)
                coins.coordinates.pop(index)
                coins.coins_collected += 1
                coins.check_coins()


# Function to handle horizontal collisions to the right of the player
def handle_right_collision(player, terrain, coins):
    player.rect.x += 5
    all_coordinates = (*terrain.coordinates, *coins.coordinates)
    for coordinate in all_coordinates:
        coordinate_rect = pygame.Rect((coordinate[0]), (coordinate[1]), (coordinate[2]), (coordinate[3]))
        if player.rect.colliderect(coordinate_rect):
            if coordinate[-1] == "The Terrain":
                player.rect.x -= player.xVel
            elif coordinate[-1] == "Coins":
                index = coins.coordinates.index(coordinate)
                coins.coordinates.pop(index)
                coins.coins_collected += 1
                coins.check_coins()

    player.rect.x -= 5

# Function to handle horizontal collisions to the left of the player
def handle_left_collision(player, terrain, coins):
    player.rect.x -= 5
    all_coordinates = [*terrain.coordinates, *coins.coordinates]
    for coordinate in all_coordinates:
        coordinate_rect = pygame.Rect((coordinate[0]), (coordinate[1]), (coordinate[2]), (coordinate[3]))
        if player.rect.colliderect(coordinate_rect):
            if coordinate[-1] == "The Terrain":
                player.rect.x -= player.xVel
            elif coordinate[-1] == "Coins":
                index = coins.coordinates.index(coordinate)
                coins.coordinates.pop(index)
                coins.coins_collected += 1
                coins.check_coins()
    player.rect.x += 5
                
                
# Draw function for drawing everything
def draw(window, background, terrain, player, canvas_rect, coins):
    
    background.draw(window, canvas_rect)

    terrain.draw(window, canvas_rect)
    player.handle_player_movement()
    handle_left_collision(player, terrain, coins)
    handle_right_collision(player, terrain, coins)
    player.gravity()
    handle_vertical_collision(player, terrain, coins)
    player.draw(window, canvas_rect)
    coins.draw(window, canvas_rect)


    # Update the display
    pygame.display.update()

    

# Main function to contain event handlers and run non-stop while program is open
def main(window, canvas_rect):
    # Starter Message
    print("Collect All The Coins to Win!")

    # A new clock variable that will be used to track the time and set a framerate
    clock = pygame.time.Clock() 

    # Array to store all the terrain block coordinates to fill the screen
    background = Background("Backgrounds", "Sky.jpg", "The Background")
    background.get_background_block_array()

    # Store terrain object in this variable
    terrain = Terrain_Blocks("Terrains", "DirtTerrain.jpg", "The Terrain")
    terrain.get_terrain_floor_array()
    terrain.get_level()

    # Store player object in this variable
    player = Player("Characters", "RunningGuy.png", "The Player's Chosen Character")

    # Store coin object in this variable
    coins = Coins("Coins", "Coins.png", "Coins")
    coins.get_level_1_coins(terrain)


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
        draw(window, background, terrain, player, canvas_rect, coins)

        # Check if the user goes past the screen enough that the screen starts scrolling
        if (player.rect.left < canvas_rect.x + 200 and player.xVel < 0) or (player.rect.right > canvas_rect.right - 200 and player.xVel > 0):
            canvas_rect.x += player.xVel


    # Quit pygame if the while loop has been broken
    pygame.quit()
    quit()


# Call main function to start the game
main(window, canvas_rect)
