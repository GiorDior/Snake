import pygame, sys, time, random, datetime, pickle, socket
from data.scripts.render import Render

class Online_game:
    def __init__(self, root, mode: str, connection) -> None:
        self.root = root
        self.mode = mode
        self.input = []

        self.score = 0
        self.passed_time = 0

        self.connection = connection

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if self.mode == "onclassic":
            self.size = (10, 10)
            self.offset = (0, 100)
            self.snake = Snake(self.root, (2, 2), self.offset)
            self.apples = [Apple((2, 6), self.offset)]
            highscore_file = open("data/onhighscore.data", "r")
            self.highscore = int(highscore_file.readline().strip())
            highscore_file.close()
        else:
            self.size = (14, 14)
            self.offset = (250, 0)
            self.snake = Snake(self.root, (11, 11), self.offset)
            self.apples = [Apple((11, 7), self.offset)]
            highscore_file = open("data/onhighscore.data", "r")
            highscore_file.readline()
            self.highscore = int(highscore_file.readline().strip())
            highscore_file.close()

            head = self.snake.pieces[0]
            rotated_image = pygame.transform.rotate(head.original_image, 180)
            head.image = rotated_image


    def change_direction(self):
        if len(self.input) > 0:
            direction = self.input[0]
            self.snake.direction = direction
            self.snake.pieces[0].direction = direction
            self.input.pop(0)

            directions_rotations = [[0, 0], [1, 90], [2, 180], [3, 270]]
            head = self.snake.pieces[0]
            for dir in directions_rotations:
                if direction == dir[0]:
                    rotated_image = pygame.transform.rotate(head.original_image, dir[1])
                    head.image = rotated_image
                    break

    def render_background(self, first_color: str = "#91f086", second_color: str = "#48bf53"):
        first_color = pygame.Color(first_color)
        second_color = pygame.Color(second_color)
        square_size = 50
        # render background:
        self.root.get_surface().fill(first_color)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if (y + x) % 2 == 0: 
                    pygame.draw.rect(self.root.get_surface(), first_color, (self.offset[0] + x * square_size, self.offset[1] + y * square_size, square_size, square_size), border_radius=2)
                else:
                    pygame.draw.rect(self.root.get_surface(), second_color, (self.offset[0] + x * square_size, self.offset[1] + y * square_size, square_size, square_size), border_radius=2)

    def render(self):
        self.render_background()
        # self.render_information()
        for apple in self.apples:
            apple.render(self.root.get_surface())
        self.snake.render()

    def render_information(self):
        surface = self.root.get_surface()
        # current score
        # Render.text(surface, "score", "data/fonts/PressStart2P.ttf", 35, (0, 113, 193), (10, 250))
        if self.mode == "onclassic":
            score_text = ""
            for i in range(3 - len(str(self.score))):
                score_text += "0"
            score_text += str(self.score)
            Render.text(surface, score_text, "data/fonts/PressStart2P.ttf", 35, (0, 113, 193), (250, 50))

            score_text = ""
            for i in range(3 - len(str(self.enemy_data[1]))):
                score_text += "0"
            score_text += str(self.enemy_data[1])
            Render.text(surface, score_text, "data/fonts/PressStart2P.ttf", 35, (127, 3, 3), (950, 50))

            Render.text(surface, "time", "data/fonts/PressStart2P.ttf", 25, "black", (600, 300))
            time_text = str(datetime.timedelta(seconds=self.passed_time))
            Render.text(surface, time_text, "data/fonts/PressStart2P.ttf", 20, "black", (600, 400))
        else:
            Render.text(surface, "time", "data/fonts/PressStart2P.ttf", 25, "black", (125, 325))
            time_text = str(datetime.timedelta(seconds=self.passed_time))
            Render.text(surface, time_text, "data/fonts/PressStart2P.ttf", 20, "black", (125, 400))

    def spawn_apple(self):
        positions = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                positions.append([x, y])
        for piece in self.snake.pieces:
            if [piece.x, piece.y] in positions:
                positions.remove([piece.x, piece.y])
        
        if self.mode == "onversus":
            for piece in self.enemy_data[0]:
                if [piece[0], piece[1]] in positions:
                    positions.remove([piece[0], piece[1]])

        apple_position = random.choice(positions)
        self.apples.append(Apple((apple_position[0], apple_position[1]), self.offset))
        
    def on_apple_collision(self):
        if self.snake.collides_apple(self.apples):
            head = self.snake.pieces[0]
            tail_direction = self.snake.pieces[-1].direction
            movement = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            tail_x = self.snake.pieces[-1].x - movement[tail_direction][0]
            tail_y = self.snake.pieces[-1].y - movement[tail_direction][1]
            self.snake.pieces.append(Piece((tail_x, tail_y), tail_direction, color=pygame.Color("#0071C1"), offset= self.offset))
            for apple in self.apples:
                if apple.x == head.x and apple.y == head.y:
                    self.apples.remove(apple)
                    self.score += 1
                    self.spawn_apple()
                    break

    def on_enemy_snake_apple_collision(self):
        enemy_head = self.enemy_data[0][0]
        for apple in self.apples:
            if apple.x == enemy_head[0] and apple.y == enemy_head[1]:
                self.apples.remove(apple)
                self.spawn_apple()
                break

    def on_enemy_apple_collision(self):
        enemy_head = self.snake.pieces[0]
        apple = self.enemy_data[2]
        if enemy_head.x == apple[0] and enemy_head.y == apple[1]:
            tail_direction = self.snake.pieces[-1].direction
            movement = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            tail_x = self.snake.pieces[-1].x - movement[tail_direction][0]
            tail_y = self.snake.pieces[-1].y - movement[tail_direction][1]
            self.snake.pieces.append(Piece((tail_x, tail_y), tail_direction, color=pygame.Color("#0071C1"), offset= self.offset))
            self.score += 1

    def run(self):
        self.total_time_tick = time.perf_counter()
        self.move_delay = 0.3
        tick = time.perf_counter()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
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

            try:
                self.connection.settimeout(10.0)
                sending_data = pickle.dumps([self.convert_snake_object(), self.score, [self.apples[0].x, self.apples[0].y]])
                self.connection.send(sending_data)
                data = self.connection.recv(4096)
                self.enemy_data = pickle.loads(data)
            except:
                return "error"


            self.passed_time = round(time.perf_counter() - self.total_time_tick)

            if time.perf_counter() - tick > self.move_delay:
                tick = time.perf_counter()
                self.on_apple_collision()
                if self.mode == "onversus":
                    self.on_enemy_apple_collision()
                    self.on_enemy_snake_apple_collision()
                self.change_direction()
                self.snake.update()
                if self.mode == "onclassic":
                    if self.snake.collides(self.size):
                        break
                else:
                    if self.snake.collides(self.size, self.enemy_data[0]):
                        return "finished"

            if self.mode == "onclassic":
                self.render()
                self.render_enemy_board_classic()
                self.render_information()
            else:
                self.render()
                self.render_enemy_versus()
                self.render_information()
                if self.enemy_data[0] == []:
                    sending_data = pickle.dumps([[], self.score, [100, 100]])
                    self.connection.send(sending_data)
                    return "finished"
                
            self.root.update(60)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            try:
                sending_data = pickle.dumps([[], self.score, [100, 100]])
                self.connection.send(sending_data)
                data = self.connection.recv(4096)
                self.enemy_data = pickle.loads(data)
            except:
                return "error"
            
            self.passed_time = round(time.perf_counter() - self.total_time_tick)
            if self.mode == "onclassic":
                self.render_background()
                self.render_enemy_board_classic()
                self.render_information()

            if self.enemy_data[0] == []:
                return "finished"
            self.root.update(60)

    def render_enemy_board_classic(self):
        first_color = (145, 240, 134)
        second_color = (72, 191, 83)
        square_size = 50

        if self.mode == "onclassic":
            x_offset = 700
        # render background:
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if (y + x) % 2 == 0: 
                    pygame.draw.rect(self.root.get_surface(), first_color, (x_offset + x * square_size, self.offset[1] + y * square_size, square_size, square_size), border_radius=2)
                else:
                    pygame.draw.rect(self.root.get_surface(), second_color, (x_offset + x * square_size, self.offset[1] + y * square_size, square_size, square_size), border_radius=2)

        # apple
        image = pygame.image.load("data/images/game/image_apple.png").convert_alpha()
        self.root.get_surface().blit(image, (x_offset + self.enemy_data[2][0] * 50, self.offset[1] + self.enemy_data[2][1] * 50))


        # snake
        for index, piece in enumerate(self.enemy_data[0]):
            if index == 0:
                image = pygame.image.load("data/images/game/image_red_snake_head.png").convert()
                directions = [[0, 0], [1, 90], [2, 180], [3, 270]]
                for dir in directions:
                    if dir[0] == piece[2]:
                        image = pygame.transform.rotate(image, (dir[1]))
                        self.root.get_surface().blit(image, (x_offset + piece[0] * 50, self.offset[1] + piece[1] * 50))
            else:
                pygame.draw.rect(self.root.get_surface(), (127, 3, 3), (x_offset + piece[0] * 50, self.offset[1] + piece[1] * 50, 50, 50))
        
    def render_enemy_versus(self):
        # apple
        image = pygame.image.load("data/images/game/image_apple.png").convert_alpha()
        self.root.get_surface().blit(image, (self.offset[0] + self.enemy_data[2][0] * 50, self.offset[1] + self.enemy_data[2][1] * 50))

        # snake
        for index, piece in enumerate(self.enemy_data[0]):
            if index == 0:
                image = pygame.image.load("data/images/game/image_red_snake_head.png").convert()
                directions = [[0, 0], [1, 90], [2, 180], [3, 270]]
                for dir in directions:
                    if dir[0] == piece[2]:
                        image = pygame.transform.rotate(image, (dir[1]))
                        self.root.get_surface().blit(image, (self.offset[0] + piece[0] * 50, self.offset[1] + piece[1] * 50))
            else:
                pygame.draw.rect(self.root.get_surface(), (127, 3, 3), (self.offset[0] + piece[0] * 50, self.offset[1] + piece[1] * 50, 50, 50))
        

    def convert_snake_object(self):
        data = []
        for piece in self.snake.pieces:
            data.append([piece.x, piece.y, piece.direction])
        return data

    def set_new_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            lines = []

            highscore_file = open("data/onhighscore.data", "r")
            for i in range(2):
                try:
                    lines.append(int(highscore_file.readline().strip()))
                except:
                    pass
            highscore_file.close()

            if self.mode == "onclassic":
                index = 0
            elif self.mode == "onversus":
                index = 1

            highscore_file = open("data/onhighscore.data", "w")
            for i in range(2):
                if i == index:
                    highscore_file.write(str(self.score) + "\n")
                else:
                    highscore_file.write(str(lines[i]) + "\n")
            highscore_file.close()
        
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
        Render.text(surface, "scores", "data/fonts/PressStart2P.ttf", 70, "black", (600, 150))
        score_text = ""
        for i in range(3 - len(str(self.score))):
            score_text += "0"
        score_text += str(self.score)
        Render.text(surface, score_text, "data/fonts/PressStart2P.ttf", 70, (0, 113, 193), (450, 250))
        score_text = ""
        for i in range(3 - len(str(self.enemy_data[1]))):
            score_text += "0"
        score_text += str(self.enemy_data[1])
        Render.text(surface, score_text, "data/fonts/PressStart2P.ttf", 70, (127, 3, 3), (750, 250))
        

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

    def final_screen(self):
        self.set_new_highscore()
        self.update_total_playtime()
        tick = time.perf_counter()
        delay = 5
        while time.perf_counter() - tick < delay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.render_final_screen()
            
            self.root.update(60)

