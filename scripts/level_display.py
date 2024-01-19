import os
from time import perf_counter
from typing import Any

from .vars import *


def load_level(level, load_last=False):
    with open(CUR_LEVEL_PROGRESS_PATH if load_last and os.path.exists(CUR_LEVEL_PROGRESS_PATH)
              else os.path.join(LEVELS_PATH, f'{level}.map')) as level_file:
        return [[*line.strip()] for line in level_file]


class Sprite(pg.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, image, width: int, height: int, pos_x: int, pos_y: int, dx: int, dy: int):
        super().__init__(sprite_group)
        self.width = width
        self.height = height
        self.image = image
        self.rect = self.image.get_rect().move(dx + self.width * (pos_x + .05), dy + self.height * (pos_y + .05))


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board: list[list[str]] = [['000000'] * width for _ in range(height)]
        self.sprites: list[list[Any]] = [[None] * width for _ in range(height)]
        self.dx = 25
        self.dy = 125
        self.cell_size = 50
        self.pt1 = None
        self.pt2 = None

    def change_tile(self, new_tile_type, x, y, images):
        self.board[y][x] = new_tile_type
        sprite_group.remove(self.sprites[y][x])
        self.sprites[y][x] = Tile(images[self.board[y][x]], self.cell_size, self.cell_size, x, y, self.dx, self.dy)

    def selected_tiles(self) -> list[tuple[int, int]]:
        if self.pt1 is None or self.pt2 is None or self.pt1 == self.pt2:
            return []
        x_sign, y_sign = -1 if self.pt1[0] > self.pt2[0] else 1, -1 if self.pt1[1] > self.pt2[1] else 1
        x_vals, y_vals = sorted((self.pt1[0], self.pt2[0]))[::x_sign], sorted((self.pt1[1], self.pt2[1]))[::y_sign]
        range_x, range_y = [*range(x_vals[0], x_vals[1] + x_sign, x_sign)], [*range(y_vals[0], y_vals[1] + y_sign, y_sign)]
        return ([(self.pt1[0], y) for y in range_y] if self.pt1[0] == self.pt2[0] else
                [(x, self.pt1[1]) for x in range_x] if self.pt1[1] == self.pt2[1] else
                [(x, y) for x, y in zip(range_x, range_y)] if abs(self.pt1[0] - self.pt2[0]) == abs(self.pt1[1] - self.pt2[1]) else [])

    def check_tiles(self):
        selected_tiles = self.selected_tiles()
        return len(selected_tiles) > 1 and len({self.board[y][x] for x, y in selected_tiles if self.board[y][x] != '000000'}) == 1

    def cut_tiles(self, images, save_progress):
        for tile in self.selected_tiles():
            self.change_tile('000000', tile[0], tile[1], images)
        self.pt1 = self.pt2 = None
        if not save_progress:
            return
        reverse_colors = {value: str(key) for key, value in color_coding.items()}
        s = '\n'.join(''.join(reverse_colors[self.board[y][x]] for x in range(self.width)) for y in range(self.height))
        with open(CUR_LEVEL_PROGRESS_PATH, 'w') as level_file:
            level_file.write(s)

    # for animation only
    def draw_selected(self, screen):
        if self.pt1 is None or self.pt2 is None or self.pt1 == self.pt2:
            return
        color = ('#00ff00' if self.check_tiles() and
                 (self.pt1[0] == self.pt2[0] or self.pt1[1] == self.pt2[1] or abs(self.pt1[0] - self.pt2[0]) == abs(self.pt1[1] - self.pt2[1]))
                 else '#ff0000')
        pg.draw.line(screen, pg.Color(color),
                     ((self.pt1[0] + .5) * self.cell_size + self.dx, (self.pt1[1] + .5) * self.cell_size + self.dy),
                     ((self.pt2[0] + .5) * self.cell_size + self.dx, (self.pt2[1] + .5) * self.cell_size + self.dy), 5)

    def generate_level(self, level_map, images):
        for y in range(len(level_map)):
            for x in range(len(level_map[y])):
                self.board[y][x] = color_coding[int(level_map[y][x])]
                self.sprites[y][x] = Tile(images[self.board[y][x]], self.cell_size, self.cell_size, x, y, self.dx, self.dy)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):

                pg.draw.rect(screen, pg.Color('#00ffff' if self.pt1 == (x, y) else '#007f7f'), (
                    x * self.cell_size + self.dx, y * self.cell_size + self.dy,
                    self.cell_size, self.cell_size), 1 + (self.pt1 == (x, y)))

    def get_cell(self, mouse_pos):
        if (self.dx <= mouse_pos[0] < self.dx + self.width * self.cell_size and
            self.dy <= mouse_pos[1] < self.dy + self.height * self.cell_size):
            return (int((mouse_pos[0] - self.dx) / self.cell_size),
                    int((mouse_pos[1] - self.dy) / self.cell_size))

    def get_click(self, mouse_pos):
        return self.get_cell(mouse_pos)

    def check_win(self):
        return all(all(tile == '000000' for tile in row) for row in self.board)


