import numpy

#price = [0, 1, 1, 2, 3, 5]

price = [0, 1, 2, 3, 5, 8]

class Appraiser:
    def __init__(self):
        pass

    red = [1, 3]
    white = [2, 4]
    dot = [1, 4]
    ring = [2, 3]

    targetList = []

    # appraise how how card will affect gameMap
    def appraise(self, move, valueMap, gameMap):
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

        valueMap[j][i].occupied = 1
        valueMap[j1][i1].occupied = 1

        if gameMap[j][i] in self.red:
            self.appraiseRed(i, j, valueMap, gameMap)
        if gameMap[j][i] in self.white:
            self.appraise_white(i, j, valueMap, gameMap)
        if gameMap[j][i] in self.dot:
            self.appraise_dot(i, j, valueMap, gameMap)
        if gameMap[j][i] in self.ring:
            self.appraise_ring(i, j, valueMap, gameMap)

        if gameMap[j1][i1] in self.red:
            self.appraiseRed(i1, j1, valueMap, gameMap)
        if gameMap[j1][i1] in self.white:
            self.appraise_white(i1, j1, valueMap, gameMap)
        if gameMap[j1][i1] in self.dot:
            self.appraise_dot(i1, j1, valueMap, gameMap)
        if gameMap[j1][i1] in self.ring:
            self.appraise_ring(i1, j1, valueMap, gameMap)

        if remove:
            i = move.sourceCoordinate1Let - 1
            j = move.sourceCoordinate1Num - 1
            i1 = move.sourceCoordinate2Let - 1
            j1 = move.sourceCoordinate2Num -1
            if gameMap[j][i] in self.red:
                self.appraiseRedRemove(i, j, valueMap, gameMap)
            if gameMap[j][i] in self.white:
                self.appraise_white(i, j, valueMap, gameMap)
            if gameMap[j][i] in self.dot:
                self.appraise_dot(i, j, valueMap, gameMap)
            if gameMap[j][i] in self.ring:
                self.appraise_ring(i, j, valueMap, gameMap)

            if gameMap[j1][i1] in self.red:
                self.appraiseRed(i1, j1, valueMap, gameMap)
            if gameMap[j1][i1] in self.white:
                self.appraise_white(i1, j1, valueMap, gameMap)
            if gameMap[j1][i1] in self.dot:
                self.appraise_dot(i1, j1, valueMap, gameMap)
            if gameMap[j1][i1] in self.ring:
                self.appraise_ring(i1, j1, valueMap, gameMap)

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

    def getScore(self, valueMap, gameMap):
        sumRed = 0
        sumWhite = 0
        sumRing = 0
        sumDot = 0
        for i in range(8):
            for j in range(12):
                sumRed += valueMap[j][i].redWeight
                sumWhite += valueMap[j][i].whiteWeight
                sumRing += valueMap[j][i].ringWeight
                sumDot += valueMap[j][i].dotWeight

        return max(sumRing, sumDot) - max(sumRed, sumWhite)

    def setInitialValue(self, valueMap):
        valueMap[0][3].redWeight = 1
        valueMap[0][3].whiteWeight = 1
        valueMap[0][3].dotWeight = 1
        valueMap[0][3].ringWeight = 1

        valueMap[0][4].redWeight = 1
        valueMap[0][4].whiteWeight = 1
        valueMap[0][4].dotWeight = 1
        valueMap[0][4].ringWeight = 1
