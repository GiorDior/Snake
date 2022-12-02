import pygame, time, sys, socket
from data.scripts.buttons import Button

class Menu:

    def __init__(self) -> None:
        self.stage = 0
        # game mode selected by the user
        self.selected_mode = "classic"

    # change the current menu section
    def change_stage(self, state: int):
        self.stage = state
        self.logo.position = 1200/2 - self.logo.width/2, 50

    # run menu
    def run(self, root):
        # window, root
        self.root = root

        # all images used for the buttons
        image_offline_button = pygame.image.load("data/images/buttons/image_offline_button_1.png").convert_alpha()

        image_online_button = pygame.image.load("data/images/buttons/image_online_button_1.png").convert_alpha()
        
        image_start_button = pygame.image.load("data/images/buttons/image_start_button_1.png").convert_alpha()
        
        images_classic_mode = [
            pygame.image.load("data/images/buttons/image_classic_mode_button_1.png").convert_alpha(),
            pygame.image.load("data/images/buttons/image_classic_mode_button_2.png").convert_alpha()
        ]

        images_advanced_mode = [
            pygame.image.load("data/images/buttons/image_advanced_mode_button_1.png").convert_alpha(),
            pygame.image.load("data/images/buttons/image_advanced_mode_button_2.png").convert_alpha()
        ]

        images_versus_mode = [
            pygame.image.load("data/images/buttons/image_versus_mode_button_1.png").convert_alpha(),
            pygame.image.load("data/images/buttons/image_versus_mode_button_2.png").convert_alpha()
        ]

        # buttons for every section of the menu saved in a list 
        buttons_stage_one = [
            Button(self.root, image_offline_button, 1200/2, 350),
            Button(self.root, image_online_button, 1200/2, 500)
            ]

        buttons_stage_two = [
            Button(self.root, image_start_button, 1050, 650),
            Button.Select(self.root, images_classic_mode, 400, 700/2),
            Button.Select(self.root, images_advanced_mode, 800, 700/2)
            ]
        buttons_stage_two[1].selected = True

        buttons_stage_three = [
            Button(self.root, image_start_button, 1050, 650),
            Button.Select(self.root, images_classic_mode, 400, 700/2),
            Button.Select(self.root, images_versus_mode, 800, 700/2)
            ]
        buttons_stage_three[1].selected = True

        # text input in online menu
        input_stage_three = [Input((325, 50), (325, 50), "host "),
                            Input((825, 50), (125, 50), "port ")
                            ]
        
        # buttons_stage_three = [
        #     Button(root, images_offline_button, 1200/2, 350),
        #     Button(root, images_online_button, 1200/2, 500)
        #     ]

        # stages:
        #   0 : offline or online
        #   1 : offline : 2 game modes
        #   2 : online  : 2 game modes

        # logo at the begining which moves
        self.logo = Menu.Logo(self.root)

        # mainloop
        while True:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    sys.exit()
                
                # left click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # user clicks offline or online
                    if self.stage == 0:
                        for button in buttons_stage_one:
                            if button.mouse_is_hovering():
                                # user presses offline button
                                if button == buttons_stage_one[0]:
                                    self.change_stage(1)
                                    self.selected_mode = "classic"
                                # user presses online button
                                else:
                                    self.change_stage(2)
                                    self.selected_mode = "onclassic"
                    
                    # user is in the offline menu
                    elif self.stage == 1:
                        for index, button in enumerate(buttons_stage_two):
                            # user presses a button
                            if button.mouse_is_hovering():
                                # user presses start button
                                if index == 0:
                                    # run return the selected mode
                                    return self.selected_mode
                                else:
                                    # user doesn't press the start button, set the mode the user chose
                                    modes = [[1, "classic"], [2, "advanced"]]
                                    for mode in modes:
                                        if mode[0] == index:
                                            self.selected_mode = mode[1]
                                    # deselect every button
                                    for j, _button in enumerate(buttons_stage_two):
                                        if j > 0:
                                            _button.selected = False
                                    # select the pressed button
                                    button.selected = True
                    
                    # user selects online menu
                    elif self.stage == 2:
                        for index, button in enumerate(buttons_stage_three):
                            if button.mouse_is_hovering():
                                # user presses start button
                                if index == 0:
                                    # check the user host and port input and try to establish a connection
                                    if self.connection_established(input_stage_three):
                                        # success
                                        return self.selected_mode
                                    else:
                                        # error
                                        buttons_stage_three[0].show_error = True
                                else:
                                    # player selects a game mode
                                    modes = [[1, "onclassic"], [2, "onversus"]]
                                    # get selected mode
                                    for mode in modes:
                                        if mode[0] == index:
                                            self.selected_mode = mode[1]
                                    # deselect all buttons
                                    for j, _button in enumerate(buttons_stage_three):
                                        if j > 0:
                                            _button.selected = False
                                    # select the clicked button
                                    button.selected = True
                        
                        # check if user pressed an input box
                        for input in input_stage_three:
                            if input.box.collidepoint(event.pos):
                                # toggle the active variable
                                input.active = not input.active
                                buttons_stage_three[0].show_error = False
                            else:
                                # active = false if user clicks else where
                                input.active = False
                            # set color depending on the input status
                            input.color = input.color_active if input.active else input.color_inactive
                
                # user clicks a key on the keybord
                if event.type == pygame.KEYDOWN:
                    # user clicks ESCAPE
                    if event.key == pygame.K_ESCAPE:
                        # return to the main menu
                        if self.stage in [1, 2]:
                            self.change_stage(0)
                    
                    # user types in the input box
                    if self.stage == 2:
                        for input in input_stage_three:
                            if input.active:
                                # user deletes symbols
                                if event.key == pygame.K_BACKSPACE:
                                    input.text = input.text[:-1]
                                # user writes into the host input box
                                elif input.label == "host " and len(input.text) < 15:
                                    input.text += event.unicode
                                # user writes into the port input box
                                elif input.label == "port " and len(input.text) < 5:
                                    input.text += event.unicode


            # render background:
            self.render_background(self.root)

            # first part of the menu
            if self.stage == 0:
                mouse_hovers = False
                # animate logo
                self.logo.update()
                # update and render buttons
                for button in buttons_stage_one:
                    button.update()
                    button.render()
                    # user hovers over a button
                    if button.mouse_is_hovering():
                        mouse_hovers = True
                # change cursor
                if mouse_hovers:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            # offline section
            elif self.stage == 1:
                mouse_hovers = False
                # render and update buttons
                for index, button in enumerate(buttons_stage_two):
                    button.update()
                    button.render()
                    if button.mouse_is_hovering():
                        mouse_hovers = True

                # change cursor
                if mouse_hovers:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # online section
            elif self.stage == 2:
                mouse_hovers = False
                # update and render buttons
                for index, button in enumerate(buttons_stage_three):
                    button.update()
                    button.render()
                    # check if mouse hovers over a button
                    if button.mouse_is_hovering():
                        mouse_hovers = True

                # render input box
                for input in input_stage_three:
                    input.render(self.root.get_surface())

                # change mouse cursor
                if mouse_hovers:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            # update root
            self.root.update(60)

    # function serving for the scene transition
    # has the exact same render steps as in run()
    def render_first_stage(self):
        # button images
        image_offline_button = pygame.image.load("data/images/buttons/image_offline_button_1.png").convert_alpha()

        image_online_button = pygame.image.load("data/images/buttons/image_online_button_1.png").convert_alpha()
        
        # buttons
        buttons_stage_one = [
            Button(self.root, image_offline_button, 1200/2, 350),
            Button(self.root, image_online_button, 1200/2, 500)
            ]

        # render background
        self.render_background(self.root)
        # animate logo
        self.logo.render()
        # render buttons
        for button in buttons_stage_one:
            button.render()

    # establish a connection with the server
    def connection_established(self, input_stage_three):
        try:
            host = str(input_stage_three[0].text)
            port = int(input_stage_three[1].text)
            
            # connect to the server
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((host, port))

            self.server.settimeout(5)
            self.server.send(bytes(self.selected_mode, "utf-8"))
            data = self.server.recv(4096).decode()
            if data != self.selected_mode:
                self.server.close()
                return False
            print("Connected to", host, port)
            return True
        except:
            return False

    # function for rendering background
    def render_background(self, root, first_color: str = "#91f086", second_color: str = "#48bf53"):
        # 2 different green colors
        first_color = pygame.Color(first_color)
        second_color = pygame.Color(second_color)
        # size of one square in pixels
        square_size = 50
        # render background:
        root.get_surface().fill(first_color)

        for x in range(24):
            for y in range(14):
                if (y + x) % 2 == 0: 
                    pygame.draw.rect(root.get_surface(), first_color, (x * square_size, y * square_size, square_size, square_size), border_radius=2)
                else:
                    pygame.draw.rect(root.get_surface(), second_color, (x * square_size, y * square_size, square_size, square_size), border_radius=2)

    class Logo:
        def __init__(self, root) -> None:
            self.root = root
            # checking if logo goes up or down
            self.animation_state = 0
            # speed
            self.animation_speed = 1.5
            # animates every 0.03 seconds
            self.animation_delay = 0.03
            self.tick = time.perf_counter()
            
            # image of the logo
            self.image = pygame.image.load("data/images/menu/image_snake_logo.png").convert_alpha()
            self.width, self.height = self.image.get_width(), self.image.get_height()

            # logo position
            self.position = 1200/2 - self.width/2, 50
        
        # change animation direction
        def set_animation_state(self):
            if self.animation_state == 0 and self.position[1] > 100:
                self.animation_state = 1
            elif self.animation_state == 1 and self.position[1] < 50:
                self.animation_state = 0

        # render logo
        def render(self):
            self.root.get_surface().blit(self.image, self.position)
        
        # animate logo
        def update(self):
            self.set_animation_state()
            if time.perf_counter() - self.tick > self.animation_delay:
                self.tick = time.perf_counter()
                if self.animation_state == 0:
                    self.position = self.position[0], self.position[1] + self.animation_speed
                else:
                    self.position = self.position[0], self.position[1] - self.animation_speed
            self.render()

    # "Markimark" screen
    def introducing_image(root):
        tick = time.perf_counter()

        # show screen for 2 seconds
        while time.perf_counter() - tick < 2:
            # user quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # render background
            # 2 different green colors
            first_color = pygame.Color("#91f086")
            second_color = pygame.Color("#48bf53")
            # size of one square in pixels
            square_size = 50
            # render background:
            root.get_surface().fill(first_color)

            for x in range(24):
                for y in range(14):
                    if (y + x) % 2 == 0: 
                        pygame.draw.rect(root.get_surface(), first_color, (x * square_size, y * square_size, square_size, square_size), border_radius=2)
                    else:
                        pygame.draw.rect(root.get_surface(), second_color, (x * square_size, y * square_size, square_size, square_size), border_radius=2)

            # root.get_surface().fill(pygame.Color("#47C162"))

            # render "Markimark" image
            image_path = "data/images/menu/image_intro.png"
            root.get_surface().blit(pygame.image.load(image_path).convert_alpha(), (0, 0))

            root.update(60)
# text input
class Input:
    def __init__(self, position: tuple, size: tuple, label: str) -> None:
        self.position = position
        self.size = size
        self.box = pygame.Rect(position[0], position[1], self.size[0], self.size[1])
        self.color_inactive = (50, 50, 50)
        self.color_active = pygame.Color('black')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        # label
        self.label = label

    def render(self, root_surface):
        pygame.draw.rect(root_surface, self.color, self.box)
        font = pygame.font.Font("data/fonts/PressStart2P.ttf", 20)
        font_text = font.render(str(self.text), False, ("white"))
        font_label = font.render(str(self.label), False, ("white"))

        text_width, text_height = font.size(self.text)
        label_width, label_height = font.size(self.label)


        root_surface.blit(font_text, (self.position[0] + 5, self.position[1] + self.size[1]/2 - text_height/2))
        transparent_surface = pygame.Surface((label_width, self.position[1]))
        transparent_surface.set_alpha(150)
        root_surface.blit(transparent_surface, (self.position[0] - label_width, self.position[1]))
        root_surface.blit(font_label, (self.position[0] - label_width + 10, self.position[1] + self.size[1]/2 - label_height/2))