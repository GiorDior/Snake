import pygame, sys, time, random, datetime
from data.scripts.render import Render
from data.scripts.buttons import Button

class Game:
    def __init__(self, root, mode: str) -> None:
        self.root = root
        # gammeode
        self.mode = mode
        # size of the board
        self.size = (14, 14)

        # user keyboard input
        self.input = []

        # user score
        self.score = 0

        # total time passed
        self.passed_time = 0

        # reset mouse cursor
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # create the snake and the first apple
        self.x_offset = 250
        self.snake = Snake(self.root, (2, 2), (self.x_offset, 0))
        self.apples = [Apple((2, 6), (self.x_offset, 0))]
        
        # read the highscore, creating other game related variables
        highscore_file = open("data/highscore.data", "r")
        if self.mode == "classic":
            # read only the first line
            self.highscore = int(highscore_file.readline().strip())
        elif self.mode == "advanced":
            # all bricks are stored here 
            self.bricks = []
            self.spawn_bricks()
            highscore_file.readline()
            # the highscore is in the second line of the file
            self.highscore = int(highscore_file.readline().strip())
        highscore_file.close()

    # changing the image of the snake as well as its moving direction
    def change_direction(self):
        if len(self.input) > 0:
            # set snake direction to input
            direction = self.input[0]
            self.snake.direction = direction
            self.snake.pieces[0].direction = direction
            self.input.pop(0)

            # [direction, rotation angle]
            # calculating the correct angle
            directions_rotations = [[0, 0], [1, 90], [2, 180], [3, 270]]
            head = self.snake.pieces[0]
            for dir in directions_rotations:
                # if given direction equals directions
                if direction == dir[0]:
                    # rotate image by xyz degrees
                    rotated_image = pygame.transform.rotate(head.original_image, dir[1])\
                    # set new image
                    head.image = rotated_image
                    break

    # render green rectangles in the background
    def render_background(self, first_color: str = "#91f086", second_color: str = "#48bf53"):
        # colors
        first_color = pygame.Color(first_color)
        second_color = pygame.Color(second_color)
        # size
        square_size = 50
        # render background:
        self.root.get_surface().fill(first_color)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                # checking which color to draw
                if (y + x) % 2 == 0: 
                    pygame.draw.rect(self.root.get_surface(), first_color, (self.x_offset + x * square_size, y * square_size, square_size, square_size), border_radius=2)
                else:
                    pygame.draw.rect(self.root.get_surface(), second_color, (self.x_offset + x * square_size, y * square_size, square_size, square_size), border_radius=2)

    # rendering the entire game
    def render(self):
        # background
        self.render_background()
        # score, highscore, time
        self.render_information()
        # render apples
        for apple in self.apples:
            apple.render(self.root.get_surface())

        # rendering the bricks additionally if the  user plays "advanced"
        if self.mode == "advanced":
            for brick in self.bricks:
                brick.render(self.root.get_surface())
        # render snake
        self.snake.render()

    def render_information(self):
        surface = self.root.get_surface()
        # current score
        Render.text(surface, "score", "data/fonts/PressStart2P.ttf", 35, "black", (125, 250))
        score_text = ""
        for i in range(3 - len(str(self.score))):
            score_text += "0"
        score_text += str(self.score)
        Render.text(surface, score_text, "data/fonts/PressStart2P.ttf", 35, "black", (125, 300))

        # highscore
        Render.text(surface, "highscore", "data/fonts/PressStart2P.ttf", 25, "black", (125, 400))
        highscore_text = ""
        for i in range(3 - len(str(self.highscore))):
            highscore_text += "0"
        highscore_text += str(self.highscore)
        Render.text(surface, highscore_text, "data/fonts/PressStart2P.ttf", 25, "black", (125, 450))

        # time
        Render.text(surface, "time", "data/fonts/PressStart2P.ttf", 35, "black", (1075, 300))
        time_text = str(datetime.timedelta(seconds=self.passed_time))
        Render.text(surface, time_text, "data/fonts/PressStart2P.ttf", 30, "black", (1075, 400))

    def spawn_apple(self):
        positions = []
        # adding all available positions to "positions"
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                positions.append([x, y])

        # remove position of the snake
        for piece in self.snake.pieces:
            if [piece.x, piece.y] in positions:
                positions.remove([piece.x, piece.y])
        
        # remove position of the bricks
        if self.mode == "advanced":
            for brick in self.bricks:
                if [brick.x, brick.y] in positions:
                    positions.remove([brick.x, brick.y])

        # select a random position in "positions"
        apple_position = random.choice(positions)
        # adding a new apple
        self.apples.append(Apple((apple_position[0], apple_position[1]), (self.x_offset, 0)))
        
    def on_apple_collision(self):
        # checking if snake collides
        if self.snake.collides_apple(self.apples):
            head = self.snake.pieces[0]
            tail_direction = self.snake.pieces[-1].direction
            movement = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            tail_x = self.snake.pieces[-1].x - movement[tail_direction][0]
            tail_y = self.snake.pieces[-1].y - movement[tail_direction][1]
            # adding a new piece in the opposit direction of the last piece of the snake
            self.snake.pieces.append(Piece((tail_x, tail_y), tail_direction, color=pygame.Color("#0071C1"), offset= (self.x_offset, 0)))
            for apple in self.apples:
                if apple.x == head.x and apple.y == head.y:
                    # remove the colliding apple
                    self.apples.remove(apple)
                    break
            
            # updating the score
            self.score += 1
            # spawn a new apple
            self.spawn_apple()
            # in advanced mode, the speed increases
            if self.mode == "advanced":
                # 1 percent faster every time
                if not self.move_delay - 0.003 == 0.1:
                    self.move_delay -= 0.003
                
                # spawn bricks when the user collects apples
                if self.score % 2 == 0:
                    self.bricks = []
                    self.spawn_bricks()
                    # spawn even more bricks
                    if self.score > 25:
                        self.spawn_bricks()

    # spawns a brick at an available position
    def spawn_bricks(self):
        positions = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                positions.append([x, y])
        
        # removing position of the snake
        for piece in self.snake.pieces:
            if [piece.x, piece.y] in positions:
                positions.remove([piece.x, piece.y])

        # removing all positions being in the direction of the snake
        if self.snake.direction % 2 == 0:
            for i in range(self.size[1]):
                x = self.snake.pieces[0].x
                y = i
                if [x, y] in positions:
                    positions.remove([x, y])
        else:
            for i in range(self.size[0]):
                y = self.snake.pieces[0].y
                x = i
                if [x, y] in positions:
                    positions.remove([x, y])

        # if there are more than at least 7 squares available in the game
        if not len(positions) < 7:
            # random brick length
            length = random.randint(1, 5)
            # random position
            position = random.choice(positions)
            # random position again and adding bricks
            if random.random() < 0.5:
                for i in range(length):
                    if [position[0], position[1] + 1] in positions and \
                        -1 < position[0] < self.size[0] and -1 < position[1] + i < self.size[1]:
                        self.bricks.append(Brick((position[0], position[1] + i), (self.x_offset, 0)))
            else:
                for i in range(length):
                    if [position[0] + i, position[1]] in positions and \
                        -1 < position[0] + i < self.size[0] and -1 < position[1] < self.size[1]:
                        self.bricks.append(Brick((position[0] + i, position[1]), (self.x_offset, 0)))


    # run the main llop
    def run(self):
        self.total_time_tick = time.perf_counter()
        # snake moves every 0.3 seconds
        self.move_delay = 0.3
        tick = time.perf_counter()

        # load buttons
        image_quit_button = pygame.image.load("data/images/buttons/image_quit_button.png").convert_alpha()
        image_resume_button = pygame.image.load("data/images/buttons/image_resume_button.png").convert_alpha()
        # buttons
        buttons_game = [
            Button(self.root, image_quit_button, 100, 650),
            Button(self.root, image_resume_button, 600, 350)
            ]

        while True:
            # events
            for event in pygame.event.get():
                # user quits
                if event.type == pygame.QUIT:
                    sys.exit()

                # user presses a key
                if event.type == pygame.KEYDOWN:
                    # user moves the snake
                    keys_directions = [ [[pygame.K_DOWN, pygame.K_s], 0],
                                        [[pygame.K_RIGHT, pygame.K_d], 1],
                                        [[pygame.K_UP, pygame.K_w], 2],
                                        [[pygame.K_LEFT, pygame.K_a], 3],
                    ]
                    for key in keys_directions:
                        if event.key in key[0]:
                            if len(self.input) == 0:
                                if not key[1] % 2 == self.snake.direction % 2:
                                    self.input.append(key[1])
                            else:
                                if not key[1] % 2 == self.input[-1] % 2:
                                    self.input.append(key[1])
                            break
                    
                    # user wants to pause the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.image.save(self.root.get_surface(), "data/images/image_temp_screenshot.png")
                        # loading pause menu images
                        background_image = pygame.image.load("data/images/image_temp_screenshot.png").convert()
                        transparent_surface = pygame.Surface((1200, 700))
                        transparent_surface.set_alpha(150)
                        resume = False
                        while not resume:
                            for event in pygame.event.get():
                                # checking if user quits the app while being in the pause menu
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                # checking if user returns to the game
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        resume = True
                                # checking if user presses the quit button to quit the game
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                    for i, button in enumerate(buttons_game):
                                        if button.mouse_is_hovering():
                                            if i == 0:
                                                return "quit"
                                            else:
                                                resume = True
                            
                            # render pause menu
                            self.root.get_surface().blit(background_image, (0, 0))
                            self.root.get_surface().blit(transparent_surface, (0, 0))

                            # render quit button
                            for button in buttons_game:
                                button.update()
                                button.render()
                            
                            # update screen
                            self.root.update(60)
                        
                        # continuing the time counter
                        self.total_time_tick = time.perf_counter() - self.passed_time
                        tick = time.perf_counter()
            
            # calculate passed time
            self.passed_time = round(time.perf_counter() - self.total_time_tick)

            # move snake 
            if time.perf_counter() - tick > self.move_delay:
                tick = time.perf_counter()
                # check apple collision
                self.on_apple_collision()
                # change direction on key input
                self.change_direction()
                # update snake position
                self.snake.update()
                # check snake collision
                if self.snake.collides(self.size):
                    return None
                
                # check brick collision
                if self.mode == "advanced" and self.snake.collides_brick(self.bricks):
                    return None

            # render the game
            self.render()   
            # update the screen
            self.root.update(60)
    
    # setting a new highscore at the end of a game
    def set_new_highscore(self):
        # compare score and current highscore
        if self.score > self.highscore:
            self.highscore = self.score
            lines = []
            
            highscore_file = open("data/highscore.data", "r")
            for i in range(2):
                try:
                    lines.append(int(highscore_file.readline().strip()))
                except:
                    pass
            highscore_file.close()

            if self.mode == "classic":
                index = 0
            elif self.mode == "advanced":
                index = 1

            # rewrite highscore
            highscore_file = open("data/highscore.data", "w")
            for i in range(2):
                if i == index:
                    highscore_file.write(str(self.score) + "\n")
                else:
                    highscore_file.write(str(lines[i]) + "\n")
            highscore_file.close()
    
    # adding total playtime to the file total.playtime
    def update_total_playtime(self):
        playtime_file = open("data/total.playtime", "r")
        playtime = int(playtime_file.readline().strip())
        playtime_file.close()

        playtime += self.passed_time

        playtime_file = open("data/total.playtime", "w")
        playtime_file.write(str(playtime))
        playtime_file.close()


    def render_final_screen(self):
        surface = self.root.get_surface()
        surface.fill(pygame.Color("#91f086"))
        # current score
        Render.text(surface, "score", "data/fonts/PressStart2P.ttf", 70, "black", (600, 150))
        score_text = ""
        for i in range(3 - len(str(self.score))):
            score_text += "0"
        score_text += str(self.score)
        Render.text(surface, score_text, "data/fonts/PressStart2P.ttf", 70, "black", (600, 250))

        # highscore
        Render.text(surface, "highscore", "data/fonts/PressStart2P.ttf", 50, "black", (600, 350))
        highscore_text = ""
        for i in range(3 - len(str(self.highscore))):
            highscore_text += "0"
        highscore_text += str(self.highscore)
        Render.text(surface, highscore_text, "data/fonts/PressStart2P.ttf", 50, "black", (600, 415))

        # time
        Render.text(surface, "time", "data/fonts/PressStart2P.ttf", 50, "black", (600, 500))
        time_text = str(datetime.timedelta(seconds=self.passed_time))
        Render.text(surface, time_text, "data/fonts/PressStart2P.ttf", 50, "black", (600, 575))

    # initiate final screen after the game
    def final_screen(self):
        self.set_new_highscore()
        self.update_total_playtime()
        tick = time.perf_counter()
        delay = 5
        while time.perf_counter() - tick < delay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # if user presses one of the keys, continue
                if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE]:
                    return None

            self.render_final_screen()
            
            self.root.update(60)

