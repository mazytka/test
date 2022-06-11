import pygame, sys

level1 = [
    " #  #  # #",
    "     #    ",
    "    ###   ",
    "          ",
    "  *###  * ",
    " *      & ",
    "    ####  ",
    "   ##     ",
    "        # ",
    "   ###    ",
]


class MoveBox:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):

        lst = lvl1.get_coord_wall()
        lst1 = lvl1.get_coord_box()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and self.y > 0:
                self.y -= speed
                if (self.x, self.y) in lst:
                    self.y += speed
            elif event.key == pygame.K_s and self.y < screen_stat['width'] * screen_stat['tile'] - 40:
                self.y += speed
                if (self.x, self.y) in lst:
                    self.y -= speed

                if (self.x, self.y) in lst1:
                    pass

            elif event.key == pygame.K_d and self.x < screen_stat['height'] * screen_stat['tile'] - 40:
                self.x += speed
                if (self.x, self.y) in lst:
                    self.x -= speed
            elif event.key == pygame.K_a and self.x > 0:
                self.x -= speed
                if (self.x, self.y) in lst:
                    self.x += speed


class Player(pygame.sprite.Sprite, MoveBox):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()


class Box(pygame.sprite.Sprite, MoveBox):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect()
        self.boxes = pygame.sprite.Group()


class Wall(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill('grey')
        self.rect = self.image.get_rect()


class GenerateLevel:

    def __init__(self, level, coord_x=0, coord_y=0):
        self.level = level
        self.coord_x = coord_x
        self.coord_y = coord_y

    def get_lvl(self):

        for x in range(len(self.level)):
            for y in range(len(self.level[x])):
                self.coord_x = x * screen_stat['tile']
                self.coord_y = y * screen_stat['tile']

                if self.level[y][x] == "#":
                    window.blit(wall.image, (self.coord_x, self.coord_y))

                if self.level[y][x] == "*":
                    window.blit(box.image, (self.coord_x, self.coord_y))

                if self.level[y][x] == "&":
                    window.blit(player.image, (player.x, player.y))

    def get_coord_wall(self):
        lst = []
        for x in range(len(self.level)):
            for y in range(len(self.level[x])):
                self.coord_x = x * 40
                self.coord_y = y * 40
                if self.level[y][x] == "#":
                    lst.append((self.coord_x, self.coord_y))
        return lst

    def get_coord_player(self):
        lst = []
        for x in range(len(self.level)):
            for y in range(len(self.level[x])):
                self.coord_x = x * 40
                self.coord_y = y * 40
                if self.level[y][x] == "&":
                    lst.append((self.coord_x, self.coord_y))
        return lst

    def get_coord_box(self):
        lst = []
        for x in range(len(self.level)):
            for y in range(len(self.level[x])):
                self.coord_x = x * 40
                self.coord_y = y * 40
                if self.level[y][x] == "*":
                    lst.append((self.coord_x, self.coord_y))

        return lst

    def collision(self):
        pass


lvl1 = GenerateLevel(level1)

player = Player(lvl1.get_coord_player()[0][0], lvl1.get_coord_player()[0][1])
box = Box()

wall = Wall()
pygame.init()
screen_stat = {'width': 10, 'height': 10, 'tile': 40}
fps = 30
title = 'Sokoban game'

black = (0, 0, 0)
display = (screen_stat['width'] * screen_stat['tile'], screen_stat['height'] * screen_stat['tile'])
window = pygame.display.set_mode(display)

pygame.display.set_caption(title)

clock = pygame.time.Clock()

speed = 40

run = True

while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        player.move()

    window.fill((135, 206, 250))
    lvl1.get_lvl()
    pygame.display.update()

pygame.quit()
