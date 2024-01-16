from os import path

import pygame as pg


FONT_PATH = path.join('font_data', 'Minecrafia-Regular.ttf')


def main_menu():
    pg.init()
    size = (300, 300)
    screen = pg.display.set_mode(size)
    screen.fill(pg.Color('white'))
    f1 = pg.font.Font(FONT_PATH, 24)
    text1 = f1.render('Cut them all!', True, (180, 0, 0))
    screen.blit(text1, (70, 50))
    pg.draw.rect(screen, pg.Color('red'), (100, 85, 100, 50))
    f2 = pg.font.Font(FONT_PATH, 20)
    text2 = f2.render('Играть', True, pg.Color('white'))
    screen.blit(text2, (110, 90))
    pg.display.flip()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if 100 < event.pos[0] < 200 and 85 < event.pos[1] < 135:
                    print('ye')
    pg.quit()


def first():
    pg.init()
    size = (300, 300)
    screen = pg.display.set_mode(size)
    screen.fill(pg.Color('blue'))
    pg.display.flip()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                main_menu()
    pg.quit()


try:
    first()
except Exception:
    pg.quit()
