import pygame
import sys
import math

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Hockey")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

# Game Objects
PADDLE_RADIUS = 20
PUCK_RADIUS = 15

# Positions
paddle1_pos = [100, HEIGHT // 2]
paddle2_pos = [WIDTH - 100, HEIGHT // 2]
puck_pos = [WIDTH // 2, HEIGHT // 2]
puck_vel = [4, 4]

# Score
score1, score2 = 0, 0
game_on = True
font = pygame.font.Font(None, 50)

# Clock
clock = pygame.time.Clock()


def draw():
    screen.fill(BLACK)

    pygame.draw.circle(screen, WHITE, puck_pos, PUCK_RADIUS)
    pygame.draw.circle(screen, BLUE, paddle1_pos, PADDLE_RADIUS)
    pygame.draw.circle(screen, RED, paddle2_pos, PADDLE_RADIUS)

    #center Line
    pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)

    # Goal rects
    goal_width = 10
    pygame.draw.rect(screen, WHITE, (0, 0, goal_width, HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - goal_width, 0, goal_width, HEIGHT))

    #Scores
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    pygame.display.flip()


def move_puck():
    global puck_pos, puck_vel, score1, score2, game_on

    puck_pos[0] += puck_vel[0]
    puck_pos[1] += puck_vel[1]

    #Wall Bounce
    if puck_pos[1] <= PUCK_RADIUS or puck_pos[1] >= HEIGHT - PUCK_RADIUS:
        puck_vel[1] = -puck_vel[1]

    #Goal detection
    if puck_pos[0] <= 0:
        score2 += 1
        if score2 == 7:
            draw()
            show_winner("Human wins")
            game_on = False
        reset_puck()
    elif puck_pos[0] >= WIDTH:
        score1 += 1
        if score1 == 7:
            draw()
            show_winner("AI wins")
            game_on = False
        reset_puck()

    #Paddle collision
    if distance(puck_pos, paddle1_pos) < PADDLE_RADIUS + PUCK_RADIUS:
        puck_vel[0] = abs(puck_vel[0])
    elif distance(puck_pos, paddle2_pos) < PADDLE_RADIUS + PUCK_RADIUS:
        puck_vel[0] = -abs(puck_vel[0])


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def reset_puck():
    global puck_pos, puck_vel
    puck_pos = [WIDTH // 2, HEIGHT // 2]
    puck_vel = [4,4]

def show_winner(text):
    winner_text = font.render(text, True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

def minimax_move():
    # Very basic minimax-style movement: go toward the puck if it's on the left half
    if puck_pos[0] < WIDTH // 2:
        if paddle1_pos[0] < puck_pos[0] and paddle1_pos[0] < WIDTH // 2 - PADDLE_RADIUS:
            paddle1_pos[0] += 4
        elif paddle1_pos[0] > puck_pos[0] and paddle1_pos[0] > PADDLE_RADIUS:
            paddle1_pos[0] -= 4

        if paddle1_pos[1] < puck_pos[1] and paddle1_pos[1] < HEIGHT - PADDLE_RADIUS:
            paddle1_pos[1] += 4
        elif paddle1_pos[1] > puck_pos[1] and paddle1_pos[1] > PADDLE_RADIUS:
            paddle1_pos[1] -= 4
    else:
        # Return to center if puck is far
        if paddle1_pos[0] < 100:
            paddle1_pos[0] += 2
        elif paddle1_pos[0] > 100:
            paddle1_pos[0] -= 2

        if paddle1_pos[1] < HEIGHT // 2:
            paddle1_pos[1] += 2
        elif paddle1_pos[1] > HEIGHT // 2:
            paddle1_pos[1] -= 2


# Game Loop
while game_on:
    clock.tick(60)  #60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player 1 AI - Minimax-style greedy movement
    minimax_move()

    # Player 2 - Arrow Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle2_pos[1] > PADDLE_RADIUS:
        paddle2_pos[1] -= 5
    if keys[pygame.K_DOWN] and paddle2_pos[1] < HEIGHT - PADDLE_RADIUS:
        paddle2_pos[1] += 5
    if keys[pygame.K_LEFT] and paddle2_pos[0] > WIDTH//2 + PADDLE_RADIUS:
        paddle2_pos[0] -= 5
    if keys[pygame.K_RIGHT] and paddle2_pos[0] < WIDTH - PADDLE_RADIUS:
        paddle2_pos[0] += 5

    move_puck()
    draw()


