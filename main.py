import pygame
import assets
import conf
import sqlite3
import datetime as dt

from objects.Pause import Pause
from objects.background import Background
from objects.column import Column
from objects.plane import Plane
from objects.game_start import GameStart
from objects.game_over import GameOver
from objects.score import Score
from objects.Trophies import Trophies

import sys
import webbrowser

pygame.init()
con = sqlite3.connect("assets/dataBase/score.sqlite")
cur = con.cursor()

pygame.display.set_caption('Ай цвайн фифти фифти Я песок и Нефертити')
screen = pygame.display.set_mode((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameover = False
gamestarted = False
start = True
bom = True


def terminate():
    pygame.quit()
    sys.exit()


assets.load_sprites()
assets.load_audios()
boom = assets.get_sprite("bum")
boom = pygame.transform.scale(boom, (150, 70))
gg = assets.get_sprite('rest')
gg = pygame.transform.scale(gg, (200, 20))
sprites = pygame.sprite.LayeredUpdates()
assets.play_audio('Смешарики - От винта!', count=-1, volume=0.05)
pause_menu = assets.get_sprite('pause_menu')
pause_menu_ch = False
database_writing = True


# Отображение игрока, начального экрана, количества набранных очков, рекорд и кнопки паузы/-----------------------------
def create_sprites():
    Background(0, sprites)
    Background(1, sprites)

    return Plane(sprites), GameStart(sprites), Score(sprites), Trophies(sprites), Pause(sprites)


plane, game_start, score, trophy, pause = create_sprites()


# ---------------------------------------------------------------------------------------------------------------------\

# Функция отвечающая за меню паузы/-------------------------------------------------------------------------------------
def paused():
    global gameover, gamestarted, start, pause_menu_ch
    gamestarted = False
    gameover = True
    pygame.time.set_timer(column_create_event, 0)
    start = True
    pause_menu_ch = True


# ---------------------------------------------------------------------------------------------------------------------\


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Проверка на спавн колон/--------------------------------------------------------------------------------------
        if event.type == column_create_event:
            Column(sprites)
        # -------------------------------------------------------------------------------------------------------------\
        if event.type == pygame.KEYDOWN:
            # Запуск игры при нажатии на пробел/------------------------------------------------------------------------
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                if start:
                    pygame.time.set_timer(column_create_event, 1000)
                gamestarted = True
                pause_menu_ch = False
                start = False
                game_start.kill()
            # ---------------------------------------------------------------------------------------------------------\

            # Рестарт при смерти/---------------------------------------------------------------------------------------
            if event.key == pygame.K_r and gameover and not pause_menu_ch:
                bom = True
                gameover = False
                gamestarted = False
                database_writing = True
                pygame.time.set_timer(column_create_event, 0)
                start = True
                sprites.empty()
                plane, game_start, score, trophy, pause = create_sprites()
                Pause(sprites)
            # ---------------------------------------------------------------------------------------------------------\

            # Вызов меню паузы/-----------------------------------------------------------------------------------------
            if event.key == pygame.K_ESCAPE and not start and gamestarted:
                paused()
            # ---------------------------------------------------------------------------------------------------------\
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                # Проверка на нажатие кнопки паузы/---------------------------------------------------------------------
                if 745 <= x <= 795 and 8 <= y <= 55 and gamestarted:
                    paused()
                # ------------------------------------------------------------------------------------------------------
                if start:
                    pygame.time.set_timer(column_create_event, 1000)
                if pause_menu_ch:
                    # Проверка на нажатие кнопки возобновления игры/----------------------------------------------------
                    if 250 <= x <= 505 and 210 <= y <= 265:
                        if start:
                            pygame.time.set_timer(column_create_event, 1000)
                        gamestarted = True
                        gameover = False
                        pause_menu_ch = False
                        start = False
                        game_start.kill()
                    # --------------------------------------------------------------------------------------------------
                    if 250 <= x <= 505 and 355 <= y <= 410:
                        webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                        terminate()
                else:
                    start = False
                    pause_menu_ch = False
                    gamestarted = True
                    game_start.kill()
        # Изменение направления движения самолета/----------------------------------------------------------------------
        if not gameover:
            plane.handle_event(event)
        # -------------------------------------------------------------------------------------------------------------\

    # Отрисовка всех спрайтов/------------------------------------------------------------------------------------------
    screen.fill(0)
    sprites.draw(screen)
    # ------------------------------------------------------------------------------------------------------------------

    # Отрисовка меню паузы/---------------------------------------------------------------------------------------------
    if pause_menu_ch:
        im, rct = Pause().check()
        screen.blit(im, rct)
    # ------------------------------------------------------------------------------------------------------------------

    if gamestarted and not gameover:
        sprites.update()

    # Проверка на пересечение спрайта самолета с препятствиями/---------------------------------------------------------
    if plane.check_collision(sprites):
        gameover = True
        # Получение очков и даты на момент конца игры, и их запись в бд, если побит рекорд/-----------------------------
        end_points = score.value
        data_score = dt.date.today().strftime("%d.%m.%Y")
        if database_writing:
            record = max([int(*i) for i in cur.execute("""SELECT score from Score""").fetchall()])
            if end_points > record:
                cur.execute(f"""INSERT INTO Score(score,Data) VALUES({end_points},'{data_score}')""").fetchall()
                con.commit()
            database_writing = False
        gamestarted = False
        # --------------------------------------------------------------------------------------------------------------

        # Отрисовка экрана конца игры и взрыва самолета/----------------------------------------------------------------
        GameOver(sprites)
        x, y = plane.get_coord()
        screen.blit(boom, (x - 20, y - 10))
        screen.blit(gg, (300, 320))
        # --------------------------------------------------------------------------------------------------------------
        if bom:
            assets.play_audio('Звук взрыва', volume=0.2)
            bom = False
        # --------------------------------------------------------------------------------------------------------------

    # Добавление очков/-------------------------------------------------------------------------------------------------
    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
    # ------------------------------------------------------------------------------------------------------------------
    pygame.display.flip()
    clock.tick(conf.FPS)

con.close()
terminate()
