import pygame # import the library "pygame"
import random # we use randomness for the position and speed of enemies

# This module contains various constants used by pygame.
from pygame.locals import ( # import Arrow Keys and ESC
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_f,
    K_r,
)

 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 320
CREATING_ENEMY_TIME_INTERVAL = 250 # milliseconds

# Score tracking
score = 0

pygame.init() # initiate pygame
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # define the main screen

# Ship
ship = pygame.sprite.Sprite()
ship.surf = pygame.Surface((60, 20)) # create a surface
ship.surf.fill((170, 255, 0)) # color of our photonic ship
ship.rect = ship.surf.get_rect() # create a variable to access the surface as a rectangle

def is_position_safe(x, y):
    # Create a temporary rect at the new position
    temp_rect = ship.rect.copy()
    temp_rect.center = (x, y)
    
    # Check if the position is within screen bounds
    if (temp_rect.left < 0 or temp_rect.right > SCREEN_WIDTH or 
        temp_rect.top < 0 or temp_rect.bottom > SCREEN_HEIGHT):
        return False
    
    # Check for collisions with enemies
    for enemy in enemies:
        if temp_rect.colliderect(enemy.rect):
            return False
    
    return True

def teleport_ship():
    # Try to find a safe position
    max_attempts = 50  # Limit attempts to prevent infinite loop
    for _ in range(max_attempts):
        # Generate random position within screen bounds
        x = random.randint(ship.rect.width//2, SCREEN_WIDTH - ship.rect.width//2)
        y = random.randint(ship.rect.height//2, SCREEN_HEIGHT - ship.rect.height//2)
        
        if is_position_safe(x, y):
            # Teleport successful
            ship.rect.center = (x, y)
            # Visual feedback - flash the ship
            ship.surf.fill((255, 255, 255))  # White flash
            return True
    
    return False  # Teleport failed

def updateShip(pressed_keys):
    if pressed_keys[K_UP]:
        ship.rect.move_ip(0, -5)
    if pressed_keys[K_DOWN]:
        ship.rect.move_ip(0, 5)
    if pressed_keys[K_LEFT]:
        ship.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
        ship.rect.move_ip(5, 0)
		
    # Keep the ship within the screen
    if ship.rect.left < 0:
        ship.rect.left = 0
    if ship.rect.right > SCREEN_WIDTH:
        ship.rect.right = SCREEN_WIDTH
    if ship.rect.top <= 0:
        ship.rect.top = 0
    if ship.rect.bottom >= SCREEN_HEIGHT:
        ship.rect.bottom = SCREEN_HEIGHT


#Enemy
enemies = pygame.sprite.Group() # keep all enemies - the enemies will be added automatically
bullets = pygame.sprite.Group() # keep all bullets
all_sprites = pygame.sprite.Group() # keep all enemies and ship(s)
all_sprites.add(ship) # add ship to the group of all sprites

# Freeze mechanism
is_frozen = False
freeze_timer = 0
FREEZE_DURATION = 60  # 2 seconds at 30 FPS

def createEnemy():
    enemy = pygame.sprite.Sprite() # create a new enemy
    enemy.surf = pygame.Surface((20, 10))  # create a surface
    enemy.surf.fill((255, 0, 0))  # color of enemy
    enemy_X = random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100) # position of x
    enemy_Y = random.randint(0, SCREEN_HEIGHT) # position of y
    enemy.rect = enemy.surf.get_rect(center=(enemy_X,enemy_Y)) # position of the new enemy
    enemy.speed = random.randint(5, 20) # we assign a random speed - how many pixel to move to the left in each frame
    enemy.original_color = (255, 0, 0)  # Store original color
    enemies.add(enemy)  # add the new enemy
    all_sprites.add(enemy)  # add the new enemy

def createBullet():
    bullet = pygame.sprite.Sprite()
    bullet.surf = pygame.Surface((10, 5))
    bullet.surf.fill((255, 255, 0))  # Yellow bullets
    bullet.rect = bullet.surf.get_rect(center=(ship.rect.right, ship.rect.centery))
    bullet.speed = 15  # Bullet speed
    bullets.add(bullet)
    all_sprites.add(bullet)

def updateEnemies():
    global is_frozen, freeze_timer
    
    # Update freeze timer
    if is_frozen:
        freeze_timer -= 1
        if freeze_timer <= 0:
            is_frozen = False
            # Reset all enemies to original color
            for enemy in enemies:
                enemy.surf.fill(enemy.original_color)
    
    for enemy in enemies:
        if not is_frozen:  # Only move enemies if not frozen
            enemy.rect.move_ip(-enemy.speed, 0) # change the horizontal position x
        if enemy.rect.right < 0:  # remove any enemy moving out side of the screen
            enemy.kill()  # a nice method of Sprite

def updateBullets():
    for bullet in bullets:
        bullet.rect.move_ip(bullet.speed, 0)
        if bullet.rect.left > SCREEN_WIDTH:  # Remove bullets that go off screen
            bullet.kill()

ADDENEMY = pygame.USEREVENT + 1 # each event is associated with an integer
pygame.time.set_timer(ADDENEMY, CREATING_ENEMY_TIME_INTERVAL)

running = True
while running:
    for event in pygame.event.get():  # check all events one by one since the last frame
        if event.type == pygame.QUIT:  # if the window is closed
            running = False
        elif event.type == ADDENEMY: # we catch the new event here and then we will create a new enemy
            createEnemy()
        elif event.type == pygame.KEYDOWN:  # Check for key press events
            if event.key == K_SPACE:  # If space is pressed
                createBullet()
            elif event.key == K_f and not is_frozen:  # If F is pressed and not already frozen
                is_frozen = True
                freeze_timer = FREEZE_DURATION
                # Change all enemies to blue color to indicate frozen state
                for enemy in enemies:
                    enemy.surf.fill((0, 0, 255))  # Blue color for frozen enemies
            elif event.key == K_r:  # If R is pressed
                if teleport_ship():
                    score += 25  # Bonus points for successful teleport
    screen.fill((0, 0, 0)) # the screen background color is set to black (Red=0,Green=0,Blue=0)
    
    # Update score
    score += 1  # Add 1 point per frame    
    # Reset ship color if it was flashed
    if ship.surf.get_at((0, 0)) == (255, 255, 255, 255):
        ship.surf.fill((170, 255, 0))
    
    # Display score
    score_font = pygame.font.SysFont('Arial', 24)
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - 120, 10))  # Display in top-left corner
    
    # update and show the ship and enemies
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]: running = False  # let's exit the game if the ship press "ESC"
    updateEnemies()
    updateBullets()  # Update bullet positions
    updateShip(pressed_keys)

    # Check for bullet-enemy collisions
    for bullet in bullets:
        enemy_hit = pygame.sprite.spritecollideany(bullet, enemies)
        if enemy_hit:
            enemy_hit.kill()  # Remove the enemy
            bullet.kill()     # Remove the bullet
            score += 50      # Bonus points for hitting an enemy

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    there_is_message = False

    if pygame.sprite.spritecollideany(ship, enemies):  # check if "ship" is hit by any enemy in the "enemies" group
        ship.kill()
        running = False
        my_font = pygame.font.SysFont('Comic Sans MS', 48)  # create a font object
        # we create a text surface to blit on the screen
        text_surface = my_font.render("Game Over! ", False, (255, 0, 0), (0, 0, 0))  # message / anti-aliasing effect / text color / background color
        screen.blit( text_surface, (SCREEN_WIDTH // 3,SCREEN_HEIGHT // 3) )  # blit the text on the screen with the specified position
        there_is_message = True

    
    pygame.display.flip()  # show everything since the last frame
    if there_is_message: pygame.time.wait(2000)  # wait for 2000 milliseconds (= 2 seconds)
    pygame.time.Clock().tick(30)  # maximum number of frames per second <- set the FPS rate
    
    