
from typing import List
import pyglet
from pyglet import shapes
import random
import concurrent.futures

width = 1500
height = 1000
window = pyglet.window.Window(width, height)
scale = 10
cols = width // scale
rows = height // scale
batch = pyglet.graphics.Batch()
width = width - scale
height = height - scale
squares = []
DEAD = [0, 0, 0]
ALIVE = [255, 255, 255]
PAUSED = False
LIVELIHOOD = 0.75
MAXTHREADS = 300
newsquares = []

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
            if aliveneighbourscount > 3:
                break
            lookup = (cols * (j + rowoffset)) + (i + coloffset)
            if lookup > (len(squares) - 1) or (coloffset == 0 and rowoffset==0):
                continue
            neighbour = squares[((cols * (j + rowoffset)) + (i + coloffset))].color
            if neighbour == ALIVE:
                aliveneighbourscount += 1
        if aliveneighbourscount > 3:
            break
    return aliveneighbourscount


def calculateNextBoard():
    global squares
    futures = []
    threadnumber = (len(squares) - 1)//MAXTHREADS
    start = 0
    end = threadnumber
    # print(f'{threadnumber} fields to check per thread. {MAXTHREADS} Threads active')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for x in range(MAXTHREADS+1):
            squaresforthread = squares[start:end]
            futures.append(executor.submit(calculateneighbourThreads, squaresforthread))
            start += threadnumber
            end = start + threadnumber
    cleanfuture = []
    for f in futures:
        result = f.result()
        if type(result) == list and len(result)>0:
            for e in result:
                cleanfuture.append(e)
    newsquares = cleanfuture
    squares = []
    for newsquare in newsquares:
        squares.append(shapes.Rectangle(newsquare['x'], newsquare['y'], scale-1, scale-1, color=newsquare['state'], batch=batch))


def calculateneighbourThreads(squaresforthread):
    threadsquares = []
    for square in squaresforthread:
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
        else:
            if n == 3:
                newsquare['state'] = ALIVE
        threadsquares.append(newsquare)
    return threadsquares


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


pyglet.clock.schedule_interval(update, 1/30)
pyglet.app.run()
