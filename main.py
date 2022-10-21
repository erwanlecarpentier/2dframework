import random
import os
import pygame as pg


# Constants
SCREEN_RECT = pg.Rect(0, 0, 640, 480)
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

def pygame_init():
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None


def load_image(file):
    file = os.path.join(MAIN_DIR, "assets", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


class Player(pg.sprite.Sprite):
    '''speed = 10
    bounce = 24
    images = []'''

    def __init__(self, images, containers, speed=10, bounce=24):
        self.containers = containers
        pg.sprite.Sprite.__init__(self, self.containers)
        self.images = images
        self.speed = speed
        self.bounce = bounce
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREEN_RECT.midbottom)
        self.origin_top = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREEN_RECT)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origin_top - (self.rect.left // self.bounce % 2)


def main():
    # Initialize pygame
    pygame_init()

    # Set the display mode
    full_screen = False
    window_style = 0
    best_depth = pg.display.mode_ok(SCREEN_RECT.size, window_style, 32)
    screen = pg.display.set_mode(SCREEN_RECT.size, window_style, best_depth)

    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    img = load_image("pixel_line_platformer/Tiles/tile_0045.png")
    player_images = [img, pg.transform.flip(img, True, False)]

    # create the background, tile the bgd image
    background_tile = load_image("winter_landscape.jpg")
    background = pg.Surface(SCREEN_RECT.size)
    for x in range(0, SCREEN_RECT.width, background_tile.get_width()):
        background.blit(background_tile, (x, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Initialize Game Groups
    all = pg.sprite.RenderUpdates()

    # Set starting sprites
    player = Player(player_images, all)

    # Run main loop
    while True:
        # clear/erase the last drawn sprites
        all.clear(screen, background)

        # update all the sprites
        all.update()


if __name__ == "__main__":
    main()
    pg.quit()
