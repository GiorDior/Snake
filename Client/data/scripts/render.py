import pygame

class Render:
    # rendering text with a given
    #   text, size, font, color and position
    def text(root_surface: pygame.Surface, text: str, font_path: str, font_size: int, color, position: tuple):
        font = pygame.font.Font(font_path, font_size)
        text_width, text_height = font.size(text)
        font_text = font.render(str(text), False, color)
        root_surface.blit(font_text, (position[0] - text_width/2, position[1] - text_height/2))