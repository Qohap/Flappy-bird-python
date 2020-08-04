import pygame as pg
from settings import *
from random import randrange
import pytweening as tween
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        self._layer = PLAYER_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bird_images[0]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.acc = 0
        self.rot = 0
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
        self.last_update = 0
        self.current_frame = 0
        self.last_rot = 0

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        if not self.game.goscreen:
            self.animate()
        if not self.game.stopped and not self.game.startscreen:
            # apply friction
            self.acc.y += self.vel.y * -PLAYER_FRICTION
            # equation of motion
            self.vel += self.acc
            self.pos.y += self.vel.y + 0.5 * (self.acc.y ** 2)
            self.rect.center = self.pos
        if self.game.startscreen:
            offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
            # print(f"offset: {offset}")
            self.rect.centery = self.pos.y + offset * self.dir
            # print(f"centery: {self.rect.centery}")
            self.step += BOB_SPEED
            if self.step > BOB_RANGE:
                self.step = 0
                self.dir *= -1
        # limiting players position max height
        if (self.pos.y - (self.rect.height / 2) + 100) <= 0:
            self.pos.y = 0 + self.rect.height - 100

    def jump(self):
        if not self.game.stopped and not self.game.startscreen:
            self.vel.y = -PLAYER_JUMP

    def animate(self):
        now = pg.time.get_ticks()
        # updating frames
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % \
            len(self.game.bird_images)
            center = self.rect.center
            self.image = self.game.bird_images[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
        # rotation
        # self.rot = round(7 * (-self.vel.y / 9), 2)
        # self.last_rot = now
        # if self.rot > 180:
        #     self.rot = 180
        # center = self.rect.center
        # self.image = pg.transform.rotate(self.image.copy(), self.rot % 360)
        # self.rect = self.image.get_rect()
        # self.rect.center = center


class Pipe(pg.sprite.Sprite):
    def __init__(self, game, x, y, v_flip=False):
        self.groups = game.all_sprites, game.pipes
        self._layer = PIPE_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.pipe_image
        self.v_flip = v_flip
        if v_flip:
            self.image = pg.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.midbottom = self.pos
        self.count_score = False

    def update(self):
        if not self.game.startscreen and not self.game.goscreen:
            self.pos.x += -PIPE_SPEED * self.game.dt
            self.rect.midbottom = self.pos
        if self.rect.centerx < self.game.player.pos.x and not self.count_score \
        and not self.v_flip:
            self.game.score += 1
            self.count_score = True
        if self.rect.right < 0:
            self.kill()

class Ground(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        self._layer = GROUND_LAYER
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((WIDTH, GROUND_HEIGHT))
        self.image.fill(DARKGREY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, HEIGHT - GROUND_HEIGHT)

    def update(self):
        pass
