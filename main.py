import sys
import pygame
from hero import Player
from border import Border
from load_image import load_image
from make_world import make_world

FPS = 30
G = 7
Velocity = 10.4
JUMP = 20
SPEED = 0

pygame.init()
size = width, height = 1600, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None
tile_images = {
    '3': load_image('grassUP.png'),
    '-2': load_image('snow.png'),
    '1': load_image('dirt.png'),
    '2': load_image('cobble.png'),
    "-1": load_image('black.png')
}
filename = "level.txt"
tile_width = tile_height = 50

def start_screen():
    intro_text = ["Aiarret", "", "Выбор мира"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 150)
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
            elif level[y][x] == '3':
                Border(tile_images["3"], tiles_group, all_sprites, x * 16, y * 16)
            elif level[y][x] == '9':
                new_player = Player(G, SPEED, JUMP, player_group, all_sprites, tiles_group, x * 16,
                                    y * 16)
    return new_player, x, y

# В разработке
#     return None
#
#
# def on_click(self, cell_coords):
#     global turn
#     if not turn and cell_coords is not None:
#         turn = self.board[cell_coords[0]][cell_coords[1]]
#     if cell_coords is not None and self.board[cell_coords[0]][cell_coords[1]] == turn:
#         for i in range(self.height):
#             self.board[i][cell_coords[1]] = turn
#         for i in range(self.width):
#             self.board[cell_coords[0]][i] = turn
#         turn = (turn % 2) + 1
#
def get_click(self, mouse_pos):
    cell = self.get_cell(mouse_pos)
    self.on_click(cell)


class Camera:
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.x = 150 * 8
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
        if 1200 < self.x - (target.rect.x + target.rect.w // 2 - width // 2) or self.x - (
                target.rect.x + target.rect.w // 2 - width // 2) < 400:
            self.dx = 0
        else:
            self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
            self.x += -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    running = True
    start_screen()
    make_world('level1.txt')
    player, level_x, level_y = generate_level(load_level('level1.txt'))
    camera = Camera((width, height))
    motion_left = 0
    motion_right = 0
    jump = 0
    jumpCount = JUMP
    for i in range(200):
        Border(tile_images["-1"], tiles_group, all_sprites, -1 * 16, i * 16)
    for i in range(200):
        Border(tile_images["-1"], tiles_group, all_sprites, 150 * 16, i * 16)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    motion_left = 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    motion_right = 1
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    jump = 1
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    motion_right = 0
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    motion_left = 0
                if event.key == pygame.K_SPACE:
                    jump = 0
            # В разработке
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     Border.get_click(event.pos)
        if jumpCount >= 0 and jump and player.check_collision(0, 100, tiles_group):
            print(jumpCount)
            player.move(0, -jumpCount, player.border_sprites)
            jumpCount -= 1
        else:
            jumpCount = player.JUMP
            jump = 0
        keys = pygame.key.get_pressed()
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
