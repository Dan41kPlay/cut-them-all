import os

import pygame as pg

from .vars import *
from . import level_display


def main_menu():
    size = 300, 350
    screen = pg.display.set_mode(size)
    pg.display.set_caption(f'{game_name} - Main menu')
    screen.fill(pg.Color('#000000'))
    text1 = get_font(30).render(game_name, True, pg.Color('#ff0000'))
    text2 = get_font(20).render('Play', True, pg.Color('#ffffff'))
    text3 = get_font(20).render('Reset progress', True, pg.Color('#ff0000'))
    text4 = get_font(20).render('How to play?', True, pg.Color('#000000'))
    text5 = get_font(20).render('Playing guide', True, pg.Color('#ffffff'))
    text6 = get_font(20).render('OK', True, pg.Color('#ffffff'))
    controls = ['Controls:',
                '[ Left MB ]  Select 1st planet',
                '[ Right MB ]  Select 2nd planet',
                '[ Esc ]  Clear selected planets',
                '[ Middle MB ] / [ Space ]  Cut', 'between selected planets']
    controls_font = get_font(14)
    guide_font = get_font(14)
    guide = ['Select two planets of the same',
             'color to then destroy all',
             'planets between them. Planets',
             'must be on one line horizontally,',
             'vertically or diagonally. Other',
             'planets can\'t be on the way and',
             'you can\'t destroy planets one',
             'by one, so think in advance. Des-',
             'troy all planets in the system to',
             'complete the level. Good luck!']
    is_guide = False
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and 40 <= event.pos[0] <= 260:
                if is_guide and 310 <= event.pos[1] <= 340:
                    is_guide = False
                elif 50 <= event.pos[1] <= 80:
                    level_display.main()
                elif 90 <= event.pos[1] <= 120:
                    current_level[0] = 1
                    with open(CUR_LEVEL_PATH, 'w') as file:
                        file.write(str(current_level[0]))
                elif 130 <= event.pos[1] <= 160:
                    is_guide = True
        screen.fill(pg.Color('#000000'))
        if is_guide:
            screen.blit(text5, text5.get_rect(centerx=150))
            text_coord = 30
            for line in guide:
                string_rendered = guide_font.render(line, 1, pg.Color('#ffffff'))
                guide_rect = string_rendered.get_rect()
                text_coord += 2
                guide_rect.top = text_coord
                guide_rect.x = 10
                text_coord += guide_rect.height
                screen.blit(string_rendered, guide_rect)
            pg.draw.rect(screen, pg.Color('#ff0000'), (40, 310, 220, 30), border_radius=15)
            screen.blit(text6, text6.get_rect(centerx=150, y=310))
        else:
            screen.blit(text1, text1.get_rect(centerx=150))
            pg.draw.rect(screen, pg.Color('#ff0000'), (40, 50, 220, 30), border_radius=15)
            screen.blit(text2, text2.get_rect(centerx=150, y=50))
            pg.draw.rect(screen, pg.Color('#222222'), (40, 90, 220, 30), border_radius=15)
            screen.blit(text3, text3.get_rect(centerx=150, y=90))
            pg.draw.rect(screen, pg.Color('#ffffff'), (40, 130, 220, 30), border_radius=15)
            screen.blit(text4, text4.get_rect(centerx=150, y=130))
            text_coord = 175
            for line in controls:
                string_rendered = controls_font.render(line, 1, pg.Color('#ffffff'))
                intro_rect = string_rendered.get_rect()
                text_coord += 2
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        pg.display.flip()
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
