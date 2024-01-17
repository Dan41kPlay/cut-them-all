import os
from sys import exit

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame as pg


__all__ = ['FONT_PATH', 'COLORS_PATH', 'LEVELS_PATH', 'CUR_LEVEL_PATH', 'START_IMG_PATH', 'MENU_IMG_PATH', 'ANIM_IMG_PATH',
           'game_name', 'color_coding', 'sprite_group', 'current_level', 'level_amount',
           'get_font', 'pgquit', 'pg']


pg.init()
FONT_PATH = os.path.join('data', 'font', 'Minecraftia-Regular.ttf')
COLORS_PATH = os.path.join('data', 'colors')
LEVELS_PATH = os.path.join('data', 'levels')
CUR_LEVEL_PATH = os.path.join('data', 'current_level.txt')
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
    current_level = [int(file.read().strip())]
level_amount = len(os.listdir(LEVELS_PATH)) - 1


def get_font(size: int):
    return pg.font.Font(FONT_PATH, size)


def pgquit():
    pg.quit()
    exit()
