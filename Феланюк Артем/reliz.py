import pygame
import random

# Ініціалізація Pygame
pygame.init()

# Константи для вікна гри
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Константи для гри
GAP = 200
GRAVITY = 0.25
FPS = 60

# Завантаження картинок
BIRD_IMAGE = pygame.image.load("bird.png")
BIRD_WIDTH, BIRD_HEIGHT = 40, 30
BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT))
BACKGROUND_IMAGE = pygame.image.load("background.png")
PIPE_WIDTH, PIPE_HEIGHT = 60, 400
PIPE_TOP_IMAGE = pygame.image.load("pipe_top.png")
PIPE_BOTTOM_IMAGE = pygame.image.load("pipe_bottom.png")

# Клас для фону
class Background:
    def __init__(self):
        self.image = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

    def draw(self):
        WIN.blit(self.image, (0, 0))

# Клас для труб
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - GAP - 50)

    def draw(self):
        WIN.blit(PIPE_TOP_IMAGE, (self.x, self.height - PIPE_TOP_IMAGE.get_height()))
        WIN.blit(PIPE_BOTTOM_IMAGE, (self.x, self.height + GAP))

# Клас для пташки
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2 - BIRD_HEIGHT // 2
        self.vel = 0

    def flap(self):
        self.vel = -7

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

    def draw(self):
        WIN.blit(BIRD_IMAGE, (self.x, self.y))

# Функція для малювання рахунку
def draw_score(score):
    font = pygame.font.SysFont(None, 50)
    text = font.render(str(score), True, (255, 255, 255))
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, 50))

# Функція для виявлення колізій
def collision(bird, pipes):
    for pipe in pipes:
        if bird.x + BIRD_WIDTH > pipe.x and bird.x < pipe.x + PIPE_TOP_IMAGE.get_width():
            if bird.y < pipe.height or bird.y + BIRD_HEIGHT > pipe.height + GAP:
                return True
    return False

# Головна функція гри
def main():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Додавання нової труби
        if pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

        # Оновлення стану пташки та труб
        bird.update()
        for pipe in pipes:
            pipe.x -= 3

        # Перевірка колізій
        if collision(bird, pipes):
            running = False

        # Видалення труб, які виходять за межі екрану
        if pipes[0].x < -PIPE_TOP_IMAGE.get_width():
            pipes.pop(0)
            score += 1

        # Малювання екрану
        Background().draw()
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        draw_score(score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
