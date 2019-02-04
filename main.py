import numpy;
from move import Move

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

# Мапа
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
    # тут принимай Move объект
    # возвращай булеан
    # валидатор дёргай отсюда.
    # по хорошему поляну надо тоже передавать методу на вход.
    if move.type == 0:
        if placeValidator(move):
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
        if recycleValidator(move):
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
            if placeValidatorCoord(i, j, rotation):
                print("second")
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


# check if anything is above in case of horizontal
def lookUpValidatorHorizontal(i1, j1, i2, j2):
    if gameMap[i1][j1 + 1] == 0 and gameMap[i2][j2 + 1] == 0:
        return True;
    return False


# check if anything is above in case vertical
def lookUpValidatorVertical(i2, j2):
    if gameMap[i2][j2 + 1] == 0:
        return True;
    return False


# validator and placer
# input is string variable move
# placer can be removed but parser for move is needed
def placeValidator(move):
    i = (move.targetCoordinateLet) - 1
    j = int(move.targetCoordinateNum) - 1
    if int(move.rotation) % 2 != 0:  # orientation check
        if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= i + 1 <= 7:  # border check
            if gameMap[j][i] == 0 and gameMap[j][i + 1] == 0:
                if j == 0:  # first line is always supported
                    return True
                else:
                    if gameMap[j - 1][i] != 0 and gameMap[- 1][i + 1] != 0:  # there is support
                        return True;
            else:
                return False
    else:
        if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= j + 1 <= 11:
            if gameMap[j][i] == 0 and gameMap[j + 1][i] == 0:
                if j == 0:  # first line is always supported
                    return True
                else:
                    if gameMap[j - 1][i] != 0:
                        return True
            else:
                return False;


def placeValidatorCoord(i, j, rotation):
    if rotation % 2 != 0:  # orientation check
        if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= i + 1 <= 7:  # border check
            if gameMap[j][i] == 0 and gameMap[j][i + 1] == 0:
                if j == 0:  # first line is always supported
                    return True
                else:
                    if gameMap[j - 1][i] != 0 and gameMap[- 1][i + 1] != 0:  # there is support
                        return True;
            else:
                return False
    else:
        if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= j + 1 <= 11:
            if gameMap[j][i] == 0 and gameMap[j + 1][i] == 0:
                if j == 0:  # first line is always supported
                    return True
                else:
                    if gameMap[j - 1][i] != 0:
                        return True
            else:
                return False;


# Проверка целестности карты
def recycleValidator(move):
    i1 = (move.sourceCoordinate1Let) - 1
    j1 = int(move.sourceCoordinate1Num) - 1

    i2 = (move.sourceCoordinate2Let) - 1
    j2 = int(move.sourceCoordinate2Num) - 1

    print("{} {} - {} {} ".format(i1, j1, i2, j2))
    print(numbToLetter.get(i1 + 1) + str(j1 + 1))
    print(numbToLetter.get(i2 + 1) + str(j2 + 1))

    rotation = coordinateToRotation.get(numbToLetter.get(i1 + 1) + str(j1 + 1), 10)
    if rotation == 10:
        rotation = coordinateToRotation.get(numbToLetter.get(i2 + 1) + str(j2 + 1), 10)
        print(rotation)
    if rotation == 10:
        print(rotation)
        return False;

    if rotation % 2 == 0:
        if i1 == i2 and abs(j1 - j2) == 1 and lookUpValidatorVertical(i2, j2):
            return True
        else:
            if abs(i1 - i2) == 1 and j1 == j2 and lookUpValidatorHorizontal(i1, j1, i2, j2):
                return True;
    return False


for k in range(7):
    input_var = input("Enter something: ")
    #
    # пример:
    # move = Move(input)
    # if place(move):
    #	"ok"
    # else:
    #	"invalid move"
    # ....
    # помимо прочего приделай сюда мейн, так красивей
    move = Move(input_var)
    place(move)
    print(numpy.flipud(gameMap))
    print(coordinateToRotation)
