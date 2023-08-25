from pygame import *

# Создание окна игры
window = display.set_mode((800, 600))
display.set_caption("Game")

# Создание спрайтов игры
background = transform.scale(
    image.load("background.png"),
    (800, 600)
)

sprite_1 = transform.scale(
    image.load("sprite1.png"),
    (100, 100)
)

sprite_1_x, sprite_1_y = 100, 100

sprite_2 = transform.scale(
    image.load("sprite2.png"),
    (100, 100)
)

sprite_2_x, sprite_2_y = 700, 100

game_over = False
clock = time.Clock()

while not game_over:

    window.blit(background, (0, 0))
    window.blit(sprite_1, (sprite_1_x, sprite_1_y))
    window.blit(sprite_2, (sprite_2_x, sprite_2_y))

    for e in event.get():
        if e.type == QUIT:
            game_over = True

    key_pressed = key.get_pressed()

    # Первый игрок
    if key_pressed[K_w] and sprite_1_y > 0:
        sprite_1_y -= 10

    if key_pressed[K_s] and sprite_1_y < 500:
        sprite_1_y += 10

    if key_pressed[K_a] and sprite_1_x > 0:
        sprite_1_x -= 10

    if key_pressed[K_d] and sprite_1_x < 700:
        sprite_1_x += 10

    # Второй игрок
    if key_pressed[K_UP] and sprite_2_y > 0:
        sprite_2_y -= 10

    if key_pressed[K_DOWN] and sprite_2_y < 500:
        sprite_2_y += 10

    if key_pressed[K_LEFT] and sprite_2_x > 0:
        sprite_2_x -= 10

    if key_pressed[K_RIGHT] and sprite_2_x < 700:
        sprite_2_x += 10

    display.update()
    clock.tick(144)
