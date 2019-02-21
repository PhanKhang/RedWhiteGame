class Validator:
    def __init__(self, gameMap):
        self.gameMap = gameMap

        self.letterToNumb = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8

        }
        self.numbToLetter = dict([[v, k] for k, v in self.letterToNumb.items()])

    lastMove = None

    # parse the move and check if the card can be placed
    def placeValidator(self, move):
        i = move.targetCoordinateLet - 1
        j = int(move.targetCoordinateNum) - 1
        rotation = move.rotation
        if self.placeValidatorCoord(i, j, rotation):
            self.lastMove = move
            return True

    # Checks:
    # 1) if card within the board's boundaries
    # 2) if there is a ground for card
    # 3) if the place is free
    def placeValidatorCoord(self, i, j, rotation):
        if rotation % 2 != 0:  # orientation check
            if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= i + 1 <= 7:  # border check
                if self.gameMap[j][i] == 0 and self.gameMap[j][i + 1] == 0:
                    if j == 0:  # first line is always supported
                        return True
                    else:
                        if self.gameMap[j - 1][i] != 0 and self.gameMap[j - 1][i + 1] != 0:  # there is support
                            return True
                        else:
                            print("No support")
                            return False
                else:
                    print("Not free")
                    return False
            else:
                print("Out of border")
                return False
        else:
            if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= j + 1 <= 11:
                if self.gameMap[j][i] == 0 and self.gameMap[j + 1][i] == 0:
                    if j == 0:  # first line is always supported
                        return True
                    else:
                        if self.gameMap[j - 1][i] != 0:
                            return True
                        else:
                            print("No support")
                            return False
                else:
                    print("Not free")
                    return False
            else:
                print("Out of border")
                return False

    # Checks if horizontal card is not piled.
    def lookUpValidatorHorizontal(self, i1, j1, i2, j2):
        if self.gameMap[j1 + 1][i1] == 0 and self.gameMap[j2 + 1][i2] == 0:
            return True
        return False

    # Checks if vertical card is not piled.
    def lookUpValidatorVertical(self, i2, j2):
        if self.gameMap[j2 + 1][i2] == 0:
            return True
        return False

    def isNotLastMove(self, move):
        i1 = move.sourceCoordinate1Let
        j1 = int(move.sourceCoordinate1Num)
        i2 = move.sourceCoordinate2Let
        j2 = int(move.sourceCoordinate2Num)

        if (i1 == self.lastMove.targetCoordinateLet and j1 == self.lastMove.targetCoordinateNum) or \
                (i2 == self.lastMove.targetCoordinateLet and j2 == self.lastMove.targetCoordinateNum):
            print("This was the last move")
            return False
        return True

    # Checks recycle move:
    # 1) checks card integrity by coordinates
    # 2) checks if there is no other cards above the given one
    def recycleValidator(self, move, coordinate_to_rotation):
        if self.isNotLastMove(move):
            i1 = move.sourceCoordinate1Let - 1
            j1 = int(move.sourceCoordinate1Num) - 1

            i2 = move.sourceCoordinate2Let - 1
            j2 = int(move.sourceCoordinate2Num) - 1

            # get the sored rotation of the card to validate the card integrity holds
            rotation = coordinate_to_rotation.get(self.numbToLetter.get(i1 + 1) + str(j1 + 1), 0)
            if rotation == 0:
                rotation = coordinate_to_rotation.get(self.numbToLetter.get(i2 + 1) + str(j2 + 1), 0)
                print(rotation)
            if rotation == 0:
                print(rotation)
                return False
            # find if 2 coordinates are of the same card
            if int(rotation) % 2 == 0:
                if i1 == i2 and abs(j1 - j2) == 1 and self.lookUpValidatorVertical(i2, j2):
                    return True
            else:
                if abs(i1 - i2) == 1 and j1 == j2 and self.lookUpValidatorHorizontal(i1, j1, i2, j2):
                    return True
        return False

    # correspondence of value to card
    red = [1, 3]
    white = [2, 4]
    dot = [1, 4]
    ring = [2, 3]

    # Checks if there is a row of 4 cells of the same type on the game map. Horizontal, vertical and both diagonals.
    def victoryCheck(self, player):
        if player == 0:
            for i in range(12):
                for j in range(8):
                    if i <= 8:
                        if self.gameMap[i][j] in self.red and self.gameMap[i + 1][j] in self.red and \
                                self.gameMap[i + 2][j] in self.red and self.gameMap[i + 3][j] in self.red:
                            return "color wins"
                        if self.gameMap[i][j] in self.white and self.gameMap[i + 1][j] in self.white and \
                                self.gameMap[i + 2][j] in self.white and self.gameMap[i + 3][j] in self.white:
                            return "color wins"

                        if self.gameMap[i][j] in self.dot and self.gameMap[i + 1][j] in self.dot and \
                                self.gameMap[i + 2][j] in self.dot and self.gameMap[i + 3][j] in self.dot:
                            return "circle wins"
                        if self.gameMap[i][j] in self.ring and self.gameMap[i + 1][j] in self.ring and \
                                self.gameMap[i + 2][j] in self.ring and self.gameMap[i + 3][j] in self.ring:
                            return "circle wins"

                    if j <= 4:
                        if self.gameMap[i][j] in self.red and self.gameMap[i][j + 1] in self.red and \
                                self.gameMap[i][j + 2] in self.red and self.gameMap[i][j + 3] in self.red:
                            return "color wins"
                        if self.gameMap[i][j] in self.white and self.gameMap[i][j + 1] in self.white and \
                                self.gameMap[i][j + 2] in self.white and self.gameMap[i][j + 3] in self.white:
                            return "color wins"

                        if self.gameMap[i][j] in self.dot and self.gameMap[i][j + 1] in self.dot and \
                                self.gameMap[i][j + 2] in self.dot and self.gameMap[i][j + 3] in self.dot:
                            return "circle wins"
                        if self.gameMap[i][j] in self.ring and self.gameMap[i][j + 1] in self.ring and \
                                self.gameMap[i][j + 2] in self.ring and self.gameMap[i][j + 3] in self.ring:
                            return "circle wins"

                    if j <= 4 and i <= 8:
                        if self.gameMap[i][j] in self.white and self.gameMap[i + 1][j + 1] in self.white and \
                                self.gameMap[i + 2][j + 2] in self.white and self.gameMap[i + 3][j + 3] in self.white:
                            return "color wins"
                        if self.gameMap[i + 3][j] in self.white and self.gameMap[i + 2][j + 1] in self.white and \
                                self.gameMap[i + 1][j + 2] in self.white and self.gameMap[i][j + 3] in self.white:
                            return "color wins"
                        if self.gameMap[i + 3][j] in self.white and self.gameMap[i + 2][j + 1] in self.white and \
                                self.gameMap[i + 1][j + 2] in self.white and self.gameMap[i][j + 3] in self.white:
                            return "color wins"
                        if self.gameMap[i][j] in self.red and self.gameMap[i + 1][j + 1] in self.red and \
                                self.gameMap[i + 2][j + 2] in self.red and self.gameMap[i + 3][j + 3] in self.red:
                            return "color wins"
                        if self.gameMap[i + 3][j] in self.red and self.gameMap[i + 2][j + 1] in self.red and \
                                self.gameMap[i + 1][j + 2] in self.red and self.gameMap[i][j + 3] in self.red:
                            return "color wins"

                        if self.gameMap[i][j] in self.dot and self.gameMap[i + 1][j + 1] in self.dot and \
                                self.gameMap[i + 2][j + 2] in self.dot and self.gameMap[i + 3][j + 3] in self.dot:
                            return "circle wins"
                        if self.gameMap[i + 3][j] in self.dot and self.gameMap[i + 2][j + 1] in self.dot and \
                                self.gameMap[i + 1][j + 2] in self.dot and self.gameMap[i][j + 3] in self.dot:
                            return "circle wins"
                        if self.gameMap[i][j] in self.ring and self.gameMap[i + 1][j + 1] in self.ring and \
                                self.gameMap[i + 2][j + 2] in self.ring and self.gameMap[i + 3][j + 3] in self.ring:
                            return "circle wins"
                        if self.gameMap[i + 3][j] in self.ring and self.gameMap[i + 2][j + 1] in self.ring and \
                                self.gameMap[i + 1][j + 2] in self.ring and self.gameMap[i][j + 3] in self.ring:
                            return "circle wins"
            return "go"
        else:
            for i in range(12):
                for j in range(8):
                    if i <= 8:
                        if self.gameMap[i][j] in self.dot and self.gameMap[i + 1][j] in self.dot and \
                                self.gameMap[i + 2][j] in self.dot and self.gameMap[i + 3][j] in self.dot:
                            return "circle wins"
                        if self.gameMap[i][j] in self.ring and self.gameMap[i + 1][j] in self.ring and \
                                self.gameMap[i + 2][j] in self.ring and self.gameMap[i + 3][j] in self.ring:
                            return "circle wins"

                        if self.gameMap[i][j] in self.red and self.gameMap[i + 1][j] in self.red and \
                                self.gameMap[i + 2][j] in self.red and self.gameMap[i + 3][j] in self.red:
                            return "color wins"
                        if self.gameMap[i][j] in self.white and self.gameMap[i + 1][j] in self.white and \
                                self.gameMap[i + 2][j] in self.white and self.gameMap[i + 3][j] in self.white:
                            return "color wins"

                    if j <= 4:
                        if self.gameMap[i][j] in self.dot and self.gameMap[i][j + 1] in self.dot and \
                                self.gameMap[i][j + 2] in self.dot and self.gameMap[i][j + 3] in self.dot:
                            return "circle wins"
                        if self.gameMap[i][j] in self.ring and self.gameMap[i][j + 1] in self.ring and \
                                self.gameMap[i][j + 2] in self.ring and self.gameMap[i][j + 3] in self.ring:
                            return "circle wins"

                        if self.gameMap[i][j] in self.red and self.gameMap[i][j + 1] in self.red and \
                                self.gameMap[i][j + 2] in self.red and self.gameMap[i][j + 3] in self.red:
                            return "color wins"
                        if self.gameMap[i][j] in self.white and self.gameMap[i][j + 1] in self.white and \
                                self.gameMap[i][j + 2] in self.white and self.gameMap[i][j + 3] in self.white:
                            return "color wins"

                    if j <= 4 and i <= 8:
                        if self.gameMap[i][j] in self.dot and self.gameMap[i + 1][j + 1] in self.dot and \
                                self.gameMap[i + 2][j + 2] in self.dot and self.gameMap[i + 3][j + 3] in self.dot:
                            return "circle wins"
                        if self.gameMap[i + 3][j] in self.dot and self.gameMap[i + 2][j + 1] in self.dot and \
                                self.gameMap[i + 1][j + 2] in self.dot and self.gameMap[i][j + 3] in self.dot:
                            return "circle wins"
                        if self.gameMap[i][j] in self.ring and self.gameMap[i + 1][j + 1] in self.ring and \
                                self.gameMap[i + 2][j + 2] in self.ring and self.gameMap[i + 3][j + 3] in self.ring:
                            return "circle wins"
                        if self.gameMap[i + 3][j] in self.ring and self.gameMap[i + 2][j + 1] in self.ring and \
                                self.gameMap[i + 1][j + 2] in self.ring and self.gameMap[i][j + 3] in self.ring:
                            return "circle wins"

                        if self.gameMap[i][j] in self.white and self.gameMap[i + 1][j + 1] in self.white and \
                                self.gameMap[i + 2][j + 2] in self.white and self.gameMap[i + 3][j + 3] in self.white:
                            return "color wins"
                        if self.gameMap[i + 3][j] in self.white and self.gameMap[i + 2][j + 1] in self.white and \
                                self.gameMap[i + 1][j + 2] in self.white and self.gameMap[i][j + 3] in self.white:
                            return "color wins"
                        if self.gameMap[i + 3][j] in self.white and self.gameMap[i + 2][j + 1] in self.white and \
                                self.gameMap[i + 1][j + 2] in self.white and self.gameMap[i][j + 3] in self.white:
                            return "color wins"
                        if self.gameMap[i][j] in self.red and self.gameMap[i + 1][j + 1] in self.red and \
                                self.gameMap[i + 2][j + 2] in self.red and self.gameMap[i + 3][j + 3] in self.red:
                            return "color wins"
                        if self.gameMap[i + 3][j] in self.red and self.gameMap[i + 2][j + 1] in self.red and \
                                self.gameMap[i + 1][j + 2] in self.red and self.gameMap[i][j + 3] in self.red:
                            return "color wins"
            return "go"
