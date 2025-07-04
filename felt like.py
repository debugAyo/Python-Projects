import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 480, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player properties
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 20
PLAYER_SPEED = 5

# Bullet properties
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
BULLET_SPEED = 7

# Enemy properties
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 20
ENEMY_SPEED = 2
ENEMY_DROP_INTERVAL = 30  # frames

# Fonts
font = pygame.font.SysFont(None, 36)

# Sounds
shoot_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.Sound.get_init() and pygame.mixer.Sound(buffer=b'\x00'*100) or pygame.mixer.Sound(buffer=b'\x00'*100)))
hit_sound = pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.Sound.get_init() and pygame.mixer.Sound(buffer=b'\x00'*100) or pygame.mixer.Sound(buffer=b'\x00'*100)))

# Player class
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, PLAYER_WIDTH, PLAYER_HEIGHT))

# Bullet class
def draw_bullet(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, BULLET_WIDTH, BULLET_HEIGHT))

# Enemy class
def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, ENEMY_WIDTH, ENEMY_HEIGHT))

# Main game function
def main():
    clock = pygame.time.Clock()
    player_x = WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = HEIGHT - PLAYER_HEIGHT - 10
    bullets = []
    enemies = []
    score = 0
    running = True
    frame_count = 0
    game_over = False

    while running:
        clock.tick(60)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH:
                player_x += PLAYER_SPEED
            if keys[pygame.K_SPACE]:
                if len(bullets) < 5 and (not bullets or bullets[-1][1] < player_y - 30):
                    bullets.append([player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player_y])
                    shoot_sound.play()

        # Update bullets
        for bullet in bullets[:]:
            bullet[1] -= BULLET_SPEED
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if not game_over and frame_count % ENEMY_DROP_INTERVAL == 0:
            enemy_x = random.randint(0, WIDTH - ENEMY_WIDTH)
            enemies.append([enemy_x, 0])
        frame_count += 1

        # Update enemies
        for enemy in enemies[:]:
            enemy[1] += ENEMY_SPEED
            if enemy[1] > HEIGHT:
                game_over = True
            # Check collision with bullets
            for bullet in bullets[:]:
                if (bullet[0] < enemy[0] + ENEMY_WIDTH and
                    bullet[0] + BULLET_WIDTH > enemy[0] and
                    bullet[1] < enemy[1] + ENEMY_HEIGHT and
                    bullet[1] + BULLET_HEIGHT > enemy[1]):
                    try:
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 1
                        hit_sound.play()
                    except ValueError:
                        pass

        # Draw player
        draw_player(player_x, player_y)
        # Draw bullets
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        # Draw enemies
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            over_text = font.render("GAME OVER", True, RED)
            screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 30))
            restart_text = font.render("Press R to Restart", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
            if keys[pygame.K_r]:
                main()
                return

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
