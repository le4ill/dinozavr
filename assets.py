import os
import pygame

sprites = {}
audios = {}


# Загрузка всех спрайтов при запуске приложения/------------------------------------------------------------------------
def load_sprites():
    path = os.path.join("assets", "sprites")
    for file in os.listdir(path):
        sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))


# ----------------------------------------------------------------------------------------------------------------------

# Функция, возвращающая спрайт по его названию/-------------------------------------------------------------------------
def get_sprite(name):
    return sprites[name]


# ----------------------------------------------------------------------------------------------------------------------

# Загрузка всех аудифайлов при запуске приложения/----------------------------------------------------------------------
def load_audios():
    path = os.path.join("assets", "audios")
    for file in os.listdir(path):
        audios[''.join(file[::-1].split('.', 1)[::-1][:-1])[::-1]] = pygame.mixer.Sound(os.path.join(path, file))


# ----------------------------------------------------------------------------------------------------------------------

# Функция возвращающая аудифайл по его имени/---------------------------------------------------------------------------
def play_audio(name, count=0, volume=1):
    audios[name].set_volume(volume)
    audios[name].play(count)
# ----------------------------------------------------------------------------------------------------------------------