# snake
class Snake:
    def __init__(self, root, position: tuple, offset: tuple = (0, 0)) -> None:
        # root window
        self.root = root
        # rendering offset
        self.offset = offset
        # snake head position
        self.x = position[0]
        self.y = position[1]
        # snake head direction
        self.direction = 0 
        
        # snake parts
        self.pieces = [
            Piece((self.x, self.y), 0, image=pygame.image.load("data/images/game/image_snake_head.png").convert_alpha(), offset=self.offset),
            Piece((self.x, self.y - 1), 0, color=pygame.Color("#0071C1"), offset= self.offset),
            Piece((self.x, self.y - 2), 0, color=pygame.Color("#0071C1"), offset= self.offset)
        ]

    # checking if snake collides with border
    def collides(self, game_size: tuple):
        head = self.pieces[0]
        for piece in self.pieces:
            if not head == piece and head.x == piece.x and head.y == piece.y:
                return True
        
        if not -1 < head.x < game_size[0] or not -1 < head.y < game_size[1]:
            return True

        return False
    
    # checking apple collision
    def collides_apple(self, apples):
        head = self.pieces[0]
        for apple in apples:
            if apple.x == head.x and apple.y == head.y:
                return True
        return False 

    # checking brick collision
    def collides_brick(self, bricks):
        head = self.pieces[0]
        for brick in bricks:
            if brick.x == head.x and brick.y == head.y:
                return True
        return False 

    # updating snake position and pieces
    def update(self):
        for index in reversed(range(len(self.pieces))):
            if not index == 0:
                self.pieces[index].x = self.pieces[index - 1].x
                self.pieces[index].y = self.pieces[index - 1].y
                self.pieces[index].direction = self.pieces[index - 1].direction

        movement = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.pieces[0].x += movement[self.direction][0]
        self.pieces[0].y += movement[self.direction][1]

    # render snakes
    def render(self):
        for piece in self.pieces:
            piece.render(self.root)

