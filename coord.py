import os

import pygame as pg

from vars import *


def proverka(pt1, pt2, screen):
    if pt2 is None or pt1 is None:
        return
    if pt2[0] == pt1[0] or pt2[1] == pt1[1] or abs(pt2[0] - pt1[0]) == abs(pt1[1] - pt2[1]):
        pg.draw.line(screen, pg.Color('#ff00ff'), (pt1[0] * 50 + 50, pt1[1] * 50 + 150), (pt2[0] * 50 + 50, pt2[1] * 50 + 150), 5)
    print(pt1, pt2)


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
        self.board = [['000000'] * width for _ in range(height)]
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

    def check_selected(self) -> list[tuple[int, int]]:
        if self.pt1 is None or self.pt2 is None or self.pt1 == self.pt2:
            return []
        range_x = range(min(self.pt1[0], self.pt2[0]), max(self.pt1[0], self.pt2[0]) + 1)
        range_y = range(min(self.pt1[1], self.pt2[1]), max(self.pt1[1], self.pt2[1]) + 1)
        return ([(self.pt1[0], y) for y in range_y] if self.pt1[0] == self.pt2[0] else
                [(x, self.pt1[1]) for x in range_x] if self.pt1[1] == self.pt2[1] else
                [(x, y) for x, y in zip(range_x, range_y)] if abs(self.pt1[0] - self.pt2[0]) == abs(self.pt1[1] - self.pt2[1]) else [])

    def draw_selected(self, screen):
        if self.pt2 is None or self.pt1 is None or self.pt1 == self.pt2:
            return
        pg.draw.line(screen, pg.Color('#00ff00'
                                              if self.pt1[0] == self.pt2[0] or self.pt1[1] == self.pt2[1] or
                                                 abs(self.pt1[0] - self.pt2[0]) == abs(self.pt1[1] - self.pt2[1]) else '#ff0000'),
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
                pg.draw.rect(screen, pg.Color('#7f7f7f'), (
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


def main() -> None:
    size = 300, 400
    screen = pg.display.set_mode(size)
    pg.display.set_caption(game_name)
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
        images[filename.split('.')[0]] = pg.transform.scale(image, (board.cell_size * .9,) * 2)
    board.generate_level(load_level(current_level), images)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                clicked_tile = board.get_click(event.pos)
                if clicked_tile is None:
                    continue
                if board.board[clicked_tile[1]][clicked_tile[0]] == '000000':
                    continue
                if event.button == 1:
                    board.pt1 = clicked_tile
                if event.button == 3:
                    board.pt2 = clicked_tile
                print(board.check_selected())
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    board.pt1 = board.pt2 = None
        screen.fill('#000000')
        text1 = get_font(26).render(f'Level {current_level}', True, pg.Color('#ffffff'))
        screen.blit(text1, (25, 25))
        if board.check_win():
            text2 = get_font(26).render('completed!', True, pg.Color('#00ffff'))
            screen.blit(text2, (25, 60))
        else:
            sprite_group.draw(screen)
            board.render(screen)
        board.draw_selected(screen)
        pg.display.flip()
    pgquit()


if __name__ == '__main__':
    main()
