import numpy;
from move import Move
from validator import Validator

# convert letters to numbers
letterTonumb = {
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
numbToLetter = dict([[v, k] for k, v in letterTonumb.items()])

coordinateToRotation = {}

# 
gameMap = numpy.zeros((12, 8))


# krasnyCherny - 1
# beluyKolco - 2
# krasnyKolco - 3
# beluyChernuy - 4

# give what is in the first half of the card according to rotation if not found return 10
def pervayaYacheyka(rotation):
    swithcer = {
        1: 1,
        2: 2,
        3: 2,
        4: 1,
        5: 3,
        6: 4,
        7: 4,
        8: 3
    }
    return swithcer.get(rotation, 10);


# give what is in the second half of the card according to rotation if not found return 10
def vtorayYacheyka(rotation):
    swithcer = {
        1: 2,
        2: 1,
        3: 1,
        4: 2,
        5: 4,
        6: 3,
        7: 3,
        8: 5
    }
    return swithcer.get(rotation, 10);

# put card at postion i j and the rotation


def place(move):
    validator = Validator(gameMap, coordinateToRotation)
    if move.type == 0:
        if validator.placeValidator(move):
            i = (move.targetCoordinateLet) - 1
            j = int(move.targetCoordinateNum) - 1
            rotation = int(move.rotation)
            coordinateToRotation[numbToLetter.get(i + 1) + str(j + 1)] = rotation;
            gameMap[j][i] = pervayaYacheyka(rotation)
            if rotation % 2 != 0:
                gameMap[j][i + 1] = vtorayYacheyka(rotation)
            else:
                gameMap[j + 1][i] = vtorayYacheyka(rotation)
    else:
        if validator.recycleValidator(move):
            i1 = (move.sourceCoordinate1Let) - 1
            j1 = int(move.sourceCoordinate1Num) - 1

            i2 = (move.sourceCoordinate2Let) - 1
            j2 = int(move.sourceCoordinate2Num) - 1
            old_val1 = gameMap[j1][i1]
            old_val2 = gameMap[j2][i2]

            gameMap[j1][i1] = 0
            gameMap[j2][i2] = 0

            i = (move.targetCoordinateLet) - 1
            j = int(move.targetCoordinateNum) - 1
            rotation = int(move.rotation)
            if validator.placeValidatorCoord(i, j, rotation):
                coordinateToRotation[numbToLetter.get(i + 1) + str(j + 1)] = rotation;
                gameMap[j][i] = pervayaYacheyka(rotation)
                if rotation % 2 != 0:
                    gameMap[j][i + 1] = vtorayYacheyka(rotation)
                else:
                    gameMap[j + 1][i] = vtorayYacheyka(rotation)
            else:
                gameMap[j1][i1] = old_val1
                gameMap[j2][i2] = old_val2
    return

red = [1,3]
white = [2,4]
dot = [1,4]
ring = [2,3]

def victoryCheck(gameMap):
    for i in range(9):
        for j in range(5):
            if gameMap[i][j] in red and gameMap[i+1][j] in red and gameMap[i+2][j] in red and gameMap[i+3][j] in red:
                return "color wins"
            elif gameMap[i][j] in red and gameMap[i][j+1] in red and gameMap[i][j+2] in red and gameMap[i][j+3] in red:
                return "color wins"
            elif gameMap[i+3][j] in red and gameMap[i+3][j+1] in red and gameMap[i+3][j+2] in red and gameMap[i+3][j+3] in red:
                return "color wins"
            elif gameMap[i][j+3] in red and gameMap[i+1][j+3] in red and gameMap[i+2][j+3] in red and gameMap[i+3][j+3] in red:
                return "color wins"
            elif gameMap[i][j] in red and gameMap[i+1][j+1] in red and gameMap[i+2][j+2] in red and gameMap[i+3][j+3] in red:
                return "color wins"
            elif gameMap[i+3][j] in red and gameMap[i+2][j+1] in red and gameMap[i+1][j+2] in red and gameMap[i][j+3] in red:
                return "color wins"
            
            elif gameMap[i][j] in white and gameMap[i+1][j] in white and gameMap[i+2][j] in white and gameMap[i+3][j] in white:
                return "color wins"
            elif gameMap[i][j] in white and gameMap[i][j+1] in white and gameMap[i][j+2] in white and gameMap[i][j+3] in white:
                return "color wins"
            elif gameMap[i+3][j] in white and gameMap[i+3][j+1] in white and gameMap[i+3][j+2] in white and gameMap[i+3][j+3] in white:
                return "color wins"
            elif gameMap[i][j+3] in white and gameMap[i+1][j+3] in white and gameMap[i+2][j+3] in white and gameMap[i+3][j+3] in white:
                return "color wins"
            elif gameMap[i][j] in white and gameMap[i+1][j+1] in white and gameMap[i+2][j+2] in white and gameMap[i+3][j+3] in white:
                return "color wins"
            elif gameMap[i+3][j] in white and gameMap[i+2][j+1] in white and gameMap[i+1][j+2] in white and gameMap[i][j+3] in white:
                return "color wins"
            
            elif gameMap[i][j] in dot and gameMap[i+1][j] in dot and gameMap[i+2][j] in dot and gameMap[i+3][j] in dot:
                return "circle wins"
            elif gameMap[i][j] in dot and gameMap[i][j+1] in dot and gameMap[i][j+2] in dot and gameMap[i][j+3] in dot:
                return "circle wins"
            elif gameMap[i+3][j] in dot and gameMap[i+3][j+1] in dot and gameMap[i+3][j+2] in dot and gameMap[i+3][j+3] in dot:
                return "circle wins"
            elif gameMap[i][j+3] in dot and gameMap[i+1][j+3] in dot and gameMap[i+2][j+3] in dot and gameMap[i+3][j+3] in dot:
                return "circle wins"
            elif gameMap[i][j] in dot and gameMap[i+1][j+1] in dot and gameMap[i+2][j+2] in dot and gameMap[i+3][j+3] in dot:
                return "circle wins"
            elif gameMap[i+3][j] in dot and gameMap[i+2][j+1] in dot and gameMap[i+1][j+2] in dot and gameMap[i][j+3] in dot:
                return "circle wins"
            
            else:
                return "go"


for k in range(2):
    input_var = input("Enter something: ")
    move = Move(input_var)
    place(move)
    result = victoryCheck(gameMap)
    if result !="go":
        print(result)
        break
    print(numpy.flipud(gameMap))
    print(coordinateToRotation)



