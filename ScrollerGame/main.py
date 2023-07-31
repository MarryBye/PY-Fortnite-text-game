import pygame
from random import randint

pygame.init()

back = (0, 0, 0, 0)
game_window = pygame.display.set_mode((1450, 800))
clock = pygame.time.Clock()


class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(game_window, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Label(Area):
    def set_text(self, text, f_size=12, t_color=(159, 200, 20)):
        self.image = pygame.font.SysFont(
            "verdana", f_size).render(text, True, t_color)

    def draw(self, s_x=0, s_y=0):
        self.fill()
        game_window.blit(self.image, (self.rect.x+s_x, self.rect.y+s_y))


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        game_window.blit(self.image, (self.rect.x, self.rect.y))


fon = Picture("menu.jpg", 0, 0, 1299, 651)
play = Picture("play_button.png", 605, 300, 446, 189)
sett = Picture("sett.png", 400, 300, 189, 189)

start_fon = Picture("prologue.png", 0, 0, 1550, 800)
tp = Picture("tp.png", 500, 0, 256, 256)
ch1 = Picture("ch1.png", 500, 330, 100, 150)

bg_game = Picture("bg.jpg", 0, 0, 7793, 650)
bg_game.type = "WORLD"


game_start = False
game_over = False

move_left, move_right, move_up = False, False, False
game_started_main = False

anim_left = []
anim_right = []

inventory = []

enemys = []

player_bullets = []

items_to_scroll = [bg_game]

# enemys_cords = []

wait_anim = 5

wait_enemy = 80

wait_to_fire = 30

ground_y = 600

points = 0

equipped_weapon = -1

bullet_picture = "bullet_left.png"
bullet_direction = 1

while not game_over:
    if wait_anim > 0:
        wait_anim -= 1
    if game_started_main:  # игра
        if wait_to_fire > 0:
            wait_to_fire -= 1
        for item in items_to_scroll:
            item.draw()
            if item.type == "WEAPON" and ch1.colliderect(item.rect):
                inventory.append(item)
                items_to_scroll.remove(item)
                item.fill()

        ch1.draw()

        score_text = Label(0, 0, 0, 0)
        score_text.set_text(
            "Очки: " + str(points), 48, (255, 0, 0))
        score_text.draw(0, 0)

        if wait_enemy > 0:
            wait_enemy -= 1
        else:
            enemy_cord_x = randint(150, 10680)
            wait_enemy = 80
            if len(enemys) < 25:
                new_enemy = Picture("enemy.png", randint(
                    150, 10680), ground_y, 100, 150)
                enemys.append(new_enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_1:
                    if len(inventory) != 0:
                        equipped_weapon = 1
                if event.key == pygame.K_SPACE:
                    if equipped_weapon != -1:
                        if inventory[equipped_weapon - 1].weapon_name == "PISTOL":
                            if wait_to_fire <= 0:
                                wait_to_fire = 30
                                if move_left:
                                    bullet_picture = "bullet_left.png"
                                    bullet_direction = -1
                                elif move_right:
                                    bullet_picture = "bullet_right.png"
                                    bullet_direction = 1
                                new_bullet = Picture(
                                    bullet_picture, ch1.rect.x, ch1.rect.y + 25, 66, 27)
                                new_bullet.direction = bullet_direction
                                player_bullets.append(new_bullet)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False

        for bullet in player_bullets:
            bullet.draw()
            bullet.rect.x += bullet.direction * 25
            for enemy in enemys:
                if enemy in enemys and bullet in player_bullets:
                    if bullet.colliderect(enemy.rect):
                        player_bullets.remove(bullet)
                        enemys.remove(enemy)
                        enemy.fill()
                        bullet.fill()
                        points += 1

        if move_left:
            ch1.rect.x -= 10
            if ch1.rect.x <= 100 and bg_game.rect.x < 0:
                for item in items_to_scroll:
                    item.rect.x += 10
                ch1.rect.x += 10
        if move_right:
            ch1.rect.x += 10
            if ch1.rect.x >= 400 and bg_game.rect.x > -7793:
                for item in items_to_scroll:
                    item.rect.x -= 10
                ch1.rect.x -= 10

        for enemy in enemys:
            # i = 1
            # enemy_text = Label(0, 100 + (100 * i), 0, 0)
            # enemy_text.set_text(
            #     "Противник №" + str(i) + ": " + str(enemy.rect.x), 48, (255, 0, 0))
            # enemys_cords.append(enemy_text)
            enemy.draw()
            if enemy.rect.x < ch1.rect.x:
                enemy.rect.x += 10
            else:
                enemy.rect.x -= 10
            if enemy.colliderect(ch1.rect):
                lose_screen = Label(0, 0, 1450, 800, (225, 225, 225))
                lose_screen.set_text(
                    "Вы умерли! Очки: " + str(points), 100, (255, 0, 0))
                lose_screen.draw(200, 400)
                game_over = True
            # i += 1

        # enemys_cords.clear()

        # for cord in enemys_cords:
        #     cord.draw()

    elif not game_start:  # меню игры
        fon.draw()
        sett.fill()
        play.fill()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                M_X, M_Y = event.pos[0], event.pos[1]
                if play.collidepoint(M_X, M_Y):
                    game_start = True
        sett.draw()
        play.draw()

    elif game_start:  # пролог
        start_fon.draw()
        tp.draw()
        ch1.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_w:
                    move_up = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_w:
                    move_up = False

        if move_left:
            ch1.rect.x -= 10
        if move_right:
            ch1.rect.x += 10
        if move_up:
            ch1.rect.y -= 10

        if ch1.colliderect(tp.rect):
            game_started_main = True
            bg_game.rect.x = 0
            bg_game.rect.y = 0
            ch1.rect.x = 150
            ch1.rect.y = ground_y
            move_right = False
            move_left = False
            move_up = False

            pistol_weapon = Picture(
                "pistol_weapon.png", 500, ground_y, 100, 100)
            pistol_weapon.type = "WEAPON"
            pistol_weapon.weapon_name = "PISTOL"
            items_to_scroll.append(pistol_weapon)

    clock.tick(30)
    pygame.display.update()
