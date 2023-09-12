from pygame import *
from assets_table import *
from classes import *
from langs import *

lang = "UKR"

game_run, game_finish = True, False

display.set_caption(languages[lang]["GAMENAME"])

clock = time.Clock()

background = MakeImage(sprites["BACKGROUND"], win_width, win_height)

player = Player(sprites["PLAYER"], 5, win_height - 100, 75, 100, 5)

monsters = sprite.Group()
for i in range(6):
    monster = Enemy(sprites["ENEMY"], randint(
        80, win_width - 80), -50, 80, 50, randint(3, 8))
    monsters.add(monster)

mixer.init()
mixer.music.load(sounds["MUSIC"])
mixer.music.play()

font.init()
font_main = font.Font(None, 48)


while game_run:
    for e in event.get():
        if e.type == QUIT:
            game_run = False

    if not game_finish:
        window.blit(background, (0, 0))

        kills_text = font_main.render(
            languages[lang]["SCORE_KILLS"] + str(kills), True, (255, 255, 255))
        window.blit(kills_text, (10, 10))

        losts_text = font_main.render(
            languages[lang]["SCORE_MISSES"] + str(losts), True, (255, 255, 255))
        window.blit(losts_text, (10, 60))

        player.reset()  # отрисовка
        player.update()  # управление

        monsters.draw(window)
        monsters.update()

        display.update()

    clock.tick(60)
