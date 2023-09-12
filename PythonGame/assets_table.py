from os import *  # path.join
# import os - os.path.join

sprites = {
    "ASTEROID": path.join("assets", "asteroid.png"),
    "BULLET": path.join("assets", "bullet.png"),
    "BACKGROUND": path.join("assets", "galaxy.jpg"),
    "PLAYER": path.join("assets", "rocket.png"),
    "ENEMY": path.join("assets", "ufo.png")
}

sounds = {
    "FIRE": path.join("music", "fire.ogg"),
    "MUSIC": path.join("music", "space.ogg")
}
