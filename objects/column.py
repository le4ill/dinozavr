import pygame.sprite
import assets
import conf
import random
from layer import Layer


# Класс отвечающий за спавн и движение колон
class Column(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.OBSTACLE
        self.gap = 150  # Переменная отвечающая за расстояние между колонными
        self.sprite = assets.get_sprite("pipe-green")
        self.sprite_rect = self.sprite.get_rect()

        self.pipe_bottom = self.sprite
        self.pipe_bottom_rect = self.pipe_bottom.get_rect(topleft=(0, self.sprite_rect.height + self.gap))

        self.pipe_top = pygame.transform.flip(self.sprite, False, True)
        self.pipe_top_rect = self.pipe_top.get_rect(topleft=(0, 0))

        self.image = pygame.surface.Surface((self.sprite_rect.width, self.sprite_rect.height * 2 + self.gap),
                                            pygame.SRCALPHA)
        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)

        min_y = 230
        max_y = 385  # Координаты x и y среди которых появляются колонны

        self.rect = self.image.get_rect(midleft=(conf.SCREEN_WIDTH, random.uniform(min_y, max_y)))

        self.mask = pygame.mask.from_surface(self.image)

        self.passed = False

        super().__init__(*groups)

    def update(self):
        self.rect.x -= 4  # Скорость движения колонны

        if self.rect.right <= 0:
            self.kill()

    def is_passed(self):
        if self.rect.x < 50 and not self.passed:
            self.passed = True
            return True
        return False
