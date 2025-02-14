import pygame
import time
import random
import math

pygame.init()

# Define colors
hot_pink = (227, 59, 123)
white = (250, 250, 250)
cherry = (245, 42, 119)
tulip_yellow = (247, 234, 119)
purple = (204, 40, 237)
pink = (252, 192, 231)
burgundy = (120, 26, 64)
baby_yellow = (250, 245, 197)
black = (0, 0, 0)

# Set the dimensions of the game window
dis_width = 600
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

# Increase the snake block size 5x
snake_block = 50
snake_speed = 4

# Load a system font
font_style = pygame.font.SysFont("comicsansms", 35)
score_font = pygame.font.SysFont("comicsansms", 25)

def draw_heart(surface, color, position, size):
    x, y = position
    points = []
    for angle in range(0, 360, 1):
        angle_rad = math.radians(angle)
        x_offset = size * (10 * math.sin(angle_rad)**3)
        y_offset = -size * (8 * math.cos(angle_rad) - 5 * math.cos(2 * angle_rad) - 2 * math.cos(3 * angle_rad) - math.cos(4 * angle_rad))
        points.append((x + x_offset, y + y_offset))
    pygame.draw.polygon(surface, color, points)

def our_snake(snake_list):
    for i, x in enumerate(snake_list):
        pygame.draw.circle(dis, white, (x[0], x[1]), snake_block // 2)
        if i == 0:  # If it's the head of the snake
            # Draw eyes
            eye_radius = 5
            eye_offset = 10
            pygame.draw.circle(dis, black, (x[0] - eye_offset, x[1] - eye_offset), eye_radius)
            pygame.draw.circle(dis, black, (x[0] + eye_offset, x[1] - eye_offset), eye_radius)
            # Draw smile
            smile_radius = 15
            smile_thickness = 3
            pygame.draw.arc(dis, black, [x[0] - smile_radius, x[1], smile_radius * 2, smile_radius], math.radians(180), math.radians(360), smile_thickness)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2))
    dis.blit(mesg, text_rect)

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    heart_positions = [(random.randint(0, dis_width), random.randint(0, dis_height)) for _ in range(20)]
    heart_colors = [cherry, pink, burgundy]

    foods_eaten = 0  # Track the number of foods eaten

    direction = "RIGHT"  # Initialize starting direction

    while not game_over:

        while game_close == True:
            dis.fill(purple)
            message("You Lost! Press Q-Quit or P-Play Again", white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change = snake_block
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y1_change = -snake_block
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y1_change = snake_block
                    x1_change = 0
                    direction = "DOWN"

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(tulip_yellow)

        # Draw hearts on background
        for i, position in enumerate(heart_positions):
            color = heart_colors[i % len(heart_colors)]
            draw_heart(dis, color, position, 5)

        pygame.draw.circle(dis, white, (foodx, foody), snake_block // 2)
        snake_Head = [x1, y1]
        snake_List.insert(0, snake_Head)  # Insert the new head at the beginning
        if len(snake_List) > Length_of_snake:
            snake_List.pop()  # Remove the last segment to maintain the length

        for x in snake_List[1:]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_List)

        pygame.display.update()

        # Check if snake has eaten the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            foods_eaten += 1

        # Display message and end game after 7 foods eaten
        if foods_eaten == 7:
            dis.fill(tulip_yellow)
            message("Happy Valentine's Day!", hot_pink)
            pygame.display.update()
            time.sleep(3)
            game_over = True

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()