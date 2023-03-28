import pygame as pg
from cookie import Cookie
from config import (
    FPS, BLACK, WIDTH, HEIGHT
)
from random import randint
import time


def update_cookie(group, max_speed):
    index = randint(0, len(cookies_surf)-1)
    x_cookie = randint(20, WIDTH-20)
    speed_cookie = randint(max_speed-1, max_speed)

    return Cookie(x_cookie, speed_cookie, cookies_surf[index], cookie_collection[index]['score'], group)


def play():
    wall = pg.image.load('Magic_Forest.png')
    font = pg.font.SysFont('Comic Sans MS', 28)
    font_missed = pg.font.SysFont('Comic Sans MS', 28)

    ginger = pg.image.load('gingerbread_icon-.png').convert_alpha()
    ginger_rect = ginger.get_rect(centerx=WIDTH//2, bottom=HEIGHT-7)

    max_speed = 3
    cookies = pg.sprite.Group()

    clock = pg.time.Clock()

    game_score, missed_cookies = 0, 0
    speed = 5
    playing = True

    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
            elif event.type == pg.USEREVENT:
                update_cookie(cookies, max_speed)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            ginger_rect.x -= speed
            if ginger_rect.x < 0:
                ginger_rect.x = 0
        elif keys[pg.K_RIGHT]:
            ginger_rect.x += speed
            if ginger_rect.x > WIDTH-ginger_rect.width:
                ginger_rect.x = WIDTH-ginger_rect.width

    #    collide_cookies()
        for cookie in cookies:
            if ginger_rect.collidepoint(cookie.rect.center):
                game_score += cookie.score
                cookie.kill()
                # Увеличивать скорость падения печенек после набора каждых 1000 очков
                # (уровень сложности)
                if game_score % 1000 == 0:
                    max_speed += 1
            elif cookie.rect.y > HEIGHT - 30:
                missed_cookies += 1
                cookie.kill()

        screen.fill(BLACK)
        screen.blit(wall, (0, 0))

        screen_text = font.render(str(game_score), 1, (153, 153, 255))
        screen.blit(screen_text, (40, 25))

        screen_missed = font.render(str(missed_cookies), 1, (255, 102, 102))
        screen.blit(screen_missed, (40, 60))

        cookies.draw(screen)
        screen.blit(ginger, ginger_rect)

        if missed_cookies > 5:
            time.sleep(1)
            playing = False


        clock.tick(FPS)

        cookies.update(HEIGHT)

        pg.display.update()

    return game_score


pg.init()
pg.time.set_timer(pg.USEREVENT, 2000)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Gingerbread Catch')
pg.display.set_icon(pg.image.load('cookie_icon.png'))

cookie_collection = ({'path': 'cookie_down.png', 'score': 50},
                     {'path': 'lollipop.png', 'score': 100},
                     {'path': 'cotton_candy.png', 'score': 200})

cookies_surf = [
    pg.image.load(collection['path']).convert_alpha()
    for collection in cookie_collection
]

font_result = pg.font.SysFont('Comic Sans MS', 52)
while True:
    score = play()
    screen.fill(BLACK)
    screen_text = font_result.render(f"Score: {score}", 1, (153, 153, 255))
    screen.blit(screen_text, (40, 25))
    pg.display.update()

    wait = True
    while wait:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                wait = False
