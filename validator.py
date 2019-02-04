class Validator:
    def __init__(self, gameMap, coordinateToRotation, move):
        self.gameMap = gameMap
        self.coordinateToRotation = coordinateToRotation
        self.moove = move

        self.letterTonumb = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8

        }
        self.numbToLetter = dict([[v, k] for k, v in self.letterTonumb.items()])



    def placeValidator(self, move):
        i = (move.targetCoordinateLet) - 1
        j = int(move.targetCoordinateNum) - 1
        if int(move.rotation) % 2 != 0:  # orientation check
            if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= i + 1 <= 7:  # border check
                if self.gameMap[j][i] == 0 and self.gameMap[j][i + 1] == 0:
                    if j == 0:  # first line is always supported
                        return True
                    else:
                        if self.gameMap[j - 1][i] != 0 and self.gameMap[- 1][i + 1] != 0:  # there is support
                            return True;
                else:
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
                    return False;

    def placeValidatorCoord(self, i, j, rotation):
        if rotation % 2 != 0:  # orientation check
            if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= i + 1 <= 7:  # border check
                if self.gameMap[j][i] == 0 and self.gameMap[j][i + 1] == 0:
                    if j == 0:  # first line is always supported
                        return True
                    else:
                        if self.gameMap[j - 1][i] != 0 and self.gameMap[- 1][i + 1] != 0:  # there is support
                            return True;
                else:
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
                    return False;




    def lookUpValidatorHorizontal(self, i1, j1, i2, j2):
        if self.gameMap[i1][j1 + 1] == 0 and self.gameMap[i2][j2 + 1] == 0:
            return True;
        return False

    # check if anything is above in case vertical
    def lookUpValidatorVertical(self, i2, j2):
        if self.gameMap[i2][j2 + 1] == 0:
            return True;
        return False

    def recycleValidator(self, move):
        i1 = (move.sourceCoordinate1Let) - 1
        j1 = int(move.sourceCoordinate1Num) - 1

        i2 = (move.sourceCoordinate2Let) - 1
        j2 = int(move.sourceCoordinate2Num) - 1

        print("{} {} - {} {} ".format(i1, j1, i2, j2))
        print(self.numbToLetter.get(i1 + 1) + str(j1 + 1))
        print(self.numbToLetter.get(i2 + 1) + str(j2 + 1))

        rotation = self.coordinateToRotation.get(self, self.numbToLetter.get(i1 + 1) + str(j1 + 1), 10)
        if rotation == 10:
            rotation = self.coordinateToRotation.get(self, self.numbToLetter.get(i2 + 1) + str(j2 + 1), 10)
            print(rotation)
        if rotation == 10:
            print(rotation)
            return False;

        if rotation % 2 == 0:
            if i1 == i2 and abs(j1 - j2) == 1 and self.lookUpValidatorVertical(self, i2, j2):
                return True
            else:
                    if abs(i1 - i2) == 1 and j1 == j2 and self.lookUpValidatorHorizontal(i1, j1, i2, j2):
                        return True;
            return False

