from pygame import *

# Создали окно игры и назвали его

window_width, window_height = 800, 600
window = display.set_mode((window_width, window_height))
display.set_caption("Лабиринт")

# Наш класс, основанный на готовом из pygame


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()

        self.image = transform.scale(
            image.load(img),
            (w, h)
        )

        self.speed = speed
        self.rect = self.image.get_rect()  # хитбокс картинки
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] or keys_pressed[K_UP]:
            if self.rect.y > 0:
                self.rect.y -= self.speed
        if keys_pressed[K_a] or keys_pressed[K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys_pressed[K_s] or keys_pressed[K_DOWN]:
            if self.rect.y < window_height:
                self.rect.y += self.speed
        if keys_pressed[K_d] or keys_pressed[K_RIGHT]:
            if self.rect.x < window_width:
                self.rect.x += self.speed


class Enemy(GameSprite):
    direction = "left"

    def update(self, x_start=100, x_end=0):
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x <= x_end:
                self.direction = "right"
        else:
            self.rect.x += self.speed
            if self.rect.x >= x_start:
                self.direction = "left"


class Wall(sprite.Sprite):
    def __init__(self, color, x, y, w, h):
        super().__init__()

        self.image = Surface((w, h))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        walls.append(self)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


def makeImage(img, w, h):
    return transform.scale(image.load(img), (w, h))


background = makeImage("background.jpg", 800, 600)

enemy_start_x, enemy_start_y = 300, 400
enemy_x_start, enemy_x_end = 300, 0

player = Player("hero.png", 100, 500, 35, 35, 5)
enemy = Enemy("cyborg.png", enemy_start_x, enemy_start_y, 50, 50, 5)
treasure = GameSprite("treasure.png", 700, 500, 75, 75, 5)

walls = []

# Wall(цвет, х, у, ширина, высота)
# Вертикальная стенка - ширина < высота
# Горизонтальная стенка - ширина > высота
# начальная координата - 100, конечная - 400
Wall((255, 128, 67), 100, 100, 300, 8)
Wall((255, 128, 67), 400, 100, 8, 150)
Wall((255, 128, 67), 400, 246, 150, 8)
Wall((255, 128, 67), 100, 108, 8, 350)
Wall((255, 128, 67), 187, 378, 150, 8)
Wall((255, 128, 67), 187, 100, 8, 278)
Wall((255, 128, 67), 278, 246, 120, 8)
Wall((255, 128, 67), 278, 100, 8, 150)
Wall((255, 128, 67), 337, 100, 8, 82)
Wall((255, 128, 67), 337, 246, 8, 82)
Wall((255, 128, 67), 100, 100, 300, 8)
Wall((255, 128, 67), 400, 100, 8, 150)
Wall((255, 128, 67), 400, 246, 150, 8)
Wall((255, 128, 67), 100, 108, 8, 350)
Wall((255, 128, 67), 187, 378, 150, 8)
Wall((255, 128, 67), 682, 100, 8, 500)
Wall((255, 128, 67), 194, 451, 490, 8)
Wall((255, 128, 67), 525, 320, 100, 8)
Wall((255, 128, 67), 575, 275, 8, 100)
Wall((255, 128, 67), 485, 100, 200, 8)
Wall((255, 128, 67), 0, 455, 108, 8)

# Вертикальные стенки, чтобы закрыть квадрат
Wall((255, 128, 67), 250, 100, 8, 150)
Wall((255, 128, 67), 250, 246, 8, 142)

finish = False
game_over = False
clock = time.Clock()
fps = 60

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()

loose_sound = mixer.Sound("kick.ogg")
win_sound = mixer.Sound("money.ogg")

font.init()
font = font.Font(None, 72)
win_text = font.render("Победа!!!", True, (220, 120, 0))
loose_text = font.render("Поражение...", True, (130, 0, 0))

while not game_over:

    for e in event.get():
        if e.type == QUIT:
            game_over = True
        if e.type == MOUSEMOTION:
            print(e.pos)

    if not finish:

        window.blit(background, (0, 0))

        player.reset()
        enemy.reset()
        treasure.reset()

        for wall in walls:
            wall.reset()

            if sprite.collide_rect(player, wall):
                loose_sound.play()
                player.rect.x = 100
                player.rect.y = 500

        player.update()
        enemy.update(enemy_x_start, enemy_x_end)

        if sprite.collide_rect(player, enemy):
            finish = True
            loose_sound.play()
            window.blit(loose_text, (200, 200))

        if sprite.collide_rect(player, treasure):
            finish = True

            win_sound.play()
            window.blit(win_text, (200, 200))

    display.update()
    clock.tick(fps)
