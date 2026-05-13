import pygame

pygame.init()
font = pygame.font.SysFont(None, 24)

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple 2D Platformer")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

def create_princess_image():
    image = pygame.Surface((50, 50), pygame.SRCALPHA)
    image.fill((0, 0, 0, 0))
    # Hair
    pygame.draw.ellipse(image, (255, 223, 0), (0, 0, 50, 34))
    pygame.draw.rect(image, (255, 223, 0), (0, 18, 50, 14))
    # Dress
    pygame.draw.polygon(image, (255, 192, 203), [(10, 24), (40, 24), (45, 48), (5, 48)])
    pygame.draw.rect(image, (235, 150, 180), (10, 24, 30, 12))
    # Face
    pygame.draw.circle(image, (255, 218, 185), (25, 16), 9)
    # Eyes
    pygame.draw.circle(image, (0, 0, 255), (20, 16), 2)
    pygame.draw.circle(image, (0, 0, 255), (30, 16), 2)
    pygame.draw.circle(image, (0, 0, 0), (20, 16), 1)
    pygame.draw.circle(image, (0, 0, 0), (30, 16), 1)
    # Crown
    pygame.draw.polygon(image, (255, 215, 0), [(16, 6), (20, 2), (24, 6), (28, 2), (32, 6), (38, 10), (12, 10)])
    pygame.draw.rect(image, (255, 215, 0), (16, 10, 18, 4))
    # Details
    pygame.draw.rect(image, (255, 192, 203), (18, 32, 14, 14))
    pygame.draw.rect(image, (255, 255, 255), (19, 34, 3, 3))
    pygame.draw.rect(image, (255, 255, 255), (28, 34, 3, 3))
    return image

player_image = create_princess_image()

# Levels
levels = [
    [  # level 1
        pygame.Rect(0, 550, 800, 50),
        pygame.Rect(200, 450, 200, 20),
        pygame.Rect(500, 350, 200, 20),
    ],
    [  # level 2
        pygame.Rect(0, 550, 800, 50),
        pygame.Rect(100, 450, 100, 20),
        pygame.Rect(300, 350, 100, 20),
        pygame.Rect(500, 250, 100, 20),
        pygame.Rect(700, 150, 100, 20),
    ],
    [  # level 3
        pygame.Rect(0, 550, 800, 50),
        pygame.Rect(50, 450, 50, 20),
        pygame.Rect(150, 350, 50, 20),
        pygame.Rect(250, 250, 50, 20),
        pygame.Rect(350, 150, 50, 20),
        pygame.Rect(450, 50, 50, 20),
    ]
]

levels_coins = [
    [pygame.Rect(250, 430, 20, 20), pygame.Rect(550, 330, 20, 20)],
    [pygame.Rect(150, 430, 20, 20), pygame.Rect(350, 330, 20, 20), pygame.Rect(750, 130, 20, 20)],
    [pygame.Rect(100, 430, 20, 20), pygame.Rect(200, 330, 20, 20), pygame.Rect(300, 230, 20, 20), pygame.Rect(400, 130, 20, 20), pygame.Rect(500, 30, 20, 20)]
]

levels_goals = [
    pygame.Rect(750, 300, 50, 50),
    pygame.Rect(750, 100, 50, 50),
    pygame.Rect(750, 0, 50, 50)
]

levels_obstacles = [
    [pygame.Rect(360, 530, 40, 20), pygame.Rect(620, 430, 40, 20)],
    [pygame.Rect(220, 430, 40, 20), pygame.Rect(520, 230, 40, 20)],
    [pygame.Rect(180, 330, 40, 20), pygame.Rect(320, 230, 40, 20), pygame.Rect(460, 130, 40, 20)]
]

# Game state
current_level = 0
platforms = levels[current_level]
coins = [coin.copy() for coin in levels_coins[current_level]]
goal = levels_goals[current_level]
obstacles = levels_obstacles[current_level]
score = 0

# Player
player = pygame.Rect(100, 500, 50, 50)
player_vel_x = 0
player_vel_y = 0
gravity = 0.5
on_ground = False
jumps_remaining = 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_vel_x = -5
            elif event.key == pygame.K_RIGHT:
                player_vel_x = 5
            elif event.key == pygame.K_SPACE and jumps_remaining > 0:
                player_vel_y = -10
                jumps_remaining -= 1
                on_ground = False
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_vel_x = 0

    # Update player
    player_vel_y += gravity
    player.x += player_vel_x
    player.y += player_vel_y

    # Collision with platforms
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform):
            if player_vel_y > 0:  # falling
                player.bottom = platform.top
                player_vel_y = 0
                on_ground = True
                jumps_remaining = 2
            elif player_vel_y < 0:  # jumping
                player.top = platform.bottom
                player_vel_y = 0

    # Check coin collision
    for coin in coins[:]:
        if player.colliderect(coin):
            score += 10
            coins.remove(coin)

    # Check obstacle collision
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            score = max(score - 5, 0)
            player.x = 100
            player.y = 500
            player_vel_x = 0
            player_vel_y = 0
            jumps_remaining = 2
            break

    # Check goal
    if player.colliderect(goal):
        if current_level < 2:
            current_level += 1
            platforms = levels[current_level]
            coins = [coin.copy() for coin in levels_coins[current_level]]
            goal = levels_goals[current_level]
            obstacles = levels_obstacles[current_level]
            player.x = 100
            player.y = 500
            player_vel_x = 0
            player_vel_y = 0
            on_ground = False
            jumps_remaining = 2
        else:
            running = False

    # Keep player in bounds
    if player.left < 0:
        player.left = 0
    if player.right > WIDTH:
        player.right = WIDTH
    if player.top < 0:
        player.top = 0
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
        on_ground = True
        player_vel_y = 0

    # Draw
    screen.fill(BLACK)
    screen.blit(player_image, player)
    for platform in platforms:
        pygame.draw.rect(screen, WHITE, platform)
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, coin.center, 10)
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)
        for i in range(4):
            spike_x = obstacle.left + i * 10
            pygame.draw.polygon(screen, BLACK, [(spike_x, obstacle.bottom), (spike_x + 5, obstacle.top), (spike_x + 10, obstacle.bottom)])
    pygame.draw.rect(screen, GREEN, goal)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    level_text = font.render(f"Level: {current_level + 1}", True, WHITE)
    screen.blit(level_text, (10, 40))
    jumps_text = font.render(f"Jumps: {jumps_remaining}", True, WHITE)
    screen.blit(jumps_text, (10, 70))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
if not running:
    print(f"You win! Final score: {score}")