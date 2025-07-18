import pygame # Import the Pygame library
import time # Import the time module for timing functions
import random # Import the random module for generating random numbers

# Initialize Pygame
pygame.init()




# Lock screen size to ensure consistent layout
WIDTH, HEIGHT = 1500, 800 # Set the desired width and height
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Create the window with the specified size
pygame.display.set_caption("TURBO DODGE: Internet Safety Edition") # Set the window title

# Load images
BG = pygame.transform.scale(pygame.image.load("Game Backround Start .jpg"), (WIDTH, HEIGHT)) 
player = pygame.transform.scale(pygame.image.load("Image 6-2-25 at 7.49 PM.jpg"), (50, 150)) 
BG2 = pygame.transform.scale(pygame.image.load("racetrackimage3.jpg"), (WIDTH, HEIGHT)) 

# Fonts
text_font = pygame.font.SysFont("Times New Roman", 30) 
text_font1 = pygame.font.SysFont("Times New Roman", 75) 
text_font2 = pygame.font.SysFont("Times New Roman", 25) 
text_font4 = pygame.font.SysFont("Times New Roman", 65)

# Game variables
Lanes = [425, 725, 1025] 
current_lane = 1 
y_pos = HEIGHT - 250 
STAR_WIDTH = 50 
STAR_HEIGHT = 50 
PLAYER_WIDTH = 50 
PLAYER_HEIGHT = 150 
hitbox_margin_x = 10 
hitbox_margin_y = 15 

# Swapped colors
OBSTACLE_COLOR = (139, 69, 19)        # Brown (now used for obstacle)
SNAIL_TEXT_COLOR = (244, 164, 96)     # Sandy brown (now used for snail text)

def drawText(text, font, text_col, x, y):    # Function to draw text on screen
    image = font.render(text, True, text_col)
    WIN.blit(image, (x, y))

def draw(show_player, x_pos, game_started, elapsed, stars, player_rect=None): # Function to draw game elements on screen
    if not show_player:
        WIN.blit(BG, (0, 0))
        drawText("Click the trackpad/mouse to enter", text_font, (255, 0, 0), 700, 220)
        drawText("TURBO DODGE: Internet Safety Edition", text_font4, (0, 0, 0), 50, 50)
    else:
        WIN.blit(BG2, (0, 0))
        WIN.blit(player, (x_pos, y_pos))
        if not game_started:
            drawText("Press Enter to Start", text_font2, (0, 255, 0), 625, 115)
            drawText("Dodge obstacles with left and right arrow keys that help you change lanes.", text_font2, (0, 255, 0), 290, 185)
            drawText("Learn a fact about internet safety when you crash!", text_font2, (255, 0, 0), 430, 255)
        else:
            time_text = text_font.render(f"Time: {round(elapsed)} seconds", True, "white")
            WIN.blit(time_text, (10, 10))
            for star in stars:
                pygame.draw.rect(WIN, OBSTACLE_COLOR, star)

    pygame.display.update()

