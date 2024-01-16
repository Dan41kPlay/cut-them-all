import pygame as pg

from . import level_display
from .vars import *


def main_menu():
    size = 300, 300
    screen = pg.display.set_mode(size)
    pg.display.set_caption(f'{game_name} - Main menu')
    screen.fill(pg.Color('#000000'))
    text1 = get_font(30).render(game_name, True, pg.Color('#ff0000'))
    screen.blit(text1, (50, 45))
    pg.draw.rect(screen, pg.Color('#ff0000'), (100, 85, 100, 50), border_radius=15)
    text2 = get_font(25).render('Play', True, pg.Color('#ffffff'))
    screen.blit(text2, (120, 90))
    intro_text = ['Controls:',
                  '[Left MB] Select first planet',
                  '[Right MB] Select second planet',
                  '[Esc] Clear selected planets',
                  '[Middle MB] / [Space] Cut', 'between selected planets']
    font = get_font(14)
    text_coord = 140
    for line in intro_text:
        string_rendered = font.render(line, 1, pg.Color('#ffffff'))
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
                    level_display.main()
    pgquit()


def first():
    size = 300, 300
    screen = pg.display.set_mode(size)
    pg.display.set_caption(game_name)
    bg = pg.transform.scale(pg.image.load(START_IMG_PATH), size)
    brightness, direction, speed = 0, 1, 2
    clock = pg.time.Clock()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type in {pg.MOUSEBUTTONDOWN, pg.KEYDOWN}:
                main_menu()
        brightness += direction * speed
        if brightness >= 255:
            brightness = 255
            direction = -1
        if brightness <= 0:
            brightness = 0
            direction = 1
        screen.fill(pg.Color('#000000'))
        screen.blit(bg, (0, 0))
        text1 = get_font(12).render('Press any key to continue', True, pg.Color((brightness,) * 3))
        screen.blit(text1, (100, 0))
        pg.display.flip()
        clock.tick(60)
    pgquit()


if __name__ == '__main__':
    first()
