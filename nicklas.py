import pygame
import sys
import random

# --- Config ---
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10  # speed of the snake

# Colors (R, G, B)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
GRAY   = (40, 40, 40)

def draw_grid(surface):
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))

def draw_snake(surface, snake_body):
    for segment in snake_body:
        pygame.draw.rect(surface, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(surface, food_pos):
    pygame.draw.rect(surface, RED, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

def random_food_position(snake_body):
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if [x, y] not in snake_body:
            return [x, y]

def show_text(surface, text, size, color, center):
    font = pygame.font.SysFont("arial", size, bold=True)
    render = font.render(text, True, color)
    rect = render.get_rect(center=center)
    surface.blit(render, rect)

def game_over_screen(surface, score):
    surface.fill(BLACK)
    show_text(surface, "GAME OVER", 40, RED, (WIDTH // 2, HEIGHT // 3))
    show_text(surface, f"Score: {score}", 30, WHITE, (WIDTH // 2, HEIGHT // 2))
    show_text(surface, "Press SPACE to play again or ESC to quit", 20, BLUE, (WIDTH // 2, HEIGHT * 2 // 3))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Initial snake
    snake_body = [
        [WIDTH // 2, HEIGHT // 2],
        [WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2],
        [WIDTH // 2 - 2 * BLOCK_SIZE, HEIGHT // 2],
    ]
    direction = "RIGHT"

    food_pos = random_food_position(snake_body)
    score = 0

    running = True
    while running:
        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # --- Move snake ---
        head_x, head_y = snake_body[0]

        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        new_head = [head_x, head_y]

        # --- Check collisions with walls ---
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT
        ):
            game_over_screen(screen, score)
            return main()  # restart game

        # --- Check collisions with itself ---
        if new_head in snake_body:
            game_over_screen(screen, score)
            return main()  # restart game

        # Insert new head
        snake_body.insert(0, new_head)

        # --- Check if ate food ---
        if new_head == food_pos:
            score += 1
            food_pos = random_food_position(snake_body)
        else:
            snake_body.pop()  # remove tail if no food eaten

        # --- Drawing ---
        screen.fill(BLACK)
        draw_grid(screen)
        draw_snake(screen, snake_body)
        draw_food(screen, food_pos)

        # Show score
        show_text(screen, f"Score: {score}", 20, WHITE, (60, 15))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
