import pygame





def load_level(name):
    fullname = name
    with open(fullname, 'r') as map_file:
        level_map = []
        for line in map_file:
            line = line.strip()
            level_map.append(line)
    return level_map


def draw_level(level_map):
    player, x, y, box, wall = None, None, None, None, None
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '#':
                wall = Wall(x, y)
            elif level_map[y][x] == '*':
                player = Player(x, y)
            elif level_map[y][x] == '&':
                box = Box(x, y)
            elif level_map[y][x] == '@':
                Tile('images/box_space.png', x, y)
            elif level_map[y][x] == '-':
                Teleport(x, y)
            elif level_map[y][x] == '.':
                Tile('images/floor.png', x, y)

    return player, x, y, box, wall,


def draw_tile():
    window.fill((135, 206, 250))

    all_sprites.draw(window)

    pygame.display.flip()


class Move():


    def update(self, event, player, box):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            player.move_up()
            if pygame.sprite.spritecollideany(player, walls_group):
                player.move_down()
            if pygame.sprite.collide_mask(player, box):
                box.rect.y -= 40
                if pygame.sprite.spritecollideany(box, walls_group):
                    box.rect.y += 40
                    player.move_down()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            player.move_down()
            if pygame.sprite.spritecollideany(player, walls_group):
                player.move_up()
            if pygame.sprite.collide_mask(player, box):
                box.rect.y += 40
                if pygame.sprite.spritecollideany(box, walls_group):
                    box.rect.y -= 40
                    player.move_up()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            player.move_left()
            if pygame.sprite.spritecollideany(player, walls_group):
                player.move_right()
            if pygame.sprite.collide_mask(player, box):
                box.rect.x -= 40
                if pygame.sprite.spritecollideany(box, walls_group):
                    box.rect.x += 40
                    player.move_right()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            player.move_right()
            if pygame.sprite.spritecollideany(player, walls_group):
                player.move_left()
            if pygame.sprite.collide_mask(player, box):
                box.rect.x += 40
                if pygame.sprite.spritecollideany(box, walls_group):
                    box.rect.x -= 40
                    player.move_left()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(tile_type), (40, 40))
        self.rect = self.image.get_rect().move(40 * pos_x, 40 * pos_y)

        if tile_type == 'images/wall.png':
            self.add(all_sprites, tiles_group)


class Teleport(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/Teleport.png'), (40, 40))
        self.rect = self.image.get_rect().move((40 * pos_x, 40 * pos_y))

        self.add(all_sprites, telep_sprites)




class Player(pygame.sprite.Sprite, Move):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(40 * pos_x, 40 * pos_y)
        self.speed = 40
        self.add(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y

    def collide_player(self, player, telep_sprites):
        if pygame.sprite.spritecollideany(player, telep_sprites):
            player.rect.x = 80

    def move_up(self):
        self.rect.y -= 40


    def move_down(self):
        self.rect.y += 40

    def move_left(self):
        self.rect.x -= 40

    def move_right(self):
        self.rect.x += 40

class Box(pygame.sprite.Sprite, Move):
    def __init__(self, pos_x, pos_y):
        super().__init__(boxes_group)
        self.image = pygame.transform.scale(pygame.image.load('images/box.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(40 * pos_x, 40 * pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.add(all_sprites, boxes_group)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/wall.png'), (40, 40))
        self.rect = self.image.get_rect().move(40 * pos_x, 40 * pos_y)

        self.add(all_sprites, walls_group)


class Button():
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            print(123)

        window.blit(self.image, (self.rect.x, self.rect.y))


pygame.init()
screen_stat = {'width': 10, 'height': 10, 'tile': 40}
fps = 30
title = 'Sokoban game'

display = (screen_stat['width'] * screen_stat['tile'], screen_stat['height'] * screen_stat['tile'])
window = pygame.display.set_mode(display)
exit_img = pygame.image.load('images/exit.png')
start_img = pygame.image.load('images/start.png')
pygame.display.set_caption(title)

clock = pygame.time.Clock()

exit_but = Button(120, 120, exit_img)
start_but = Button(120, 120, start_img)
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
telep_sprites = pygame.sprite.Group()
move = Move()


def level_1():
    player, level_x, level_y, box, wall = draw_level(load_level('level1.txt'))

    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                all_sprites.empty()
                player_group.empty()
                run = False
                level_1()

            move.update(event, player, box)

        player.collide_player(player, telep_sprites)

        if pygame.sprite.spritecollideany(box, tiles_group):
            all_sprites.empty()
            walls_group.empty()
            player_group.empty()

            run = False

        draw_tile()

        pygame.display.flip()


def level_2():
    player, level_x, level_y, box, wall = draw_level(load_level('level2.txt'))
    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                all_sprites.empty()
                walls_group.empty()
                player_group.empty()
                boxes_group.empty()
                tiles_group.empty()
                run = False
                level_2()

            move.update(event, player, box)

        if pygame.sprite.spritecollideany(box, tiles_group):
            run = False

        draw_tile()


if __name__ == '__main__':
    level_1()
    level_2()
