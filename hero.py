import pygame
import numpy
from load_image import load_image

f = "left"


class Player(pygame.sprite.Sprite):
    def __init__(self, G, SPEED, JUMP, player_group, all_sprites, border_sprites, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("hero_idle_animated1.png")
        self.border_sprites = border_sprites
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.JUMP = JUMP
        self.SPEED = SPEED
        self.G = G
        self.vy = self.G
        self.idle_animation = 1
        self.walk_animation = 1
        self.Move = 1

    def update(self, motion_right, motion_left, jump, Velocity):
        jumpCount = self.JUMP
        c = 1
        self.Move = 1
        global f
        if self.check_collision(0, 10, self.border_sprites):
            c = 0
        if c == 1:
            self.move(0, self.vy, self.border_sprites)
        # В разработке
        #     self.image = load_image("hero_jump_animated.png")
        #     self.mask = pygame.mask.from_surface(self.image)
        # else:
        #     ...
        #     self.image = load_image("hero_idle_animated1.png")
        #     self.mask = pygame.mask.from_surface(self.image)\
        if motion_left and motion_right:
            # В разработке
            # if not c:
            #     self.image = load_image(f"hero_walk_animated{self.idle_animation}.png")
            #     self.walk_animation %= 4
            #     self.walk_animation += 1
            #     self.mask = pygame.mask.from_surface(self.image)
            #     if f == "right":
            #         self.flip()
            ...
        elif motion_left:
            self.SPEED = min(Velocity, self.SPEED + 1)
            self.move(-self.SPEED, 0, self.border_sprites)
            # В разработке
            # if not c:
            #     self.image = load_image(f"hero_walk_animated{self.idle_animation}.png")
            #     self.walk_animation %= 4
            #     self.walk_animation += 1
            if f == "right":
                f = "left"
                self.flip()
        elif motion_right:
            self.SPEED = min(Velocity, self.SPEED + 1)
            self.move(self.SPEED, 0, self.border_sprites)
            # В разработке
            # print(c)
            # if not c:
            #     self.image = load_image(f"hero_walk_animated{self.idle_animation}.png")
            #     self.walk_animation %= 4
            #     self.walk_animation += 1
            #     self.flip()
            if f == "left":
                f = "right"
                self.flip()
        else:
            # В разработке
            # if not c:
            #     self.image = load_image(f"hero_idle_animated{self.idle_animation}.png")
            #     self.idle_animation %= 4
            #     self.idle_animation += 1
            #     self.mask = pygame.mask.from_surface(self.image)
            # if f == "left":
            #     self.flip()
            self.SPEED = max(self.SPEED - 1, 0)

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def check_collision(self, x, y, border):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, border)
        self.rect.move_ip([-x, -y])
        return collide

    def move(self, x, y, border):
        dx = x
        dy = y

        while self.check_collision(0, dy, border):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, border):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])
