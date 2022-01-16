import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'data')

WIDTH = 480
HEIGHT = 600
FPS = 60


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starfall")
clock = pygame.time.Clock()


def draw_text(up, text, size, x, y):
    shrift_name = pygame.font.match_font('arial')
    shrift = pygame.font.Font(shrift_name, size)
    text_up = shrift.render(text, True, (255, 255, 255))
    text_down = text_up.get_rect()
    text_down.midtop = (x, y)
    up.blit(text_up, text_down)

def show_start_screen():
    screen.blit(background, background_rect)
    f = open('records.txt', 'r')
    recst = f.read()
    draw_text(screen, "STARFALL", 70, 240, 150)
    draw_text(screen, "Управление стрелками лево, право", 20, 240, 300)
    pstrec = "Ваш рекорд: " + str(recst)
    draw_text(screen, pstrec, 20, 240, 350)
    draw_text(screen, "Нажмите SPACE, чтобы начать игру", 18, 240, 400)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def show_back_screen():
    screen.blit(background, background_rect)
    f = open('records.txt', 'r')
    recgo = f.read()
    draw_text(screen, "STARFALL", 70, 240, 150)
    draw_text(screen, "Вы проиграли!", 20, 240, 300)
    pgorec = "Ваш рекорд: " + str(recgo)
    draw_text(screen, pgorec, 20, 240, 350)
    draw_text(screen, "Нажмите SPACE, чтобы начать с начала", 18, 240, 400)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.radius = 16
        #pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(meteor_img, (50, 38))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.radius = 19
        #pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


background = pygame.image.load(path.join(img_dir, "fon.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "stickman.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir, "star.png")).convert()

all_sprites = pygame.sprite.Group()
stars = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


start = True
game_over = False
running = True

while running:
    if start:
        show_start_screen()
        sec = 0
        start = False
        all_sprites = pygame.sprite.Group()
        stars = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(25):
            s = Star()
            all_sprites.add(s)
            stars.add(s)
        score = 0

    if game_over:
        show_back_screen()
        sec = 0
        game_over = False
        all_sprites = pygame.sprite.Group()
        stars = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(25):
            s = Star()
            all_sprites.add(s)
            stars.add(s)
        score = 0
    clock.tick(FPS)
    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, stars, False, pygame.sprite.collide_circle)
    if hits:
        game_over = True


    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    psec = "Score: " + str(sec)
    draw_text(screen, str(psec), 18, WIDTH / 2, 10)
    sec += 1
    f = open('records.txt', 'r')
    rec = f.read()
    f.close()
    if sec > int(rec):
        f = open('records.txt', 'w')
        f.write(str(sec))
        f.close()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
