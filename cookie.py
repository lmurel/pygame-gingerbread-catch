import pygame as pg


class Cookie(pg.sprite.Sprite):

    def __init__(self, x_cookie, speed_cookie, surf, score, group):
        pg.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x_cookie, 0))
        self.speed = speed_cookie
        self.score = score
        self.add(group)

    def update(self, *args):  # обновление спрайта / изменение координат спрайта

        if self.rect.y < args[0] - 20: # высота кл обл окна, проверяет, долетел ли шарик
            self.rect.y += self.speed
        else:
            self.kill()
