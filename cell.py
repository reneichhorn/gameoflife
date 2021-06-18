DEAD = [0, 0, 0]
ALIVE = [255, 255, 255]
ALIVESTATE1 = [255, 0, 0]
ALIVESTATE2 = [255, 165, 0]
ALIVESTATE3 = [255, 255, 0]
ALIVESTATE4 = [0, 128, 0]
ALIVESTATE5 = [0, 0, 255]
ALIVESTATE6 = [75, 0, 130]
ALIVESTATE7 = [238, 130, 238]
ALIVESTATE8 = [255, 255, 255]
WITHCOLOR = True


class Cell:
    def __init__(self, gameobject, i, j, state):
        self.gameobject = gameobject
        self.i = i
        self.j = j
        self.neighbours = []
        self.hasChanged = True
        self.state = state
        self.aliveNeighbours = 0
        self.aliveTime = 0

    def getNeighbours(self, cells, cols):
        i = self.i
        j = self.j
        for rowoffset in range(-1, 2):
            for coloffset in range(-1, 2):
                lookup = ((cols * (j + rowoffset)) + (i + coloffset)) % (len(cells) - 1)
                if (coloffset == 0 and rowoffset==0):
                    continue
                self.neighbours.append(cells[lookup])

    def countAliveNeighbours(self):
        alivecount = 0
        for neighbour in self.neighbours:
            if not neighbour.hasChanged and neighbour.state == DEAD:
                continue
            if neighbour.gameobject.color != DEAD:
                alivecount += 1
            if alivecount > 3:
                break
        self.aliveNeighbours = alivecount

    def setState(self):
        self.hasChanged = False
        if self.state != DEAD:
            if self.aliveNeighbours < 2:
                self.hasChanged = True
                self.state = DEAD
                self.aliveTime = 0
            elif self.aliveNeighbours > 3:
                self.state = DEAD
                self.hasChanged = True
                self.aliveTime = 0
        else:
            if self.aliveNeighbours == 3:
                self.state = ALIVE
                self.hasChanged = True
        if self.hasChanged:
            self.gameobject.color = self.state
        self.setColor()

    def die(self):
        self.state = DEAD
        self.gameobject.color = self.state

    def setColor(self):
        if WITHCOLOR:
            if self.state != DEAD:
                self.aliveTime += 1
                if self.aliveTime < 40:
                    self.gameobject.color = ALIVESTATE1
                elif self.aliveTime < 80:
                    self.gameobject.color = ALIVESTATE2
                elif self.aliveTime < 160:
                    self.gameobject.color = ALIVESTATE3
                elif self.aliveTime < 320:
                    self.gameobject.color = ALIVESTATE4
                elif self.aliveTime < 640:
                    self.gameobject.color = ALIVESTATE5
                elif self.aliveTime < 1280:
                    self.gameobject.color = ALIVESTATE6
                elif self.aliveTime < 2560:
                    self.gameobject.color = ALIVESTATE7
                elif self.aliveTime < 5120:
                    self.gameobject.color = ALIVESTATE8
                self.aliveTime += 1

    def setStateManually(self, state):
        self.hasChanged = True
        self.state = state
        self.gameobject.state = self.state
        print(self.state)
