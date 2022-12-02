import pygame

# class of buttons which execute a command
class Button:
    def __init__(self, root, image: pygame.Surface, position_x: float, position_y: float, command = None):
        # root window
        self.root = root
        # command to execute if given
        self.command = command
        # button image to render
        self.image = image
        # render a red rectangle if self.show_error == True
        self.show_error = False
        # button size
        self.width, self.height = self.image.get_width(), self.image.get_height()

        # button position
        self.position = (position_x, position_y)
        # update position regarding its size
        self.reset_position()
    
    # checking if mouse is hovering the button
    def mouse_is_hovering(self):
        # button rectangle
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    # update position regarding its size
    def reset_position(self):
        self.x = self.position[0] - self.width/2
        self.y = self.position[1] - self.height/2

    # update hovering animation and render it
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

    # render button image
    def render(self):
            self.root.get_surface().blit(self.image, (self.x, self.y))

    # different class of buttons which can be selected
    class Select:
        def __init__(self, root, images: list[pygame.Surface], position_x: float, position_y: float, command = None):
            # root window
            self.root = root
            # command to execute
            self.command = command
            # button images for the different states
            self.images = images
            self.current_image = images[0]

            # button size
            self.width, self.height = self.current_image.get_width(), self.current_image.get_height()
            self.original_width, self.original_height = self.width, self.height

            # button position
            self.position = (position_x, position_y)
            self.reset_position()

            # button is selected
            self.selected = False

        def reset_position(self):
            self.x = self.position[0] - self.width/2
            self.y = self.position[1] - self.height/2

        # checking if mouse howervs
        def mouse_is_hovering(self):
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            if rect.collidepoint(pygame.mouse.get_pos()):
                return True
            return False
        
        # hovering animation, draw images[1] if the button is selected
        def update(self):
            if self.mouse_is_hovering():
                # on hoever, increase button size by 10 percent
                if self.selected:
                    image = pygame.transform.scale(self.images[1], (self.original_width * 1.1, self.original_height * 1.1))
                else:
                    image = pygame.transform.scale(self.images[0], (self.original_width * 1.1, self.original_height * 1.1))
                self.current_image = image
                self.width, self.height = self.current_image.get_width(), self.current_image.get_height()
                self.reset_position()
            else:
                # put button to normal state
                if self.selected:
                    image = self.images[1]
                else:
                    image = self.images[0]
                self.current_image = image
                self.current_image = image
                self.width, self.height = self.current_image.get_width(), self.current_image.get_height()
                self.reset_position()

        # render button
        def render(self):
            self.root.get_surface().blit(self.current_image, (self.x, self.y))