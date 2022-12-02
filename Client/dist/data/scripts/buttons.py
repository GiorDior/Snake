import pygame

class Button:
    def __init__(self, root, image: pygame.Surface, position_x: float, position_y: float, command = None):
        self.root = root
        self.command = command
        self.image = image
        self.show_error = False
        self.width, self.height = self.image.get_width(), self.image.get_height()

        self.position = (position_x, position_y)
        self.reset_position()
        
    def mouse_is_hovering(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def reset_position(self):
        self.x = self.position[0] - self.width/2
        self.y = self.position[1] - self.height/2

    def update(self):
        alpha = 100    
        if self.mouse_is_hovering():
            surface = pygame.Surface((self.width, self.height))
            surface.fill("black")
            surface.set_alpha(alpha)
            self.root.get_surface().blit(surface, (self.x, self.y)) 
        
        if self.show_error:
            surface = pygame.Surface((self.width, self.height))
            surface.fill("red")
            surface.set_alpha(125)
            self.root.get_surface().blit(surface, (self.x, self.y)) 

        


    def render(self):
            self.root.get_surface().blit(self.image, (self.x, self.y))

    class Select:
        def __init__(self, root, images: list[pygame.Surface], position_x: float, position_y: float, command = None):
            self.root = root
            self.command = command
            self.images = images
            self.current_image = images[0]


            self.width, self.height = self.current_image.get_width(), self.current_image.get_height()
            self.original_width, self.original_height = self.width, self.height

            self.position = (position_x, position_y)
            self.reset_position()

            self.selected = False

        def reset_position(self):
            self.x = self.position[0] - self.width/2
            self.y = self.position[1] - self.height/2

        def mouse_is_hovering(self):
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if rect.collidepoint(pygame.mouse.get_pos()):
                return True
            return False

        def update(self):
            if self.mouse_is_hovering():
                if self.selected:
                    image = pygame.transform.scale(self.images[1], (self.original_width * 1.1, self.original_height * 1.1))
                else:
                    image = pygame.transform.scale(self.images[0], (self.original_width * 1.1, self.original_height * 1.1))
                self.current_image = image
                self.width, self.height = self.current_image.get_width(), self.current_image.get_height()
                self.reset_position()
            else:
                if self.selected:
                    image = self.images[1]
                else:
                    image = self.images[0]
                self.current_image = image
                self.current_image = image
                self.width, self.height = self.current_image.get_width(), self.current_image.get_height()
                self.reset_position()

        def render(self):
            self.root.get_surface().blit(self.current_image, (self.x, self.y))