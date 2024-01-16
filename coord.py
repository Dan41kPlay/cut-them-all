import os

import pygame as pg

from vars import *


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0x000000] * width for _ in range(height)]
        # значения по умолчанию
        self.dx = 10
        self.dy = 10
        self.cell_size = 50
        self.images = {}

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.dx = left
        self.dy = top
        self.cell_size = cell_size

    def load_images(self, colorkey=None):
        for filename in os.listdir(os.path.join('data', 'colors')):
            fullname = os.path.join('data', 'colors', filename)
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
            self.images[filename.split('.')[0]] = image

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
    board.load_images()
    print(board.images)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                board.get_click(mouse_pos)
        screen.fill('#000000')
        text1 = get_font(26).render('Level 0', True, pg.Color('#ffffff'))
        screen.blit(text1, (25, 25))
        board.render(screen)
        pg.display.flip()
    pgquit()


if __name__ == '__main__':
    main()
