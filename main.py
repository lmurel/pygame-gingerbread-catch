import pygame as pg
from cookie import Cookie
from config import (
    FPS, BLACK, WIDTH, HEIGHT,
    speed, game_score
)
from random import randint
import time

pg.init()
pg.time.set_timer(pg.USEREVENT, 2000)


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Gingerbread Catch')
pg.display.set_icon(pg.image.load('cookie_icon.png'))
wall = pg.image.load('Magic_Forest.png')

font = pg.font.SysFont('Comic Sans MS', 28)

font_missed = pg.font.SysFont('Comic Sans MS', 28)


ginger = pg.image.load('gingerbread_icon-.png').convert_alpha()
ginger_rect = ginger.get_rect(centerx=WIDTH//2, bottom=HEIGHT-7)

cookie_collection = ({'path': 'cookie_down.png', 'score': 50},
                     {'path': 'lollipop.png', 'score': 100},
                     {'path': 'cotton_candy.png', 'score': 200})

cookies_surf = [pg.image.load(collection['path']).convert_alpha() for collection in cookie_collection]

def update_cookie(group):
    index = randint(0, len(cookies_surf)-1)
    x_cookie = randint(20, WIDTH-20)
    speed_cookie = randint(2, 3)

    return Cookie(x_cookie, speed_cookie, cookies_surf[index], cookie_collection[index]['score'], group)


def collide_cookies():
    global game_score, missed_cookies
    for cookie in cookies:
        if ginger_rect.collidepoint(cookie.rect.center):
            game_score += cookie.score
            cookie.kill()
        elif cookie.rect.y > HEIGHT - 30:
            missed_cookies += 1
            cookie.kill()
            print(missed_cookies)

cookies = pg.sprite.Group()

update_cookie(cookies)

missed_cookies = 0

clock = pg.time.Clock()
playing = True
while playing:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
        elif event.type == pg.USEREVENT:
            update_cookie(cookies)

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        ginger_rect.x -= speed
        if ginger_rect.x < 0:
            ginger_rect.x = 0
    elif keys[pg.K_RIGHT]:
        ginger_rect.x += speed
        if ginger_rect.x > WIDTH-ginger_rect.width:
            ginger_rect.x = WIDTH-ginger_rect.width


    collide_cookies()

    screen.fill(BLACK)
    screen.blit(wall, (0, 0))

    screen_text = font.render(str(game_score), 1, (153, 153, 255))
    screen.blit(screen_text, (40, 25))

    screen_missed = font.render(str(missed_cookies), 1, (255, 102, 102))
    screen.blit(screen_missed, (40, 60))

    cookies.draw(screen)
    screen.blit(ginger, ginger_rect)

    if missed_cookies >= 6:
        time.sleep(1)
        quit()

    clock.tick(FPS)

    cookies.update(HEIGHT)

    pg.display.update()