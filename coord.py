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

    def generate_level(self, level_map, images):
        for y in range(len(level_map)):
            for x in range(len(level_map[y])):
                self.board[y][x] = color_coding[int(level_map[y][x])]
                Tile(images[self.board[y][x]], self.cell_size, self.cell_size,
                     x, y, self.dx, self.dy)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pg.draw.rect(screen, pg.Color('#ffffff'), (
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
                if event.button == 1:
                    board.pt1 = clicked_tile
                    board.change_tile('000000', clicked_tile[0], clicked_tile[1], images)
                if event.button == 3:
                    board.pt2 = clicked_tile
                if event.button == 2:
                    board.pt1 = board.pt2 = None
                print(board.pt1, board.pt2)
        screen.fill('#000000')
        text1 = get_font(26).render(f'Level {current_level}', True, pg.Color('#ffffff'))
        screen.blit(text1, (25, 25))
        if board.check_win():
            text2 = get_font(26).render('completed!', True, pg.Color('#00ffff'))
            screen.blit(text2, (25, 60))
        else:
            sprite_group.draw(screen)
            board.render(screen)
        pg.display.flip()
    pgquit()


if __name__ == '__main__':
    main()
