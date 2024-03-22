import pygame
import random

# Initialize the game
pygame.init()

# Set the screen
# Use the full screen, detect size
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

# Load the background image
background = pygame.image.load("background.webp").convert()
background = pygame.transform.scale(background, (width, height))

# Load kuku.jpeg
kuku_image = pygame.image.load("kuku.jpeg").convert_alpha()
kuku_image = pygame.transform.scale(kuku_image, (100, 100))

# Load mindy image
mindy_image = pygame.image.load("mindy.webp").convert_alpha()
mindy_image = pygame.transform.scale(mindy_image, (100, 100))


# Load the shield image
shield_image = pygame.image.load("shield.webp").convert_alpha()  # Adjust filename as necessary
shield_image = pygame.transform.scale(shield_image, (200, 200))  # Adjust size as necessary

# Load and scale the saw image
saw_image = pygame.image.load("saw.webp").convert_alpha()  # Replace "saw.webp" with your saw image file
saw_image = pygame.transform.scale(saw_image, (100, 100))  # Scale to match character size, adjust as needed


# Load music file to play in the background
pygame.mixer.music.load("The_Clash_of_Titans.mp3")
pygame.mixer.music.play(-1)

#load heart image
heart = pygame.image.load("heart_transparent.webp").convert_alpha()
#make background of heart image transparent
heart.set_colorkey((255, 255, 255))

#load broken heart image
broken_heart = pygame.image.load("broken-heart.webp").convert_alpha()
#make background of broken heart image transparent
broken_heart.set_colorkey((255, 255, 255))
#scale heart and broken heart images
broken_heart = pygame.transform.scale(broken_heart, (50, 50))


#load stoney image
stoney = pygame.image.load("stoney.webp").convert_alpha()
#scale stoney image
stoney = pygame.transform.scale(stoney, (200, 200))

heart = pygame.transform.scale(heart, (50, 50))


