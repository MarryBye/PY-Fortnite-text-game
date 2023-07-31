import pygame
from random import randint
pygame.init()

file_path = "Python\\TestPyGame\\"

back = (0, 0, 0, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_window = pygame.display.set_mode((500, 500))
game_window.fill(back)

clock = pygame.time.Clock()

game_over = False


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
        self.image = pygame.image.load(f"{file_path}{filename}")

    def draw(self):
        game_window.blit(self.image, (self.rect.x, self.rect.y))


start_player_x, start_player_y = 250, 400
player_move_left, player_move_right = False, False
player_speed = 15
player_can_shoot = True

player_balls = []
ball_speed = 15
fire_rate = 30
need_to_wait = 0
player_points = 0

enemy_spawn_rate = 50
enemy_wait = enemy_spawn_rate
enemys = []
enemy_balls = []
enemy_speed = 5

player_spaceship = Picture(
    "player.png", start_player_x, start_player_y, 75, 75)
background = Picture("bg.png", 0, 0, 500, 500)

while not game_over:

    background.draw()

    if enemy_wait > 0:
        enemy_wait -= 1
    else:
        enemy_wait = enemy_spawn_rate
        enemy_x, enemy_y = randint(75, 425), randint(50, 175)
        enemy = Picture("enemy.png", enemy_x, enemy_y, 50, 50)
        enemy.dir = 1
        enemys.append(enemy)
        for enemy in enemys:
            enemy_ball = Picture(
                "enemy_ball.png", enemy.rect.x + enemy.rect.width / 2.5, enemy.rect.y, 15, 15)
            enemy_balls.append(enemy_ball)

    if need_to_wait > 0:
        need_to_wait -= 1

    for ball in player_balls:
        if ball.rect.y > 0:
            ball.rect.y -= ball_speed
            ball.draw()
        else:
            player_balls.remove(ball)

    for ball in enemy_balls:
        if ball.rect.y < 500:
            ball.rect.y += ball_speed
            ball.draw()
        else:
            enemy_balls.remove(ball)

    for enemy in enemys:
        enemy.rect.x += enemy_speed * enemy.dir
        if enemy.rect.x >= 450:
            enemy.dir = -1
        if enemy.rect.x <= 0:
            enemy.dir = 1
        enemy.draw()
        for ball in player_balls:
            if enemy.colliderect(ball.rect):
                enemys.remove(enemy)
                player_balls.remove(ball)
                player_points += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_move_left = True
            if event.key == pygame.K_d:
                player_move_right = True
            if event.key == pygame.K_z:
                if player_can_shoot and need_to_wait == 0:
                    player_can_shoot = False
                    player_ball = Picture("ball.png", player_spaceship.rect.x +
                                          player_spaceship.rect.width / 2.5, player_spaceship.rect.y, 15, 15)
                    player_balls.append(player_ball)
                    need_to_wait = fire_rate
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_move_left = False
            if event.key == pygame.K_d:
                player_move_right = False
            if event.key == pygame.K_z:
                player_can_shoot = True

    if player_move_right and player_spaceship.rect.x < 425:
        player_spaceship.rect.x += player_speed
    elif player_move_left and player_spaceship.rect.x > 0:
        player_spaceship.rect.x -= player_speed

    for ball in enemy_balls:
        if player_spaceship.colliderect(ball.rect):
            ball.fill()
            player_spaceship.fill()
            enemy_balls.remove(ball)
            end_text = Label(70, 200, 0, 0)
            end_text.set_text(
                f"Вы проиграли!\nОчки: {player_points}", 50, GREEN)
            end_text.draw()
            game_over = True

    player_spaceship.draw()

    pygame.display.update()
    clock.tick(30)
