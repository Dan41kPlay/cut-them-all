import os
import sys

import pygame as pg


__all__ = ['FONT_PATH', 'getFont', 'pgquit']


FONT_PATH = os.path.join('data', 'font_data', 'Minecraftia-Regular.ttf')
pg.init()


def getFont(size: int):
    return pg.font.Font(FONT_PATH, size)


def pgquit():
    pg.quit()
    sys.exit()