class Snake:
    def __init__(self, root, position: tuple, offset: tuple = (0, 0)) -> None:
        self.root = root
        self.offset = offset
        self.x = position[0]
        self.y = position[1]

        
        
        if not position == (11, 11):
            self.direction = 0 
            self.pieces = [
                Piece((self.x, self.y), 0, image=pygame.image.load("data/images/game/image_snake_head.png").convert_alpha(), offset=self.offset),
                Piece((self.x, self.y - 1), 0, color=pygame.Color("#0071C1"), offset= self.offset),
                Piece((self.x, self.y - 2), 0, color=pygame.Color("#0071C1"), offset= self.offset)
            ]
        else:
            self.direction = 2 
            self.pieces = [
            Piece((self.x, self.y), 2, image=pygame.image.load("data/images/game/image_snake_head.png").convert_alpha(), offset=self.offset),
            Piece((self.x, self.y + 1), 2, color=pygame.Color("#0071C1"), offset= self.offset),
            Piece((self.x, self.y + 2), 2, color=pygame.Color("#0071C1"), offset= self.offset)
        ]

    def collides(self, game_size: tuple, enemy_snake_pieces = None):
        head = self.pieces[0]
        for piece in self.pieces:
            if not head == piece and head.x == piece.x and head.y == piece.y:
                return True
        
        if not -1 < head.x < game_size[0] or not -1 < head.y < game_size[1]:
            return True

        if not enemy_snake_pieces == None:
            for piece in enemy_snake_pieces:
                if head.x == piece[0] and head.y == piece[1]:
                    return True

        return False
    
    def collides_apple(self, apples):
        head = self.pieces[0]
        for apple in apples:
            if apple.x == head.x and apple.y == head.y:
                return True
        return False 

    def update(self):
        for index in reversed(range(len(self.pieces))):
            if not index == 0:
                self.pieces[index].x = self.pieces[index - 1].x
                self.pieces[index].y = self.pieces[index - 1].y
                self.pieces[index].direction = self.pieces[index - 1].direction

        movement = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.pieces[0].x += movement[self.direction][0]
        self.pieces[0].y += movement[self.direction][1]

    def render(self):
        for piece in self.pieces:
            piece.render(self.root)

class Piece:
    def __init__(self, position: tuple, direction, image = None, color = None, offset = (0, 0)) -> None:
        self.x = position[0]
        self.y = position[1]
        self.direction = direction
        self.offset = offset

        self.width = 50
        self.height = 50

        self.color = color

        self.original_image = image
        self.image = self.original_image
        
    def render(self, root):
        if not self.color == None:
            pygame.draw.rect(root.get_surface(), self.color, 
            (self.x * self.width + self.offset[0], self.y * self.width + self.offset[1], self.width, self.height))
        
        if not self.image == None:
            root.get_surface().blit(self.image, (self.x * self.width + self.offset[0], self.y * self.height + self.offset[1]))

class Apple:
    def __init__(self, position: tuple, offset: tuple) -> None:
        self.x = position[0]
        self.y = position[1]
        self.offset = offset

        self.image = pygame.image.load("data/images/game/image_apple.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def render(self, root_surface: pygame.Surface):
        root_surface.blit(self.image, (self.x * self.width + self.offset[0], self.y * self.height + self.offset[1]))