class Stoney:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    #move automatically left right and down only. radomly pick a direction
    def move(self):
        #move a space in a random direction (left, right, down)
        dx = random.choice([-1, 1, 0])
        dy = random.choice([0, 1])
        # Update position with gravity and edge constraints
        new_x = min(max(0, self.x + dx), width - self.width)
        new_y = min(max(0, self.y + dy), height - self.height)
        self.x, self.y = new_x, new_y

        #if stoney hits the bottom of the screen, move to the top
        if self.y == height - self.height:
            self.y = 0


    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Character:
    def __init__(self, name, image, x, y):
        self.name = name
        self.image = image
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.lives = 3
        self.collision_cooldown = 0  # Cooldown time remaining (in frames)
        self.is_squashed = False
        self.respawn_time = 0  # Time until respawn in milliseconds
        self.show_shield = False  # New attribute for shield visibility
        self.original_image = image
        self.alternative_image = None 
        self.angle = 0  # New attribute for rotation angle
        self.is_transformed = False  # Indicates if transformed into saw

    def transform_into_saw(self):
       if not self.show_shield:  # Check if the shield is not active
            self.is_transformed = not self.is_transformed
            if self.is_transformed:
                self.image = self.alternative_image
            else:
                self.image = self.original_image


    def apply_gravity(self):
        # Simple gravity simulation
        if self.y < height - self.height:  # Check if above ground
            self.y += 5  # Gravity effect

    def move(self, dx, dy):
        # Update position with gravity and edge constraints
        new_x = min(max(0, self.x + dx), width - self.width)  # Prevent going past left and right edges
        new_y = min(max(0, self.y + dy), height - self.height)  # Prevent going past top and bottom edges
        self.x, self.y = new_x, new_y


    def update_rotation(self):
        # Update the rotation angle for a spinning effect
        self.angle = (self.angle + 10) % 360  # Adjust rotation speed as needed

    def draw(self, screen):
        
        if self.show_shield:
            # Calculate shield position to center it around the character
            shield_x = self.x + self.width / 2 - shield_image.get_width() / 2
            shield_y = self.y + self.height / 2 - shield_image.get_height() / 2
            screen.blit(shield_image, (shield_x, shield_y))
        elif self.image != self.original_image:
            rotated_image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image
            new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)  # Calculate new rectangle
            screen.blit(rotated_image, new_rect.topleft)  # Draw the rotated image
        else:
            screen.blit(self.image, (self.x, self.y))
        
        
        if self.is_squashed and self.name == "kuku":
            squashed_image = pygame.transform.scale(self.image, (self.width, self.height // 2))  # Example squashed appearance
            screen.blit(squashed_image, (self.x, self.y + self.height // 2))  # Adjust position
        elif not self.is_squashed and self.name == "kuku":
            screen.blit(self.image, (self.x, self.y))

      

        


    #draw hearts in top left corner as the lives of the character
    def draw_lives(self, screen, full_heart, broken_heart):
        for i in range(int(self.lives)):
            screen.blit(full_heart, (10 + i*60, 10))  # Adjust spacing as needed
        if self.lives % 1 != 0:  # Check for half life
            screen.blit(broken_heart, (10 + int(self.lives)*60, 10))  # Position after the last full heart

    def lose_half_life(self):
        self.lives -= 0.5
        if self.lives < 0:
            self.lives = 0  # Prevent negative lives

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        # Call this method every frame to update the cooldown
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        if self.lives <= 0:
            self.is_squashed = True
            self.respawn_time = pygame.time.get_ticks() + 3000  # Set to respawn in 1 second
            self.lives = 3  # Reset lives for respawn
            
        if self.is_squashed and pygame.time.get_ticks() >= self.respawn_time:
            # Reset character state for respawn
            self.is_squashed = False
            self.x, self.y = width // 2, height // 2  # Example respawn position, adjust as needed  




#load custom font and set font size
font = pygame.font.Font('zekton.ttf', 32)


# Create kuku and mindy objects
kuku = Character("kuku", kuku_image, width // 2, height // 2)
mindy = Character("mindy", mindy_image, width // 2 + 100, height // 2)
mindy.alternative_image = saw_image


# Create stoney object
stoney = Stoney(stoney, width // 2 - 100, 100)


# Flag for who is being moved
active_character = mindy

mindy.lives = 3
kuku.lives = 3

running = True
while running:
    # Place the background image
    screen.blit(background, (0, 0))

    # Draw characters
    kuku.draw(screen)
    mindy.draw(screen)

    # Draw the text
    text = font.render('Meanwhile... Space invasion: battle of Velix', True, (255, 255, 255))
    screen.blit(text, (width // 2 - text.get_width() // 2, 50))
    
    #draw three hearts in top left corner
   # Focused test with heart image
    #screen.blit(heart, (10, 10))
    #screen.blit(heart, (60, 10))
    #screen.blit(heart, (110, 10))

    if active_character == mindy:
        mindy.draw_lives(screen, heart, broken_heart)
    else:
        kuku.draw_lives(screen, heart, broken_heart)

    #draw stoney in top center
    stoney.draw(screen)
    stoney.move()

    # Apply gravity to both characters
    kuku.apply_gravity()
    mindy.apply_gravity()

    # Single event loop to handle all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Check for key presses
            if event.key == pygame.K_x:  # Switch active character
                active_character = mindy if active_character == kuku else kuku
            elif event.key == pygame.K_a:
               if active_character.name == "mindy":  # Ensure this applies only to Mindy
                if not mindy.is_transformed:  # Prevent activating the shield if transformed
                    mindy.show_shield = not mindy.show_shield
            elif event.key == pygame.K_y:
            # Check if Mindy is the active character, then transform
                if active_character == mindy:
                    mindy.transform_into_saw()
            dx, dy = 0, 0
            if event.key == pygame.K_LEFT:
                dx = -active_character.width
            elif event.key == pygame.K_RIGHT:
                dx = active_character.width
            if event.key == pygame.K_UP:
                dy = -active_character.height  # Assuming you want up to move by height, adjust as needed

            # Apply the movement
            if dx != 0 or dy != 0:
                active_character.move(dx, dy)
                if active_character.image != active_character.original_image:
                    active_character.update_rotation()

            active_character.update()

    # Check for collision
    if active_character.get_rect().colliderect(stoney.get_rect()) and active_character.collision_cooldown == 0:
        if not (active_character.show_shield and active_character.name == "mindy"):
    
            active_character.lose_half_life()
            active_character.collision_cooldown = 5

    pygame.display.flip()

pygame.quit()
