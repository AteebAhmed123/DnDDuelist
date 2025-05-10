import pygame # import the library "pygame"
import random # we use randomness for the position and speed of enemies
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector

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
    K_x,
    K_h,
    K_z,
)

 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640  # Doubled height
CREATING_ENEMY_TIME_INTERVAL = 250 # milliseconds

# Score tracking
score = 0

# Initialize quantum circuit and state
qc = QuantumCircuit(1)  # One qubit for our ship's state
sampler = StatevectorSampler()
ship_state = 0  # 0 for |0⟩, 1 for |1⟩, 2 for |+⟩, 3 for |-⟩
is_quantum_mode = False
superposition_ship = None
measurement_message = None
measurement_timer = 0

# Random gate application parameters
RANDOM_GATE_INTERVAL = 60  # Check for random gate every 60 frames (2 seconds at 30 FPS)
frame_count = 0  # Counter for random gate application

pygame.init() # initiate pygame
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) # define the main screen

# Ship
ship = pygame.sprite.Sprite()
ship.surf = pygame.Surface((60, 20)) # create a surface
ship.surf.fill((170, 255, 0)) # color of our photonic ship
ship.rect = ship.surf.get_rect() # create a variable to access the surface as a rectangle
ship.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)  # Start in |0⟩ state

