import numpy;

price_red = 10
price_white = 10
price_dot = 10
price_ring = 10


class Appraiser:
    def __init__(self, gameMap):
        self.gameMap = gameMap

    gameMap_red = numpy.zeros((12, 8))
    gameMap_white = numpy.zeros((12, 8))
    gameMap_dot = numpy.zeros((12, 8))
    gameMap_ring = numpy.zeros((12, 8))

    red = [1, 3]
    white = [2, 4]
    dot = [1, 4]
    ring = [2, 3]

    def appraise(self, move):
        i = int(move.targetCoordinateLet) - 1
        j = move.targetCoordinateNum - 1
        i1 = i
        j1 = j
        if move.rotation % 2 != 0:
            i1 += 1
        else:
            j1 += 1

        if self.gameMap[j][i] in self.red:
            self.appraise_red(i, j)
        if self.gameMap[j][i] in self.white:
            self.appraise_white(i, j)
        if self.gameMap[j][i] in self.dot:
            self.appraise_dot(i, j)
        if self.gameMap[j][i] in self.ring:
            self.appraise_ring(i, j)

        if self.gameMap[j1][i1] in self.red:
            self.appraise_red(i1, j1)
        if self.gameMap[j1][i1] in self.white:
            self.appraise_white(i1, j1)
        if self.gameMap[j1][i1] in self.dot:
            self.appraise_dot(i1, j1)
        if self.gameMap[j1][i1] in self.ring:
            self.appraise_ring(i1, j1)

    def appraise_red(self, i, j):
        for step in range(4):
            self.gameMap_red[j + step][i] += price_red
            self.gameMap_red[j - step][i] += price_red
            self.gameMap_red[j][i + step] += price_red
            self.gameMap_red[j][i - step] += price_red

            self.gameMap_red[j + step][i + step] += price_red
            self.gameMap_red[j - step][i - step] += price_red
            self.gameMap_red[j + step][i - step] += price_red
            self.gameMap_red[j - step][i + step] += price_red

        pass

    def appraise_white(self, i, j):
        for step in range(4):
            self.gameMap_white[j + step][i] += price_white
            self.gameMap_white[j - step][i] += price_white
            self.gameMap_white[j][i + step] += price_white
            self.gameMap_white[j][i - step] += price_white

            self.gameMap_white[j + step][i + step] += price_white
            self.gameMap_white[j - step][i - step] += price_white
            self.gameMap_white[j + step][i - step] += price_white
            self.gameMap_white[j - step][i + step] += price_white
        pass

    def appraise_dot(self, i, j):
        for step in range(4):
            self.gameMap_dot[j + step][i] += price_dot
            self.gameMap_dot[j - step][i] += price_dot
            self.gameMap_dot[j][i + step] += price_dot
            self.gameMap_dot[j][i - step] += price_dot

            self.gameMap_dot[j + step][i + step] += price_dot
            self.gameMap_dot[j - step][i - step] += price_dot
            self.gameMap_dot[j + step][i - step] += price_dot
            self.gameMap_dot[j - step][i + step] += price_dot
        pass

    def appraise_ring(self, i, j):
        for step in range(4):
            self.gameMap_ring[j + step][i] += price_ring
            self.gameMap_ring[j - step][i] += price_ring
            self.gameMap_ring[j][i + step] += price_ring
            self.gameMap_ring[j][i - step] += price_ring

            self.gameMap_ring[j + step][i + step] += price_ring
            self.gameMap_ring[j - step][i - step] += price_ring
            self.gameMap_ring[j + step][i - step] += price_ring
            self.gameMap_ring[j - step][i + step] += price_ring
        pass

    @property
    def getRed(self):
        return self.gameMap_red

    def getWhite(self):
        return self.gameMap_white

    def getDot(self):
        return self.gameMap_dot

    def getRing(self):
        return self.gameMap_ring
