from .vars import *
from . import level_display


class Levels:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dx = 25
        self.dy = 25
        self.cell_size = 50

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.get_level((x, y)) > level_amount:
                    break
                pg.draw.rect(screen, pg.Color('#000f3f' if self.get_level((x, y)) > current_level[0] else '#001f7f'), (
                    (x + .05) * self.cell_size + self.dx, (y + .05) * self.cell_size + self.dy,
                    self.cell_size * .95, self.cell_size * .95), border_radius=15)
                level_text = get_font(20).render(str(self.get_level((x, y,))), True, pg.Color('#ffffff'))
                screen.blit(level_text, level_text.get_rect(center=((x + .5) * self.cell_size + self.dx, (y + .5) * self.cell_size + self.dy)))
            else:
                continue
            break

    def get_cell(self, mouse_pos):
        if (self.dx <= mouse_pos[0] < self.dx + self.width * self.cell_size and
            self.dy <= mouse_pos[1] < self.dy + self.height * self.cell_size):
            return (int((mouse_pos[0] - self.dx) / self.cell_size),
                    int((mouse_pos[1] - self.dy) / self.cell_size))

    def get_click(self, mouse_pos):
        return self.get_cell(mouse_pos)

    def get_level(self, clicked_level):
        return clicked_level[1] * self.width + clicked_level[0] + 1


def main_menu():
    size = 300, 400
    screen = pg.display.set_mode(size)
    pg.display.set_caption(game_name)
    levels = Levels(5, 5)
    bg = pg.transform.scale(pg.image.load(MENU_IMG_PATH), size)
    texts = [get_font(25).render(game_name, True, pg.Color('#00ffff')),
             get_font(20).render(f'Play {f'(level {current_level[0]})' if current_level[0] else ''}', True, pg.Color('#ffffff')),
             get_font(20).render('Select level', True, pg.Color('#ffffff')),
             get_font(20).render('How to play?', True, pg.Color('#ffffff')),
             get_font(20).render('Reset progress', True, pg.Color('#ffffff')),
             get_font(20).render('Playing guide', True, pg.Color('#ffffff')),
             get_font(20).render('Okay, thanks', True, pg.Color('#ffffff')),
             get_font(20).render('Cancel', True, pg.Color('#ffffff')),
             get_font(20).render('Good luck!', True, pg.Color('#ffffff'))]
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
             'by one, so think in advance.',
             'Destroy all planets in the',
             'system to complete the level.']
    is_guide = False
    level_selection = False
    return_to_main_menu = True
    running = True
    while running:
        mouse_pos = pg.mouse.get_pos()
        screen.fill(pg.Color('#000000'))
        screen.blit(bg, (0, 0))
        texts[1] = get_font(20).render(f'Play {f'(level {current_level[0]})' if current_level[0] else ''}', True, pg.Color('#ffffff'))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if 40 <= event.pos[0] <= 260 and not is_guide and not level_selection:
                    if 50 <= event.pos[1] <= 80:
                        if not current_level[0]:
                            current_level[0] += 1
                            is_guide = True
                            return_to_main_menu = False
                            continue
                        level_display.main(main_menu)
                    elif 90 <= event.pos[1] <= 120:
                        level_selection = True
                        continue
                    elif 130 <= event.pos[1] <= 160:
                        is_guide = True
                    elif 170 <= event.pos[1] <= 200:
                        current_level[0] = 0
                        with open(CUR_LEVEL_PATH, 'w') as file:
                            file.write(str(current_level[0]))
                if level_selection:
                    clicked_level = levels.get_click(mouse_pos)
                    if clicked_level is not None:
                        selected_level = levels.get_level(clicked_level)
                        if selected_level <= current_level[0]:
                            current_level[1] = selected_level
                            print(current_level[1])
                            level_display.main(main_menu, False)
                if 40 <= event.pos[0] <= 260 and 360 <= event.pos[1] <= 390:
                    if is_guide:
                        is_guide = False
                        if not return_to_main_menu:
                            level_display.main(main_menu)
                        return_to_main_menu = True
                    elif level_selection:
                        level_selection = False
        if level_selection:
            at_level = levels.get_click(mouse_pos)
            if at_level is not None and levels.get_level(at_level) <= current_level[0]:
                x, y = at_level
                pg.draw.rect(screen, pg.Color('#00ffff'), (
                    (x + .05) * levels.cell_size + levels.dx - 2, (y + .05) * levels.cell_size + levels.dy - 2,
                    levels.cell_size * .95 + 4, levels.cell_size * .95 + 4), border_radius=17)
        if 40 <= mouse_pos[0] <= 260:
            to_outline = [[*range(360, 391)]] if is_guide or level_selection else [[*range(50, 81)], [*range(90, 121)], [*range(130, 161)], [*range(170, 201)]]
            found = [idx for idx, rng in enumerate(to_outline) if mouse_pos[1] in rng]
            if found:
                top_left = to_outline[found[0]]
                pg.draw.rect(screen, pg.Color('#00ffff'), (38, top_left[0] - 2, 224, 34), 2, border_radius=17)
        if is_guide:
            screen.blit(texts[5], texts[5].get_rect(centerx=150))
            text_coord = 30
            for line in guide:
                string_rendered = guide_font.render(line, 1, pg.Color('#ffffff'))
                guide_rect = string_rendered.get_rect()
                text_coord += 2
                guide_rect.top = text_coord
                guide_rect.x = 10
                text_coord += guide_rect.height
                screen.blit(string_rendered, guide_rect)
            screen.blit(texts[8], texts[8].get_rect(centerx=150, y=310))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 360, 220, 30), border_radius=15)
            screen.blit(texts[6], texts[6].get_rect(centerx=150, y=360))
        elif level_selection:
            levels.render(screen)
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 360, 220, 30), border_radius=15)
            screen.blit(texts[7], texts[7].get_rect(centerx=150, y=360))
        else:
            screen.blit(texts[0], texts[0].get_rect(centerx=150, y=5))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 50, 220, 30), border_radius=15)
            screen.blit(texts[1], texts[1].get_rect(centerx=150, y=50))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 90, 220, 30), border_radius=15)
            screen.blit(texts[2], texts[2].get_rect(centerx=150, y=90))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 130, 220, 30), border_radius=15)
            screen.blit(texts[3], texts[3].get_rect(centerx=150, y=130))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 170, 220, 30), border_radius=15)
            screen.blit(texts[4], texts[4].get_rect(centerx=150, y=170))
            text_coord = 225
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
