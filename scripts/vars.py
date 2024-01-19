import os
from sys import exit
from threading import Thread
from time import sleep

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame as pg


__all__ = ['FONT_PATH', 'COLORS_PATH', 'LEVELS_PATH', 'CUR_LEVEL_PATH', 'CUR_LEVEL_PROGRESS_PATH', 'START_IMG_PATH', 'MENU_IMG_PATH', 'ANIM_IMG_PATH',
           'game_name', 'color_coding', 'sprite_group', 'current_level', 'level_amount', 'images',
           'animation', 'get_font', 'pgquit', 'pg']


pg.init()
FONT_PATH = os.path.join('data', 'font', 'Minecraftia-Regular.ttf')
COLORS_PATH = os.path.join('data', 'colors')
LEVELS_PATH = os.path.join('data', 'levels')
CUR_LEVEL_PATH = os.path.join('data', 'current_level.txt')
CUR_LEVEL_PROGRESS_PATH = os.path.join('data', 'current_level_progress.map')
START_IMG_PATH = os.path.join('data', 'start.jpg')
MENU_IMG_PATH = os.path.join('data', 'main_menu_bg.jpg')
ANIM_IMG_PATH = os.path.join('data', 'planets_round-round.png')

game_name = 'Destroy them all!'
color_coding = {0: '000000', 1: 'ff0000', 2: 'ff7f00', 3: 'ffff00', 4: '00ff00', 5: '00ffff', 6: '0000ff', 7: 'ff00ff'}
sprite_group = pg.sprite.Group()
if not os.path.exists(CUR_LEVEL_PATH):
    with open(CUR_LEVEL_PATH, 'w') as file:
        file.write('0')
with open(CUR_LEVEL_PATH) as file:
    current_level = [*map(int, file.read().strip().split(',')), 0]
level_amount = len(os.listdir(LEVELS_PATH)) - 1
images = {}
for filename in os.listdir(COLORS_PATH):
    fullname = os.path.join(COLORS_PATH, filename)
    if not os.path.isfile(fullname):
        continue
    image = pg.image.load(fullname)
    images[filename.split('.')[0]] = pg.transform.scale(image, (45, 45))
planet_image = pg.transform.scale(pg.image.load(ANIM_IMG_PATH), (150, 150))


def rotate(img, pos, angle):
    w, h = img.get_size()
    img2 = pg.Surface((w * 2, h * 2), pg.SRCALPHA)
    img2.blit(img, (w - pos[0], h - pos[1]))
    return pg.transform.rotate(img2, angle)


def animation(screen, center, rotations=1):
    for i in range(int(360 * rotations)):
        im = pg.transform.scale(planet_image, (250, 250))
        im = rotate(im, (125, 127), i)
        rect = im.get_rect()
        rect.center = center
        screen.blit(im, rect)
        pg.display.update()
        sleep(0.001)


def get_font(size: int):
    return pg.font.Font(FONT_PATH, size)


def pgquit():
    size = 300, 350
    screen = pg.display.set_mode(size)
    pg.display.set_caption(f'DТA! - Закрывается...')
    text = get_font(25).render('Схоранение...', True, pg.Color('#ffffff'))
    screen.blit(text, text.get_rect(centerx=150, y=15))
    anim = Thread(target=animation, args=(screen, (150, 200)))
    anim.start()
    with open(CUR_LEVEL_PATH, 'w') as file:
        file.write(','.join(map(str, current_level[:2])))
    anim.join()
    pg.quit()
    exit()
