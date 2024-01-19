from functools import cache
import os
from sys import exit
from threading import Thread
from time import sleep

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame as pg


__all__ = ['FONT_PATH', 'COLORS_PATH', 'LEVELS_PATH', 'CUR_LEVEL_PATH', 'CUR_LEVEL_PROGRESS_PATH',
           'START_IMG_PATH', 'MENU_IMG_PATH', 'ANIM_IMG_PATH', 'SUN_IMG_PATH',
           'game_name', 'color_coding', 'sprite_group', 'current_level', 'level_amount', 'images', 'planet_image', 'sun_image',
           'rotate', 'animate', 'get_font', 'finish', 'pg']


pg.init()

FONT_PATH = os.path.join('data', 'font', 'Minecraftia-Regular.ttf')
COLORS_PATH = os.path.join('data', 'colors')
LEVELS_PATH = os.path.join('data', 'levels')
CUR_LEVEL_PATH = os.path.join('data', 'current_level.txt')
CUR_LEVEL_PROGRESS_PATH = os.path.join('data', 'current_level_progress.map')
START_IMG_PATH = os.path.join('data', 'start.jpg')
MENU_IMG_PATH = os.path.join('data', 'main_menu_bg.jpg')
ANIM_IMG_PATH = os.path.join('data', 'planets_round-round.png')
SUN_IMG_PATH = os.path.join('data', 'sun.png')

game_name: str = 'Destroy them all!'
color_coding: dict[int, str] = {0: '000000', 1: 'ff0000', 2: 'ff7f00', 3: 'ffff00', 4: '00ff00', 5: '00ffff', 6: '0000ff', 7: 'ff00ff'}
sprite_group = pg.sprite.Group()
if not os.path.exists(CUR_LEVEL_PATH):
    with open(CUR_LEVEL_PATH, 'w') as file:
        file.write('0')
with open(CUR_LEVEL_PATH) as file:
    current_level: list[int] = [*map(int, file.read().strip().split(',')), 0]
level_amount: int = len(os.listdir(LEVELS_PATH)) - 1
images: dict[str, pg.Surface] = {}
for filename in os.listdir(COLORS_PATH):
    fullname = os.path.join(COLORS_PATH, filename)
    if not os.path.isfile(fullname):
        continue
    image = pg.image.load(fullname)
    images[filename.split('.')[0]] = pg.transform.scale(image, (45, 45))
planet_image: pg.Surface = pg.transform.scale(pg.image.load(ANIM_IMG_PATH), (150, 150))
sun_image: pg.Surface = pg.transform.scale(pg.image.load(SUN_IMG_PATH), (50, 50))


def rotate(img: pg.Surface, pos: tuple[int, int], angle: int | float) -> pg.Surface:
    w, h = img.get_size()
    img2 = pg.Surface((w * 2, h * 2), pg.SRCALPHA)
    img2.blit(img, (w - pos[0], h - pos[1]))
    return pg.transform.rotate(img2, angle)


def animate(screen: pg.Surface, image: pg.Surface,center: tuple[int | float, int | float],
            size: tuple[int | float, int | float], rotations: int | float = 1) -> None:
    for i in range(int(360 * rotations)):
        img = pg.transform.scale(image, size)
        img = rotate(img, (size[0] // 2, size[1] // 2), i)
        screen.blit(img, img.get_rect(center=center))
        pg.display.update()
        sleep(0.001)


@cache
def get_font(size: int, style: str = FONT_PATH) -> pg.font.Font:
    return pg.font.Font(style, size)


def finish() -> None:
    size = 300, 350
    screen = pg.display.set_mode(size)
    pg.display.set_caption(f'DТA! - Закрывается...')
    text = get_font(25).render('Сохранение...', True, pg.Color('#ffffff'))
    screen.blit(text, text.get_rect(centerx=150, y=15))
    anim = Thread(target=animate, args=(screen, planet_image, (150, 200), (250, 250)))
    anim.start()
    with open(CUR_LEVEL_PATH, 'w') as file:
        file.write(','.join(map(str, current_level[:2])))
    anim.join()
    pg.quit()
    exit()
