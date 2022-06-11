import pygame, sys


pygame.init()
screen_stat = {'width': 10, 'height': 10, 'tile': 40}
fps = 30
title = 'Sokoban game'

black = (0, 0, 0)
display = (screen_stat['width'] * screen_stat['tile'], screen_stat['height'] * screen_stat['tile'])
window = pygame.display.set_mode(display)

pygame.display.set_caption(title)

clock = pygame.time.Clock()


def load_image(name):
    fullname =  name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('name', '213')
        raise SystemExit()

    return image


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

    return player, x, y, box


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(pygame.image.load(tile_type), (40, 40))
        self.rect = self.image.get_rect().move(40*pos_x, 40*pos_y)

        if tile_type == 'images/wall.png':
            self.add(walls_group, all_sprites, tiles_group)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(40*pos_x, 40*pos_y)
        self.speed = 40
        self.add(player_group)

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed



class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/box.png'), (40, 40))
        self.rect = self.image.get_rect().move(40*pos_x, 40*pos_y)

        self.add(all_sprites, boxes_group)

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/wall.png'), (40, 40))
        self.rect = self.image.get_rect().move(40*pos_x, 40*pos_y)

        self.add(all_sprites, walls_group)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()


def level_1():
    player, level_x, level_y, box = draw_level(load_level('level1.txt'))
    speed = 40
    run = True
    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                player.move_up()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move_down()
                if pygame.sprite.spritecollideany(player, boxes_group):
                    box.rect.y -= speed

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                player.move_down()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move_up()
                if pygame.sprite.spritecollideany(player, boxes_group):
                    box.rect.y += speed

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                player.move_left()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move_right()
                if pygame.sprite.spritecollideany(player, boxes_group):
                    box.rect.x -= speed

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                player.move_right()
                if pygame.sprite.spritecollideany(player, walls_group):
                    player.move_left()
                if pygame.sprite.spritecollideany(player, boxes_group):
                    box.rect.x += speed

        window.fill((135, 206, 250))
        all_sprites.draw(window)
        player_group.draw(window)
        walls_group.draw(window)
        pygame.display.flip()


level_1()





