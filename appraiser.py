import numpy
# price = [21, 34, 55, 89, 144]
price = [2, 3, 5, 8, 13, 21]

class Appraiser:
    def __init__(self):
        pass

    red = [1, 3]
    white = [2, 4]
    dot = [1, 4]
    ring = [2, 3]

    targetList = []

    # appraise how how card will affect gameMap
    def appraise(self, move, valueMapRed, valueMapWhite, valueMapRing, valueMapDot , gameMap, party):
        winC = False
        winD = False
        if move.type == 1:
            print("triggered")
            ir = move.sourceCoordinate1Let - 1
            jr = move.sourceCoordinate1Num - 1
            ir1 = move.sourceCoordinate2Let - 1
            jr1 = move.sourceCoordinate2Num - 1
            if gameMap[jr][ir] in self.red:
                self.appraiseRecycleMove(ir, jr, valueMapRed, gameMap, self.red)
            if gameMap[jr][ir] in self.white:
                self.appraiseRecycleMove(ir, jr, valueMapWhite, gameMap, self.white)
            if gameMap[jr][ir] in self.dot:
                self.appraiseRecycleMove(ir, jr, valueMapDot, gameMap, self.dot)
            if gameMap[jr][ir] in self.ring:
                self.appraiseRecycleMove(ir, jr, valueMapRing, gameMap, self.ring)

            if gameMap[jr1][ir1] in self.red:
                self.appraiseRecycleMove(ir1, jr1, valueMapRed, gameMap, self.red)
            if gameMap[jr1][ir1] in self.white:
                self.appraiseRecycleMove(ir1, jr1, valueMapWhite, gameMap, self.white)
            if gameMap[jr1][ir1] in self.dot:
                self.appraiseRecycleMove(ir1, jr1, valueMapDot, gameMap, self.dot)
            if gameMap[jr1][ir1] in self.ring:
                self.appraiseRecycleMove(ir1, jr1, valueMapRing, gameMap, self.ring)

        i = move.targetCoordinateLet - 1
        j = move.targetCoordinateNum - 1
        i1 = i
        j1 = j

        if move.rotation % 2 != 0:
            i1 += 1
        else:
            j1 += 1

        if gameMap[j][i] in self.red:
            if self.appraiseMove(i, j, valueMapRed, gameMap, self.red):
                winC = True
        if gameMap[j][i] in self.white:
            if self.appraiseMove(i, j, valueMapWhite, gameMap, self.white):
                winC = True
        if gameMap[j][i] in self.dot:
            if self.appraiseMove(i, j, valueMapDot, gameMap, self.dot):
                winD = True
        if gameMap[j][i] in self.ring:
            if self.appraiseMove(i, j, valueMapRing, gameMap, self.ring):
                winD = True

        if gameMap[j1][i1] in self.red:
            if self.appraiseMove(i1, j1, valueMapRed, gameMap, self.red):
                winC = True
        if gameMap[j1][i1] in self.white:
            if self.appraiseMove(i1, j1, valueMapWhite, gameMap, self.white):
                winC = True
        if gameMap[j1][i1] in self.dot:
            if self.appraiseMove(i1, j1, valueMapDot, gameMap, self.dot):
                winD = True
        if gameMap[j1][i1] in self.ring:
            if self.appraiseMove(i1, j1, valueMapRing, gameMap, self.ring):
                winD = True

        # if party == 0:
        #     self.applyMatrix(valueMapDot, i, j)
        #     self.applyMatrix(valueMapRing, i, j)
        #     self.applyMatrix(valueMapDot, i1, j1)
        #     self.applyMatrix(valueMapRing, i1, j1)
        # else:
        #     self.applyMatrix(valueMapWhite, i, j)
        #     self.applyMatrix(valueMapRed, i, j)
        #     self.applyMatrix(valueMapWhite, i1, j1)
        #     self.applyMatrix(valueMapRed, i1, j1)

        if winD and winC:
            return "winDC"
        elif winD:
            return "winD"
        elif winC:
            return "winC"
        else:
            return "go"

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
        win = False
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k] < price[rate]+1 and gameMap[j][i - step + k] != 0: #here
                            valueMap[j][i - step + k] = price[rate]+1
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i] < price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i] = price[rate]
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k] < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k] = price[rate]
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k] < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k] = price[rate]
        return win

    def appraiseRecycleMove(self, i, j, valueMap, gameMap, colorOrDot):
        valueMap[j][i] = 0
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, colorOrDot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k] > price[rate]+1 and gameMap[j][i - step + k] != 0: #here
                            valueMap[j][i - step + k] = price[rate]+1
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, colorOrDot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i] > price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i] = price[rate]
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, colorOrDot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k] > price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k] = price[rate]
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, colorOrDot, gameMap)
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k] > price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k] = price[rate]


    # check and apply the weight on the window of 4 elements if there is possibility of creating 4 in a row
    # total fields check is 7
    def getScore(self, valueMapRed, valueMapWhite, valueMapRing, valueMapDot, party, goalState):
        sumRed = 0
        sumWhite = 0
        sumRing = 0
        sumDot = 0

        if party == 0:
            for j in range(12):
                for i in range(8):
                    redWeight = valueMapRed[j][i]
                    whiteWeight = valueMapWhite[j][i]
                    ringWeight = valueMapRing[j][i]
                    dotWeight = valueMapDot[j][i]

                    if redWeight >= price[3]:
                        redWeight *= 1.5
                    if whiteWeight >= price[3]:
                        whiteWeight *= 1.5


                    sumRed += redWeight
                    sumWhite += whiteWeight
                    sumRing += ringWeight
                    sumDot += dotWeight
        else:
            for j in range(12):
                for i in range(8):
                    redWeight = valueMapRed[j][i]
                    whiteWeight = valueMapWhite[j][i]
                    ringWeight = valueMapRing[j][i]
                    dotWeight = valueMapDot[j][i]

                    if dotWeight >= price[3]:
                        dotWeight *= 1.5
                    if dotWeight >= price[3]:
                        dotWeight *= 1.5

                    sumRed += redWeight
                    sumWhite += whiteWeight
                    sumRing += ringWeight
                    sumDot += dotWeight

        # if party == 0:
        #     if goalState == "winC":
        #         return max(sumRing, sumDot) - 10*max(sumRed, sumWhite)
        #     elif goalState == "winD" or goalState == "winDC":
        #         return 10*max(sumRing, sumDot) - max(sumRed, sumWhite)
        #     else:
        #         return max(sumRing, sumDot) - max(sumRed, sumWhite)
        # if party == 1:
        #     if goalState == "winD":
        #         return 10*max(sumRing, sumDot) - max(sumRed, sumWhite)
        #     elif goalState == "winC" or goalState == "winDC":
        #         return max(sumRing, sumDot) - 10*max(sumRed, sumWhite)
        #     else:
        #         return max(sumRing, sumDot) - max(sumRed, sumWhite)

        if party == 0:
            if goalState == "winC":
                return (sumRing + sumDot) - 10 * (sumRed + sumWhite)
            elif goalState == "winD" or goalState == "winDC":
                return 10*(sumRing + sumDot) - (sumRed + sumWhite)
            else:
                return (sumRing + sumDot) - (sumRed + sumWhite)
        if party == 1:
            if goalState == "winD":
                return 10*(sumRing + sumDot) - (sumRed + sumWhite)
            elif goalState == "winC" or goalState == "winDC":
                return (sumRing + sumDot) - 10*(sumRed + sumWhite)
            else:
                return (sumRing + sumDot) - (sumRed + sumWhite)

    def applyMatrix(self, valueMap, i,j):
        if j < 11:
            if valueMap[j + 1][i] > 0:
                valueMap[j + 1][i] += 1

        if i < 7:
            if valueMap[j][i + 1] > 0:
                valueMap[j][i + 1] += 1

        if j < 11 and i < 7:
            if valueMap[j + 1][i + 1] > 0:
                valueMap[j + 1][i + 1] += 1

        if j >= 0:
            if valueMap[j - 1][i] > 0:
                valueMap[j - 1][i] += 1
        if i >= 0:
            if valueMap[j][i - 1] > 0:
                valueMap[j][i - 1] += 1
        if i >= 0:
            if valueMap[j - 1][i - 1] > 0:
                valueMap[j - 1][i - 1] += 1
        if j >= 0 and i < 7:
            if valueMap[j - 1][i + 1] > 0 :
                valueMap[j - 1][i + 1] += 1

        if j < 11 and i >= 0:
            if valueMap[j + 1][i - 1] > 0:
                valueMap[j + 1][i - 1] += 1
