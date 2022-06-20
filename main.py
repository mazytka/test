import sys
import pygame


def load_level(name):
    """Функция, принимающая имя файла уровня"""
    fullname = 'Levels' + '/' + name
    with open(fullname, 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            level_map.append(line)
    return level_map  # Возвращает готовый уровень из файла


def draw_level(level_map):
    """Функция отрисовки самого уровня"""
    player, x, y, box, wall, telep_ex = None, None, None, None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '#':
                wall = Wall(x, y)
            elif level_map[y][x] == '*':
                player = Player(x, y)
            elif level_map[y][x] == '&':
                box = Box(x, y)  # Прорисовка уровня, каждому символу соответствует объект
            elif level_map[y][x] == '@':
                Tile('images/box_space.png', x, y)
            elif level_map[y][x] == '-':
                TeleportIn(x, y)
            elif level_map[y][x] == '+':
                telep_ex = TeleportEx(x, y)
            elif level_map[y][x] == '.':
                Tile('images/floor.png', x, y)

    return player, x, y, box, wall, telep_ex


def main_menu():
    """Функция отображения главного меню пользователя"""
    while True:
        window.blit(bg, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        menu_title = pygame.font.SysFont("cambria", 75).render("SOKOBAN", True, 'black')
        menu_rect = menu_title.get_rect(center=(200, 50))

        start_but = Button(start_img, 209, 160, 'START')  # Создание двух экземпляров класса Button
        quit_but = Button(exit_img, 210, 300, 'EXIT')

        window.blit(menu_title, menu_rect)
        for button in [start_but, quit_but]:
            button.changeColor(mouse_pos)
            button.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_but.checkForInput(mouse_pos):
                    return False

                if quit_but.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def game_over():
    """Функция отображения конечного меню пользователя"""
    while True:
        window.fill((135, 206, 250))

        mouse_pos = pygame.mouse.get_pos()

        menu_title = pygame.font.SysFont("cambria", 75).render("GAME OVER", True, 'black')
        menu_rect = menu_title.get_rect(center=(200, 50))

        quit_but = Button(exit_img, 210, 300, 'EXIT')

        window.blit(menu_title, menu_rect)

        quit_but.changeColor(mouse_pos)
        quit_but.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_but.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def draw_sprite():
    """Функция отрисовки главного экрана и всех спрайтов"""
    window.fill((135, 206, 250))
    all_sprites.draw(window)
    player_group.draw(window)


def game_run(level_txt):
    global goals
    player, level_x, level_y, box, wall, telep_ex = draw_level(load_level(level_txt))
    run = True
    lst = []
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                all_sprites.empty()
                walls_group.empty()
                player_group.empty()
                boxes_group.empty()
                box_spaces.empty()

                run = False
                game_run(level_txt)

            move.update(event, player, box)

        if pygame.sprite.groupcollide(boxes_group, box_spaces, True, True):
            if not box_spaces.sprites():
                all_sprites.empty()
                player_group.empty()
                walls_group.empty()
                telep_sprites.empty()
                run = False

        if pygame.sprite.spritecollideany(player, telep_sprites):
            player.rect.x, player.rect.y = telep_ex.rect.x,  telep_ex.rect.y

        draw_sprite()

        pygame.display.update()


class Move:
    """Класс для отслеживания действий персонажа с другими объектами"""

    def update(self, event, player, box):
        global vector

        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            player.move_up()
            vector = 'UP'
            if pygame.sprite.spritecollideany(player, walls_group):
                player.move_down()
            if pygame.sprite.spritecollideany(player, boxes_group):
                boxes_group.update(player, walls_group)
                if pygame.sprite.spritecollideany(box, walls_group):
                    boxes_group.update(player, walls_group)
                if pygame.sprite.spritecollideany(player, boxes_group):
                    player.move_down()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            player.move_down()
            vector = 'DOWN'
            if pygame.sprite.spritecollideany(player, walls_group):
                player.move_up()
            if pygame.sprite.spritecollideany(player, boxes_group):
                boxes_group.update(player, walls_group)
                if pygame.sprite.spritecollideany(box, walls_group):
                    boxes_group.update(player, walls_group)
                if pygame.sprite.spritecollideany(player, boxes_group):
                    player.move_up()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            player.move_left()
            vector = 'LEFT'
            if pygame.sprite.spritecollideany(player, walls_group):
                player.move_right()
            if pygame.sprite.spritecollideany(player, boxes_group):
                boxes_group.update(player, walls_group)
                if pygame.sprite.spritecollideany(box, walls_group):
                    boxes_group.update(player, walls_group)
                if pygame.sprite.spritecollideany(player, boxes_group):
                    player.move_right()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            player.move_right()
            vector = 'RIGHT'
            if pygame.sprite.spritecollideany(player, walls_group):
                player.move_left()
            if pygame.sprite.spritecollideany(player, boxes_group):
                boxes_group.update(player, walls_group)
                if pygame.sprite.spritecollideany(box, walls_group):
                    boxes_group.update(player, walls_group)
                if pygame.sprite.spritecollideany(player, boxes_group):
                    player.move_left()


class Tile(pygame.sprite.Sprite):
    """Класс тайлов"""

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(tile_type), (40, 40))
        self.rect = self.image.get_rect().move(40 * pos_x, 40 * pos_y)

        if tile_type == 'images/box_space.png':
            self.add(box_spaces)


class TeleportIn(pygame.sprite.Sprite):
    """Класс телепорта"""

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/Teleport.png'), (40, 40))
        self.rect = self.image.get_rect().move((40 * pos_x, 40 * pos_y))

        self.add(all_sprites, telep_sprites)


class TeleportEx(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/teleport_exit.png'), (40, 40))
        self.rect = self.image.get_rect().move((40 * pos_x, 40 * pos_y))

        self.add(all_sprites)


class Player(pygame.sprite.Sprite, Move):
    """Класс игрока"""

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/player.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(40 * pos_x, 40 * pos_y)
        self.speed = 40
        self.add(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y

    def move_up(self):
        self.rect.y -= 40

    def move_down(self):
        self.rect.y += 40

    def move_left(self):
        self.rect.x -= 40

    def move_right(self):
        self.rect.x += 40


class Box(pygame.sprite.Sprite, Move):
    """Класс ящика"""

    def __init__(self, pos_x, pos_y):
        super().__init__(boxes_group)
        self.image = pygame.transform.scale(pygame.image.load('images/box.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(40 * pos_x, 40 * pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.add(all_sprites, boxes_group)

    def update(self, *args):
        global vector
        lst = []
        for b in boxes_group:
            lst.append((b.rect.x, b.rect.y))
        if vector == 'UP':
            if pygame.sprite.collide_mask(self, args[0]):
                if (self.rect.x, self.rect.y - 40) in lst:
                    self.rect.y += 40
                self.rect.y -= 40

            if pygame.sprite.spritecollideany(self, args[1]):
                self.rect.y += 40

        if vector == 'DOWN':
            if pygame.sprite.collide_mask(self, args[0]):
                if (self.rect.x, self.rect.y + 40) in lst:
                    self.rect.y -= 40
                self.rect.y += 40
            if pygame.sprite.spritecollideany(self, args[1]):
                self.rect.y -= 40

        if vector == 'LEFT':
            if pygame.sprite.collide_mask(self, args[0]):
                if (self.rect.x - 40, self.rect.y) in lst:
                    self.rect.x += 40
                self.rect.x -= 40
            if pygame.sprite.spritecollideany(self, args[1]):
                self.rect.x += 40

        if vector == 'RIGHT':
            if pygame.sprite.collide_mask(self, args[0]):
                if (self.rect.x + 40, self.rect.y) in lst:
                    self.rect.x -= 40
                self.rect.x += 40
            if pygame.sprite.spritecollideany(self, args[1]):
                self.rect.x -= 40


class Wall(pygame.sprite.Sprite):
    """Класс стены"""

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/wall.png'), (40, 40))
        self.rect = self.image.get_rect().move(40 * pos_x, 40 * pos_y)

        self.add(all_sprites, walls_group)


class Button:
    """Класс для изображения кнопок и их взаимодейсвия с курсором мыши"""

    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        window.blit(self.image, self.rect)
        window.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = main_font.render(self.text_input, True, "green")
        else:
            self.text = main_font.render(self.text_input, True, "white")


vector = ''
pygame.init()
screen_stat = {'width': 10, 'height': 10, 'tile': 40}
fps = 30
title = 'Sokoban game'
main_font = pygame.font.SysFont("cambria", 45)
bg = pygame.transform.scale(pygame.image.load('images/bg.png'), (400, 400))
display = (screen_stat['width'] * screen_stat['tile'], screen_stat['height'] * screen_stat['tile'])
window = pygame.display.set_mode(display)

exit_img = pygame.transform.scale(pygame.image.load('images/exit.png'), (136, 50))
start_img = pygame.transform.scale(pygame.image.load('images/start.png'), (136, 60))

pygame.display.set_caption(title)
clock = pygame.time.Clock()
goals = []
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
telep_sprites = pygame.sprite.Group()
box_spaces = pygame.sprite.Group()
move = Move()

if __name__ == '__main__':
    main_menu()
    game_run('level1.txt')
    game_run('level2.txt')
    game_run('level3.txt')
    game_run('level4.txt')
    game_over()
