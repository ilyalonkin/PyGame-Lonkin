import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 74)
SMALL_FONT = pygame.font.Font(None, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лиса и Сыр")

bg_img = pygame.image.load('./assets/bg.jpg').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
cheese_img = pygame.image.load('./assets/cheese.png').convert_alpha()
crow_img = pygame.image.load('./assets/crow.png').convert_alpha()
fox_img_right = pygame.image.load('./assets/fox.png').convert_alpha()
fox_img_left = pygame.transform.flip(fox_img_right, True, False)

pygame.mixer.init()
background_sound = pygame.mixer.Sound('./assets/звук фона.mp3')
hit_sound = pygame.mixer.Sound('./assets/звук удара.mp3')
score_sound = pygame.mixer.Sound('./assets/начисление очков.mp3')
lose_sound = pygame.mixer.Sound('./assets/проигрыш.mp3')

all_sprites = pygame.sprite.Group()
all_sprites_cheeses = pygame.sprite.Group()


class Cheese(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(cheese_img, (int(SCREEN_WIDTH * 0.06), int(SCREEN_HEIGHT * 0.06)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.fall_speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.fall_speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            return True
        return False


class Crow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(crow_img, (int(SCREEN_WIDTH * 0.06), int(SCREEN_HEIGHT * 0.12)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def cheese_drop(self):
        cheese = Cheese(self.rect.centerx, self.rect.bottom)
        all_sprites_cheeses.add(cheese)


class Fox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(fox_img_right, (int(SCREEN_WIDTH * 0.20), int(SCREEN_HEIGHT * 0.35)))
        self.image_left = pygame.transform.scale(fox_img_left, (int(SCREEN_WIDTH * 0.20), int(SCREEN_HEIGHT * 0.35)))
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.88)

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_d]:
            self.rect.x += 5
            self.image = self.image_right
        elif pressed_keys[pygame.K_a]:
            self.rect.x -= 5
            self.image = self.image_left
        self.rect.clamp_ip(screen.get_rect())


def start_screen():
    screen.blit(bg_img, (0, 0))
    title = FONT.render("Лиса и Сыр", True, WHITE)
    instruction = SMALL_FONT.render("Нажмите ПРОБЕЛ, чтобы начать", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2))
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


def load_scores():
    try:
        with open("scores.txt", "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        scores = [0] * 3
    return scores


def save_scores(scores):
    with open("scores.txt", "w") as file:
        for score in scores:
            file.write(f"{score}\n")


def update_high_scores(scores, new_score):
    scores.append(new_score)
    scores.sort(reverse=True)
    return scores[:3]


def game_over_screen(score):
    scores = load_scores()
    scores = update_high_scores(scores, score)
    save_scores(scores)

    screen.blit(bg_img, (0, 0))
    game_over_text = FONT.render("Игра Окончена", True, WHITE)
    score_text = SMALL_FONT.render(f"Ваш счет: {score}", True, WHITE)
    high_scores_text = SMALL_FONT.render("Топ-3 рекорда:", True, WHITE)
    instruction = SMALL_FONT.render("Нажмите ПРОБЕЛ, чтобы начать заново", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(high_scores_text, (SCREEN_WIDTH // 2 - high_scores_text.get_width() // 2, SCREEN_HEIGHT // 2))

    for i, high_score in enumerate(scores[:3]):
        score_display = SMALL_FONT.render(f"{i + 1}. {high_score}", True, WHITE)
        screen.blit(score_display,
                    (SCREEN_WIDTH // 2 - score_display.get_width() // 2, SCREEN_HEIGHT // 2 + 50 + i * 40))

    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT * 3 // 4))
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


def main():
    global all_sprites, all_sprites_cheeses

    all_sprites = pygame.sprite.Group()
    all_sprites_cheeses = pygame.sprite.Group()

    fox = Fox()
    crow1 = Crow(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.35)
    crow2 = Crow(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.32)
    crow3 = Crow(SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.32)

    all_sprites.add(fox, crow1, crow2, crow3)
    fox_sprites = pygame.sprite.Group(fox)

    clock = pygame.time.Clock()
    score = 0
    speed = 1
    drop_interval = 2000
    pygame.time.set_timer(pygame.USEREVENT + 1, drop_interval)

    background_sound.play(-1)

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT + 1:
                random.choice([crow1, crow2, crow3]).cheese_drop()

        # Обновление
        pressed_keys = pygame.key.get_pressed()
        all_sprites.update(pressed_keys)
        for cheese in all_sprites_cheeses:
            if cheese.update():
                lose_sound.play()
                game_over = True

        hits = pygame.sprite.groupcollide(fox_sprites, all_sprites_cheeses, False, True)
        for _ in hits:
            score += 1
            hit_sound.play()
            score_sound.play()

        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        all_sprites_cheeses.draw(screen)

        score_text = SMALL_FONT.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

        if game_over:
            background_sound.stop()
            game_over_screen(score)
            return

    pygame.quit()


if __name__ == "__main__":
    while True:
        start_screen()
        main()