def main(): # Main function to run the game

    #variables for game loop
    global current_lane
    run = True
    show_player = False
    game_started = False

    clock = pygame.time.Clock()

    start_time = None
    elapsed = 0

    star_add_increment = 2750 #can be changed to determine how often stars appear
    star_count = 0

    stars = []
    hit = False

    star_vel = 3
    last_speed_increase = 0

    while run: # Main game loop
        dt = clock.tick(60) 
        star_count += dt 

        for event in pygame.event.get(): # Event handling loop
            if event.type == pygame.QUIT: # If the user clicks the close button, exit the game
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN: # If the user clicks the mouse, show the player
                show_player = True

            if show_player and event.type == pygame.KEYDOWN: # If the player is shown and a key is pressed, handle the key press
                if event.key == pygame.K_RETURN: # If the Enter key is pressed, start the game
                    game_started = True
                    start_time = time.time()
                if game_started: # If the game has started, handle lane changes
                    if event.key == pygame.K_LEFT and current_lane > 0:
                        current_lane -= 1 # Move the player to the left lane
                    elif event.key == pygame.K_RIGHT and current_lane < len(Lanes) - 1:
                        current_lane += 1 # Move the player to the right lane

        if game_started and start_time:
            elapsed = time.time() - start_time

            # Increase star speed every 15 seconds
            if elapsed - last_speed_increase >= 15:
                star_vel += 1
                last_speed_increase = elapsed

            # Spawn stars
            if star_count > star_add_increment:
                num_stars = random.choice([1, 2]) 
                lanes_for_stars = random.sample(Lanes, num_stars)
                for star_x in lanes_for_stars:
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)
                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            # Move stars
            for star in stars[:]:
                star.y += star_vel
                if star.y > HEIGHT: 
                    stars.remove(star)

            # Player position and hitbox to detect collision
            x_pos = Lanes[current_lane] 
            player_rect = pygame.Rect( # Create a rectangle for the player's hitbox
                x_pos + hitbox_margin_x // 2,
                y_pos + hitbox_margin_y // 2,
                PLAYER_WIDTH - hitbox_margin_x,
                PLAYER_HEIGHT - hitbox_margin_y
            )

            for star in stars[:]:
                if star.colliderect(player_rect):# Check for collision between player and star
                    hit = True # Set the hit flag to True
                    break # Exit the loop if a collision is detected

            if hit: # If the player has hit a star, display the game over screen
                lost_text = text_font1.render("Your car is busted! Play again?", True, "red") 
                lost_x = WIDTH / 2 - lost_text.get_width() / 2
                lost_y = HEIGHT / 2 - lost_text.get_height() / 2
                WIN.blit(lost_text, (lost_x, lost_y)) # Draw the game over text on the screen
                Internet_Safety_Facts = ["Using strong, unique passwords makes your accounts much harder to hack.",
                                        "Two-factor authentication (2FA) adds an extra layer of security to your accounts.",
                                        "Once you post something online, it’s nearly impossible to delete it completely.",
                                        "Private accounts aren't fully private — screenshots and resharing still happen.",
                                        "Strangers online aren’t always who they say they are.",
                                        "Cyberbullying can be reported on most platforms — don't hesitate to block and report.",
                                        "Avoid clicking links in suspicious messages — they could be phishing scams.",
                                        "Sharing your location online can reveal more than you think.",
                                        "Free Wi-Fi isn’t always safe — avoid logging into personal accounts on public networks.",
                                        "Oversharing personal details like your school, birthday, or address can put you at risk.",
                                        "Not everything you read online is true — always fact-check from reliable sources.",
                                        "You can limit who sees your posts by adjusting your privacy settings.",
                                        "It’s okay to say no if someone asks for pictures or private info.",
                                        "Digital footprints are permanent — colleges and employers may see what you post.",
                                        "Gaming chats and communities can be fun but also risky — watch out for toxic behavior and scams."]

                
                if 0 <= elapsed < 15: # Determine the player's speed based on the elapsed time and display the corresponding text
                    animal_text = text_font1.render("You are a snail!", True, SNAIL_TEXT_COLOR)
                elif 15 <= elapsed < 30:
                    animal_text = text_font1.render("You are a turtle!", True, "green")
                elif 30 <= elapsed < 45:
                    animal_text = text_font1.render("You are a rabbit!", True, "white")
                elif 45 <= elapsed < 60:
                    animal_text = text_font1.render("You are a cheetah!", True, "yellow")
                elif 60 <= elapsed < 75:
                    animal_text = text_font1.render("You are a speeding bullet!", True, "orange")
                else:
                    animal_text = text_font1.render("You are faster than light!", True, "purple")

                animal_x = WIDTH / 2 - animal_text.get_width() / 2
                animal_y = lost_y + lost_text.get_height() + 20
                safety_text = text_font.render(random.choice(Internet_Safety_Facts), True, "gray")
                WIN.blit(animal_text, (animal_x, animal_y)) # Draw the player's speed text on the screen
                safety_x = WIDTH / 2 - safety_text.get_width() / 2
                safety_y = animal_y + animal_text.get_height() + 20
                WIN.blit(safety_text, (safety_x, safety_y))
                pygame.display.update()
                pygame.time.delay(4000)
                break
        else: # If the game has not started, reset the player's position and hitbox
            x_pos = Lanes[current_lane]
            player_rect = None

        draw(show_player, Lanes[current_lane], game_started, elapsed, stars, player_rect) # Draw the game elements on the screen
    time.sleep(5)
    pygame.quit()

if __name__ == "__main__": 
    main() 
