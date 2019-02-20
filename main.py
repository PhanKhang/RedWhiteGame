#!/usr/bin/python3
import numpy
from move import Move
from validator import Validator
from appraiser import Appraiser

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

coordinateToRotation = {}

# game map
gameMap = numpy.zeros((12, 8))

# krasnyCherny - 1
# beluyKolco - 2
# krasnyKolco - 3
# beluyChernuy - 4
row_labels = ['12', '11', '10', '9 ', '8 ', '7 ', '6 ', '5 ', '4 ', '3 ', '2 ', '1 ']

# player 1 is colors
# player 2 is circles
validator = Validator(gameMap, coordinateToRotation)
appraiser = Appraiser(gameMap)
red = [1, 3]
white = [2, 4]
dot = [1, 4]
ring = [2, 3]


# give what is in the first half of the card according to rotation if not found return 0
def pervayaYacheyka(rotation):
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


# give what is in the second half of the card according to rotation if not found return 0
def vtorayYacheyka(rotation):
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


# put card at position i j and the rotation. keep in mind that coordinates are reversed j before i;
def getCard(i):
    whiteB = '\033[0;37;40m'
    redB = '\033[0;37;41m'
    dot = u" \u25CF"
    ring = u" \u25EF"
    if i == 1 :
        return redB + dot
    if i == 2 :
        return whiteB + ring
    if i == 3 :
        return redB + ring
    if i == 4 :
        return whiteB + dot
    return " 0"


def getCardL(i):
    whiteB = "W"
    redB = "R"
    dot = "D"
    ring = "C"
    if i == 1 :
        return redB + dot
    if i == 2 :
        return whiteB + ring
    if i == 3 :
        return redB + ring
    if i == 4 :
        return whiteB + dot
    return " 0"


def correctPrinter(gameMap):
    print("       A    B    C    D    E    F    G    H")
    for row_label, row in zip(row_labels, numpy.flipud(gameMap)):
        print('%s [%s]' % (row_label, ' '.join('%04s' % int(i) for i in row)))


def correctPrinterMapL(gameMap):
    ENDC = '\033[2m'
    print("     A  B  C  D  E  F  G  H")
    for j in range(11, -1, -1):
        s = str(j+1)+"\t"
        for i in range(8):
            s += getCardL(gameMap[j][i])
            s += " "
            s += ENDC
        print(s, ENDC)
    print("     A  B  C  D  E  F  G  H")


def correctPrinterMap(gameMap):
    ENDC = '\033[2m'
    print("     A  B  C  D  E  F  G  H")
    for j in range(11, -1, -1):
        s = str(j+1)+"\t"
        for i in range(8):
            s += getCard(gameMap[j][i])
            s += " "
            s += ENDC
        print(s, ENDC)
    print("     A  B  C  D  E  F  G  H")


def place(move):
    if move.type == 0:
        if validator.placeValidator(move):
            i = move.targetCoordinateLet - 1
            j = int(move.targetCoordinateNum) - 1
            rotation = int(move.rotation)
            coordinateToRotation[numbToLetter.get(i + 1) + str(j + 1)] = rotation;
            gameMap[j][i] = pervayaYacheyka(rotation)
            if rotation % 2 != 0 and rotation != 0:
                gameMap[j][i + 1] = vtorayYacheyka(rotation)
            else:
                gameMap[j + 1][i] = vtorayYacheyka(rotation)
            return True
        else:
            return False
    else:
        if validator.recycleValidator(move):
            i1 = move.sourceCoordinate1Let - 1
            j1 = move.sourceCoordinate1Num - 1

            i2 = move.sourceCoordinate2Let - 1
            j2 = move.sourceCoordinate2Num - 1

            old_val1 = gameMap[j1][i1]
            old_val2 = gameMap[j2][i2]

            gameMap[j1][i1] = 0
            gameMap[j2][i2] = 0

            i = move.targetCoordinateLet - 1
            j = int(move.targetCoordinateNum) - 1
            rotation = int(move.rotation)
            if validator.placeValidator(move):
                # remove the value from dictionary of moves
                if coordinateToRotation.pop(numbToLetter.get(i1 + 1) + str(j1 + 1), 0) == 0:
                    coordinateToRotation.pop(numbToLetter.get(i2 + 1) + str(j2 + 1), 0)

                coordinateToRotation[numbToLetter.get(i + 1) + str(j + 1)] = rotation
                gameMap[j][i] = pervayaYacheyka(rotation)
                if rotation % 2 != 0:
                    gameMap[j][i + 1] = vtorayYacheyka(rotation)
                else:
                    gameMap[j + 1][i] = vtorayYacheyka(rotation)
                return True
            else:
                gameMap[j1][i1] = old_val1
                gameMap[j2][i2] = old_val2
                return False
    return


def main():
    choice = int(input("Write 0 for dots and 1 a for colors: "))
    if choice == 0:
        print("Player 1: Dots")
        print("Player 2: Colors")
    else:
        print("Player 1: Colors")
        print("Player 2: Dots")
    legal = False

    for k in range(1, 61):
        # print("Turn " + str(k) + " Player " + str((k-1) % 2+1))
        if choice == 0 and (k - 1) % 2 + 1 == 1:
            print("Turn " + str(k) + " Player 1" + " playing with dots")
        elif choice == 0 and (k - 1) % 2 + 1 == 2:
            print("Turn " + str(k) + " Player 2" + " playing with colors")
        elif choice == 1 and (k - 1) % 2 + 1 == 1:
            print("Turn " + str(k) + " Player 1" + " playing with colors")
        elif choice == 1 and (k - 1) % 2 + 1 == 2:
            print("Turn " + str(k) + " Player 2" + " playing with dots")

        # чекер на написание хода надо не хочется чтобы все ломалос
        while not legal:
            movok = False
            while not movok:
                input_var = input()
                # print(input_var)
                try:
                    move = Move(input_var)
                    movok = True
                except:
                    print("unable to parse the move, try again")
            if k <= 24 and move.type == 0:
                legal = place(move)
            elif k > 24 and move.type == 1:
                legal = place(move)
            if not legal:
                print("illegal move, try again")

        print("Current Game field")
        # print(numpy.flipud(gameMap))
        correctPrinterMap(gameMap)
        # print(coordinateToRotation)
        appraiser.appraise(move)
        print("Red map")
        print(appraiser.getAvailableMoves(appraiser.getRedMap()))
        correctPrinter(appraiser.getRedMap())

        print("White map")
        print(appraiser.getAvailableMoves(appraiser.getRingMap()))
        correctPrinter(appraiser.getRingMap())

        print("White map")
        print(appraiser.getAvailableMoves(appraiser.getWhiteMap()))
        correctPrinter(appraiser.getWhiteMap())

        print("Dot map")
        print(appraiser.getAvailableMoves(appraiser.getDotMap()))
        correctPrinter(appraiser.getDotMap())

        result = validator.victoryCheck((k + choice) % 2)

        if result != "go":
            print(result)
            break
        legal = False

main()
