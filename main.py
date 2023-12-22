import sys
import pygame
import time
from hero import Player
from Grass import Border
from load_image import load_image

FPS = 50
STEP = 10
G = 1

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None
player_image = load_image('hero.png')
tile_images = {
    'grass': load_image('grassUP.png')
}
tile_width = tile_height = 50


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    running = True
    player = Player(G, player_group, all_sprites, tiles_group, player_image, 250, 200)
    for i in range(100):
        Border(tiles_group, all_sprites, tile_images, i * 16, 300)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rect.x -= STEP
                if event.key == pygame.K_RIGHT:
                    player.rect.x += STEP
                if event.key == pygame.K_SPACE and pygame.sprite.spritecollideany(player, tiles_group):
                    for i in range(10):
                        player.rect.y -= STEP / 5
        player.update()
        screen.fill((255, 255, 255))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()

#
#
# def load_level(filename):
#     filename = 'data/' + filename
#     with open(filename, 'r') as mapFile:
#         level_map = [line.strip() for line in mapFile]
#     max_width = max(map(len, level_map))
#     return list(map(lambda x: x.ljust(max_width, '.'), level_map))
#
#
#
#
# def start_screen():
#     intro_text = ["ЗАСТАВКА", "", "Правила игра", "Если в правилах несколько строк,",
#                   "приходится выводить их построчно"]
#     fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
#     screen.blit(fon, (0, 0))
#     font = pygame.font.Font(None, 30)
#     text_coord = 50
#     for line in intro_text:
#         s_render = font.render(line, True, pygame.Color("black"))
#         intro_rect = s_render.get_rect()
#         text_coord += 10
#         intro_rect.top = text_coord
#         intro_rect.x = 10
#         text_coord += intro_rect.height
#         screen.blit(s_render, intro_rect)
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 terminate()
#             elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
#                 return
#         pygame.display.flip()
#         clock.tick(FPS)
#
#
#
#
# class Tile(pygame.sprite.Sprite):
#     def __init__(self, tile_type, pos_x, pos_y):
#         super().__init__(tiles_group, all_sprites)
#         self.image = tile_images[tile_type]
#         self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
#
#
#
#
#
#     def update(self, *args):
#         if pygame.sprite.spritecollideany(self, border_group):
#             if args[1] == "x":
#                 self.rect.x -= args[0] * STEP
#             if args[1] == "y":
#                 self.rect.y -= args[0] * STEP
#
#
# def generate_level(level):
#     new_player, x, y = None, None, None
#     for y in range(len(level)):
#         for x in range(len(level[y])):
#             if level[y][x] == '.':
#                 Tile('empty', x, y)
#             elif level[y][x] == '#':
#                 Tile('wall', x, y)
#                 Border(x, y)
#             elif level[y][x] == '@':
#                 Tile('empty', x, y)
#                 new_player = Player(x, y)
#     return new_player, x, y
#
#
# class Camera:
#     def __init__(self, field_size):
#         self.dx = 0
#         self.dy = 0
#         self.field_size = field_size
#
#     def apply(self, obj):
#         obj.rect.x += self.dx
#         if obj.rect.x < -obj.rect.width:
#             obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
#         if obj.rect.x >= self.field_size[0] * obj.rect.width:
#             obj.rect.x += (self.field_size[0] + 1) * (-obj.rect.width)
#         obj.rect.y += self.dy
#         if obj.rect.y < -obj.rect.height:
#             obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
#         if obj.rect.y >= self.field_size[1] * obj.rect.height:
#             obj.rect.y += (self.field_size[1] + 1) * (-obj.rect.height)
#
#     def update(self, target):
#         self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
#         self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
