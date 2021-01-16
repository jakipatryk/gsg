import turtle
import game

block_pixel_size = 24

wn = turtle.Screen()
wn.bgcolor("black")
tiles_size = 6

tiles_pixel_size = tiles_size * block_pixel_size
screen_size = tiles_pixel_size + 100
tiles_border = ((tiles_size - 1) // 2) * block_pixel_size

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Work smart not hard")
wn.setup(screen_size, screen_size)


class Unknown(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("white")
        self.shape('square')
        self.penup()
        self.speed(0)


class Empty(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("green")
        self.shape('square')
        self.penup()
        self.speed(0)


class Full(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("red")
        self.shape('square')
        self.penup()
        self.speed(0)


def print_tiles(n):
    unknown = Unknown()
    for y in range(n):
        for x in range(n):
            screen_x = -tiles_border + (x * block_pixel_size)
            screen_y = tiles_border - (y * block_pixel_size)

            unknown.goto(screen_x, screen_y)
            unknown.stamp()


def pixel_coords_to_pos(i, j):
    pos_x = (i + tiles_border) // block_pixel_size
    pos_y = (tiles_border - j) // block_pixel_size

    return pos_x, pos_y


empty = Empty()
full = Full()
level = game.Level([[1, 0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1, 0]], 100, 100)
levels = [level]

gsg = game.Game(levels)


def restart_level():
    turtle.Screen().resetscreen()
    for turtl in turtle.Screen().turtles():
        turtl.hideturtle()
    print_tiles(tiles_size)
    gsg.restart_level()


def next_level():
    turtle.Screen().resetscreen()
    for turtl in turtle.Screen().turtles():
        turtl.hideturtle()
    print_tiles(tiles_size)
    gsg.next_level()


def click(x, y):
    print(x, y)
    x, y = int(x), int(y)
    pos_x, pos_y = pixel_coords_to_pos(x, y)
    screen_x = -tiles_border + (pos_x * block_pixel_size)
    screen_y = tiles_border - (pos_y * block_pixel_size)

    tile = gsg.pick_tile(pos_x, pos_y)
    if tile == 0 or tile == -2:
        gotoresult = empty.goto(screen_x, screen_y)
        empty.stamp()
    if tile == 1 or tile == -1:
        gotoresult = full.goto(screen_x, screen_y)
        full.stamp()
    if tile == -1:
        next_level()
    if tile == -2:
        restart_level()

    return gotoresult


print_tiles(tiles_size)
wn.onscreenclick(click)

turtle.done()
