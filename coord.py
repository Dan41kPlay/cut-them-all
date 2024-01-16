import pygame as pg

from vars import *


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pg.draw.rect(screen, pg.Color('#ffffff'), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def on_click(self, cell_coords):
        print(cell_coords)

    def get_cell(self, mouse_pos):
        if (self.left <= mouse_pos[1] < self.left + self.height * self.cell_size and self.top <=
                mouse_pos[0] < self.top + self.width * self.cell_size):
            return (int((mouse_pos[1] - self.left) / self.cell_size),
                    int((mouse_pos[0] - self.top) / self.cell_size))

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


def main() -> None:
    size = 300, 400
    screen = pg.display.set_mode(size)
    board = Board(5, 5)
    # board.set_view(25, 125, 50)
    text1 = getFont(26).render('Cut them all!', True, pg.Color('#ffffff'))
    screen.blit(text1, (25, 25))
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                board.get_click(mouse_pos)
        screen.fill('#000000')
        board.render(screen)
        pg.display.flip()
    pgquit()


if __name__ == '__main__':
    main()
