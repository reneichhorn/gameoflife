
import pyglet
from pyglet import shapes
import random
from cell import Cell


width = 2500
height = 1300
window = pyglet.window.Window(width, height)
scale = 10
cols = width // scale
rows = height // scale
batch = pyglet.graphics.Batch()
width = width - scale
height = height - scale
DEAD = [0, 0, 0]
ALIVE = [255, 255, 255]
PAUSED = False
LIVELIHOOD = 0.45
cells = []
alreadyvisited = []
lastshownplace = None
mousepos = 0, 0
figureToPlace = None
figures = [
    [(0, -1), (1, -1), (1, 0), (0, 0)],
    [(-4, 0), (-4, -1), (-4, 1), (-3, -2), (-3, 2), (-2, -3), (-2, 3), (-1, -3), (-1, 3), (0,0), (1, -2), (1, 2), (2, -1), (2, 0), (2, 1), (3, 0)],
    [(-7, -8), (-7, 7), (-7, -7), (-7, 6), (-7, -6), (-7, 5),
    (-6, -5), (-6, 4), (-6, -8), (-6, 7),
    (-5, -8), (-5, 7),
    (-4, -4), (-4, 3), (-4, -8), (-4, 7),
    (-3, -4), (-3, 3), (-3, -8), (-3, 7),
    (-2, -3), (-2, 2), (-2, 6), (-2, -7),
    (-1, -2), (-1, 1),
    (0, 0), (0, -1),
    (1, 1), (1, -2), (1, -4), (1, 3),
    (2, -4), (2, 3),
    (3, -3), (3, 2), (3, -2), (3, 1),
    (4, -5), (4, 4), (4, -4), (4, 3),
    (5, -6), (5, 5), (5, -5), (5, 4), (5, -4), (5, 3), (5, -2), (5, 1),
    (6, -7), (6, 6), (6, -6), (6, 5), (6, -3), (6, 2),
    (7, -7), (7, 6), (7, -5), (7, 4),
    (8, -6), (8, 5), (8, -5), (8, 4), (8, -4), (8, 3),
    (9, -6), (9, 5), (9, -5), (9, 4), (9, -4), (9, 3),
    (10, -6), (10, 5), (10, -5), (10, 4)
    ]

]


for j in range(0, rows):
    for i in range(0, cols):
        state = DEAD
        if random.random() > LIVELIHOOD:
            state = ALIVE
        gameobject = shapes.Rectangle(0+i*scale, height-j*scale,
                                        scale-1, scale-1, color=state,
                                        batch=batch)
        cells.append(Cell(gameobject, i, j, state))

for cell in cells:
    cell.getNeighbours(cells, cols)


def calculateNextBoard():
    global cells
    for cell in cells:
        cell.countAliveNeighbours()
    for cell in cells:
        cell.setState()
        cell.setColor()


def cellCountAliveNeighbours(cells):
    for cell in cells:
        cell.countAliveNeighbours()


def cellSetState(cells):
    for cell in cells:
        cell.setState()


def cleanEverything():
    global cells
    for cell in cells:
        cell.die()


@window.event
def on_draw():
    window.clear()
    batch.draw()


@window.event
def on_key_press(symbol, modifiers):
    global PAUSED, figures
    if chr(symbol) == 'p':
        PAUSED = not PAUSED
    if chr(symbol) == 'c':
        PAUSED = True
        cleanEverything()
    if chr(symbol) == '1':
        PAUSED = True
        # figureToPlace = figures[1]
        showFigure(figures[0])
    if chr(symbol) == '2':
        PAUSED = True
        # figureToPlace = figures[1]
        showFigure(figures[1])
    if chr(symbol) == '3':
        PAUSED = True
        # figureToPlace = figures[1]
        showFigure(figures[2])


def showFigure(figure):
    global cells, mousepos, height, cols, lastshownplace
    i, j = mousepos
    x = (i // scale)
    y = (height - j + scale//2)//scale
    lookup = cols * y + x
    origin = cells[lookup]
    offsets = figure
    if lastshownplace != (x, y) and lastshownplace is not None:
        for offset in offsets:
            xoffset = offset[0]
            yoffset = offset[1]
            lastshownplacex = lastshownplace[0]
            lastshownplacey = lastshownplace[1]
            neighbourlookup = (cols * (lastshownplacey + yoffset) + (lastshownplacex + xoffset)) % len(cells) - 1
            neighbour = cells[neighbourlookup]
            neighbour.state = DEAD
            neighbour.gameobject.color = DEAD
    for offset in offsets:
        xoffset = offset[0]
        yoffset = offset[1]
        neighbourlookup = (cols * (y + yoffset) + (x + xoffset)) % len(cells) - 1
        neighbour = cells[neighbourlookup]
        neighbour.state = ALIVE
        neighbour.gameobject.color = ALIVE
    lastshownplace = (x, y)
    pass


@window.event
def on_mouse_press(x, y, button, modifiers):
    print('mousepress')
    global height
    x = x//scale
    y = (height - y + scale//2)//scale
    global cells, cols, ALIVE, DEAD
    lookup = cols * y + x
    print(cells[lookup])
    state = cells[lookup].state
    if state != DEAD:
        state = DEAD
    elif state == DEAD:
        state = ALIVE
    print(state)
    cells[lookup].state = state
    cells[lookup].gameobject.state = state
    print(cells[lookup].state, cells[lookup].gameobject.state)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    print('mousedrag')
    global height, cells, cols, ALIVE, DEAD, alreadyvisited
    x = x//scale
    y = (height - y + scale//2)//scale
    lookup = cols * y + x
    if lookup not in alreadyvisited:
        state = cells[lookup].state
        if state != DEAD:
            state = DEAD
        elif state == DEAD:
            state = ALIVE
        cells[lookup].state = state
        cells[lookup].gameobject.state = state
    alreadyvisited.append(lookup)


@window.event
def on_mouse_release(x, y, button, modifiers):
    global alreadyvisited
    alreadyvisited = []


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mousepos
    mousepos = x, y


def update(dt):
    window.clear()
    batch.draw()
    global PAUSED
    if not PAUSED:
        calculateNextBoard()


pyglet.clock.schedule_interval(update, 1/20)
pyglet.app.run()
