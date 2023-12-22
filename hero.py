import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, G, player_group, all_sprites, border_sprites, player_image, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.border_sprites = border_sprites
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.G = G
        self.vy = self.G

    def update(self, *args):
        c = 1
        for border in self.border_sprites:
            if pygame.sprite.collide_mask(self, border):
                c = 0
                break
        if c:
            self.rect = self.rect.move(0, self.vy)
