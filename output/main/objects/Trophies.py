import pygame.sprite
import assets
import conf
import sqlite3
from layer import Layer

con = sqlite3.connect("assets/dataBase/score.sqlite")
cur = con.cursor()


# Класс отвечающий за отображение трофеев
class Trophies(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.__create()
        super().__init__(*groups)

    def __create(self):
        # Получение максимального большого набранного ранее результата
        record = str(max([int(*i) for i in cur.execute("""SELECT score from Score""").fetchall()]))
        self.width = 0
        self.png_record = []
        # Преобразование числа в спрайты/-------------------------------------------------------------------------------
        for i in record:
            img = assets.get_sprite(i)
            self.png_record.append(img)
            self.width += img.get_width()
        # --------------------------------------------------------------------------------------------------------------

        # Добавление в список спрайта кубка и прочие страшные махинации/------------------------------------------------
        trophies = assets.get_sprite('trophy1')
        self.png_record.append(trophies)
        self.width += trophies.get_width()
        self.height = self.png_record[-1].get_height()
        self.image = pygame.surface.Surface((self.width + 30, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(conf.SCREEN_WIDTH - self.width + 40, 85))
        # --------------------------------------------------------------------------------------------------------------

        # Отображение полученных спрайтов на экран/---------------------------------------------------------------------
        for n, img in enumerate(self.png_record):
            if n == len(self.png_record) - 1:
                self.image.blit(img, (n * img.get_width() - 29, 0))
            else:
                self.image.blit(img, (n * img.get_width(), 15))
        # --------------------------------------------------------------------------------------------------------------

    def update(self):
        self.__create()
