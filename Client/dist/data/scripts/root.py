import pygame

class Root:
    # creating the root window
    def __init__(self, size: tuple, caption: str) -> None:
        # window size
        self.size = size
        # caption
        self.caption = caption
        # clock which keeps track of the fps
        self.clock = pygame.time.Clock()
        # rendering surface
        self.surface = pygame.display.set_mode(self.size)
        # set icon and caption
        pygame.display.set_icon(pygame.image.load("data/images/menu/image_snake_transparent.png").convert_alpha())
        pygame.display.set_caption(self.caption + "-host " + str(round(self.clock.get_fps(), 1)))

    # get rendering surface
    def get_surface(self):
        return self.surface
    
    # update screen
    def update(self, fps: int):
        pygame.display.set_caption(self.caption + "-host " + str(round(self.clock.get_fps(), 1)))
        self.delta_time = self.clock.tick(fps)
        pygame.display.update()