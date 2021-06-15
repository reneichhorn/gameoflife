
import pyglet
from pyglet import shapes
import random

width = height = 2000
window = pyglet.window.Window(width, height)
scale = 20
cols = width // scale
rows = height // scale
batch = pyglet.graphics.Batch()
width = height = width - scale
squares = []
DEAD = [0, 0, 0]
ALIVE = [255, 255, 255]
PAUSED = False
LIVELIHOOD = 0.75

for j in range(0, rows):
    for i in range(0, cols):
        state = DEAD
        if random.random() > LIVELIHOOD:
            state = ALIVE
        squares.append(shapes.Rectangle(0+i*scale, height-j*scale,
                                        scale-1, scale-1, color=state,
                                        batch=batch))


def calulateNeighbours(i, j):
    global squares
    aliveneighbourscount = 0
    for rowoffset in range(-1, 2):
        for coloffset in range(-1, 2):
            if ((cols * (j + rowoffset)) + (i + coloffset)) > (len(squares) - 1) or (coloffset == 0 and rowoffset==0):
                continue
            neighbour = squares[((cols * (j + rowoffset)) + (i + coloffset))].color
            if neighbour == ALIVE:
                aliveneighbourscount += 1
    return aliveneighbourscount


def calculateNextBoard():
    global squares
    newsquares = []
    for square in squares:
        newsquare = {}
        newsquare['state'] = square.color
        newsquare['x'] = square.x
        newsquare['y'] = square.y

        n = calulateNeighbours(square.x//scale, (height-square.y)//scale)

        if square.color == ALIVE:
            if n < 2:
                newsquare['state'] = DEAD
            elif n > 3:
                newsquare['state'] = DEAD
        elif square.color == DEAD:
            if n == 3:
                newsquare['state'] = ALIVE
        newsquares.append(newsquare)
    squares = []
    for newsquare in newsquares:
        squares.append(shapes.Rectangle(newsquare['x'], newsquare['y'], scale-1, scale-1, color=newsquare['state'], batch=batch))


@window.event
def on_draw():
    window.clear()
    batch.draw()


@window.event
def on_key_press(symbol, modifiers):
    global PAUSED
    if chr(symbol) == 'p':
        PAUSED = not PAUSED


@window.event
def on_mouse_press(x, y, button, modifiers):
    global height
    x = x//scale
    y = (height - y + scale//2)//scale
    global squares, cols, ALIVE, DEAD
    state = squares[cols * y + x].color
    if state == ALIVE:
        state = DEAD
    elif state == DEAD:
        state = ALIVE
    squares[cols * y + x].color = state


def update(dt):
    window.clear()
    batch.draw()
    global PAUSED
    if not PAUSED:
        calculateNextBoard()


pyglet.clock.schedule_interval(update, 1/5)
pyglet.app.run()
