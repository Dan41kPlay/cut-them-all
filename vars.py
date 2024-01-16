import os
import sys

import pygame as pg


__all__ = ['FONT_PATH', 'COLORS_PATH', 'LEVELS_PATH', 'CUR_LEVEL_PATH',
           'game_name', 'color_coding', 'sprite_group', 'current_level',
           'get_font', 'pgquit']


pg.init()
FONT_PATH = os.path.join('data', 'font_data', 'Minecraftia-Regular.ttf')
COLORS_PATH = os.path.join('data', 'colors')
LEVELS_PATH = os.path.join('data', 'levels')
CUR_LEVEL_PATH = os.path.join('data', 'current_level.txt')

game_name = 'Cut them all!'
color_coding = {0: 'ff0000', 1: 'ff7f00', 2: 'ffff00', 3: '00ff00', 4: '00ffff', 5: '0000ff', 6: 'ff00ff'}
sprite_group = pg.sprite.Group()
with open(CUR_LEVEL_PATH) as file:
    current_level = int(file.read().strip())


def get_font(size: int):
    return pg.font.Font(FONT_PATH, size)


def pgquit():
    pg.quit()
    sys.exit()