def main(go_to=None, level_up=True) -> None:
    global sprite_group
    if current_level[(not level_up) + 1] > level_amount:
        current_level[(not level_up) + 1] = 0
    if (not level_up) and current_level[2] == current_level[1]:
        level_up = True
    size = 300, 400
    screen = pg.display.set_mode(size)
    pg.display.set_caption(f'DTA! - Уровень {current_level[(not level_up) + 1]}')
    board = Board(5, 5)
    sprite_group = pg.sprite.Group()
    board.generate_level(load_level(current_level[(not level_up) + 1], level_up), images)
    bg = pg.transform.scale(pg.image.load(MENU_IMG_PATH), size)
    text2 = get_font(20).render('Меню', True, pg.Color('#ffffff'))
    text3 = get_font(20).render('Рестарт', True, pg.Color('#ffffff'))
    text4 = get_font(20).render('выполнен за               !', True, pg.Color('#00ffff'))
    text4c = text4.copy()
    a_surf = pg.Surface(text4c.get_size(), pg.SRCALPHA)
    alpha = 0
    clock = pg.time.Clock()
    seconds_x, speed = 25, 10
    won, need_move = False, False
    second, seconds = perf_counter(), current_level[0] if level_up else 0
    running, to_menu = True, False
    while running:
        if level_up:
            current_level[0] = seconds
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT and not won:
                if 165 <= event.pos[0] <= 285:
                    if 25 <= event.pos[1] <= 55:
                        running = False
                        to_menu = True
                    if 65 <= event.pos[1] <= 95:
                        sprite_group = pg.sprite.Group()
                        board.generate_level(load_level(current_level[(not level_up) + 1]), images)
                        if os.path.exists(CUR_LEVEL_PROGRESS_PATH):
                            os.remove(CUR_LEVEL_PROGRESS_PATH)
                        break
                clicked_tile = board.get_click(event.pos)
                if clicked_tile is None:
                    continue
                if board.board[clicked_tile[1]][clicked_tile[0]] == '000000':
                    continue
                if board.pt1 == clicked_tile:
                    board.pt1 = None
                elif board.pt1 is None:
                    board.pt1 = clicked_tile
                elif board.pt2 is None:
                    board.pt2 = clicked_tile
                    if board.check_tiles():
                        board.cut_tiles(images, level_up)
                        continue
                    else:
                        board.pt2 = None
        if perf_counter() - second >= 1:
            second = perf_counter()
            seconds += 1
        screen.fill(pg.Color('#000000'))
        screen.blit(bg, (0, 0))
        text1 = get_font(25).render(f'Ур. {current_level[(not level_up) + 1]}' if current_level[(not level_up) + 1] else 'Все уровни',
                                    True, pg.Color('#ffffff'))
        screen.blit(text1, (25, 20))
        if won:
            if seconds_x < 177:
                seconds_x = min(seconds_x + speed, 177)
                speed *= .935
                alpha = min(alpha + 4, 255)
                text4c = text4.copy()
                a_surf.fill((255, 255, 255, alpha))
                text4c.blit(a_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
                screen.blit(text4c, (25, 60))
                need_move = True
            else:
                speed = 10
                need_move = False
        if not won:
            if seconds_x > 25:
                seconds_x = max(seconds_x - speed, 25)
                speed *= .935
                alpha = max(alpha - 4, 0)
                text4c = text4.copy()
                a_surf.fill((255, 255, 255, alpha))
                text4c.blit(a_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
                screen.blit(text4c, (25, 60))
                need_move = True
            else:
                speed = 10
                need_move = False
        text5 = get_font(20).render(f'{seconds // 60:0>2}:{seconds % 60:0>2}', True, pg.Color('#ffffff'))
        screen.blit(text5, (seconds_x, 60))
        if need_move:
            pg.display.flip()
            clock.tick(60)
            continue
        if board.check_win():
            if not won:
                won = True
                continue
            screen.blit(text4, (25, 60))
            current_level[(not level_up) + 1] += 1
            with open(CUR_LEVEL_PATH, 'w') as file:
                file.write(','.join(map(str, current_level[:2])))
            pg.display.flip()
            animation(screen, (150, 250), 2)
            pg.display.set_caption(f'DTA! - Ур. {current_level[(not level_up) + 1]}')
            sprite_group = pg.sprite.Group()
            board.generate_level(load_level(current_level[(not level_up) + 1]), images)
            second, seconds = perf_counter(), 0
            if won:
                won = False
            continue
        else:
            mouse_pos = pg.mouse.get_pos()
            if 165 <= mouse_pos[0] <= 285:
                if 25 <= mouse_pos[1] <= 55:
                    pg.draw.rect(screen, pg.Color('#00ffff'), (163, 23, 124, 34),2, 12)
                if 65 <= mouse_pos[1] <= 95:
                    pg.draw.rect(screen, pg.Color('#00ffff'), (163, 63, 124, 34), 2, 12)
            sprite_group.draw(screen)
            board.render(screen)
            pg.draw.rect(screen, pg.Color('#001f7f'), (165, 25, 120, 30), border_radius=10)
            screen.blit(text2, text2.get_rect(centerx=225, y=25))
            pg.draw.rect(screen, pg.Color('#001f7f'), (165, 65, 120, 30), border_radius=10)
            screen.blit(text3, text3.get_rect(centerx=225, y=65))
        pg.display.flip()
    if go_to is None or not to_menu:
        pgquit()
    else:
        go_to()


if __name__ == '__main__':
    main()
