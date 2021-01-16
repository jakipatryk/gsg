import turtle
import game
import generate_levels


block_pixel_size = 24

# turtle.register_shape("green_tile.gif")
# turtle.register_shape("red_tile.gif")
# turtle.register_shape("grey_tile.gif")
# turtle.register_shape("grey_to_green_tile.gif")
# turtle.register_shape("grey_appear.gif")

wn = turtle.Screen()
wn.bgcolor("black")
tiles_size = 10

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
        self.color("red")
        self.shape('square')
        self.penup()
        self.speed(0)


class Full(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("green")
        self.shape('square')
        self.penup()
        self.speed(0)


class DownWriter(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("red")
        self.penup()
        self.hideturtle()
        self.speed(0)
        self.goto(-tiles_border, -tiles_border-(block_pixel_size * 2.5))


class UpWriter(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("orange")
        self.penup()
        self.hideturtle()
        self.speed(0)
        self.goto(-tiles_border, tiles_border+block_pixel_size)


class Tiles:
    def __init__(self, n):
        self.n = n
        self.tiles = [[False for i in range(n)] for j in range(n)]

    def pick(self, i, j):
        if self.tiles[i][j]:
            return False
        else:
            self.tiles[i][j] = True
            return True

    def reset(self):
        self.tiles = [[False for i in range(self.n)] for j in range(self.n)]


def print_tiles(n):
    unknown = Unknown()
    for y in range(n):
        for x in range(n):
            screen_x = -tiles_border + (x * block_pixel_size)
            screen_y = tiles_border - (y * block_pixel_size)

            unknown.goto(screen_x, screen_y)
            unknown.stamp()


def pixel_coords_to_pos(i, j):
    pos_x = (i + tiles_border + block_pixel_size//2) // block_pixel_size
    pos_y = (tiles_border - j + block_pixel_size//2) // block_pixel_size

    return pos_x, pos_y


def restart_level():
    print_tiles(tiles_size)
    tiles.reset()


def next_level():
    print_tiles(tiles_size)
    tiles.reset()
    down_writer.clear()
    down_writer.write(
        f"Current level: {gsg.current_level_index + 1}", font=("Arial", 16, "normal"))


def in_tiles_range(pos_x, pos_y):
    return 0 <= pos_x < tiles_size and 0 <= pos_y < tiles_size


empty = Empty()
full = Full()
down_writer = DownWriter()
down_writer.write("Current level: 1", font=("Arial", 16, "normal"))
up_writer = UpWriter()
up_writer.write("q - quite | r - restart level",
                font=("Arial", 16, "normal"))

levels = generate_levels.generate_levels(tiles_size)
tiles = Tiles(tiles_size)

gsg = game.Game(levels)


def click(x, y):
    x, y = int(x), int(y)
    pos_x, pos_y = pixel_coords_to_pos(x, y)
    if not in_tiles_range(pos_x, pos_y):
        return
    pick = tiles.pick(pos_x, pos_y)
    if not pick:
        return
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

turtle.listen()
turtle.onkey(exit, "q")
turtle.onkey(restart_level, "r")
wn.onscreenclick(click)

turtle.done()
