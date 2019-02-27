import numpy
from cell import Cell

price: int = 10

priceing_blocked = -1000;

letterToNumb = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8

}
# convert numbers to letters
numbToLetter = dict([[v, k] for k, v in letterToNumb.items()])


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

        if move.type == 1:
            valueMap[move.sourceCoordinate1Num - 1][move.sourceCoordinate1Let - 1].occupied = 0
            valueMap[move.sourceCoordinate2Num - 1][move.sourceCoordinate2Let - 1].occupied = 0

        if gameMap[j][i] in self.red:
            self.appraise_red(i, j, valueMap, gameMap)
        if gameMap[j][i] in self.white:
            self.appraise_white(i, j, valueMap, gameMap)
        if gameMap[j][i] in self.dot:
            self.appraise_dot(i, j, valueMap, gameMap)
        if gameMap[j][i] in self.ring:
            self.appraise_ring(i, j, valueMap, gameMap)

        if gameMap[j1][i1] in self.red:
            self.appraise_red(i1, j1, valueMap, gameMap)
        if gameMap[j1][i1] in self.white:
            self.appraise_white(i1, j1, valueMap, gameMap)
        if gameMap[j1][i1] in self.dot:
            self.appraise_dot(i1, j1, valueMap, gameMap)
        if gameMap[j1][i1] in self.ring:
            self.appraise_ring(i1, j1, valueMap, gameMap)

        self.targetList.clear()
        for j in range(12):
            for i in range(8):
                if self.isTargeted(i, j, gameMap) and valueMap[j][i].occupied == 0:
                    self.targetList.append(valueMap[j][i])

    # look for next 4 fields to see if there is possibility of creating 4 in a row
    def isHorizontalWindowFree(self, i, j, self_color, gameMap):
        rate = 0
        if i > 3:
            return 0
        for step in range(4):
            if step + i < 8:
                if not (gameMap[j][i + step] in self_color or gameMap[j][i + step] == 0):
                    return 0
                elif gameMap[j][i + step] in self_color:
                    rate += 1
            else:
                return 0
            if rate == 3:
                return 10
        return rate

    def isVerticalWindowFree(self, i, j, self_color, gameMap):
        rate = 0
        if j > 8:
            return 0
        for step in range(4):
            if step + j < 12:
                if not (gameMap[j + step][i] in self_color or gameMap[j + step][i] == 0):
                    return 0
                elif gameMap[j + step][i] in self_color:
                    rate += 1
            else:
                return 0
            if rate == 3:
                return 10
        return rate

    def isUpDiagonalWindowFree(self, i, j, self_color, gameMap):
        rate = 0
        if i > 3 or j > 8:
            return 0
        for step in range(4):
            if step + j < 12 and step + i < 8:
                if not (gameMap[j + step][i + step] in self_color or gameMap[j + step][i + step] == 0):
                    return 0
                elif gameMap[j + step][i + step] in self_color:
                    rate += 1
            else:
                return 0
            if rate == 3:
                return 10
        return rate

    def isDownDiagonalWindowFree(self, i, j, self_color, gameMap):
        rate = 0
        if i < 3 or j > 8:
            return 0
        for step in range(4):
            if j - step >= 0 and step + i < 8:
                if not (gameMap[j - step][i + step] in self_color or gameMap[j - step][i + step] == 0):
                    return 0
                elif gameMap[j - step][i + step] in self_color:
                    rate += 1
            else:
                return 0
            if rate == 3:
                return 10
        return rate

    # not used for now
    # def moveBlocking(self, i, j, color_or_dot):
    #     tmp = self.getCorrectMap(color_or_dot)
    #
    #     if self.isBlockingVertical(i, j, color_or_dot) == 3:
    #         print("Vertical is blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j + step < 12:
    #                 tmp[j + step][i] += priceing_blocked
    #             if j - step >= 0:
    #                 tmp[j - step][i] += priceing_blocked
    #     if self.isBlockingVertical(i, j, color_or_dot) == 2:
    #         print("Vertical is down blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j - step >= 0:
    #                 tmp[j - step][i] += priceing_blocked
    #     if self.isBlockingVertical(i, j, color_or_dot) == 1:
    #         print("Vertical is up blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j + step < 12:
    #                 tmp[j + step][i] += priceing_blocked
    #
    #     if self.isBlockingHorizontal(i, j, color_or_dot) == 3:
    #         print("Horizontal is blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if i + step < 8:
    #                 tmp[j][i + step] += priceing_blocked
    #             if i - step >= 0:
    #                 tmp[j][i - step] += priceing_blocked
    #     if self.isBlockingHorizontal(i, j, color_or_dot) == 2:
    #         print("Horizontal is left blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if i - step >= 0:
    #                 tmp[j][i - step] += priceing_blocked
    #     if self.isBlockingHorizontal(i, j, color_or_dot) == 1:
    #         print("Horizontal is right blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if i + step < 8:
    #                 tmp[j][i + step] += priceing_blocked
    #
    #     if self.isBlockingLeftDiagonal(i, j, color_or_dot) == 3:
    #         print("Left Diagonal is blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j + step < 12 and i - step >= 0:
    #                 tmp[j + step][i - step] += priceing_blocked
    #             if j - step >= 0 and i + step < 8:
    #                 tmp[j - step][i + step] += priceing_blocked
    #     if self.isBlockingLeftDiagonal(i, j, color_or_dot) == 2:
    #         print("Left Diagonal is left blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j + step < 12 and i - step >= 0:
    #                 tmp[j + step][i - step] += priceing_blocked
    #     if self.isBlockingLeftDiagonal(i, j, color_or_dot) == 1:
    #         print("Left Diagonal is right blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j - step >= 0 and i + step < 8:
    #                 tmp[j - step][i + step] += priceing_blocked
    #
    #     if self.isBlockingRightDiagonal(i, j, color_or_dot) == 3:
    #         print("Right Diagonal is blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j + step < 12 and i + step < 8:
    #                 tmp[j + step][i + step] += priceing_blocked
    #             if j - step >= 0 and i - step >= 0:
    #                 tmp[j - step][i - step] += priceing_blocked
    #     if self.isBlockingRightDiagonal(i, j, color_or_dot) == 2:
    #         print("Right Diagonal is left blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j - step >= 0 and i - step >= 0:
    #                 tmp[j - step][i - step] += priceing_blocked
    #     if self.isBlockingRightDiagonal(i, j, color_or_dot) == 1:
    #         print("Right Diagonal is right blocked for " + str(i) + " " + str(j))
    #         for step in range(1, 5):
    #             if j + step < 12 and i + step < 8:
    #                 tmp[j + step][i + step] += priceing_blocked
    #     pass
    #
    # def getCorrectMap(self, color_or_dot):
    #     if color_or_dot == self.red:
    #         return gameMap_red
    #     elif color_or_dot == self.white:
    #         return gameMap_white
    #     elif color_or_dot == self.dot:
    #         return gameMap_dot
    #     elif color_or_dot == self.ring:
    #         return gameMap_ring
    #     else:
    #         print("non found")
    #         return None
    #
    # # return 0 for not blocking from both sides
    # # return 1 for blocking right
    # # return 2 for blocking left
    # # return 3 for blocking left and right
    # def isBlockingVertical(self, i, j, opposite_color_or_dot):
    #     free_r = 0
    #     free_l = 0
    #     for step in range(1, 5):
    #         if j + step < 12:
    #             if gameMap[j + step][i] in opposite_color_or_dot or gameMap[j + step][i] == 0:
    #                 free_r += 1
    #             else:
    #                 break
    #     for step in range(1, 5):
    #         if j - step >= 0:
    #             if gameMap[j - step][i] in opposite_color_or_dot or gameMap[j - step][i] == 0:
    #                 free_l += 1
    #             else:
    #                 break
    #     out = 0
    #     if free_r < 3:
    #         out += 1
    #     if free_l < 3:
    #         out += 2
    #     return out
    #
    # def isBlockingHorizontal(self, i, j, opposite_color_or_dot):
    #     free_r = 0
    #     free_l = 0
    #     for step in range(1, 5):
    #         if i + step < 7:
    #             if gameMap[j][i + step] in opposite_color_or_dot or gameMap[j][i + step] == 0:
    #                 free_r += 1
    #             else:
    #                 break
    #
    #     for step in range(1, 5):
    #         if i - step >= 0:
    #             if gameMap[j][i - step] in opposite_color_or_dot or gameMap[j][i - step] == 0:
    #                 free_l += 1
    #             else:
    #                 break
    #     out = 0
    #     if free_r < 3:
    #         out += 1
    #     if free_l < 3:
    #         out += 2
    #     return out
    #
    # def isBlockingRightDiagonal(self, i, j, opposite_color_or_dot):
    #     free_r = 0
    #     free_l = 0
    #     for step in range(1, 5):
    #         if j + step < 12 and i + step < 8:
    #             if gameMap[j + step][i + step] in opposite_color_or_dot or gameMap[j + step][i + step] == 0:
    #                 free_r += 1
    #             else:
    #                 break
    #     for step in range(1, 5):
    #         if j - step >= 0 and i - step >= 0:
    #             if gameMap[j - step][i - step] in opposite_color_or_dot or gameMap[j - step][i - step] == 0:
    #                 free_l += 1
    #             else:
    #                 break
    #     out = 0
    #     if free_r < 3:
    #         out += 1
    #     if free_l < 3:
    #         out += 2
    #     return out
    #
    # def isBlockingLeftDiagonal(self, i, j, opposite_color_or_dot):
    #     free_r = 0
    #     free_l = 0
    #     for step in range(1, 5):
    #         if j - step >= 0 and i + step < 8:
    #             if gameMap[j - step][i + step] in opposite_color_or_dot or gameMap[j - step][i + step] == 0:
    #                 free_r += 1
    #             else:
    #                 break
    #     for step in range(1, 5):
    #         if j + step < 12 and i - step >= 0:
    #             if gameMap[j + step][i - step] in opposite_color_or_dot or gameMap[j + step][i - step] == 0:
    #                 free_l += 1
    #             else:
    #                 break
    #     out = 0
    #     if free_r < 3:
    #         out += 1
    #     if free_l < 3:
    #         out += 2
    #     return out

    # check and apply the weight on the window of 4 elements if there is possibility of creating 4 in a row
    # total fields check is 7
    def appraise_red(self, i, j, valueMap, gameMap):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                            valueMap[j][i - step + k].redWeight += price * rate
        for step in range(4):
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j - step + k][i].redWeight += price * rate
        for step in range(4):
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j + step - k][i - step + k].redWeight += price * rate
        for step in range(4):
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.red, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j - step + k][i - step + k].redWeight += price * rate
        # for step in range(1, 4):
        #     if j + step < 12:
        #         gameMap_red[j + step][i] += price        #     if j - step >= 0:
        #         gameMap_red[j - step][i] += price        #     if i + step < 8:
        #         gameMap_red[j][i + step] += price        #     if i - step >= 0:
        #         gameMap_red[j][i - step] += price        #     if j + step < 12 and i + step < 8:
        #         gameMap_red[j + step][i + step] += price        #     if j - step >= 0 and i - step >= 0:
        #         gameMap_red[j - step][i - step] += price        #     if j + step < 12 and i - step >= 0:
        #         gameMap_red[j + step][i - step] += price        #     if j - step >= 0 and i + step < 8:
        #         gameMap_red[j - step][i + step] += price        pass

    def appraise_white(self, i, j, valueMap, gameMap):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.white, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j][i - step + k].whiteWeight += price * rate
        for step in range(4):
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.white, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j - step + k][i].whiteWeight += price * rate
        for step in range(4):
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.white, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j + step - k][i - step + k].whiteWeight += price * rate
        for step in range(4):
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.white, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j - step + k][i - step + k].whiteWeight += price * rate
        # for step in range(1, 4):
        #     if j + step < 12:
        #         gameMap_white[j + step][i] += price
        #     if j - step >= 0:
        #         gameMap_white[j - step][i] += price
        #     if i + step < 8:
        #         gameMap_white[j][i + step] += price
        #     if i - step >= 0:
        #         gameMap_white[j][i - step] += price
        #     if j + step < 12 and i + step < 8:
        #         gameMap_white[j + step][i + step] += price
        #     if j - step >= 0 and i - step >= 0:
        #         gameMap_white[j - step][i - step] += price
        #     if j + step < 12 and i - step >= 0:
        #         gameMap_white[j + step][i - step] += price
        #     if j - step >= 0 and i + step < 8:
        #         gameMap_white[j - step][i + step] += price
        pass

    def appraise_dot(self, i, j, valueMap, gameMap):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.dot, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j][i - step + k].dotWeight += price * rate
        for step in range(4):
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.dot, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j - step + k][i].dotWeight += price * rate
        for step in range(4):
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.dot, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j + step - k][i - step + k].dotWeight += price * rate
        for step in range(4):
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.dot, gameMap)
                if rate > 0:
                    for k in range(4):
                        valueMap[j - step + k][i - step + k].dotWeight += price * rate
        # for step in range(1, 4):
        #     if j + step < 12:
        #         gameMap_dot[j + step][i] += price        #     if j - step >= 0:
        #         gameMap_dot[j - step][i] += price        #     if i + step < 8:
        #         gameMap_dot[j][i + step] += price        #     if i - step >= 0:
        #         gameMap_dot[j][i - step] += price        #     if j + step < 12 and i + step < 8:
        #         gameMap_dot[j + step][i + step] += price        #     if j - step >= 0 and i - step >= 0:
        #         gameMap_dot[j - step][i - step] += price        #     if j + step < 12 and i - step >= 0:
        #         gameMap_dot[j + step][i - step] += price        #     if j - step >= 0 and i + step < 8:
        #         gameMap_dot[j - step][i + step] += price        pass

    def appraise_ring(self, i, j, valueMap, gameMap):
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, self.ring, gameMap)
                if rate > 0:
                    for k in range(4):
                        # gameMap_ring[j][i - step + k] += price
                        valueMap[j][i - step + k].ringWeight += price * rate
        for step in range(4):
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, self.ring, gameMap)
                if rate > 0:
                    for k in range(4):
                        # gameMap_ring[j - step + k][i] += price
                        valueMap[j - step + k][i].ringWeight += price * rate
        for step in range(4):
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, self.ring, gameMap)
                if rate > 0:
                    for k in range(4):
                        # gameMap_ring[j + step - k][i - step + k] += price
                        valueMap[j + step - k][i - step + k].ringWeight += price * rate
        for step in range(4):
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, self.ring, gameMap)
                if rate > 0:
                    for k in range(4):
                        # gameMap_ring[j - step + k][i - step + k] += price
                        valueMap[j - step + k][i - step + k].ringWeight += price * rate
        # for step in range(1, 4):
        #     if j + step < 12:
        #         gameMap_ring[j + step][i] += price
        #     if j - step >= 0:
        #         gameMap_ring[j - step][i] += price
        #     if i + step < 8:
        #         gameMap_ring[j][i + step] += price
        #     if i - step >= 0:
        #         gameMap_ring[j][i - step] += price
        #     if j + step < 12 and i + step < 8:
        #         gameMap_ring[j + step][i + step] += price
        #     if j - step >= 0 and i - step >= 0:
        #         gameMap_ring[j - step][i - step] += price
        #     if j + step < 12 and i - step >= 0:
        #         gameMap_ring[j + step][i - step] += price
        #     if j - step >= 0 and i + step < 8:
        #         gameMap_ring[j - step][i + step] += price
        pass

    # returns coordinate with non zero weight and free on the gameMap
    def getAvailableMoves(self, colorMap, maxMoves, gameMap):
        aveMoves = {}
        max = 0
        for i in range(8):
            for j in range(12):
                if colorMap[j][i] > 0 and gameMap[j][i] == 0 and self.isTargeted(i, j, gameMap):
                    # print(numbToLetter.get(i+1)+str(j+1)+": "+str(colorMap[j][i]))
                    aveMoves[numbToLetter.get(i + 1) + str(j + 1)] = colorMap[j][i]
                    if colorMap[j][i] > max:
                        max = colorMap[j][i]

        for m in aveMoves.keys():
            if abs(aveMoves.get(m) - max) <= price:
                maxMoves[m] = aveMoves.get(m)
        return max

    def isTargeted(self, i, j, gameMap):
        if gameMap[j - 1][i] != 0 or gameMap[j - 2][i] != 0 or j == 0 or j - 1 == 0:
            return True
        else:
            return False

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

    def getScoreDots(self, valueMap, gameMap):
        tmp = {}
        return max(self.getAvailableMoves(self.getDotMap(valueMap), tmp, gameMap),
                   self.getAvailableMoves(self.getRingMap(valueMap), tmp, gameMap)) - self.getAvgColors(valueMap)

    def getScoreColors(self, valueMap, gameMap):
        tmp = {}
        return max(self.getAvailableMoves(self.getRedMap(valueMap), tmp, gameMap),
                   self.getAvailableMoves(self.getWhiteMap(valueMap), tmp, gameMap)) - self.getAvgDots(valueMap)

    def getAvgColors(self, valueMap):
        count = 0
        sumWeights = 0
        for i in range(8):
            for j in range(12):
                if valueMap[j][i].redWeight != 0:
                    count += 1
                    sumWeights += valueMap[j][i].redWeight
                if valueMap[j][i].whiteWeight != 0:
                    count += 1
                    sumWeights += valueMap[j][i].whiteWeight
        if count == 0:
            return 0
        return sumWeights / count

    def getAvgDots(self, valueMap):
        count = 0
        sumWeights = 0
        for i in range(8):
            for j in range(12):
                if valueMap[j][i].ringWeight != 0:
                    count += 1
                    sumWeights += valueMap[j][i].ringWeight
                if valueMap[j][i].dotWeight != 0:
                    count += 1
                    sumWeights += valueMap[j][i].dotWeight
        if count == 0:
            return 0
        return sumWeights / count

    def setInitialValue(self, valueMap):
        valueMap[0][3].redWeight = 1
        valueMap[0][3].whiteWeight = 1
        valueMap[0][3].dotWeight = 1
        valueMap[0][3].ringWeight = 1

        valueMap[0][4].redWeight = 1
        valueMap[0][4].whiteWeight = 1
        valueMap[0][4].dotWeight = 1
        valueMap[0][4].ringWeight = 1
