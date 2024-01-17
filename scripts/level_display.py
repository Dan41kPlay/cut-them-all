import os
from random import randint
from time import sleep, perf_counter

from .vars import *


def rotate(img, pos, angle):
    w, h = img.get_size()
    img2 = pg.Surface((w * 2, h * 2), pg.SRCALPHA)
    img2.blit(img, (w - pos[0], h - pos[1]))
    return pg.transform.rotate(img2, angle)


def load_level(level):
    with open(os.path.join(LEVELS_PATH, f'{level}.map')) as level_file:
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
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board: list[list[str]] = [['000000'] * width for _ in range(height)]
        # значения по умолчанию
        self.dx = 10
        self.dy = 10
        self.cell_size = 50
        self.pt1 = None
        self.pt2 = None

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.dx = left
        self.dy = top
        self.cell_size = cell_size

    def change_tile(self, new_tile_type, x, y, images):
        self.board[y][x] = new_tile_type
        Tile(images[self.board[y][x]], self.cell_size, self.cell_size, x, y, self.dx, self.dy)

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

    def cut_tiles(self, images):
        for tile in self.selected_tiles():
            self.change_tile('000000', tile[0], tile[1], images)
        self.pt1 = self.pt2 = None

    def draw_selected(self, screen):
        if self.pt1 is None or self.pt2 is None or self.pt1 == self.pt2:
            return
        color = '#00ff00' if (self.check_tiles() and
                              (self.pt1[0] == self.pt2[0] or self.pt1[1] == self.pt2[1] or abs(self.pt1[0] - self.pt2[0]) == abs(self.pt1[1] - self.pt2[1])))\
            else '#ff0000'
        pg.draw.line(screen, pg.Color(color),
                     ((self.pt1[0] + .5) * self.cell_size + self.dx, (self.pt1[1] + .5) * self.cell_size + self.dy),
                     ((self.pt2[0] + .5) * self.cell_size + self.dx, (self.pt2[1] + .5) * self.cell_size + self.dy), 5)

    def generate_level(self, level_map, images):
        for y in range(len(level_map)):
            for x in range(len(level_map[y])):
                self.board[y][x] = color_coding[int(level_map[y][x])]
                Tile(images[self.board[y][x]], self.cell_size, self.cell_size,
                     x, y, self.dx, self.dy)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pg.draw.rect(screen, pg.Color('#007f7f'), (
                    x * self.cell_size + self.dx, y * self.cell_size + self.dy, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_pos):
        if (self.dx <= mouse_pos[0] < self.dx + self.width * self.cell_size and
            self.dy <= mouse_pos[1] < self.dy + self.height * self.cell_size):
            return (int((mouse_pos[0] - self.dx) / self.cell_size),
                    int((mouse_pos[1] - self.dy) / self.cell_size))

    def get_click(self, mouse_pos):
        return self.get_cell(mouse_pos)

    def check_win(self):
        return all(all(tile == '000000' for tile in row) for row in self.board)


def main(go_to=None) -> None:
    global sprite_group
    if current_level[0] > level_amount:
        current_level[0] = 0
    size = 300, 400
    screen = pg.display.set_mode(size)
    pg.display.set_caption(f'{game_name} - Level {current_level[0]}')
    board = Board(5, 5)
    board.set_view(25, 125, 50)
    images = {}
    for filename in os.listdir(COLORS_PATH):
        fullname = os.path.join(COLORS_PATH, filename)
        if not os.path.isfile(fullname):
            continue
        image = pg.image.load(fullname).convert_alpha()
        images[filename.split('.')[0]] = pg.transform.scale(image, (board.cell_size * .9,) * 2)
    sprite_group = pg.sprite.Group()
    board.generate_level(load_level(current_level[0]), images)
    stars = [[randint(0, 300), randint(0, 400)] for _ in range(100)]
    text1 = get_font(25).render(f'Level {current_level[0]}' if current_level[0] else 'All levels', True, pg.Color('#ffffff'))
    text2 = get_font(20).render(f'Restart', True, pg.Color('#ffffff'))
    text3 = get_font(20).render('completed in              !', True, pg.Color('#00ffff'))
    second, seconds = perf_counter(), 0
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if 165 <= event.pos[0] <= 285 and 25 <= event.pos[1] <= 55:
                    main(go_to)
                if event.button == 2 and board.check_tiles():
                    board.cut_tiles(images)
                    continue
                clicked_tile = board.get_click(event.pos)
                if clicked_tile is None:
                    continue
                if board.board[clicked_tile[1]][clicked_tile[0]] == '000000':
                    continue
                if event.button == 1:
                    board.pt1 = clicked_tile
                if event.button == 3:
                    board.pt2 = clicked_tile
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    board.pt1 = board.pt2 = None
                if event.key == pg.K_SPACE and board.check_tiles():
                    board.cut_tiles(images)
        if perf_counter() - second >= 1:
            second = perf_counter()
            seconds += 1
        screen.fill(pg.Color('#000000'))
        screen.blit(text1, (25, 20))
        text4 = get_font(20).render(f'{seconds // 60:0>2}:{seconds % 60:0>2}', True, pg.Color('#ffffff'))
        screen.blit(text4, (177, 60))
        if board.check_win():
            screen.blit(text3, (25, 60))
            planet_image = pg.transform.scale(pg.image.load(ANIM_IMG_PATH), (150, 150))
            current_level[0] += 1
            with open(CUR_LEVEL_PATH, 'w') as file:
                file.write(str(current_level[0]))
            pg.display.flip()
            for i in range(720):
                im = pg.transform.scale(planet_image, (250, 250))
                im = rotate(im, (125, 127), i)
                rect = im.get_rect()
                rect.center = (150, 250)
                screen.blit(im, rect)
                pg.display.update()
                sleep(0.001)
            main(go_to)
        else:
            mouse_pos = pg.mouse.get_pos()
            if 165 <= mouse_pos[0] <= 285 and 25 <= mouse_pos[1] <= 55:
                pg.draw.rect(screen, pg.Color('#00ffff'), (163, 23, 124, 34), 2, border_radius=17)
            sprite_group.draw(screen)
            for star in stars:
                pg.draw.rect(screen, pg.Color('#ffffff'), (star[0], star[1], 1, 1))
            board.render(screen)
            pg.draw.rect(screen, pg.Color('#001f7f'), (165, 25, 120, 30), border_radius=15)
            screen.blit(text2, text2.get_rect(centerx=225, y=25))
        board.draw_selected(screen)
        pg.display.flip()
    if go_to is None:
        pgquit()
    else:
        go_to()


if __name__ == '__main__':
    main()
