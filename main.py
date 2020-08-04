import pygame as pg
import sys
from os import path
from random import randrange
from settings import *
from sprites import *

def pipe_combo(game, x, h):
    y1 = PIPE_SPRITE_HEIGHT - h - GROUND_HEIGHT + HEIGHT
    y2 = HEIGHT - (GROUND_HEIGHT + h + PIPE_V_GAP)
    Pipe(game, x, y1)
    Pipe(game, x, y2, v_flip=True)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.font_name = pg.font.match_font('arial')
        self.last_pipe_spawn = 0
        self.last_screen_change = 0
        self.stopped = False
        self.startscreen = True
        self.goscreen = False
        self.hasdelayed = False

    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, 'img')
        self.pipe_image = pg.image.load(path.join(self.img_dir, 'pipe.png'))\
        .convert_alpha()
        self.bird_images = []
        for i in range(1, 5):
            image = pg.image.load(path.join(self.img_dir,
            f'bird{i}.png')).convert_alpha()
            image = pg.transform.scale(image, (54, 36))
            self.bird_images.append(image)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.pipes = pg.sprite.Group()
        self.player = Player(self, WIDTH / 2 - 50, HEIGHT / 2)
        self.ground = Ground(self)
        self.score = 0

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        # player hits ground
        hits = pg.sprite.collide_rect(self.player, self.ground)
        if hits:
            self.stopped = True
            self.goscreen = True
            self.player.vel.y = 0
            self.player.rect.bottom = self.ground.rect.top
        # player hits pipe
        if not self.goscreen:
            hits = pg.sprite.spritecollide(self.player, self.pipes, False)
            if hits:
                self.goscreen = True
                self.player.vel.y = 10
        # spawning pipes
        t = (PIPE_H_GAP + PIPE_WIDTH) / PIPE_SPEED
        if pg.time.get_ticks() - self.last_pipe_spawn > t * 1000 \
        and not self.stopped and not self.startscreen and not self.goscreen:
            self.last_pipe_spawn = pg.time.get_ticks()
            pipe_combo(self, 1000, randrange(80, HEIGHT - GROUND_HEIGHT - PIPE_V_GAP - 80))

    def draw(self):
        if SHOW_FPS:
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) # shows the fps of the game
        self.screen.fill(SKYBLUE)
        self.all_sprites.draw(self.screen)
        # score when playing
        if not self.startscreen and not self.goscreen:
            self.draw_text(str(self.score), 60, WHITE, WIDTH / 2, HEIGHT / 8)
        # game over screen + score
        if self.goscreen:
            self.draw_text("Game Over", 60, WHITE, WIDTH / 2, HEIGHT / 8)
            self.draw_text(f"Score: {self.score}", 30, WHITE, WIDTH / 2, HEIGHT / 8 + 60)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    # Preventing the game from progressing right after player died or starts game so that button spam won't skip the gameoverscreen
                    now = pg.time.get_ticks()
                    if self.startscreen and pg.time.get_ticks() - self.last_screen_change > 500:
                        self.startscreen = False
                        self.last_screen_change = now
                    if self.goscreen and pg.time.get_ticks() - self.last_screen_change > 5000:
                        self.goscreen = False
                        self.stopped = False
                        self.startscreen = True
                        self.last_screen_change = now
                        self.new()
                    # jumping
                    self.player.jump()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

# create the game object
g = Game()
while True:
    g.new()
    g.run()
