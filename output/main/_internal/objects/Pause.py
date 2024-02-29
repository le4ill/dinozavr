import pygame.sprite
import assets
import conf
from layer import Layer


# Класс отвечающий за кнопку паузы и вызова меню паузы
class Pause(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.pause_menu = assets.get_sprite('pause_menu')
        self._layer = Layer.UI
        self.image = assets.get_sprite('pause')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(conf.SCREEN_WIDTH - 60, 0))
        self.rect_p = self.image.get_rect(topleft=(conf.SCREEN_WIDTH / 2 - 150, conf.SCREEN_HEIGHT / 2 - 90))
        super().__init__(*groups)

    def check(self):
        # Возвращает спрайт меню паузы и его координаты
        return self.pause_menu, self.rect_p
