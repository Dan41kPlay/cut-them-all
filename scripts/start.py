from random import randint
from time import perf_counter

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
                pg.draw.rect(screen, pg.Color('#000f3f' if self.get_level((x, y)) > current_level[1] else '#001f7f'), (
                    (x + .05) * self.cell_size + self.dx, (y + .05) * self.cell_size + self.dy,
                    self.cell_size * .95, self.cell_size * .95), border_radius=10)
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
    levels = Levels(5, 6)
    bg = pg.transform.scale(pg.image.load(MENU_IMG_PATH), size)
    texts = [get_font(25).render(game_name, True, pg.Color('#00ffff')),
             get_font(20).render('Играть' + (f'(ур. {current_level[1]})' if current_level[1] else ''), True, pg.Color('#ffffff')),
             get_font(20).render('Выбор уровня', True, pg.Color('#ffffff')),
             get_font(20).render('Как играть?', True, pg.Color('#ffffff')),
             get_font(20).render('Сброс прогресса', True, pg.Color('#ffffff')),
             get_font(20).render('Как играть', True, pg.Color('#ffffff')),
             get_font(20).render('Хорошо, спасибо', True, pg.Color('#ffffff')),
             get_font(20).render('Отмена', True, pg.Color('#ffffff')),
             get_font(20).render('Удачи! =)', True, pg.Color('#ffffff'))]
    controls = ['Управление:',
                'Всё делается с помощью ЛКМ:',
                'чтобы выбрать 1-ю планету,',
                'нажми на неё. Чтобы отменить',
                'выбор, нажми на неё ещё раз.',
                'Чтобы разрушить планеты,',
                'нажми на 2-ю планету.']
    controls_font = get_font(14)
    guide_font = get_font(14)
    guide = ['Выбери две планеты одного',
             'цвета, чтобы разрушить все',
             'планеты между ними. Они дол-',
             'жны быть на одной прямой по',
             'горизонтали, вертикали или',
             'диагонали. Другие планеты не',
             'могут быть на пути, и ты не',
             'можешь уничтожать их по од-',
             'ной, поэтому думай наперёд.',
             'Уничтожь все планеты в сис-',
             'теме, чтобы пройти уровень.']
    is_guide = False
    level_selection = False
    return_to_main_menu = True
    running = True
    while running:
        mouse_pos = pg.mouse.get_pos()
        screen.fill(pg.Color('#000000'))
        screen.blit(bg, (0, 0))
        texts[1] = get_font(20).render(f'Играть {f'(ур. {current_level[1]})' if current_level[1] else ''}', True, pg.Color('#ffffff'))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if 40 <= event.pos[0] <= 260 and not is_guide and not level_selection:
                    if 50 <= event.pos[1] <= 80:
                        if not current_level[1]:
                            current_level[1] += 1
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
                        current_level[1] = 0
                        with open(CUR_LEVEL_PATH, 'w') as file:
                            file.write(','.join(map(str, current_level[:2])))
                if level_selection:
                    clicked_level = levels.get_click(mouse_pos)
                    if clicked_level is not None:
                        selected_level = levels.get_level(clicked_level)
                        if selected_level <= current_level[1]:
                            current_level[2] = selected_level
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
            if at_level is not None and levels.get_level(at_level) <= current_level[1]:
                x, y = at_level
                pg.draw.rect(screen, pg.Color('#00ffff'), (
                    (x + .05) * levels.cell_size + levels.dx - 2, (y + .05) * levels.cell_size + levels.dy - 2,
                    levels.cell_size * .95 + 4, levels.cell_size * .95 + 4), border_radius=12)
        if 40 <= mouse_pos[0] <= 260:
            to_outline = [[*range(360, 391)]] if is_guide or level_selection else [[*range(50, 81)], [*range(90, 121)], [*range(130, 161)], [*range(170, 201)]]
            found = [idx for idx, rng in enumerate(to_outline) if mouse_pos[1] in rng]
            if found:
                top_left = to_outline[found[0]]
                pg.draw.rect(screen, pg.Color('#00ffff'), (38, top_left[0] - 2, 224, 34), 2, border_radius=12)
        if is_guide:
            screen.blit(texts[5], texts[5].get_rect(centerx=150))
            text_coord = 30
            for line in guide:
                string_rendered = guide_font.render(line, 1, pg.Color('#ffffff'))
                guide_rect = string_rendered.get_rect()
                guide_rect.top = text_coord
                guide_rect.x = 10
                text_coord += guide_rect.height
                screen.blit(string_rendered, guide_rect)
            screen.blit(texts[8], texts[8].get_rect(centerx=150, y=310))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 360, 220, 30), border_radius=10)
            screen.blit(texts[6], texts[6].get_rect(centerx=150, y=360))
        elif level_selection:
            levels.render(screen)
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 360, 220, 30), border_radius=10)
            screen.blit(texts[7], texts[7].get_rect(centerx=150, y=360))
        else:
            screen.blit(texts[0], texts[0].get_rect(centerx=150, y=5))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 50, 220, 30), border_radius=10)
            screen.blit(texts[1], texts[1].get_rect(centerx=150, y=50))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 90, 220, 30), border_radius=10)
            screen.blit(texts[2], texts[2].get_rect(centerx=150, y=90))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 130, 220, 30), border_radius=10)
            screen.blit(texts[3], texts[3].get_rect(centerx=150, y=130))
            pg.draw.rect(screen, pg.Color('#001f7f'), (40, 170, 220, 30), border_radius=10)
            screen.blit(texts[4], texts[4].get_rect(centerx=150, y=170))
            text_coord = 210
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
    rand_stutter = randint(30, 70) * 2
    bar_size = time_ctr = 0
    alpha = 255
    brightness, direction = 0, 1
    sun_size_start, sun_size_end = 50, 4
    sun_rot = 0
    start_sun_x, start_sun_y = 150, 125
    end_sun_x, end_sun_y = 18, 77
    clock = pg.time.Clock()
    loading = True
    transitioning = False
    running = True

    while running:
        screen.fill(pg.Color('#000000'))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if not loading and event.type in {pg.MOUSEBUTTONDOWN, pg.KEYDOWN, pg.CONTROLLERBUTTONDOWN, pg.CONTROLLERTOUCHPADDOWN, pg.FINGERDOWN}:
                main_menu()
        if bar_size >= 200:
            loading = False
            transitioning = True
        if not alpha:
            transitioning = False

        if loading:
            bar_color = pg.Color(bar_size * 51 // 40, 255 - bar_size * 51 // 80, 255 - bar_size * 51 // 40)
            pg.draw.rect(screen, bar_color, (48, 176, 204, 24), 2)
            pg.draw.rect(screen, bar_color, (50, 178, bar_size, 20))
            img = pg.transform.scale(sun_image, (sun_size_start,) * 2)
            img = rotate(img, (sun_size_start // 2, sun_size_start // 2), sun_rot)
            screen.blit(img, img.get_rect(center=(150, 125)))
            sun_rot -= 5
            if bar_size != rand_stutter:
                bar_size += 2
                time_ctr = perf_counter()
            if perf_counter() - time_ctr >= 1:
                bar_size += 2

        elif transitioning:
            bg_copy = bg.copy()
            dark_bg = pg.Surface(bg.get_size()).convert_alpha()
            dark_bg.fill((0, 0, 0, alpha))
            bg_copy.blit(dark_bg, (0, 0))
            screen.blit(bg_copy, (0, 0))
            bright_bar = pg.Surface((204 * alpha / 264, 24 * alpha // 264)).convert_alpha()
            bright_bar.fill((0, 0, 0, 255 - alpha))
            pg.draw.rect(bright_bar, pg.Color(255, 127, 0, alpha), (0, 0, 204, 24))
            screen.blit(bright_bar, bright_bar.get_rect(center=(150, 188)))
            sun_cropped = pg.transform.scale(sun_image, (sun_size_start,) * 2)
            screen.blit(sun_cropped, sun_cropped.get_rect(center=(start_sun_x, start_sun_y)))
            sun_size_start -= .55
            start_sun_x = max(start_sun_x - 1.65, end_sun_x)
            start_sun_y = max(start_sun_y - .6, end_sun_y)
            alpha = max(alpha - 3, 0)

        else:
            brightness += direction * 2.5
            if brightness >= 255:
                brightness = 255
                direction = -1
            if brightness <= 0:
                brightness = 0
                direction = 1
            screen.blit(bg, (0, 0))
            text1 = get_font(12).render('Нажми на любую кнопку,', True, pg.Color((brightness,) * 3))
            text2 = get_font(12).render('чтобы продолжить', True, pg.Color((brightness,) * 3))
            screen.blit(text1, (120, 0))
            screen.blit(text2, (150, 15))
        pg.display.flip()
        clock.tick(60)
    pgquit()


if __name__ == '__main__':
    first()