def create_superposition_ship():
    global superposition_ship
    superposition_ship = pygame.sprite.Sprite()
    superposition_ship.surf = pygame.Surface((60, 20))
    superposition_ship.surf.fill((170, 255, 0))
    superposition_ship.rect = superposition_ship.surf.get_rect()
    # Position the superposition ship in the other screen
    if ship.rect.centery < SCREEN_HEIGHT//2:
        superposition_ship.rect.center = (ship.rect.centerx, ship.rect.centery + SCREEN_HEIGHT//2)
    else:
        superposition_ship.rect.center = (ship.rect.centerx, ship.rect.centery - SCREEN_HEIGHT//2)
    all_sprites.add(superposition_ship)

def remove_superposition_ship():
    global superposition_ship
    if superposition_ship:
        superposition_ship.kill()
        superposition_ship = None

def get_quantum_state():
    # Get the current statevector
    state = Statevector.from_instruction(qc)
    return state

def apply_hadamard():
    global ship_state, is_quantum_mode
    
    # Apply Hadamard gate to the quantum circuit
    qc.h(0)
    
    # Get the new state
    state = get_quantum_state()
    
    if not is_quantum_mode:  # Going from classical to quantum
        is_quantum_mode = True
        if ship_state == 0:  # |0⟩ to |+⟩
            ship_state = 2
        else:  # |1⟩ to |-⟩
            ship_state = 3
        create_superposition_ship()
    else:  # Going from quantum to classical
        is_quantum_mode = False
        if abs(state[0]) > 0.99:  # |+⟩ to |0⟩
            ship_state = 0
        else:  # |-⟩ to |1⟩
            ship_state = 1
        remove_superposition_ship()
    
    # Visual feedback - flash the ship
    ship.surf.fill((255, 255, 255))  # White flash
    if superposition_ship:
        superposition_ship.surf.fill((255, 255, 255))

def apply_x_gate():
    global ship_state
    
    # Only apply X gate in classical states (|0⟩ or |1⟩)
    if ship_state >= 2:  # If in superposition (|+⟩ or |-⟩)
        return
    
    # Apply X gate to the quantum circuit
    qc.x(0)
    
    # Toggle the ship state
    ship_state = 1 - ship_state
    
    # Calculate relative position within current half
    half_height = SCREEN_HEIGHT // 2
    current_relative_pos = ship.rect.centery % half_height
    
    # Calculate new y position maintaining relative position
    if ship_state == 0:  # Moving to |0⟩ state (top half)
        new_y = current_relative_pos
    else:  # Moving to |1⟩ state (bottom half)
        new_y = half_height + current_relative_pos
    
    # Update ship position
    ship.rect.centery = new_y
    
    # Visual feedback - flash the ship
    ship.surf.fill((255, 255, 255))  # White flash

def apply_z_gate():
    global ship_state
    
    # Only apply Z gate in superposition states (|+⟩ or |-⟩)
    if ship_state < 2:  # If in classical state (|0⟩ or |1⟩)
        return
    
    # Apply Z gate to the quantum circuit
    qc.z(0)
    
    # Toggle between |+⟩ and |-⟩ states
    ship_state = 5 - ship_state  # 2 (|+⟩) <-> 3 (|-⟩)
    
    # Visual feedback - flash the ship
    ship.surf.fill((255, 255, 255))  # White flash
    if superposition_ship:
        superposition_ship.surf.fill((255, 255, 255))

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

def updateShip(pressed_keys, previous_state):
    if is_quantum_mode:
        return  # Don't move ship in quantum mode
    
    if pressed_keys[K_UP]:
        ship.rect.move_ip(0, -5)
    if pressed_keys[K_DOWN]:
        ship.rect.move_ip(0, 5)
    if pressed_keys[K_LEFT]:
        ship.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
        ship.rect.move_ip(5, 0)
		
    # Keep the ship within screen bounds horizontally
    if ship.rect.left < 0:
        ship.rect.left = 0
    if ship.rect.right > SCREEN_WIDTH:
        ship.rect.right = SCREEN_WIDTH
    
    # Keep ship within its quantum state's half of the screen
    # but maintain relative position within that half
    half_height = SCREEN_HEIGHT // 2
    if (previous_state != ship_state):
        previous_top_diff = abs(ship.rect.centery - half_height)
        if (ship_state == 0):
            ship.rect.centery = half_height - previous_top_diff
        elif (ship_state == 1):
            ship.rect.centery = half_height + previous_top_diff

    if ship_state == 0:  # |0⟩ state (top half)
        if ship.rect.bottom > half_height:
            ship.rect.bottom = half_height
        elif ship.rect.top < 0:
            ship.rect.top = 0
    else:  # |1⟩ state (bottom half)
        if ship.rect.top < half_height:
            ship.rect.top = half_height
        elif ship.rect.bottom > SCREEN_HEIGHT:
            ship.rect.bottom = SCREEN_HEIGHT

    # Remove debug print



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
            # Always move left
            enemy.rect.move_ip(-enemy.speed, 0)
            
            # Handle vertical movement in quantum mode
            if is_quantum_mode:
                # Get pressed keys
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_UP]:
                    enemy.rect.move_ip(0, -3)  # Move up
                if pressed_keys[K_DOWN]:
                    enemy.rect.move_ip(0, 3)   # Move down
                
                # Wrap around vertically
                if enemy.rect.top > SCREEN_HEIGHT:
                    enemy.rect.bottom = 0
                elif enemy.rect.bottom < 0:
                    enemy.rect.top = SCREEN_HEIGHT
            
        if enemy.rect.right < 0:  # remove any enemy moving out side of the screen
            enemy.kill()  # a nice method of Sprite

def updateBullets():
    for bullet in bullets:
        bullet.rect.move_ip(bullet.speed, 0)
        if bullet.rect.left > SCREEN_WIDTH:  # Remove bullets that go off screen
            bullet.kill()

ADDENEMY = pygame.USEREVENT + 1 # each event is associated with an integer
pygame.time.set_timer(ADDENEMY, CREATING_ENEMY_TIME_INTERVAL)

def perform_measurement():
    global ship_state, is_quantum_mode, superposition_ship, measurement_message, measurement_timer
    
    # Get current state
    state = get_quantum_state()
    
    # Calculate probabilities
    prob_0 = abs(state[0])**2
    prob_1 = abs(state[1])**2
    
    # Perform measurement based on probabilities
    measured_state = 0 if random.random() < prob_0 else 1
    
    # Update circuit to reflect measurement
    qc.reset(0)  # Reset to |0⟩
    if measured_state == 1:
        qc.x(0)  # Apply X if measured |1⟩
    
    # Update ship state
    ship_state = measured_state
    is_quantum_mode = False
    
    # Remove superposition ship
    remove_superposition_ship()
    
    # Set measurement message
    measurement_message = f"Measured |{measured_state}⟩"
    measurement_timer = 60  # Show message for 2 seconds (30 FPS)
    
    return measured_state

def handle_quantum_collision():
    global ship_state, is_quantum_mode, superposition_ship, measurement_message, measurement_timer
    
    if not is_quantum_mode:
        # Check only the original ship in classical mode
        if pygame.sprite.spritecollideany(ship, enemies):
            return True
        return False
    
    # Check which ship was hit (original or superposition)
    hit_original_ship = pygame.sprite.spritecollideany(ship, enemies)
    hit_superposition = False
    if superposition_ship and pygame.sprite.spritecollideany(superposition_ship, enemies):
        hit_superposition = True
    
    if not (hit_original_ship or hit_superposition):
        return False  # No collision detected
    
    # Perform measurement
    measured_state = perform_measurement()
    
    # Determine which ship was hit (top or bottom)
    hit_ship_is_top = False
    if hit_original_ship:
        hit_ship_is_top = ship.rect.centery < SCREEN_HEIGHT//2
    elif hit_superposition and superposition_ship:  # Double check superposition_ship exists
        hit_ship_is_top = superposition_ship.rect.centery < SCREEN_HEIGHT//2
    
    # Ship is destroyed if the measured state matches the hit ship's position
    measured_ship_is_top = measured_state == 0
    if hit_ship_is_top == measured_ship_is_top:
        measurement_message += " - Ship Destroyed!"
        return True
    
    # Ship survived the measurement
    measurement_message += " - Ship Survived!"
    return False

def apply_random_gate():
    global frame_count
    
    frame_count += 1
    if frame_count >= RANDOM_GATE_INTERVAL:
        frame_count = 0
        random_num = random.randint(1, 100)  # Random number between 1 and 100
        
        # Debug print
        print(f"Random number: {random_num}")
        
        # 20% chance for X gate in classical mode
        if 1 <= random_num <= 20 and not is_quantum_mode:
            print("Applying X gate")
            apply_x_gate()
            return "X"
        # 20% chance for Z gate in quantum mode
        elif 21 <= random_num <= 40 and is_quantum_mode:
            print("Applying Z gate")
            apply_z_gate()
            return "Z"
        # 10% chance for H gate in any mode
        elif 41 <= random_num <= 50:
            print("Applying H gate")
            apply_hadamard()
            return "H"
        else:
            print(f"No gate applied. Mode: {'Quantum' if is_quantum_mode else 'Classical'}")
    
    return None

running = True
while running:
    current_state_of_ship = ship_state
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
            elif event.key == K_x:  # If X is pressed
                apply_x_gate()
                score += 10  # Bonus points for state switching
            elif event.key == K_z:  # If Z is pressed
                apply_z_gate()
                score += 10  # Bonus points for state switching
            elif event.key == K_h:  # If H is pressed
                apply_hadamard()
                score += 15  # Bonus points for entering/exiting quantum mode
    screen.fill((0, 0, 0)) # the screen background color is set to black (Red=0,Green=0,Blue=0)
    
    # Draw the dividing line
    pygame.draw.line(screen, (100, 100, 100), (0, SCREEN_HEIGHT//2), (SCREEN_WIDTH, SCREEN_HEIGHT//2), 2)
    
    # Draw state labels
    state_font = pygame.font.SysFont('Arial', 24)
    state0_text = state_font.render("|0⟩", True, (255, 255, 255))
    state1_text = state_font.render("|1⟩", True, (255, 255, 255))
    screen.blit(state0_text, (10, 10))
    screen.blit(state1_text, (10, SCREEN_HEIGHT//2 + 10))
    
    # Get current quantum state
    state = get_quantum_state()
    
    # Draw current state information in top-right corner
    state_names = ["|0⟩", "|1⟩", "|+⟩", "|-⟩"]
    current_state = state_names[ship_state]
    
    # Calculate state probabilities
    prob_0 = abs(state[0])**2
    prob_1 = abs(state[1])**2
    
    # Apply random gate and get the applied gate
    applied_gate = apply_random_gate()
    
    state_info = [
        f"Current State: {current_state}",
        f"Mode: {'Quantum' if is_quantum_mode else 'Classical'}",
        f"P(|0⟩) = {prob_0:.2f}",
        f"P(|1⟩) = {prob_1:.2f}",
        f"Controls: {'Move Enemies' if is_quantum_mode else 'Move Ship'}",
        f"Frame Count: {frame_count}/{RANDOM_GATE_INTERVAL}"
    ]
    
    # Add random gate information if a gate was applied
    # if applied_gate:
    #     state_info.append(f"Random Gate Applied: {applied_gate}")
    
    # Display state information
    for i, text in enumerate(state_info):
        state_text = state_font.render(text, True, (170, 255, 0))
        screen.blit(state_text, (SCREEN_WIDTH - 300, 10 + i * 30))
    
    # Display measurement message if active
    if measurement_message and measurement_timer > 0:
        measurement_text = state_font.render(measurement_message, True, (255, 255, 0))
        screen.blit(measurement_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 20))
        measurement_timer -= 1
        if measurement_timer <= 0:
            measurement_message = None
    
    # Update score
    score += 1  # Add 1 point per frame
    
    # Reset ship color if it was flashed
    if ship.surf.get_at((0, 0)) == (255, 255, 255, 255):
        ship.surf.fill((170, 255, 0))
    
    # Display score
    score_font = pygame.font.SysFont('Arial', 24)
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - 120, 10))
    
    # update and show the ship and enemies
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]: running = False  # let's exit the game if the ship press "ESC"
    updateEnemies()
    updateBullets()  # Update bullet positions


    quantum_collision = handle_quantum_collision()
    updateShip(pressed_keys, current_state_of_ship)

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

    if quantum_collision:  # Returns True if ship should be destroyed
        print(quantum_collision)
        ship.kill()
        running = False
        my_font = pygame.font.SysFont('Comic Sans MS', 48)  # create a font object
        # we create a text surface to blit on the screen
        text_surface = my_font.render("Game Over! ", False, (255, 0, 0), (0, 0, 0))  # message / anti-aliasing effect / text color / background color
        screen.blit(text_surface, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))  # blit the text on the screen with the specified position
        there_is_message = True
    
    pygame.display.flip()  # show everything since the last frame
    if there_is_message: pygame.time.wait(2000)  # wait for 2000 milliseconds (= 2 seconds)
    pygame.time.Clock().tick(30)  # maximum number of frames per second <- set the FPS rate
    
    