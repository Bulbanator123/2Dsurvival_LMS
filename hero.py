import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, G, player_group, all_sprites, border_sprites, player_image, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.border_sprites = border_sprites
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.G = G
        self.vy = self.G

    def update(self, *args):
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, self.border_sprites):
            self.vy = 0
        else:
            self.vy = self.G
