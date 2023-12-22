import pygame


class Border(pygame.sprite.Sprite):
    def __init__(self, border_group, all_sprites, tile_images, pos_x, pos_y):
        super().__init__(border_group, all_sprites)
        self.image = tile_images["grass"]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
