import pygame
import random
import pygame_menu 
from pygame_menu import themes 

# Initialize Pygame
pygame.init()

# Constants for game dimensions and colors
WIDTH, HEIGHT = 700, 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FPS = 60
RUNNING, PAUSED = 1, 0

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong.Game')

# Game variables
score_left, score_right = 0, 0
paddle_length, speed, winning_score  = 2, 2, 5
rx= random.choice([-4, 4])  # Random horizontal ball speed
ry=random.choice([-2, 2])   # Random vertical ball speed
speed_x, speed_y = rx, ry
paddle_width, paddle_length = 10, 150

# Rectangles for paddles and ball
left_paddle = pygame.Rect(0, 200, paddle_width, paddle_length)
right_paddle = pygame.Rect(WIDTH - paddle_width, 200, paddle_width, paddle_length)
square = pygame.Rect(WIDTH // 2, HEIGHT // 2, 20, 20)

# Menu bar options
menubar_options = {'Pause': [(100, 10), (100, 30)], 'Restart': [(300, 10), (100, 30)],
                   'Menu': [(500, 10), (100, 30)]}

# Fonts for text rendering
font_main = pygame.font.SysFont('Courier', 40)
side_font = pygame.font.SysFont('Courier', 30)
small_font = pygame.font.SysFont("Courier", 20)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Game state variables
running = True
move_allowed = False
game_restart = False
game_state = RUNNING 

# Main game loop function
def main():
    global move_allowed, game_state
    game_start = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RETURN:
                        running = False
                        pygame.quit()
                    case pygame.K_SPACE:
                        if not game_start:
                            game_start = True
                            move_allowed = True
                        elif game_state == PAUSED:
                            game_state = RUNNING
                        elif not game_restart:
                             pass
                        else:
                            reset_position()
                            clear_score()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    x, y = event.pos
                    for option, (pos, size) in menubar_options.items():
                        btn = pygame.Rect((*pos, *size))
                        if btn.collidepoint(x, y):
                            menubar_click(option)

        if game_state==PAUSED:

            screen.fill(BLACK)
            draw_elements()

            text_paused = font_main.render("PAUSED", True, WHITE)
            text_paused_rect = text_paused.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
            screen.blit(text_paused, text_paused_rect)

            text_space = side_font.render("Press SPACE to continue", True, WHITE)
            text_space_rect = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 +20))
            screen.blit(text_space, text_space_rect)

            pygame.display.update()

        else:

            screen.fill(BLACK)
            pygame.draw.rect(screen, BLUE, left_paddle)
            pygame.draw.rect(screen, RED, right_paddle)
    
        if not game_start:
            text_start = side_font.render("Press SPACE to start", True, WHITE)
            text_start_rect = text_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 -20))
            screen.blit(text_start, text_start_rect)
            text_exit = side_font.render("Press ENTER to exit", True, WHITE)
            text_exit_rect = text_exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(text_exit, text_exit_rect)
        else:
            if game_state == RUNNING:
                paddle_movement()
                update()
                draw_elements()

                if score_left == winning_score:
                    screen.fill(BLACK)
                    display_winner(player1_name.get_value())
                    reset_position()
                    clear_score()

                elif score_right == winning_score:
                    screen.fill(BLACK)
                    display_winner(player2_name.get_value())
                    reset_position()
                    clear_score()
        if game_start:           
             draw_menubar()   
        pygame.display.flip()
        clock.tick(FPS)

# Starts the game by resetting score and positions
def start_the_game():
    clear_score()
    reset_position()
    main()

