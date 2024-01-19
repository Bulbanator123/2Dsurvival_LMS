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
DELETE_BLOCKS = 0
PLACE_BLOCKS = 0
GAME_ACTIVE = 0

pygame.init()
current_world = 1
Update_lvl = 0
size = width, height = 1600, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
level_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()
player = None
tile_images = {
    '8': load_image('sand.png'),
    '7': load_image('jungle_dirtUp.png'),
    '6': load_image('jungle_dirt.png'),
    '5': load_image('sandblock_underground.png'),
    '4': load_image('snow.png'),
    '3': load_image('grassUp.png'),
    '1': load_image('dirt.png'),
    '2': load_image('cobble.png'),
    "-1": load_image('black.png'),
}
current_block = "1"
filename = {1: "level1",
            2: "level2",
            3: "level3",
            4: "level4",
            5: "level5"}
tile_width = tile_height = 50


class PNG(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(level_group, all_sprites)
        self.image = load_image(f"{name}.png")
        self.rect = self.image.get_rect().move(x, y)


class Level(pygame.sprite.Sprite):
    def __init__(self, current_number, x, y):
        super().__init__(level_group, all_sprites)
        self.current_number = current_number
        self.image = load_image(f"{filename[current_number]}.jpg")
        self.rect = self.image.get_rect().move(x, y)

    def return_current_number(self):
        return int(self.current_number)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(button_group, all_sprites)
        self.image = load_image(f"End_Button.png")
        self.x = x
        self.y = y
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        self.rect = self.image.get_rect().move(self.x, self.y)


def get_cell(mouse_pos):
    x = mouse_pos[1] // 16
    y = mouse_pos[0] // 16
    if 0 <= x < 150 and 0 <= y < 150:
        return x, y
    return None


def delete():
    for el in tiles_group:
        if el.rect.collidepoint(event.pos) and el not in border_group:
            if get_cell(event.pos) is None:
                return
            tiles_group.remove(el)
            global DELETE_BLOCKS
            DELETE_BLOCKS += 1
            save_update(*get_cell(event.pos), "0")


def place():
    for el in tiles_group:
        if el.rect.collidepoint(event.pos):
            return
    for x in range(player.rect.centerx - 32, player.rect.centerx + 32):
        for j in range(player.rect.centery - 32, player.rect.centery + 32):
            if event.pos[0] == x and event.pos[1] == j:
                return
    if get_cell(event.pos) is None:
        return
    Border(tile_images[current_block], tiles_group, all_sprites, (event.pos[0]) - (event.pos[0] - 8) % 16,
           (event.pos[1]) - (event.pos[1] - 8) % 16)
    save_update(*get_cell(event.pos), current_block)
    global PLACE_BLOCKS
    PLACE_BLOCKS += 1


def orf(a):
    if a % 10 == 1 and a % 100 != 11:
        return ""
    elif a % 10 in [2, 3, 4] and a % 100 not in [12, 13, 14]:
        return "a"
    else:
        return "ов"


def final_screen():
    intro_text = ["Вы завершили игру!", f"Вы поставили {PLACE_BLOCKS} блок{orf(PLACE_BLOCKS)}",
                  f"Вы удалили {DELETE_BLOCKS} блок{orf(DELETE_BLOCKS)}"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 72)
    text_coord = 30
    for line in intro_text:
        s_render = font.render(line, True, pygame.Color(0, 0, 0))
        intro_rect = s_render.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width / 2 - 250
        text_coord += intro_rect.height
        screen.blit(s_render, intro_rect)
    finalbtn = Button(700, 500)
    br = finalbtn.rect
    bi = finalbtn.image
    screen.blit(bi, br)
    while True:
        for nevent in pygame.event.get():
            if nevent.type == pygame.QUIT:
                terminate()
            elif nevent.type == pygame.MOUSEBUTTONDOWN:
                for el in button_group:
                    if el.rect.collidepoint(nevent.pos):
                        for el in button_group:
                            button_group.remove(el)
                        start_screen()
                        return
        finalbtn.update()
        pygame.display.flip()
        clock.tick(FPS)


def save_update(x, y, swap):
    with open(f"data/{filename[current_world]}.txt", "r") as file:
        mapa = [i for i in file.readlines() if i != "\n"]
        m = list(mapa[x])
        m[y] = swap
        mapa[x] = "".join(m)
        with open(f"data/{filename[current_world]}.txt", "w") as file:
            file.writelines("".join(["".join([str(j) for j in i]) for i in mapa]))


def start_screen():
    intro_text = ["", "", "", "", "Выбор мира"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 72)
    text_coord = 30
    for line in intro_text:
        s_render = font.render(line, True, pygame.Color(0, 10, 0))
        intro_rect = s_render.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = width / 2 - text_coord / 2
        text_coord += intro_rect.height
        screen.blit(s_render, intro_rect)
    Game_Name = PNG(500, 30, "Name_of_the_game")
    gr, gi = Game_Name.rect, Game_Name.image
    screen.blit(gi, gr)
    text_coord = 700
    x = 200
    for level in range(1, 6):
        image = Level(level, x, text_coord)
        s_image = image.image
        s_render = s_image.get_rect()
        s_render.width = 200
        s_render.height = 200
        s_render.y = text_coord
        s_render.x = x
        screen.blit(s_image, s_render)
        x += 250
    while True:
        for nevent in pygame.event.get():
            if nevent.type == pygame.QUIT:
                terminate()
            elif nevent.type == pygame.MOUSEBUTTONDOWN:
                for el in level_group:
                    if el.rect.collidepoint(nevent.pos):
                        global current_world, Update_lvl, GAME_ACTIVE
                        GAME_ACTIVE = 1
                        if nevent.button == 3:
                            Update_lvl = 1
                        current_world = el.return_current_number()
                        return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(level_filename):
    level_filename = 'data/' + level_filename
    with open(level_filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '0'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] not in ["9", "0"]:
                Border(tile_images[level[y][x]], tiles_group, all_sprites, x * 16, y * 16)
            elif level[y][x] == '9':
                new_player = Player(G, SPEED, JUMP, player_group, all_sprites, tiles_group, border_group, x * 16,
                                    y * 16)
    return new_player, x, y


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
        if 1200 <= self.x - (target.rect.x + target.rect.w // 2 - width // 2) or self.x - (
                target.rect.x + target.rect.w // 2 - width // 2) <= 400:
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
    new_cur_num = current_world
    GAME_ACTIVE = 1
    while running:
        if GAME_ACTIVE:
            if Update_lvl:
                make_world(f'{filename[current_world]}.txt')
            for i in range(200):
                Border(tile_images["-1"], border_group, all_sprites, -1 * 16, i * 16)
            for i in range(200):
                Border(tile_images["-1"], border_group, all_sprites, 1600, i * 16)
            player, level_x, level_y = generate_level(load_level(f'{filename[current_world]}.txt'))
            camera = Camera((width, height))
            motion_left = 0
            motion_right = 0
            jump = 0
            jumpCount = JUMP
            button = Button(1400, 50)
            GAME_ACTIVE = 0
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
                if event.key == pygame.K_1:
                    current_block = "1"
                elif event.key == pygame.K_2:
                    current_block = "2"
                elif event.key == pygame.K_3:
                    current_block = "3"
                elif event.key == pygame.K_4:
                    current_block = "4"
                elif event.key == pygame.K_5:
                    current_block = "5"
                elif event.key == pygame.K_6:
                    current_block = "6"
                elif event.key == pygame.K_7:
                    current_block = "7"
                elif event.key == pygame.K_8:
                    current_block = "8"
                elif event.key == pygame.K_9:
                    current_block = "9"
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    motion_right = 0
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    motion_left = 0
                if event.key == pygame.K_SPACE:
                    jump = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                delete()
                for el in button_group:
                    if el.rect.collidepoint(event.pos):
                        surface = pygame.Surface((1600, 1000))
                        screen.blit(surface, (0, 0))
                        for el in all_sprites:
                           all_sprites.remove(el)
                        for el in tiles_group:
                           tiles_group.remove(el)
                        for el in player_group:
                           player_group.remove(el)
                        player = None
                        final_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                place()
        if not GAME_ACTIVE:
            if jumpCount >= 0 and jump:
                player.move(0, -jumpCount, player.border_sprites)
                jumpCount -= 1
            else:
                jumpCount = 0
                jump = 0
            if player.check_collision(0, 10, tiles_group):
                jumpCount = player.JUMP
            if not jump and player.check_collision(0, 10, tiles_group) and not (motion_right or motion_left):
                player.idle_animation_f()
            elif not jump and player.check_collision(0, 10, tiles_group) and (motion_right or motion_left):
                player.walk_animation_f()
            else:
                player.make_zero()
                player.jump_animation()
            keys = pygame.key.get_pressed()
            player.update(motion_right, motion_left, jump, Velocity)
            camera.update(player)
            button.update()
            for sprite in all_sprites:
                if sprite not in button_group and sprite not in border_group:
                    camera.apply(sprite)
        screen.fill((0, 204, 204))
        tiles_group.draw(screen)
        player_group.draw(screen)
        button_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    terminate()