# one piece of the snake
class Piece:
    def __init__(self, position: tuple, direction, image = None, color = None, offset = (0, 0)) -> None:
        # position
        self.x = position[0]
        self.y = position[1]
        # piece direction
        self.direction = direction
        # render offset
        self.offset = offset

        # piece size
        self.width = 50
        self.height = 50

        # rendering color
        self.color = color

        # rendering image in case there is an image
        self.original_image = image
        self.image = self.original_image
        
    def render(self, root) -> None:
        # draw color in case there is no image
        if not self.color == None:
            pygame.draw.rect(root.get_surface(), self.color, 
            (self.x * self.width + self.offset[0], self.y * self.width + self.offset[1], self.width, self.height))
        
        # draw image in case there is an image
        if not self.image == None:
            root.get_surface().blit(self.image, (self.x * self.width + self.offset[0], self.y * self.height + self.offset[1]))

# red apple eaten by snakes
class Apple:
    def __init__(self, position: tuple, offset: tuple) -> None:
        # position
        self.x = position[0]
        self.y = position[1]
        # rendering offset
        self.offset = offset

        # image of the apple
        self.image = pygame.image.load("data/images/game/image_apple.png").convert_alpha()
        # apple size
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def render(self, root_surface: pygame.Surface):
        root_surface.blit(self.image, (self.x * self.width + self.offset[0], self.y * self.height + self.offset[1]))

# brick in advanced mode
class Brick:
    def __init__(self, position: tuple, offset: tuple) -> None:
        # position in indexes
        self.x = position[0]
        self.y = position[1]
        # rendering offset
        self.offset = offset

        # image
        self.image = pygame.image.load("data/images/game/image_brick.png").convert_alpha()
        # size
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    # rendering brick
    def render(self, root_surface: pygame.Surface):
        root_surface.blit(self.image, (self.x * self.width + self.offset[0], self.y * self.height + self.offset[1]))
