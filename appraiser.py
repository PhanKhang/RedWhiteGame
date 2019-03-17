import numpy
# price = [21, 34, 55, 89, 144]
price = [1, 2, 3, 5, 8]

class Appraiser:
    def __init__(self):
        pass

    red = [1, 3]
    white = [2, 4]
    dot = [1, 4]
    ring = [2, 3]

    targetList = []

    # appraise how how card will affect gameMap
    def appraise(self, move, valueMapRed, valueMapWhite, valueMapRing, valueMapDot , gameMap):
        remove = False
        if move.type == 1:
            remove = True

        i = int(move.targetCoordinateLet) - 1
        j = move.targetCoordinateNum - 1
        i1 = i
        j1 = j

        if move.rotation % 2 != 0:
            i1 += 1
        else:
            j1 += 1

        if gameMap[j][i] in self.red:
            self.appraiseMove(i, j, valueMapRed, gameMap, self.red)
        if gameMap[j][i] in self.white:
            self.appraiseMove(i, j, valueMapWhite, gameMap, self.white)
        if gameMap[j][i] in self.dot:
            self.appraiseMove(i, j, valueMapDot, gameMap, self.dot)
        if gameMap[j][i] in self.ring:
            self.appraiseMove(i, j, valueMapRing, gameMap, self.ring)

        if gameMap[j1][i1] in self.red:
            self.appraiseMove(i1, j1, valueMapRed, gameMap, self.red)
        if gameMap[j1][i1] in self.white:
            self.appraiseMove(i1, j1, valueMapWhite, gameMap, self.white)
        if gameMap[j1][i1] in self.dot:
            self.appraiseMove(i1, j1, valueMapDot, gameMap, self.dot)
        if gameMap[j1][i1] in self.ring:
            self.appraiseMove(i1, j1, valueMapRing, gameMap, self.ring)

        # if move.type == 1:
        #     valueMap[move.sourceCoordinate1Num - 1][move.sourceCoordinate1Let - 1].occupied = 0
        #     valueMap[move.sourceCoordinate2Num - 1][move.sourceCoordinate2Let - 1].occupied = 0

    # look for next 4 fields to see if there is possibility of creating 4 in a row
    def isHorizontalWindowFree(self, i, j, self_color, gameMap):
        rate = 0
        if i + 3 > 7:
            return 0
        for step in range(4):
            if step + i < 8:
                if not (gameMap[j][i + step] in self_color or gameMap[j][i + step] == 0):
                    return 0
                elif gameMap[j][i + step] in self_color:
                    rate += 1
            else:
                return 0
        return rate

    def isVerticalWindowFree(self, i, j, self_color, gameMap):
        rate = 0
        if j + 3 > 11:
            return 0
        for step in range(4):
            if step + j < 12:
                if not (gameMap[j + step][i] in self_color or gameMap[j + step][i] == 0):
                    return 0
                elif gameMap[j + step][i] in self_color:
                    rate += 1
            else:
                return 0
        return rate

    def isUpDiagonalWindowFree(self, i, j, self_color, gameMap):
        rate = 0
        if i + 3 > 7 or j + 3 > 11:
            return 0
        for step in range(4):
            if step + j < 12 and step + i < 8:
                if not (gameMap[j + step][i + step] in self_color or gameMap[j + step][i + step] == 0):
                    return 0
                elif gameMap[j + step][i + step] in self_color:
                    rate += 1
            else:
                return 0
        return rate

    def isDownDiagonalWindowFree(self, i, j, self_color, gameMap):
        rate = 0
        if i + 3 > 7 or j - 3 < 0:
            return 0
        for step in range(4):
            if j - step >= 0 and step + i < 8:
                if not (gameMap[j - step][i + step] in self_color or gameMap[j - step][i + step] == 0):
                    return 0
                elif gameMap[j - step][i + step] in self_color:
                    rate += 1
            else:
                return 0
        return rate

    def appraiseMove(self, i, j, valueMap, gameMap, colorOrDot):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, colorOrDot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k] < price[rate] and gameMap[j][i - step + k] != 0:
                            valueMap[j][i - step + k] = price[rate]
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, colorOrDot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i] < price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i] = price[rate]
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, colorOrDot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k] < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k] = price[rate]
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, colorOrDot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k] < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k] = price[rate]


    # check and apply the weight on the window of 4 elements if there is possibility of creating 4 in a row
    # total fields check is 7
    def appraiseRed(self, i, j, valueMap, gameMap):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k].redWeight < price[rate] and gameMap[j][i - step + k] != 0:
                            valueMap[j][i - step + k].redWeight = price[rate]
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i].redWeight < price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i].redWeight = price[rate]
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k].redWeight < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k].redWeight = price[rate]
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k].redWeight < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k].redWeight = price[rate]

    def appraiseRedRemove(self, i, j, valueMap, gameMap):
        valueMap[j][i].redWeight = 0
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k].redWeight > price[rate] and gameMap[j][i - step + k] != 0:
                            valueMap[j][i - step + k].redWeight = price[rate]
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i].redWeight > price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i].redWeight = price[rate]
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k].redWeight > price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k].redWeight = price[rate]
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k].redWeight > price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k].redWeight = price[rate]

    def appraise_white(self, i, j, valueMap, gameMap):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.white, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k].whiteWeight < price[rate] and gameMap[j][i - step + k] != 0:
                            valueMap[j][i - step + k].whiteWeight = price[rate]
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.white, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i].whiteWeight < price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i].whiteWeight = price[rate]
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.white, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k].whiteWeight < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k].whiteWeight = price[rate]
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.white, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k].whiteWeight < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k].whiteWeight = price[rate]

    def appraise_dot(self, i, j, valueMap, gameMap):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.dot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k].dotWeight < price[rate] and gameMap[j][i - step + k] != 0:
                            valueMap[j][i - step + k].dotWeight = price[rate]
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.dot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i].dotWeight < price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i].dotWeight = price[rate]
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.dot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k].dotWeight < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k].dotWeight = price[rate]
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.dot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k].dotWeight < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k].dotWeight = price[rate]

    def appraise_ring(self, i, j, valueMap, gameMap):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.ring, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k].ringWeight < price[rate] and gameMap[j][i - step + k] != 0:
                            valueMap[j][i - step + k].ringWeight = price[rate]
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.ring, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i].ringWeight < price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i].ringWeight = price[rate]
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.ring, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k].ringWeight < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k].ringWeight = price[rate]
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.ring, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k].ringWeight < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k].ringWeight = price[rate]

    # returns coordinate with non zero weight and free on the gameMap
    def getRedMap(self, valueMap):
        Matrix = numpy.zeros((12, 8))
        for j in range(12):
            for i in range(8):
                Matrix[j][i] = valueMap[j][i].redWeight
        return Matrix

    def getWhiteMap(self, valueMap):
        Matrix = numpy.zeros((12, 8))
        for j in range(12):
            for i in range(8):
                Matrix[j][i] = valueMap[j][i].whiteWeight
        return Matrix

    def getDotMap(self, valueMap):
        Matrix = numpy.zeros((12, 8))
        for j in range(12):
            for i in range(8):
                Matrix[j][i] = valueMap[j][i].dotWeight
        return Matrix

    def getRingMap(self, valueMap):
        Matrix = numpy.zeros((12, 8))
        for j in range(12):
            for i in range(8):
                Matrix[j][i] = valueMap[j][i].ringWeight
        return Matrix

    def getScore(self, valueMapRed, valueMapWhite, valueMapRing, valueMapDot, party):
        sumRed = 0
        sumWhite = 0
        sumRing = 0
        sumDot = 0

        if party == 0:
            for i in range(8):
                for j in range(12):
                    redWeight = valueMapRed[j][i]
                    whiteWeight = valueMapWhite[j][i]
                    ringWeight = valueMapRing[j][i]
                    dotWeight = valueMapDot[j][i]

                    if ringWeight >= price[3] or dotWeight >= price[3]:
                        ringWeight *= 10
                        dotWeight *= 10

                    if ringWeight >= price[4] or dotWeight >= price[4]:
                        ringWeight *= 10
                        dotWeight *= 10

                    if i > 0:
                        if valueMapRed[j][i-1] != 0 and valueMapRed[j][i] == 0:
                            sumRed -= 1
                        if valueMapWhite[j][i-1] != 0 and valueMapWhite[j][i] == 0:
                            sumWhite -= 1
                        if valueMapRing[j][i-1] != 0 and valueMapRing[j][i] == 0:
                            sumRing -= 1
                        if valueMapDot[j][i-1] != 0 and valueMapDot[j][i] == 0:
                            sumDot -= 1

                    sumRed += redWeight
                    sumWhite += whiteWeight
                    sumRing += ringWeight
                    sumDot += dotWeight
        else:
            for i in range(8):
                for j in range(12):
                    redWeight = valueMapRed[j][i]
                    whiteWeight = valueMapWhite[j][i]
                    ringWeight = valueMapRing[j][i]
                    dotWeight = valueMapDot[j][i]

                    if redWeight >= price[3] or whiteWeight >= price[3]:
                        whiteWeight *= 10
                        redWeight *= 10

                    if redWeight >= price[4] or whiteWeight >= price[4]:
                        whiteWeight *= 10
                        redWeight *= 10

                    if i > 0:
                        if valueMapRed[j][i-1] != 0 and valueMapRed[j][i] == 0:
                            sumRed -= 1
                        if valueMapWhite[j][i-1] != 0 and valueMapWhite[j][i] == 0:
                            sumWhite -= 1
                        if valueMapRing[j][i-1] != 0 and valueMapRing[j][i] == 0:
                            sumRing -= 1
                        if valueMapDot[j][i-1] != 0 and valueMapDot[j][i] == 0:
                            sumDot -= 1

                    sumRed += redWeight
                    sumWhite += whiteWeight
                    sumRing += ringWeight
                    sumDot += dotWeight

        return max(sumRing, sumDot) - max(sumRed, sumWhite)


    def applyMatrix(self, valueMap, i,j):
        if valueMap[j + 1][i] > 0 and j < 11:
            valueMap[j + 1][i] += 1

        if valueMap[j][i + 1] > 0 and i < 7:
            valueMap[j][i + 1] += 1

        if valueMap[j + 1][i + 1] > 0 and j < 11 and i < 7:
            valueMap[j + 1][i + 1] += 1

        if valueMap[j - 1][i] > 0 and j >= 0:
            valueMap[j - 1][i] += 1

        if valueMap[j][i - 1].redWeight > 0 and i >= 0:
            valueMap[j][i - 1].redWeight += 1

        if valueMap[j - 1][i + 1].redWeight > 0 and j >= 0 and i < 7:
            valueMap[j - 1][i + 1].redWeight += 1

        if valueMap[j + 1][i - 1] > 0 and j < 11 and i >= 0:
            valueMap[j + 1][i - 1] += 1
