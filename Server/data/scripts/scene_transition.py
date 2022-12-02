# author: Mark

import pygame, time

# when this function is called, the squares shrink by a given shrink rate
# other squares are activated around squares which are already shrinking
def shrink_square(squares, shrink_rate):

    # the array "squares" is structured like this:
    #   square = squares[y coordinate][x coordinate]
    # square contains its size and a bool which indicates if the square shrinks
    #   size = square[0]
    #   square_is_shrinking = square[1]

    for y in range(len(squares)):
        for x in range(len(squares[0])):
            square = squares[y][x]
            # if the square_is_shrinking
            if square[1] == True:
                #  if square is larger than 0, shrink
                if square[0] > 0:
                    square[0] -= shrink_rate
    
    # a square is activated, if there is an active square around 
    # a newly activated square isn't supposed to activate new squares
    # thats why we have to save all active squares before we activate new squares 
    active_squares_position = []
    for y in range(len(squares)):
        for x in range(len(squares[0])):
            #  if square is active
            if squares[y][x][1]:
                # add the position of the square to the array "active_squares_position"
                active_squares_position.append([x, y])

    # activating new squares
    for y in range(len(squares)):
        for x in range(len(squares[0])):
            square = squares[y][x]
            for pos in active_squares_position:
                # if "active_squares_position" includes the current square
                if pos[0] == x and pos[1] == y:
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    position_x = x
                    position_y = y
                    # activating all squares around
                    #                                   [square will be activated]
                    #  [square will be activated]           [square is active]      [square will be activated]
                    #                                   [square will be activated]
                    for direction in directions:
                        new_position_x = position_x + direction[0]
                        new_position_y = position_y + direction[1]
                        # checking if calculated coordinates exist
                        if -1 < new_position_x < len(squares[0]) and -1 < new_position_y < len(squares):
                            # activate square
                            square = squares[new_position_y][new_position_x]
                            square[1] = True
                    break
    return squares

# checking if the size of every square is smaller than 0
def animation_finished(squares):
    for line in squares:
        for square in line:
            if square[0] > 0:
                return False
    return True

# in order to start the animation, we need squares which are already active from the beginning
# at first, all square being at a corner will be activated 
def init_corner_squares(square_size, screen_size: tuple) -> list[list[float, bool]]:
    
    # adding all squares to an array
    squares = []
    for i in range(screen_size[1]):
        squares.append([[square_size, False] for i in range(screen_size[0])])

    # calculating coordinates of the squares
    squares[0][0][1] = True
    squares[len(squares) - 1][len(squares[0]) - 1][1] = True
    squares[0][len(squares[0]) - 1][1] = True
    squares[len(squares) - 1][0][1] = True

    return squares

#  same procedure, but now we activate every square being in the center
def init_center_squares(square_size, screen_size: tuple) -> list[list[float, bool]]:
    # adding all squares to an array
    squares = []
    for i in range(screen_size[1]):
        squares.append([[square_size, False] for i in range(screen_size[0])])

    # calculating coordinates of the squares
    center_x = int(screen_size[0]/2) - 1
    center_y = int(screen_size[1]/2) - 1

    squares[center_y][center_x][1] = True
    squares[center_y + 1][center_x][1] = True
    squares[center_y][center_x + 1][1] = True
    squares[center_y + 1][center_x + 1][1] = True

    return squares

def scene_animation(root, square_size, screen_size: tuple, render_function, first_image: pygame.Surface = None):
    squares = init_corner_squares(square_size, screen_size)

    tick = time.perf_counter()
    # shrink every 0.0175 seconds
    animation_delay = 0.0175
    # pixel/per shrink
    shrink_rate = 5

    # if no additional picture is provided, the first picture in the animation is a screen shot
    if first_image == None:
        pygame.image.save(root.get_surface(), "data/images/image_temp_screenshot.png")
        first_image = pygame.image.load("data/images/image_temp_screenshot.png").convert()

    while not animation_finished(squares):
        # if time exceeded, shrink
        if time.perf_counter() - tick > animation_delay:
            tick = time.perf_counter()
            squares = shrink_square(squares, shrink_rate)
        
        # render animation

        # render background
        root.get_surface().blit(first_image, (0, 0))
        # render squares
        for y in range(len(squares)):
            for x in range(len(squares[0])):
                draw_square_size = square_size - squares[y][x][0] 
                pygame.draw.rect(root.get_surface(), "black", 
                (x * square_size + (square_size-draw_square_size)/2, y * square_size + (square_size-draw_square_size)/2, draw_square_size, draw_square_size))
        
        # update screen
        root.update(60)

    # restart animation process, but with other squares
    squares = init_center_squares(square_size, screen_size)
    tick = time.perf_counter()

    while not animation_finished(squares):
         # if time exceeded, shrink
        if time.perf_counter() - tick > animation_delay:
            tick = time.perf_counter()
            squares = shrink_square(squares, shrink_rate)
        
        # render animation

        # to render the background, a function is provided which renders the background
        render_function()

        # render squares
        for y in range(len(squares)):
            for x in range(len(squares[0])):
                draw_square_size = squares[y][x][0] 
                pygame.draw.rect(root.get_surface(), "black", (x * square_size + (square_size-draw_square_size)/2, y * square_size + (square_size-draw_square_size)/2, draw_square_size, draw_square_size))
        
        # update screen
        root.update(60)
        