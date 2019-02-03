import numpy;
import copy as cp;

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

numbToLetter = dict([[v, k] for k, v in letterTonumb.items()])

coordinateToRotation = {}

gameMap = numpy.zeros((12, 8))


# krasnyCherny - 1
# beluyKolco - 2
# krasnyKolco - 3
# beluyChernuy - 4
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


def place(i, j, rotation):
    gameMap[j][i] = pervayaYacheyka(rotation)
    if rotation % 2 != 0:
        gameMap[j][i + 1] = vtorayYacheyka(rotation)
    else:
        gameMap[j + 1][i] = vtorayYacheyka(rotation)
    return;

def lookUpValidator(i1,j1,i2,j2):
    if (gameMap[i1][j1-1] == 0 and gameMap[i2][j2-1] == 0):
        return True;
    return False
def lookUpValidator(i2,j2):
    if (gameMap[i2][j2-1] == 0):
        return True;
    return False

def validator(move):
    if move[:1].isdigit():
        print("Its a normal move")
        if int(move[1:2]) % 2 != 0:
            print("Card is horizontal")
            i = letterTonumb.get(move[2:3], 10) - 1
            j = int(move[3:]) - 1
            # print("{} {}".format(i, j))
            if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= i + 1 <= 7:
                if gameMap[j][i] == 0 and gameMap[j][i + 1] == 0:
                    print("place is free")
                    if j == 0:  # first line is always supported
                        place(i, j, int(move[1:2]))
                        coordinateToRotation[move[2:]] = int(move[1:2])
                        return True
                    else:
                        if gameMap[j - 1][i] != 0 and gameMap[- 1][i + 1] != 0:
                            coordinateToRotation[move[2:]] = int(move[1:2])
                            place(i, j, int(move[1:2]))
                            return True;
                else:
                    print("not free {} and {}".format(gameMap[j][i], gameMap[j][i + 1]))
        else:
            print("Card is vertical")
            i = letterTonumb.get(move[2:3]) - 1
            j = int(move[3:]) - 1
            # print("{} {}".format(i, j))
            if 0 <= i <= 7 and 0 <= j <= 11 and 0 <= j + 1 <= 11:
                if gameMap[j][i] == 0 and gameMap[j + 1][i] == 0:
                    print("place is free")
                    if j == 0:  # first line is always supported
                        coordinateToRotation[move[2:]] = int(move[1:2])
                        place(i, j, int(move[1:2]))
                        return True
                    else:
                        if gameMap[j - 1][i] != 0:
                            coordinateToRotation[move[2:]] = int(move[1:2])
                            place(i, j, int(move[1:2]))
                            return True
                else:
                    print("not free {} and {}".format(gameMap[j][i], gameMap[j + 1][i]))

    else:
        print("Might be recycle move")
        if move[1:3].isdigit() and move[4:6].isdigit():
            if int(move[4:6]) <= 12:
                i1 = letterTonumb.get(move[:1], 10) - 1
                j1 = int(move[1:3]) - 1

                i2 = letterTonumb.get(move[3:4], 10) - 1
                j2 = int(move[4:6]) - 1

                rotation = coordinateToRotation.get(move[:3], 10)
                if rotation == 10:
                    rotation = coordinateToRotation.get(move[3:6], 10)
                if rotation == 10:
                    return False;
                old_val1 = gameMap[j1][i1]
                old_val2 = gameMap[j2][i2]
                gameMap[j1][i1] = 0
                gameMap[j2][i2] = 0

                if rotation % 2 == 0:
                    if i1 == i2 and abs(j1 - j2) == 1 and lookUpValidator(i2, j2):
                        if validator("0" + move[6:]):
                            print("{} {} - {} {} ".format(i1, j1, i2, j2) + move[6:])
                            return True

                else:
                    if abs(i1 - i2) == 1 and j1 == j2 and lookUpValidator(i1, j1, i2, j2):
                        if validator("0" + move[6:]):
                            print("{} {} - {} {} ".format(i1, j1, i2, j2) + move[6:])
                            return True

                gameMap[j1][i1] = old_val1
                gameMap[j2][i2] = old_val2
                return False

        if move[1:2].isdigit() and move[3:5].isdigit():
            if int(move[3:5]) <= 12:
                i1 = letterTonumb.get(move[:1], 10) - 1
                j1 = int(move[1:2]) - 1

                i2 = letterTonumb.get(move[2:3], 10) - 1
                j2 = int(move[3:5]) - 1

                rotation = coordinateToRotation.get(move[:2], 10)
                if rotation == 10:
                    rotation = coordinateToRotation.get(move[2:5], 10)
                if rotation == 10:
                    return False;
                old_val1 = gameMap[j1][i1]
                old_val2 = gameMap[j2][i2]
                gameMap[j1][i1] = 0
                gameMap[j2][i2] = 0

                if rotation % 2 == 0:
                    if i1 == i2 and abs(j1 - j2) == 1 and lookUpValidator(i2, j2):
                        if validator("0" + move[5:]):
                            print("{} {} - {} {} ".format(i1, j1, i2, j2) + move[5:])
                            return True

                else:
                    if abs(i1 - i2) == 1 and j1 == j2 and lookUpValidator(i1, j1, i2, j2):
                        if validator("0" + move[5:]):
                            print("{} {} - {} {} ".format(i1, j1, i2, j2) + move[5:])
                            return True

                gameMap[j1][i1] = old_val1
                gameMap[j2][i2] = old_val2
                return False

        if move[1:3].isdigit() and move[4:5].isdigit():
            i1 = letterTonumb.get(move[:1], 10) - 1
            j1 = int(move[1:3]) - 1

            i2 = letterTonumb.get(move[3:4], 10) - 1
            j2 = int(move[4:5]) - 1

            rotation = coordinateToRotation.get(move[:3], 10)
            print(rotation)
            if rotation == 10:
                rotation = coordinateToRotation.get(move[3:5], 10)
            if rotation == 10:
                return False;
            old_val1 = gameMap[j1][i1]
            old_val2 = gameMap[j2][i2]
            gameMap[j1][i1] = 0
            gameMap[j2][i2] = 0

            if rotation % 2 == 0:
                if i1 == i2 and abs(j1 - j2) == 1 and lookUpValidator(i2, j2):
                    if validator("0" + move[5:]):
                        print("{} {} - {} {} ".format(i1, j1, i2, j2) + move[5:])
                        return True

            else:
                if abs(i1 - i2) == 1 and j1 == j2 and lookUpValidator(i1, j1, i2, j2):
                    if validator("0" + move[5:]):
                        print("{} {} - {} {} ".format(i1, j1, i2, j2) + move[5:])
                        return True

            gameMap[j1][i1] = old_val1
            gameMap[j2][i2] = old_val2
            return False

        if move[1:2].isdigit() and move[3:4].isdigit():
            i1 = letterTonumb.get(move[:1], 10) - 1
            j1 = int(move[1:2]) - 1

            i2 = letterTonumb.get(move[2:3], 10) - 1
            j2 = int(move[3:4]) - 1

            rotation = coordinateToRotation.get(move[:2], 10)
            if rotation == 10:
                rotation = coordinateToRotation.get(move[2:4], 10)
            if rotation == 10:
                return False;

            old_val1 = gameMap[j1][i1]
            old_val2 = gameMap[j2][i2]
            gameMap[j1][i1] = 0
            gameMap[j2][i2] = 0

            if rotation % 2 == 0:
                if i1 == i2 and abs(j1 - j2) == 1 and lookUpValidator(i2, j2):
                    if validator("0" + move[4:]):
                        print("{} {} - {} {} ".format(i1, j1, i2, j2) + move[4:])
                        return True

            else:
                if abs(i1 - i2) == 1 and j1 == j2 and lookUpValidator(i1, j1, i2, j2):
                    if validator("0" + move[4:]):
                        print("{} {} - {} {} ".format(i1, j1, i2, j2) + move[4:])
                        return True

            gameMap[j1][i1] = old_val1
            gameMap[j2][i2] = old_val2
            return False

    return False;


# input_var = input("Enter something: ")
# validator(input_var)
# # print(gameMap)
# print(numpy.flipud(gameMap))
# input_var = input("Enter something: ")
# validator(input_var)
# # print(gameMap)
# print(numpy.flipud(gameMap))

for k in range(7):
    input_var = input("Enter something: ")
    if validator(input_var):
        print("good move")
        # i = letterTonumb.get(input_var[2:3]) - 1
        # j = int(input_var[3:]) - 1
        # place(i, j, int(input_var[1:2]))
    else:
        print("invalid move")
    print(numpy.flipud(gameMap))
    print(coordinateToRotation)
