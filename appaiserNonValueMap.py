import numpy

# price = [21, 34, 55, 89, 144]
price = [2, 3, 5, 8, 13, 21]
multi = [8, 13, 21]

class AppraiserNonValueMap:
    def __init__(self):
        pass

    red = [1, 3]
    white = [2, 4]
    dot = [1, 4]
    ring = [2, 3]

    # valueMapRed = numpy.zeros((12, 8))
    # valueMapWhite = numpy.zeros((12, 8))
    # valueMapDot = numpy.zeros((12, 8))
    # valueMapRing = numpy.zeros((12, 8))


    # appraise how how card will affect gameMap
    def appraise(self, gameMap, node):
        winC = False
        winD = False

        for j in range(12):
            for i in range(8):
                if gameMap[j][i] in self.red:
                    if self.appraiseMoveRed(i, j, gameMap, self.red, node, True):
                        winC = True
                if gameMap[j][i] in self.white:
                    if self.appraiseMoveWhite(i, j, gameMap, self.white, node, True):
                        winC = True
                if gameMap[j][i] in self.dot:
                    if self.appraiseMoveDot(i, j, gameMap, self.dot, node, False):
                        winD = True
                if gameMap[j][i] in self.ring:
                    if self.appraiseMoveRing(i, j, gameMap, self.ring, node, False):
                        winD = True

        if winD and winC:
            return "winDC"
        elif winD:
            return "winD"
        elif winC:
            return "winC"
        else:
            return "go"

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

    def appraiseMove(self, i, j, gameMap, valueMap, colorOrDot, score, isColor):
        win = False
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if valueMap[j][i - step + k] < price[rate] + 1 and gameMap[j][i - step + k] != 0:  # here
                            valueMap[j][i - step + k] = price[rate] + 1
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i] < price[rate] and gameMap[j - step + k][i] != 0:
                            valueMap[j - step + k][i] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if valueMap[j + step - k][i - step + k] < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            valueMap[j + step - k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if valueMap[j - step + k][i - step + k] < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            valueMap[j - step + k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
        return win

    def appraiseMoveRed(self, i, j, gameMap, colorOrDot, score, isColor):
        win = False
        colorOrDot = self.red

        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapRed[j][i - step + k] < price[rate] + 1 and gameMap[j][i - step + k] != 0:  # here
                            score.valueMapRed[j][i - step + k] = price[rate] + 1
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapRed[j - step + k][i] < price[rate] and gameMap[j - step + k][i] != 0:
                            score.valueMapRed[j - step + k][i] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1

            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapRed[j + step - k][i - step + k] < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            score.valueMapRed[j + step - k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapRed[j - step + k][i - step + k] < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            score.valueMapRed[j - step + k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
        return win

    def appraiseMoveWhite(self, i, j, gameMap, colorOrDot, score, isColor):
        win = False
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapWhite[j][i - step + k] < price[rate] + 1 and gameMap[j][i - step + k] != 0:  # here
                            score.valueMapWhite[j][i - step + k] = price[rate] + 1
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapWhite[j - step + k][i] < price[rate] and gameMap[j - step + k][i] != 0:
                            score.valueMapWhite[j - step + k][i] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapWhite[j + step - k][i - step + k] < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            score.valueMapWhite[j + step - k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapWhite[j - step + k][i - step + k] < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            score.valueMapWhite[j - step + k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
        return win

    def appraiseMoveDot(self, i, j, gameMap, colorOrDot, score, isColor):
        win = False
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapDot[j][i - step + k] < price[rate] + 1 and gameMap[j][i - step + k] != 0:  # here
                            score.valueMapDot[j][i - step + k] = price[rate] + 1
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapDot[j - step + k][i] < price[rate] and gameMap[j - step + k][i] != 0:
                            score.valueMapDot[j - step + k][i] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapDot[j + step - k][i - step + k] < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            score.valueMapDot[j + step - k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapDot[j - step + k][i - step + k] < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            score.valueMapDot[j - step + k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
        return win

    def appraiseMoveRing(self, i, j, gameMap, colorOrDot, score, isColor):
        win = False
        for step in range(4):
            if i - step >= 0:
                rate = self.isHorizontalWindowFree(i - step, j, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapRing[j][i - step + k] < price[rate] + 1 and gameMap[j][i - step + k] != 0:  # here
                            score.valueMapRing[j][i - step + k] = price[rate] + 1
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0:
                rate = self.isVerticalWindowFree(i, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapRing[j - step + k][i] < price[rate] and gameMap[j - step + k][i] != 0:
                            score.valueMapRing[j - step + k][i] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if i - step >= 0 and j + step < 12:
                rate = self.isDownDiagonalWindowFree(i - step, j + step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapRing[j + step - k][i - step + k] < price[rate] \
                                and gameMap[j + step - k][i - step + k] != 0:
                            score.valueMapRing[j + step - k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
            if j - step >= 0 and i - step >= 0:
                rate = self.isUpDiagonalWindowFree(i - step, j - step, colorOrDot, gameMap)
                if rate >= 4:
                    win = True
                if rate > 0:
                    for k in range(4):
                        if score.valueMapRing[j - step + k][i - step + k] < price[rate] \
                                and gameMap[j - step + k][i - step + k] != 0:
                            score.valueMapRing[j - step + k][i - step + k] = price[rate]
                            if isColor:
                                score.scoreColor += price[rate] + 1
                            else:
                                score.scoreDots += price[rate] + 1
        return win

    # check and apply the weight on the window of 4 elements if there is possibility of creating 4 in a row
    # total fields check is 7
    def getScore(self, party, goalState, node):
        sumRed = 0
        sumWhite = 0
        sumRing = 0
        sumDot = 0

        if party == 0:
            for j in range(12):
                for i in range(8):
                    redWeight = node.valueMapRed[j][i]
                    whiteWeight = node.valueMapWhite[j][i]
                    ringWeight = node.valueMapRing[j][i]
                    dotWeight = node.valueMapDot[j][i]

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
                    redWeight = node.valueMapRed[j][i]
                    whiteWeight = node.valueMapWhite[j][i]
                    ringWeight = node.valueMapRing[j][i]
                    dotWeight = node.valueMapDot[j][i]

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
                return (sumRing + sumDot) - multi[node.depth] * (sumRed + sumWhite)
                # return (sumRing + sumDot) - 10 * (sumRed + sumWhite)
            elif goalState == "winD" or goalState == "winDC":
                return multi[node.depth] * (sumRing + sumDot) - (sumRed + sumWhite)
                # return 10 * (sumRing + sumDot) - (sumRed + sumWhite)
            else:
                return (sumRing + sumDot) - (sumRed + sumWhite)
        if party == 1:
            if goalState == "winD":
                return multi[node.depth] * (sumRing + sumDot) - (sumRed + sumWhite)
                # return 10 * (sumRing + sumDot) - (sumRed + sumWhite)
            elif goalState == "winC" or goalState == "winDC":
                return (sumRing + sumDot) - multi[node.depth] * (sumRed + sumWhite)
                # return (sumRing + sumDot) - 10 * (sumRed + sumWhite)
            else:
                return (sumRing + sumDot) - (sumRed + sumWhite)

