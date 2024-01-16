import os

import pygame as pg

from vars import *


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
        self.rect = self.image.get_rect().move(dx + self.width * pos_x, dy + self.height * pos_y)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['000000'] * width for _ in range(height)]
        # значения по умолчанию
        self.dx = 10
        self.dy = 10
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.dx = left
        self.dy = top
        self.cell_size = cell_size

    def generate_level(self, level_map, images):
        for y in range(len(level_map)):
            for x in range(len(level_map[y])):
                tile_type = color_coding[int(level_map[y][x])]
                Tile(images[tile_type], self.cell_size, self.cell_size,
                     x, y, self.dx, self.dy)
                self.board[y][x] = tile_type

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pg.draw.rect(screen, pg.Color('#ffffff'), (
                    x * self.cell_size + self.dx, y * self.cell_size + self.dy, self.cell_size,
                    self.cell_size), 1)

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_cell(self, mouse_pos):
        if (self.dx <= mouse_pos[0] < self.dx + self.width * self.cell_size and
            self.dy <= mouse_pos[1] < self.dy + self.height * self.cell_size):
            return (int((mouse_pos[0] - self.dx) / self.cell_size),
                    int((mouse_pos[1] - self.dy) / self.cell_size))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def main() -> None:
    size = 300, 400
    screen = pg.display.set_mode(size)
    board = Board(5, 5)
    board.set_view(25, 125, 50)
    colorkey = None
    images = {}
    for filename in os.listdir(COLORS_PATH):
        fullname = os.path.join(COLORS_PATH, filename)
        if not os.path.isfile(fullname):
            continue
        image = pg.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        images[filename.split('.')[0]] = pg.transform.scale(image, (board.cell_size,) * 2)
    print(load_level(current_level))
    board.generate_level(load_level(current_level), images)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                board.get_click(mouse_pos)
        screen.fill('#000000')
        text1 = get_font(26).render(f'Level {current_level}', True, pg.Color('#ffffff'))
        screen.blit(text1, (25, 25))
        sprite_group.draw(screen)
        board.render(screen)
        pg.display.flip()
    pgquit()


if __name__ == '__main__':
    main()
