import os
import sys

import pygame as pg


__all__ = ['FONT_PATH', 'get_font', 'pgquit']


FONT_PATH = os.path.join('data', 'font_data', 'Minecraftia-Regular.ttf')
pg.init()


def get_font(size: int):
    return pg.font.Font(FONT_PATH, size)


def pgquit():
    pg.quit()
    sys.exit()
