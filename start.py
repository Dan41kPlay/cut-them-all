import pygame as pg

import coord
from vars import *


def main_menu():
    size = (300, 300)
    screen = pg.display.set_mode(size)
    screen.fill(pg.Color('#ffffff'))
    text1 = get_font(24).render('Cut them all!', True, (180, 0, 0))
    screen.blit(text1, (70, 50))
    pg.draw.rect(screen, pg.Color('#ff0000'), (100, 85, 100, 50), border_radius=10)
    text2 = get_font(24).render('Play', True, pg.Color('#ffffff'))
    screen.blit(text2, (110, 90))
    intro_text = ['Controls:',
                  '[Left MB] Select first point',
                  '[Right MB] Select second point',
                  '[Esc] Clear selected points',
                  '[Middle MB] / [Enter] Cut', 'between selected points']
    font = get_font(14)
    text_coord = 140
    for line in intro_text:
        string_rendered = font.render(line, 1, pg.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 2
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pg.display.flip()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if 100 < event.pos[0] < 200 and 85 < event.pos[1] < 135:
                    coord.main()
    pgquit()


def first():
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
    pgquit()


if __name__ == '__main__':
    first()
