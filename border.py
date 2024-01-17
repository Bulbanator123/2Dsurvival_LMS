import pygame


class Border(pygame.sprite.Sprite):
    def __init__(self, border_image, tile_group, all_sprites, pos_x, pos_y):
        super().__init__(tile_group, all_sprites)
        self.image = border_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
