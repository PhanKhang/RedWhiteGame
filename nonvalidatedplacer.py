def secondCell(rotation):
    translator = {
        1: 2,
        2: 1,
        3: 1,
        4: 2,
        5: 4,
        6: 3,
        7: 3,
        8: 4
    }
    return translator.get(rotation, 0);


def firstCell(rotation):
    translator = {
        1: 1,
        2: 2,
        3: 2,
        4: 1,
        5: 3,
        6: 4,
        7: 4,
        8: 3
    }
    return translator.get(rotation, 0);


# convert letters to numbers
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


class Nonvalidatedplacer:
    def __init__(self):
        pass

    # give what is in the first half of the card according to rotation if not found return 0
    def place(self, move, validator, gameMap):
        if move.type == 0:
            i = move.targetCoordinateLet - 1
            j = int(move.targetCoordinateNum) - 1
            rotation = int(move.rotation)
            validator.coordinateToRotation[numbToLetter.get(i + 1) + str(j + 1)] = rotation;
            gameMap[j][i] = firstCell(rotation)
            if rotation % 2 != 0 and rotation != 0:
                gameMap[j][i + 1] = secondCell(rotation)
            else:
                gameMap[j + 1][i] = secondCell(rotation)
        else:
            if validator.recycleValidator(move, gameMap):
                i1 = move.sourceCoordinate1Let - 1
                j1 = move.sourceCoordinate1Num - 1

                i2 = move.sourceCoordinate2Let - 1
                j2 = move.sourceCoordinate2Num - 1

                gameMap[j1][i1] = 0
                gameMap[j2][i2] = 0

                i = move.targetCoordinateLet - 1
                j = int(move.targetCoordinateNum) - 1
                rotation = int(move.rotation)

                # remove the value from dictionary of moves
                if validator.coordinateToRotation.pop(numbToLetter.get(i1 + 1) + str(j1 + 1), 0) == 0:
                    validator.coordinateToRotation.pop(numbToLetter.get(i2 + 1) + str(j2 + 1), 0)

                validator.coordinateToRotation[numbToLetter.get(i + 1) + str(j + 1)] = rotation
                gameMap[j][i] = firstCell(rotation)
                if rotation % 2 != 0:
                    gameMap[j][i + 1] = secondCell(rotation)
                else:
                    gameMap[j + 1][i] = secondCell(rotation)