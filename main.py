import sys
import pygame
from hero import Player
from border import Border
from load_image import load_image

FPS = 30
G = 3
Velocity = 3.4
JUMP = 10
SPEED = 0

pygame.init()
size = width, height = 1600, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None
player_image = load_image("hero_idle_animated1.png")
tile_images = {
    '-1': load_image('grassUP.png'),
    '-2': load_image('snow.png'),
    '1': load_image('dirt.png'),
    '2': load_image('cobble.png')
}
filename = "level.txt"
tile_width = tile_height = 50

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
def start_screen():
    intro_text = ["Aiarret", "", "", "", "Выбор мира"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 172)
    text_coord = 50
    for line in intro_text:
        s_render = font.render(line, True, pygame.Color(0, 150, 0))
        intro_rect = s_render.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width / 2 - 250
        text_coord += intro_rect.height
        screen.blit(s_render, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '0'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "1":
                Border(tile_images["1"], tiles_group, all_sprites, x * 16, y * 16)
            elif level[y][x] == '2':
                Border(tile_images["2"], tiles_group, all_sprites, x * 16, y * 16)
            elif level[y][x] == '9':
                new_player = Player(G, SPEED, JUMP, player_group, all_sprites, tiles_group, player_image, x * 16,
                                    y * 16)
    return new_player, x, y


class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
        if obj.rect.x >= self.field_size[0] * obj.rect.width:
            obj.rect.x += (self.field_size[0] + 1) * (-obj.rect.width)
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
        if obj.rect.y >= self.field_size[1] * obj.rect.height:
            obj.rect.y += (self.field_size[1] + 1) * (-obj.rect.height)

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    running = True
    start_screen()
    player, level_x, level_y = generate_level(load_level('level1.txt'))
    camera = Camera((width, height))
    motion_left = 0
    motion_right = 0
    jump = 0
    jumpCount = JUMP
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    motion_left = 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    motion_right = 1
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) \
                        and pygame.sprite.spritecollideany(player, tiles_group):
                    jump = 1
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    motion_right = 0
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    motion_left = 0
                if event.key == pygame.K_SPACE:
                    jump = 0
        keys = pygame.key.get_pressed()
        if jumpCount >= 0 and jump:
            player.rect.y -= (jumpCount * abs(jumpCount)) * 0.25
            jumpCount -= 1
        else:
            jumpCount = JUMP
            jump = 0
        player.update(motion_right, motion_left, jump, Velocity)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill((0, 204, 204))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()

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
#
#
