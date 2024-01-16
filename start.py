import os

import pygame as pg

import coord


FONT_PATH = os.path.join('data', 'font_data', 'Minecraftia-Regular.ttf')


def main_menu():
    try:
        pg.init()
        size = (300, 300)
        screen = pg.display.set_mode(size)
        screen.fill(pg.Color('#ffffff'))
        f1 = pg.font.Font(FONT_PATH, 24)
        text1 = f1.render('Cut them all!', True, (180, 0, 0))
        screen.blit(text1, (70, 50))
        pg.draw.rect(screen, pg.Color('#ff0000'), (100, 85, 100, 50))
        f2 = pg.font.Font(FONT_PATH, 20)
        text2 = f2.render('Играть', True, pg.Color('#ffffff'))
        screen.blit(text2, (110, 90))
        pg.display.flip()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if 100 < event.pos[0] < 200 and 85 < event.pos[1] < 135:
                        coord.main()
        pg.quit()
    except Exception as e:
        print(e)


def first():
    pg.init()
    size = (300, 300)
    screen = pg.display.set_mode(size)
    screen.fill(pg.Color('#0000ff'))
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