# Draw the elements of the game (paddles, ball, score)
def draw_elements():
    global player1_name, player2_name, score_left, score_right
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, left_paddle)
    pygame.draw.rect(screen, RED, right_paddle)
    pygame.draw.rect(screen, WHITE, square)
    score = side_font.render(f'{player1_name.get_value()}: {score_left} - {score_right} :{player2_name.get_value()}', True, WHITE)
    score_place=(WIDTH // 2 - score.get_width() // 2, 50)
    screen.blit(score,score_place)

# Handle paddle movement
def paddle_movement():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= 5
    elif keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += 5

    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= 5
    elif keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += 5

# Update game elements (ball movement, score, and collision)
def update():
    global score_left, score_right, speed_x, speed_y, move_allowed

    if move_allowed:
        square.x += speed_x
        square.y += speed_y
        
        if square.colliderect(left_paddle) or square.colliderect(right_paddle):
            speed_x *= -1 

            if square.colliderect(left_paddle):
                part = (square.centery - left_paddle.top) / paddle_length
            else:
                part = (square.centery - right_paddle.top) / paddle_length

            if part < 0.3:  
                speed_y = ry * 1.5  
            elif part > 0.6: 
                speed_y = ry * -1.5 
            else: 
                speed_y = ry 

            square.x += speed_x
            square.y += speed_y

        if square.left <= 0:
            score_right += 1
            speed_x, speed_y = rx, ry
            square.center = (WIDTH // 2, HEIGHT // 2)

        elif square.right >= WIDTH:
            score_left += 1
            speed_x, speed_y = rx, ry
            square.center = (WIDTH // 2, HEIGHT // 2)

        if square.top <= 0 or square.bottom >= HEIGHT:
            speed_y *= -1  

# Reset the score
def clear_score():
    global score_left, score_right
    score_left, score_right = 0, 0

# Reset the position of the paddles and ball
def reset_position():
    global speed_x, speed_y, left_paddle, right_paddle,square
    speed_x, speed_y  = rx, ry
    square.center = (WIDTH // 2, HEIGHT // 2)
    left_paddle = pygame.Rect(0, 200, paddle_width, paddle_length)
    right_paddle = pygame.Rect(WIDTH - paddle_width, 200, paddle_width, paddle_length)

# Set the difficulty of the game
def set_difficulty(value,difficulty):
    global paddle_length, winning_score
    match difficulty:
        case 1:
            paddle_length, winning_score = 100, 5
        case 2:  
            paddle_length, winning_score = 50, 10
        case 3:  
            paddle_length, winning_score = 200, 3

# Open the settings menu
def open_settings():
    mainmenu._open(stngs)

# Menu setup and handling
def menu():
    global stngs, mainmenu, player1_name, player2_name
    mainmenu = pygame_menu.Menu('Pong Game', 600, 400, theme = themes.THEME_BLUE)
    player1_name = mainmenu.add.text_input('Player 1: ', default = 'Player 1',maxchar = 10)
    player2_name = mainmenu.add.text_input('Player 2: ', default = 'Player 2',maxchar = 10)
    mainmenu.add.button('Play', start_the_game)
    mainmenu.add.button('Settings', open_settings)
    mainmenu.add.button('Exit', pygame.quit)
    stngs = pygame_menu.Menu('Select Difficulty', 600, 400, theme = themes.THEME_BLUE)
    stngs.add.selector('Difficulty: ', [ ('Normal', 1),('Hard', 2),('Easy', 3)], onchange = set_difficulty)
    mainmenu.mainloop(screen)

# Draw the menu bar
def draw_menubar():
    for option, (position, size) in menubar_options.items():
        pygame.draw.rect(screen, 'gray', (*position, *size))
        menubar_text = small_font.render(option, True, BLACK)
        menubar_text_place = menubar_text.get_rect(center = (position[0] + size[0] // 2, position[1] + size[1] // 2))
        screen.blit(menubar_text, menubar_text_place)

# Render and manage menu bar clicks
def menubar_click(option):
    global game_state, menubar_options
    match option:
        case 'Pause':
            game_state = PAUSED
        case 'Restart':
            game_state = RUNNING
            clear_score()
            reset_position()
        case 'Menu':
            menu()

# Display winner message
def display_winner(winner):
    winner = font_main.render(f"The winner is {winner}", True, WHITE)
    winner_place = winner.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(winner, winner_place)

    play_again = font_main.render("Press SPACE to play again", True, WHITE)
    play_again_place = play_again.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(play_again, play_again_place)

    exit = font_main.render("Press ENTER to exit", True, WHITE)
    exit_place = exit.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(exit, exit_place)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    draw_elements()
                    pygame.display.update()
                    waiting = False
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    waiting = False

# Start the menu
menu()
