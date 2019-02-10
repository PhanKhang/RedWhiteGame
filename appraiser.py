import numpy

price_red = 10
price_white = 10
price_dot = 10
price_ring = 10

price_of_being_blocked = -1000;


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

    # оценка влиянии карты на поля
    def appraise(self, move, player):
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

        # if player == 0:
        #     print("Playing with Dots")
        if self.gameMap[j][i] in self.dot:
            self.moveBlocking(i, j, self.ring)
        else:
            self.moveBlocking(i, j, self.dot)

        if self.gameMap[j][i] in self.red:
            self.moveBlocking(i, j, self.white)
        else:
            self.moveBlocking(i, j, self.red)

        if self.gameMap[j1][i1] in self.dot:
            self.moveBlocking(i1, j1, self.ring)
        else:
            self.moveBlocking(i1, j1, self.dot)

        if self.gameMap[j1][i1] in self.red:
            self.moveBlocking(i1, j1, self.white)
        else:
            self.moveBlocking(i1, j1, self.red)

        # else:
        #     print("Playing with colors")

    def moveBlocking(self, i, j, color_or_dot):

        if self.isBlockingVertical(i, j, color_or_dot) == 3:
            print("Vertical is blocked for " + str(i) + " " + str(j))
            tmp = self.getCorrectMap(color_or_dot)
            for step in range(1, 5):
                if j + step < 12:
                    tmp[j + step][i] += price_of_being_blocked
                if j - step >= 0:
                    tmp[j - step][i] += price_of_being_blocked
        if self.isBlockingVertical(i, j, color_or_dot) == 2:
            print("Vertical is down blocked for " + str(i) + " " + str(j))
            tmp = self.getCorrectMap(color_or_dot)
            for step in range(1, 5):
                if j - step >= 0:
                    tmp[j - step][i] += price_of_being_blocked
        if self.isBlockingVertical(i, j, color_or_dot) == 1:
            print("Vertical is up blocked for " + str(i) + " " + str(j))
            tmp = self.getCorrectMap(color_or_dot)
            for step in range(1, 5):
                if j + step < 12:
                    tmp[j + step][i] += price_of_being_blocked

        if self.isBlockingHorizontal(i, j, color_or_dot) == 3:
            print("Horizontal is blocked for " + str(i) + " " + str(j))
            tmp = self.getCorrectMap(color_or_dot)
            for step in range(1, 5):
                if i + step < 8:
                    tmp[j][i + step] += price_of_being_blocked
                if i - step >= 0:
                    tmp[j - step][i - step] += price_of_being_blocked
        if self.isBlockingHorizontal(i, j, color_or_dot) == 2:
            print("Horizontal is left blocked for " + str(i) + " " + str(j))
            for step in range(1, 5):
                if i - step >= 0:
                    tmp[j][i - step] += price_of_being_blocked
        if self.isBlockingHorizontal(i, j, color_or_dot) == 1:
            print("Horizontal is right blocked for " + str(i) + " " + str(j))
            for step in range(1, 5):
                if i + step >= 0:
                    tmp[j][i + step] += price_of_being_blocked

        if self.isBlockingLeftDiagonal(i, j, color_or_dot) == 3:
            print("Left Diagonal is blocked for " + str(i) + " " + str(j))
            for step in range(1, 5):
                if j + step < 12 and i - step >= 0:
                    tmp[j + step][i - step] += price_of_being_blocked
                if j - step >= 0 and i + step < 8:
                    tmp[j - step][i + step] += price_of_being_blocked
        if self.isBlockingLeftDiagonal(i, j, color_or_dot) == 2:
            print("Left Diagonal is left blocked for " + str(i) + " " + str(j))
            for step in range(1, 5):
                if j + step < 12 and i - step >= 0:
                    tmp[j + step][i - step] += price_of_being_blocked
        if self.isBlockingLeftDiagonal(i, j, color_or_dot) == 1:
            print("Left Diagonal is right blocked for " + str(i) + " " + str(j))
            for step in range(1, 5):
                if j - step >= 0 and i + step < 8:
                    tmp[j - step][i + step] += price_of_being_blocked

        if self.isBlockingRightDiagonal(i, j, color_or_dot) == 3:
            print("Right Diagonal is blocked for " + str(i) + " " + str(j))
            for step in range(1, 5):
                if j + step < 12 and i + step < 8:
                    tmp[j + step][i + step] += price_of_being_blocked
                if j - step >= 0 and i - step >= 0:
                    tmp[j - step][i - step] += price_of_being_blocked
        if self.isBlockingRightDiagonal(i, j, color_or_dot) == 2:
            print("Right Diagonal is left blocked for " + str(i) + " " + str(j))
            for step in range(1, 5):
                if j - step >= 0 and i - step >= 0:
                    tmp[j - step][i - step] += price_of_being_blocked
        if self.isBlockingRightDiagonal(i, j, color_or_dot) == 1:
            print("Right Diagonal is right blocked for " + str(i) + " " + str(j))
            for step in range(1, 5):
                if j + step < 12 and i + step < 8:
                    tmp[j + step][i + step] += price_of_being_blocked
        pass

    def getCorrectMap(self, color_or_dot):
        if color_or_dot == self.red:
            return self.gameMap_red
        elif color_or_dot == self.white:
            return self.gameMap_white
        elif color_or_dot == self.dot:
            return self.gameMap_dot
        elif color_or_dot == self.ring:
            return self.gameMap_ring
        else:
            print("non found")
            return None

    # return 0 for not blocking from both sides
    # return 1 for blocking right
    # return 2 for blocking left
    # return 3 for blocking left and right
    def isBlockingVertical(self, i, j, opposite_color_or_dot):
        free_r = 0
        free_l = 0
        for step in range(1, 5):
            if j + step < 12:
                if self.gameMap[j + step][i] in opposite_color_or_dot or self.gameMap[j + step][i] == 0:
                    free_r += 1
                else:
                    break
        for step in range(1, 5):
            if j - step >= 0:
                if self.gameMap[j - step][i] in opposite_color_or_dot or self.gameMap[j - step][i] == 0:
                    free_l += 1
                else:
                    break
        out = 0
        if free_r < 4:
            out += 1
        if free_l < 4:
            out += 2
        return out

    def isBlockingHorizontal(self, i, j, opposite_color_or_dot):
        free_r = 0
        free_l = 0
        for step in range(1, 5):
            if i + step < 7:
                if self.gameMap[j][i + step] in opposite_color_or_dot or self.gameMap[j][i + step] == 0:
                    free_r += 1
                else:
                    break

        for step in range(1, 5):
            if i - step >= 0:
                if self.gameMap[j][i - step] in opposite_color_or_dot or self.gameMap[j][i - step] == 0:
                    free_l += 1
                else:
                    break
        out = 0
        if free_r < 4:
            out += 1
        if free_l < 4:
            out += 2
        return out

    def isBlockingRightDiagonal(self, i, j, opposite_color_or_dot):
        free_r = 0
        free_l = 0
        for step in range(1, 5):
            if j + step < 12 and i + step < 8:
                if self.gameMap[j + step][i + step] in opposite_color_or_dot or self.gameMap[j + step][i + step] == 0:
                    free_r += 1
                else:
                    break
        for step in range(1, 5):
            if j - step >= 0 and i - step >= 0:
                if self.gameMap[j - step][i - step] in opposite_color_or_dot or self.gameMap[j - step][i - step] == 0:
                    free_l += 1
                else:
                    break
        out = 0
        if free_r < 4:
            out += 1
        if free_l < 4:
            out += 2
        return out

    def isBlockingLeftDiagonal(self, i, j, opposite_color_or_dot):
        free_r = 0
        free_l = 0
        for step in range(1, 5):
            if j - step >= 0 and i + step < 8:
                if self.gameMap[j - step][i + step] in opposite_color_or_dot or self.gameMap[j - step][i + step] == 0:
                    free_r += 1
                else:
                    break
        for step in range(1, 5):
            if j + step < 12 and i - step >= 0:
                if self.gameMap[j + step][i - step] in opposite_color_or_dot or self.gameMap[j + step][i - step] == 0:
                    free_l += 1
                else:
                    break
        out = 0
        if free_r < 4:
            out += 1
        if free_l < 4:
            out += 2
        return out

    def appraise_red(self, i, j):
        for step in range(1, 4):
            if j + step < 12:
                self.gameMap_red[j + step][i] += price_red
            if j - step >= 0:
                self.gameMap_red[j - step][i] += price_red
            if i + step < 8:
                self.gameMap_red[j][i + step] += price_red
            if i - step >= 0:
                self.gameMap_red[j][i - step] += price_red
            if j + step < 12 and i + step < 8:
                self.gameMap_red[j + step][i + step] += price_red
            if j - step >= 0 and i - step >= 0:
                self.gameMap_red[j - step][i - step] += price_red
            if j + step < 12 and i - step >= 0:
                self.gameMap_red[j + step][i - step] += price_red
            if j - step >= 0 and i + step < 8:
                self.gameMap_red[j - step][i + step] += price_red
        pass

    def appraise_white(self, i, j):
        for step in range(1, 4):
            if j + step < 12:
                self.gameMap_white[j + step][i] += price_white
            if j - step >= 0:
                self.gameMap_white[j - step][i] += price_white
            if i + step < 8:
                self.gameMap_white[j][i + step] += price_white
            if i - step >= 0:
                self.gameMap_white[j][i - step] += price_white
            if j + step < 12 and i + step < 8:
                self.gameMap_white[j + step][i + step] += price_white
            if j - step >= 0 and i - step >= 0:
                self.gameMap_white[j - step][i - step] += price_white
            if j + step < 12 and i - step >= 0:
                self.gameMap_white[j + step][i - step] += price_white
            if j - step >= 0 and i + step < 8:
                self.gameMap_white[j - step][i + step] += price_white
        pass

    def appraise_dot(self, i, j):
        for step in range(1, 4):
            if j + step < 12:
                self.gameMap_dot[j + step][i] += price_dot
            if j - step >= 0:
                self.gameMap_dot[j - step][i] += price_dot
            if i + step < 8:
                self.gameMap_dot[j][i + step] += price_dot
            if i - step >= 0:
                self.gameMap_dot[j][i - step] += price_dot
            if j + step < 12 and i + step < 8:
                self.gameMap_dot[j + step][i + step] += price_dot
            if j - step >= 0 and i - step >= 0:
                self.gameMap_dot[j - step][i - step] += price_dot
            if j + step < 12 and i - step >= 0:
                self.gameMap_dot[j + step][i - step] += price_dot
            if j - step >= 0 and i + step < 8:
                self.gameMap_dot[j - step][i + step] += price_dot
        pass

    def appraise_ring(self, i, j):
        for step in range(1, 4):
            if j + step < 12:
                self.gameMap_ring[j + step][i] += price_ring
            if j - step >= 0:
                self.gameMap_ring[j - step][i] += price_ring
            if i + step < 8:
                self.gameMap_ring[j][i + step] += price_ring
            if i - step >= 0:
                self.gameMap_ring[j][i - step] += price_ring
            if j + step < 12 and i + step < 8:
                self.gameMap_ring[j + step][i + step] += price_ring
            if j - step >= 0 and i - step >= 0:
                self.gameMap_ring[j - step][i - step] += price_ring
            if j + step < 12 and i - step >= 0:
                self.gameMap_ring[j + step][i - step] += price_ring
            if j - step >= 0 and i + step < 8:
                self.gameMap_ring[j - step][i + step] += price_ring
        pass

