import pygame


def main_menu():
    pygame.init()
    size = (300, 300)
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('white'))
    f1 = pygame.font.SysFont('serif', 26)
    text1 = f1.render('Супер название', True, (180, 0, 0))
    screen.blit(text1, (70, 50))
    pygame.draw.rect(screen, pygame.Color('red'), (100, 85, 100, 50))
    f2 = pygame.font.SysFont('serif', 26)
    text2 = f2.render('Играть', True, pygame.Color('white'))
    screen.blit(text2, (110, 90))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 100 < event.pos[0] < 200 and 85 < event.pos[1] < 135:
                    print('ye')
    pygame.quit()


def first():
    pygame.init()
    size = (300, 300)
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('blue'))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()
    pygame.quit()


try:
    first()
except Exception:
    pygame.quit()