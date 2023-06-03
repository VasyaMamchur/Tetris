from settings import *
from tetris import Tetris, Text
from figurines import Block, Tetromino
import sys
import pathlib


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.background_image = pg.image.load('applications/background/bg.jpg').convert()
        self.music = pg.mixer.Sound('applications/music/tetris.mp3')
        self.music.set_volume(0.5)
        self.music_playing = False
        pg.mixer.init()

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def toggle_music(self):
        if self.music_playing:
            self.music.stop()
        else:
            self.music.play(loops=-1)
        self.music_playing = not self.music_playing

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    self.toggle_music()
                elif event.key == pg.K_r:
                    self.restart_game()
                elif event.key == pg.K_p:
                    self.toggle_pause()
                else:
                    self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def toggle_pause(self):
        self.tetris.paused = not self.tetris.paused

    def restart_game(self):
        self.tetris = Tetris(self)

    def run(self):
        self.music.play(loops=-1)
        while True:
            self.check_events()
            if not self.tetris.paused:
                self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
