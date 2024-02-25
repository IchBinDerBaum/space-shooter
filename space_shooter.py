import pygame

pygame.init()
HEIGHT = 600
WIDTH = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (115, 215, 255)
BROWN = (123, 63, 0)
YELLOW = (255, 255, 0)
GRASGREEN = (34, 139, 34)
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("example")
clock = pygame.time.Clock()
shooterspeed = 10

playerheight = 45
playerwidth = 30
level = 1


def gettext(message, color, x, y, size):
    font = pygame.font.SysFont("Impact", size)
    text = font.render(message, True, color)
    place = text.get_rect(center=(x, y))
    sc.blit(text, place)


def gameover():
    sc.fill(RED)
    gettext("GAME OVER", LIGHTBLUE, WIDTH // 2, HEIGHT // 2, 96)
    pygame.display.flip()
    playing = True
    while playing:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                playing = False
    pygame.quit()
    exit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((playerwidth, playerheight))
        self.rect = self.surf.get_rect(center=(WIDTH // 2, HEIGHT - playerheight + 10))

    def draw(self):
        pygame.draw.polygon(sc, WHITE, (
            (self.rect.x + playerwidth // 2, self.rect.y), (self.rect.x, self.rect.y + playerheight),
            (self.rect.x + playerwidth, self.rect.y + playerheight)))

    def update(self):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((2, 6))
        self.rect = self.surf.get_rect(center=(x, y))

    def draw(self):
        pygame.draw.rect(sc, WHITE, self.rect)

    def update(self):
        if self.rect.bottom < 0:
            self.kill()
        self.rect.y -= 10


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.surf = pygame.Surface((width, 20))
        self.rect = self.surf.get_rect(center=(x, y))

    def draw(self):
        pygame.draw.rect(sc, WHITE, self.rect)

    def update(self):
        if freeze != 1:
            self.rect.move_ip(0, 1)
        collisions = pygame.sprite.spritecollideany(self, bullets)
        if collisions:
            self.kill()
            collisions.kill()
        if self.rect.bottom > HEIGHT:
            gameover()


def generateenemies():
    amount = level + 2 # 1 + level * 2   level + 2
    alienswidth = (WIDTH - 40) // amount - 20
    y = -30 * level * 2

    for i in range(amount):
        x = 30 + alienswidth // 2
        for j in range(amount):
            alien = Aliens(x, y, alienswidth)
            allsprites.add(alien)
            aliens.add(alien)
            x += alienswidth + 20
        y += 30


player = Player()
allsprites = pygame.sprite.Group()
allsprites.add(player)
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

freeze = 0

trigger = False

play = True
while play:
    clock.tick(FPS)

    if len(aliens) == 0 and len(bullets) == 0 and trigger:
        trigger = False
        level += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullets(player.rect.x + 15, player.rect.y)
                allsprites.add(bullet)
                bullets.add(bullet)
            if event.key == pygame.K_RETURN and not trigger:
                trigger = True
                generateenemies()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet = Bullets(player.rect.x + 15, player.rect.y)
                allsprites.add(bullet)
                bullets.add(bullet)

    keys = pygame.key.get_pressed()
    allsprites.update()
    sc.fill(BLACK)

    for sprite in allsprites:
        sprite.draw()
    if not trigger:
        gettext(f"Press 'Return' to switch to level {level}.", WHITE, WIDTH // 2, HEIGHT // 2, 36)

    pygame.display.flip()
pygame.quit()
